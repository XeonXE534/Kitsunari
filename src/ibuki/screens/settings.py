from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Static, Footer, Button, Input, Select, Label, SelectionList
from textual.widgets.selection_list import Selection

from ..backend.backend_v3 import AnimeBackend


class SettingsScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Go Back", priority=True),
        Binding("s", "save_settings", "Save", show=True),
        Binding("r", "reset_settings", "Reset", show=True),
    ]
    CSS_PATH = '../css/settings_styles.css'

    def __init__(self, backend: AnimeBackend):
        super().__init__()
        self.backend = backend
        self.settings = backend.settings
        self.modified = False

    def compose(self) -> ComposeResult:
        with Container(id="settings_container"):
            with ScrollableContainer(id="settings_scroll"):
                yield Label("Video Quality", classes="section-header")
                yield Select(
                    options=[
                        ("1080p", 1080),
                        ("720p", 720),
                        ("480p", 480),
                    ],
                    value=self.settings.get("quality", 1080),
                    id="quality_select",
                    classes="setting-widget"
                )

                yield Label("Preferred Language", classes="setting-label")
                yield Select(
                    options=[
                        ("Subtitles", "sub"),
                        ("Dubbed", "dub"),
                    ],
                    value=self.settings.get("preferred_language", "sub"),
                    id="language_select",
                    classes="setting-widget"
                )

                yield Label("Player Options", classes="section-header")
                yield SelectionList[str](
                    Selection("Fullscreen Mode", "fullscreen", self.settings.get("fullscreen", True)),
                    Selection("Auto Resume", "auto_resume", self.settings.get("auto_resume", True)),
                    Selection("Auto Next Episode", "auto_next_episode", self.settings.get("auto_next_episode", False)),
                    id="player_options"
                )

                yield Label("Player Volume (0-100)", classes="section-header")
                yield Input(
                    value=str(self.settings.get("player_volume", 100)),
                    placeholder="0-100",
                    id="volume_input",
                    classes="setting-widget",
                    type="integer"
                )

                yield Label("Skip Intro (seconds)", classes="setting-label")
                yield Input(
                    value=str(self.settings.get("skip_intro_seconds", 0)),
                    placeholder="0",
                    id="skip_intro_input",
                    classes="setting-widget",
                    type="integer"
                )

                yield Label("Skip Outro (seconds)", classes="setting-label")
                yield Input(
                    value=str(self.settings.get("skip_outro_seconds", 0)),
                    placeholder="0",
                    id="skip_outro_input",
                    classes="setting-widget",
                    type="integer"
                )

                yield Label("Save Progress Interval (seconds)", classes="setting-label")
                yield Input(
                    value=str(self.settings.get("save_progress_interval", 10)),
                    placeholder="10",
                    id="save_interval_input",
                    classes="setting-widget",
                    type="integer"
                )

                yield Label("Minimum Watch % Before Saving", classes="setting-label")
                yield Input(
                    value=str(int(self.settings.get("minimal_progress_threshold", 0.1) * 100)),
                    placeholder="10",
                    id="threshold_input",
                    classes="setting-widget",
                    type="integer"
                )

                yield Label("History Limit", classes="setting-label")
                yield Input(
                    value=str(self.settings.get("history_limit", 10)),
                    placeholder="10",
                    id="history_limit_input",
                    classes="setting-widget",
                    type="integer"
                )

            with Horizontal(id="settings_actions"):
                yield Button("Save", id="save_btn", variant="success")
                yield Button("Reset", id="reset_btn", variant="error")
                yield Button("Back", id="back_btn", variant="primary")

            yield Static("", id="status_message")
            yield Footer()

    def on_mount(self) -> None:
        """Setup when screen is mounted"""
        self.query_one("#settings_scroll").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "save_btn":
            self.action_save_settings()

        elif event.button.id == "reset_btn":
            self.action_reset_settings()

        elif event.button.id == "back_btn":
            self.action_go_back()

    def on_input_changed(self) -> None:
        """Mark as modified when any input changes"""
        self.modified = True

    def on_selection_list_selected_changed(self) -> None:
        """Mark as modified when selection changes"""
        self.modified = True

    def on_select_changed(self) -> None:
        """Mark as modified when select changes"""
        self.modified = True

    def action_save_settings(self) -> None:
        """Save all settings to backend"""
        try:
            updates = {}

            updates["quality"] = self.query_one("#quality_select", Select).value
            updates["preferred_language"] = self.query_one("#language_select", Select).value

            player_options = self.query_one("#player_options", SelectionList)
            updates["fullscreen"] = "fullscreen" in player_options.selected
            updates["auto_resume"] = "auto_resume" in player_options.selected
            updates["auto_next_episode"] = "auto_next_episode" in player_options.selected
            updates["notifications_enabled"] = "notifications" in player_options.selected

            volume = int(self.query_one("#volume_input", Input).value or "100")
            updates["player_volume"] = max(0, min(100, volume))

            updates["skip_intro_seconds"] = max(0, int(self.query_one("#skip_intro_input", Input).value or "0"))
            updates["skip_outro_seconds"] = max(0, int(self.query_one("#skip_outro_input", Input).value or "0"))
            updates["save_progress_interval"] = max(1, int(self.query_one("#save_interval_input", Input).value or "30"))
            updates["history_limit"] = max(1, int(self.query_one("#history_limit_input", Input).value or "50"))

            threshold = int(self.query_one("#threshold_input", Input).value or "10")
            updates["minimal_progress_threshold"] = max(0.0, min(100.0, threshold)) / 100.0

            self.settings.update_multiple(updates)
            self.backend.global_quality = updates["quality"]

            self.modified = False
            self._show_status("✓ Settings saved", "success")

        except ValueError as e:
            self._show_status(f"✗ Invalid number: {e}", "error")
        except Exception as e:
            self._show_status(f"✗ Save failed: {e}", "error")

    def action_reset_settings(self) -> None:
        """Reset all settings to defaults"""
        try:
            self.settings.reset()
            self.backend.global_quality = self.settings.get("quality", 1080)

            self.app.pop_screen()
            self.app.push_screen(SettingsScreen(self.backend))
            self._show_status("Reset to defaults :3", "warning")

        except Exception as e:
            self._show_status(f"Reset failed: {e} :(", "error")

    def action_go_back(self) -> None:
        """Go back to previous screen"""
        if self.modified:
            self._show_status("Unsaved changes :/", "warning")
            self.app.pop_screen()
        else:
            self.app.pop_screen()

    def _show_status(self, message: str, status_type: str = "info") -> None:
        """Show temporary status message"""
        status = self.query_one("#status_message", Static)
        status.update(message)
        status.remove_class("success", "error", "warning", "info")
        status.add_class(status_type)
        self.set_timer(3, lambda: status.update(""))