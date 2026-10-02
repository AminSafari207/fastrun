from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from fastrun.errors import ConfigError
from fastrun.models import Runnable


class ConfigLoader:
    CONFIG_DIRECTORY = Path.home() / ".config" / "fastrun"

    CONFIG_FILES = ("runnables.json", "runnables.yaml", "runnables.yml")

    TEMPLATE = {  # noqa: RUF012
        "example": {"path": "/path/to/runnable", "command": "./run.sh --example-flag"}
    }

    def load(self) -> dict[str, Runnable]:
        config_path = self._find_config()

        if config_path is None:
            config_path = self._create_template()

        try:
            raw_data = self._load_file(config_path)
        except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
            raise ConfigError(
                f"Failed to load configuration '{config_path}': {exc}"
            ) from exc

        return self._parse(raw_data, config_path)

    def _find_config(self) -> Path | None:
        for filename in self.CONFIG_FILES:
            path = self.CONFIG_DIRECTORY / filename

            if path.is_file():
                return path

        return None

    def _create_template(self) -> Path:
        self.CONFIG_DIRECTORY.mkdir(parents=True, exist_ok=True)

        config_path = self.CONFIG_DIRECTORY / "runnables.json"

        with config_path.open("w", encoding="utf-8") as file:
            json.dump(self.TEMPLATE, file, indent=2)
            file.write("\n")

        return config_path

    def _load_file(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as file:
            if path.suffix == ".json":
                return json.load(file)

            if path.suffix in {".yaml", ".yml"}:
                return yaml.safe_load(file)

        raise ConfigError(f"Unsupported configuration format: {path.suffix}")

    def _parse(self, data: Runnable, path: Path) -> dict[str, Runnable]:
        if not isinstance(data, dict):
            raise ConfigError(f"Configuration root must be an object: {path}")

        result: dict[str, Runnable] = {}

        for name, value in data.items():
            if not isinstance(name, str):
                raise ConfigError(f"Runnable name must be a string: {path}")

            if not isinstance(value, dict):
                raise ConfigError(
                    f"Configuration for '{name}' must be an object: {path}"
                )

            command = value.get("command")
            runnable_path = value.get("path")

            if not isinstance(command, str) or not command.strip():
                raise ConfigError(
                    f"Runnable '{name}' must define a non-empty 'command'"
                )

            if runnable_path is not None and not isinstance(runnable_path, str):
                raise ConfigError(f"Runnable '{name}' has an invalid 'path'")

            result[name] = Runnable(command=command, path=runnable_path)

        return result
