import time
import json
import socket
import threading
import subprocess
from pathlib import Path
from ..logs.logger import get_logger

# MPVControl v2

class MPVPlayer:
    def __init__(self, sock_path="/tmp/kitsunari-mpv.sock"):
        self.logger = get_logger("MPVControl")
        self.sock_path = sock_path
        self.process = None
        self.socket = None
        self.running = False
        self._progress_thread = None
        self.on_exit = None
        self._recv_buffer = ""
        self.current_duration = None
        self._current_position = None

    def _cleanup_socket(self):
        try:
            Path(self.sock_path).unlink()

        except FileNotFoundError:
            pass

        except Exception as e:
            self.logger.error(f"Failed to clean up socket: {e} :(")

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
                  "-fs"
                  "--keep-open=no",
              ] + extra_args

        self.process = subprocess.Popen(cmd)
        self.running = True
        self.current_duration = None
        self._current_position = None

        for _ in range(50):
            if Path(self.sock_path).exists():
                try:
                    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    self.socket.connect(self.sock_path)
                    self.socket.settimeout(0.5)
                    break
                except Exception as e:
                    self.logger.error(f"Failed to connect to MPV socket: {e} :/")
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

        threading.Thread(target=self._listen_ipc, daemon=True).start()

    def _listen_ipc(self):
        """
        Listen for JSON events from MPV with proper buffer handling.
        """
        try:
            while self.running:
                try:
                    data = self.socket.recv(4096)
                    if not data:
                        break

                    self._recv_buffer += data.decode("utf-8")

                    while "\n" in self._recv_buffer:
                        line, self._recv_buffer = self._recv_buffer.split("\n", 1)
                        if not line.strip():
                            continue

                        try:
                            msg = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        if msg.get("error") == "success" and "data" in msg:
                            request_id = msg.get("request_id", 0)

                            if request_id == 1:
                                self._current_position = msg["data"]

                            elif request_id == 2:
                                self.current_duration = msg["data"]

                        event = msg.get("event")
                        if event == "end-file":
                            self.running = False
                            if self.on_exit:
                                self.on_exit()
                            break

                except socket.timeout:
                    continue

        except Exception as e:
            self.logger.error(f"Error in MPV IPC listener: {e} :/")

        finally:
            self.running = False
            self.close()

    def send(self, command, args=None, request_id=0):
        """
        Send a command to MPV IPC with optional request_id for tracking responses.
        """
        if args is None:
            args = []

        try:
            payload = json.dumps({"command": [command] + args, "request_id": request_id})
            self.socket.send(payload.encode("utf-8") + b"\n")

        except Exception as e:
            self.logger.error(f"Failed to send command to MPV: {e} :/")

    def get_current_state(self):
        """
        Get current playback position and duration.
        Returns: (position, duration) or (None, None)
        """
        try:
            self.send("get_property", ["time-pos"], request_id=1)
            self.send("get_property", ["duration"], request_id=2)

            time.sleep(0.1)
            return self._current_position, self.current_duration

        except Exception as e:
            self.logger.error(f"Failed to get playback state: {e} :/")
            return None, None

    def start_progress_tracker(self, callback, interval=10):
        """
        callback(elapsed_seconds, total_duration)
        Tracks MPV's actual playback time AND duration.
        """
        def _track():
            while self.running:
                try:
                    position, duration = self.get_current_state()

                    if position is not None and duration is not None:
                        callback(int(position), int(duration))

                    elif position is not None:
                        self.logger.debug("Duration not available yet, using estimated")
                        callback(int(position), int(position) + 300)

                except Exception as e:
                    self.logger.error(f"Error tracking progress: {e} :/")

                time.sleep(interval)

        self._progress_thread = threading.Thread(target=_track, daemon=True)
        self._progress_thread.start()

    def get_elapsed_time(self):
        """
        Get current elapsed time synchronously.
        """
        position, _ = self.get_current_state()
        return int(position) if position is not None else 0

    def close(self):
        self.running = False
        if self.process:
            try:
                self.process.terminate()
            except Exception as e:
                self.logger.error(f"Failed to terminate MPV process: {e} :/")

        if self.socket:
            try:
                self.socket.close()

            except:
                pass
        self._cleanup_socket()