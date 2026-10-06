import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

SRC_DIR = Path(__file__).parent / "src"

sys.path.insert(0, str(SRC_DIR))

from fastrun.completion.completion import CompletionManager
from fastrun.config import ConfigLoader


class PostInstallCommand(install):

    def run(self):
        super().run()
        ConfigLoader().initialize()
        CompletionManager().install()


setup(
    cmdclass={
        "install": PostInstallCommand,
    },
)
