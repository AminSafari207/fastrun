import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastrun.completion.completion import CompletionManager
from fastrun.completion.provider import get_completions
from fastrun.completion.shell import get_shell
from fastrun.completion.shells.bash import get_script as get_bash_script
from fastrun.completion.shells.zsh import get_script as get_zsh_script


class CompletionProviderTests(unittest.TestCase):

    @patch("fastrun.completion.provider.ConfigLoader")
    def test_returns_options_and_runnables(self, config_loader):
        config_loader.return_value.load.return_value = {
            "zulu": object(),
            "alpha": object(),
        }

        completions = get_completions()

        self.assertEqual(
            completions,
            [
                "--debug",
                "--version",
                "--help",
                "alpha",
                "zulu",
            ],
        )


class ShellDetectionTests(unittest.TestCase):

    @patch.dict(os.environ, {"SHELL": "/usr/bin/bash"})
    def test_detects_bash(self):
        self.assertEqual(get_shell(), "bash")

    @patch.dict(os.environ, {"SHELL": "/bin/zsh"})
    def test_detects_zsh(self):
        self.assertEqual(get_shell(), "zsh")

    @patch.dict(os.environ, {}, clear=True)
    def test_returns_none_when_shell_is_missing(self):
        self.assertIsNone(get_shell())


class ShellScriptTests(unittest.TestCase):

    def test_bash_script_contains_fastrun_completion(self):
        script = get_bash_script()

        self.assertIn("_fastrun()", script)
        self.assertIn("fastrun.completion.provider", script)
        self.assertIn("complete -F _fastrun", script)

    def test_zsh_script_contains_fastrun_completion(self):
        script = get_zsh_script()

        self.assertIn("#compdef fastrun", script)
        self.assertIn("_fastrun()", script)
        self.assertIn("fastrun.completion.provider", script)


class CompletionManagerTests(unittest.TestCase):

    def test_install_writes_completion_file(self):
        manager = CompletionManager()

        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "fastrun"

            manager._install(
                path,
                "completion script",
            )

            self.assertTrue(path.exists())
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "completion script",
            )

    def test_install_updates_existing_completion_file(self):
        manager = CompletionManager()

        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "fastrun"

            manager._install(
                path,
                "old completion script",
            )

            manager._install(
                path,
                "new completion script",
            )

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "new completion script",
            )

    @patch("fastrun.completion.completion.system", return_value="Linux")
    @patch("fastrun.completion.completion.get_shell", return_value="bash")
    @patch.object(CompletionManager, "_install")
    def test_linux_bash_uses_bash_completion(
        self,
        install,
        get_shell,
        system,
    ):
        manager = CompletionManager()

        manager.install()

        install.assert_called_once()

        path, script = install.call_args.args

        self.assertEqual(path.name, "fastrun")
        self.assertIn("_fastrun()", script)

    @patch("fastrun.completion.completion.system", return_value="Linux")
    @patch("fastrun.completion.completion.get_shell", return_value="zsh")
    @patch.object(CompletionManager, "_install")
    def test_linux_zsh_uses_zsh_completion(
        self,
        install,
        get_shell,
        system,
    ):
        manager = CompletionManager()

        manager.install()

        install.assert_called_once()

        path, script = install.call_args.args

        self.assertEqual(path.name, "_fastrun")
        self.assertIn("#compdef fastrun", script)

    @patch("fastrun.completion.completion.system", return_value="Linux")
    @patch("fastrun.completion.completion.get_shell", return_value="fish")
    @patch.object(CompletionManager, "_install")
    def test_unsupported_linux_shell_does_nothing(
        self,
        install,
        get_shell,
        system,
    ):
        manager = CompletionManager()

        manager.install()

        install.assert_not_called()


if __name__ == "__main__":
    unittest.main()
