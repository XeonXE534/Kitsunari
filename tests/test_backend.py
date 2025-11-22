import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from ibuki.backend.backend_v3 import AnimeBackend
from ibuki.backend.utils_v3 import WatchHistory, clean_html
from ibuki.backend.mpv_control import MPVPlayer
from anipy_api.provider import LanguageTypeEnum

# Unit tests for utils_v3.py, backend_v3.py, and mpv_control.py


def test_clean_html_basic():
    assert clean_html("<b>hello</b>") == "hello"
    assert clean_html(None) == "Not available :("
    assert clean_html("<div>test &amp; decode</div>") == "test & decode"

"""
WatchHistory Tests
"""
def test_watchhistory_load_empty(tmp_path):
    file_path = tmp_path / "dummy.json"
    wh = WatchHistory(file_path=file_path)
    assert isinstance(wh.history, dict)
    assert wh.history == {}

def test_watchhistory_update_progress(tmp_path):
    file_path = tmp_path / "progress.json"
    wh = WatchHistory(file_path=file_path)
    wh.update_progress("anime1", "Test Anime", 1, 50, 100)
    entry = wh.get_entry("anime1")
    assert entry["episode"] == 1
    assert entry["progress_percent"] == 50.0

"""
AnimeBackend Tests
"""

@patch("ibuki.backend.backend_v3.AllAnimeProvider")
@patch("ibuki.backend.backend_v3.MPVPlayer")
def test_play_episode_calls_mpv(mock_mpv, mock_provider):
    backend = AnimeBackend()
    anime = MagicMock()
    stream = MagicMock()
    stream.url = "http://example.com"
    stream.referrer = None

    backend.play_episode(anime, 1, stream, start_time=5)
    mock_mpv.return_value.launch.assert_called_once()
    assert backend.current_anime == anime
    assert backend.current_episode == 1

def test_get_referrer_for_url():
    backend = AnimeBackend()
    assert backend.get_referrer_for_url("https://fast4speed.xyz") == "https://allanime.day"
    assert backend.get_referrer_for_url("https://sunshinerays.xyz") == "https://allmanga.to"
    assert backend.get_referrer_for_url("https://unknown.xyz") == "https://allanime.day"


@patch("ibuki.backend.backend_v3.AllAnimeProvider")
def test_get_anime_by_query_caching(mock_provider_class):
    mock_provider = mock_provider_class.return_value
    mock_result = MagicMock()
    mock_result.id = "123"
    mock_provider.get_search.return_value = [mock_result]

    backend = AnimeBackend()
    backend.provider = mock_provider

    anime_list = backend.get_anime_by_query("test")
    assert len(anime_list) == 1
    cached = backend.get_anime_by_query("test")
    assert cached[0] is anime_list[0]


def test_choose_stream_logic():
    backend = AnimeBackend()
    # Create mock streams with resolutions
    streams = [MagicMock(resolution=r) for r in [480, 720, 1080]]

    # Exact match
    s = backend._choose_stream(streams, 720)
    assert s.resolution == 720

    # Lower resolution fallback
    s = backend._choose_stream(streams, 800)
    assert s.resolution == 720

    # Highest available
    s = backend._choose_stream(streams, 2000)
    assert s.resolution == 1080

    # Empty streams
    s = backend._choose_stream([], 720)
    assert s is None

@patch("ibuki.backend.backend_v3.AnimeBackend.get_anime_by_query")
@patch("ibuki.backend.backend_v3.AnimeBackend.get_episode_stream")
@patch("ibuki.backend.backend_v3.AnimeBackend.play_episode")
def test_resume_anime(mock_play, mock_get_stream, mock_get_query):
    backend = AnimeBackend()

    # Fake watch history entry
    backend.watch_history.update_progress("anime1", "Test Anime", 1, 50, 100)
    entry = backend.watch_history.get_entry("anime1")

    mock_get_stream.return_value = MagicMock(url="http://example.com")
    mock_get_query.return_value = [MagicMock()]

    result = backend.resume_anime("anime1", quality=720)
    assert result is True
    mock_play.assert_called_once()

    # No entry case
    result = backend.resume_anime("missing_anime")
    assert result is False

@patch("ibuki.backend.mpv_player.socket.socket")
@patch("ibuki.backend.mpv_player.subprocess.Popen")
@patch("ibuki.backend.mpv_player.Path.exists", return_value=True)
def test_mpv_launch_process(mock_exists, mock_popen, mock_socket):
    mock_proc = MagicMock()
    mock_proc.poll.return_value = None
    mock_popen.return_value = mock_proc

    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance

    mpv = MPVPlayer(sock_path="/tmp/test.sock")
    mpv._cleanup_socket = MagicMock()
    mpv.launch("http://example.com")
    assert mpv.running is True
    mpv._cleanup_socket.assert_called()

def test_mpv_get_elapsed_time_none(monkeypatch):
    mpv = MPVPlayer()
    monkeypatch.setattr(mpv, "get_current_state", lambda: (None, None))
    assert mpv.get_elapsed_time() == 0
