from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

from fastrun.errors import ConfigError
from fastrun.models import Runnable


class ConfigLoader:
    CONFIG_DIRECTORY = Path.home() / ".config" / "fastrun" / "runnables"
    EXAMPLES_DIRECTORY = Path.home() / ".config" / "fastrun" / "examples"

    CONFIG_FILES = (
        "runnables.json",
        "runnables.yaml",
        "runnables.yml",
    )

    TEMPLATE = {"runnables": {}}  # noqa: RUF012

    def initialize(self) -> Path:
        config_path = self._find_config()

        if config_path is None:
            config_path = self._create_template()

        self._copy_examples()

        return config_path

    def load(self) -> dict[str, Runnable]:
        config_path = self.initialize()

        try:
            raw_data = self._load_file(config_path)
        except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
            raise ConfigError(
                f"Failed to load configuration '{config_path}': {exc}"
            ) from exc

        return self._parse(raw_data, config_path)

    def _find_config(self) -> Path | None:
        self.CONFIG_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        found = [
            self.CONFIG_DIRECTORY / name
            for name in self.CONFIG_FILES
            if (self.CONFIG_DIRECTORY / name).is_file()
        ]

        if len(found) > 1:
            names = ", ".join(path.name for path in found)

            raise ConfigError(
                "Multiple runnable configuration files found: "
                f"{names}. Use only one of "
                "runnables.json, runnables.yaml, or runnables.yml."
            )

        unsupported = [
            path
            for path in self.CONFIG_DIRECTORY.glob("runnables.*")
            if path.is_file() and path.name not in self.CONFIG_FILES
        ]

        if unsupported:
            name = unsupported[0].name

            raise ConfigError(
                f"Unsupported runnable configuration file '{name}'. "
                "Use only runnables.json, runnables.yaml, or runnables.yml."
            )

        return found[0] if found else None

    def _create_template(self) -> Path:
        config_path = self.CONFIG_DIRECTORY / "runnables.json"

        with config_path.open("w", encoding="utf-8") as file:
            json.dump(self.TEMPLATE, file, indent=2)
            file.write("\n")

        return config_path

    def _copy_examples(self) -> None:
        self.EXAMPLES_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        examples = resources.files("fastrun").joinpath("examples")

        for example in examples.iterdir():
            if not example.is_file():
                continue

            destination = self.EXAMPLES_DIRECTORY / example.name

            if destination.exists():
                continue

            destination.write_bytes(example.read_bytes())

    def _load_file(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as file:
            if path.suffix == ".json":
                return json.load(file)

            if path.suffix in {".yaml", ".yml"}:
                return yaml.safe_load(file)

        raise ConfigError(f"Unsupported configuration format: '{path.name}'")

    def _parse(
        self,
        data: Any,
        path: Path,
    ) -> dict[str, Runnable]:
        if not isinstance(data, dict):
            raise ConfigError(f"Configuration '{path.name}' must contain an object.")

        runnables = data.get("runnables")

        if runnables is None:
            return {}

        if not isinstance(runnables, dict):
            raise ConfigError(
                f"Configuration '{path.name}' must contain " "a 'runnables' object."
            )

        result: dict[str, Runnable] = {}

        for name, value in runnables.items():
            if not isinstance(name, str):
                raise ConfigError("Runnable names must be strings.")

            if not isinstance(value, dict):
                raise ConfigError(f"Runnable '{name}' must contain an object.")

            command = value.get("command")
            runnable_path = value.get("path")

            if not isinstance(command, str) or not command.strip():
                raise ConfigError(
                    f"Runnable '{name}' must have a non-empty " "'command' value."
                )

            if runnable_path is not None and not isinstance(
                runnable_path,
                str,
            ):
                raise ConfigError(f"Runnable '{name}' has an invalid 'path' value.")

            result[name] = Runnable(
                command=command,
                path=runnable_path,
            )

        return result
