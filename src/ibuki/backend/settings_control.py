import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from ..logs.logger import get_logger

# Animesettings v1
# 90% of the code in this file is by Claude lol

class AnimeSettings:
    DEFAULT_SETTINGS = {
        "quality": 1080,
        "preferred_language": "sub",

        "auto_resume": True,
        "fullscreen": True,
        "player_volume": 100,
        "skip_intro_seconds": 0,
        "skip_outro_seconds": 0,
        "auto_next_episode": False,

        "save_progress_interval": 30,
        "minimal_progress_threshold": 0.1,
        "history_limit": 50,
    }

    def __init__(
            self,
            config_path: Optional[Path] = None,
            use_yaml: bool = True
    ):
        self.logger = get_logger("AnimeSettings")
        self.use_yaml = use_yaml

        if config_path:
            self.config_path = config_path
        else:
            config_dir = Path.home() / "Project-Ibuki" / "config"
            ext = "yaml" if use_yaml else "json"
            self.config_path = config_dir / f"settings.{ext}"

        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        """Load settings from disk, create defaults if missing"""
        if not self.config_path.exists():
            self.logger.info(f"No config found at {self.config_path}, creating defaults")
            self.save()
            return

        try:
            with open(self.config_path, 'r') as f:
                if self.use_yaml and self.config_path.suffix in ['.yaml', '.yml']:
                    loaded = yaml.safe_load(f) or {}
                else:
                    loaded = json.load(f)

            self.settings.update(loaded)
            self.logger.info(f"Settings loaded from {self.config_path}")

        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in config: {e}, using defaults :|")

        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config: {e}, using defaults :|")

        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}, using defaults :|")

    def save(self):
        """Persist current settings to disk"""
        try:
            self._ensure_config_dir()

            with open(self.config_path, 'w') as f:
                if self.use_yaml and self.config_path.suffix in ['.yaml', '.yml']:
                    yaml.dump(
                        self.settings,
                        f,
                        default_flow_style=False,
                        sort_keys=False,
                        indent=2
                    )
                else:
                    json.dump(self.settings, f, indent=2)

            self.logger.debug(f"Settings saved to {self.config_path} :)")

        except Exception as e:
            self.logger.error(f"Failed to save settings: {e} :(")

    def get(self, key: str, default=None):
        """Get a setting value with optional default"""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any, save: bool = True):
        """
        Set a setting value
        Args:
            key: Setting key
            value: New value
            save: Whether to immediately persist to disk (default: True)
        """
        old_value = self.settings.get(key)
        self.settings[key] = value

        if save:
            self.save()

        if old_value != value:
            self.logger.info(f"Setting '{key}' changed: {old_value} -> {value}")

    def update_multiple(self, updates: Dict[str, Any]):
        """Update multiple settings at once"""
        self.settings.update(updates)
        self.save()
        self.logger.info(f"Updated {len(updates)} settings")

    def reset(self):
        """Reset to default settings"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
        self.logger.info("Settings reset to defaults")

    def reset_key(self, key: str):
        """Reset a single setting to its default value"""
        if key in self.DEFAULT_SETTINGS:
            self.set(key, self.DEFAULT_SETTINGS[key])
            self.logger.info(f"Reset '{key}' to default: {self.DEFAULT_SETTINGS[key]}")
        else:
            self.logger.warning(f"No default value for '{key}'")

    def get_all(self) -> Dict[str, Any]:
        """Return copy of all settings"""
        return self.settings.copy()

    def export_to_file(self, path: Path):
        """Export settings to a different file"""
        try:
            with open(path, 'w') as f:
                if path.suffix in ['.yaml', '.yml']:
                    yaml.dump(self.settings, f, default_flow_style=False, indent=2)
                else:
                    json.dump(self.settings, f, indent=2)
            self.logger.info(f"Settings exported to {path}")
        except Exception as e:
            self.logger.error(f"Failed to export settings: {e}")

    def import_from_file(self, path: Path):
        """Import settings from another file"""
        try:
            with open(path, 'r') as f:
                if path.suffix in ['.yaml', '.yml']:
                    loaded = yaml.safe_load(f)
                else:
                    loaded = json.load(f)

            self.settings.update(loaded)
            self.save()
            self.logger.info(f"Settings imported from {path}")

        except Exception as e:
            self.logger.error(f"Failed to import settings: {e}")

    def __str__(self):
        """Pretty print current settings"""
        return yaml.dump(self.settings, default_flow_style=False, sort_keys=False)

    def __repr__(self):
        return f"<AnimeSettings config_path={self.config_path}>"

def load_settings(config_path: Optional[Path] = None) -> AnimeSettings:
    """Quick load settings from default or custom path"""
    return AnimeSettings(config_path)

def get_default_config_path(use_yaml: bool = True) -> Path:
    """Get the default config file path"""
    ext = "yaml" if use_yaml else "json"
    return Path.home() /"Project-Ibuki" / "config" / f"settings.{ext}"