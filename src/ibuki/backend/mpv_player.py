import subprocess
import socket
import json
import threading
import time
from pathlib import Path


class MPVPlayer:
    def __init__(self, sock_path="/tmp/kitsunari-mpv.sock"):
        self.sock_path = sock_path
        self.process = None
        self.socket = None
        self.running = False
        self._progress_thread = None
        self.on_exit = None  # callback when MPV closes

    def _cleanup_socket(self):
        try:
            Path(self.sock_path).unlink()
        except FileNotFoundError:
            pass
        except Exception:
            pass

    def launch(self, url, start_time=0, extra_args=None):
        if extra_args is None:
            extra_args = []

        self._cleanup_socket()

        cmd = [
            "mpv",
            url,
            f"--start={start_time}",
            f"--input-ipc-server={self.sock_path}",
            "--force-window=immediate",
            "--no-terminal",
            "--idle=no",
            "--keep-open=no",
        ] + extra_args

        self.process = subprocess.Popen(cmd)
        self.running = True

        # Wait for MPV to create socket (0.5s max)
        for _ in range(50):
            if Path(self.sock_path).exists():
                try:
                    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    self.socket.connect(self.sock_path)
                    break
                except Exception:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)

        threading.Thread(target=self._listen_ipc, daemon=True).start()

    def _listen_ipc(self):
        """
        Listen for JSON events from MPV.
        """
        try:
            while self.running:
                data = self.socket.recv(4096)
                if not data:
                    break

                try:
                    msg = json.loads(data.decode("utf-8"))
                except Exception:
                    continue

                event = msg.get("event")

                if event == "end-file":
                    self.running = False
                    if self.on_exit:
                        self.on_exit()
                    break

        except Exception:
            pass

        finally:
            self.running = False
            self.close()

    def send(self, command, args=None):
        """
        Send a command to MPV IPC.
        Example: send("set_property", ["pause", True])
        """
        if args is None:
            args = []
        try:
            payload = json.dumps({"command": [command] + args})
            self.socket.send(payload.encode("utf-8") + b"\n")
        except Exception:
            pass

    def start_progress_tracker(self, callback, interval=10):
        """
        callback(elapsed_seconds)
        """
        def _track():
            start = time.time()
            while self.running:
                time.sleep(1)
                elapsed = int(time.time() - start)
                if elapsed % interval == 0:
                    callback(elapsed)

        self._progress_thread = threading.Thread(target=_track, daemon=True)
        self._progress_thread.start()

    def close(self):
        self.running = False
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
        self._cleanup_socket()
