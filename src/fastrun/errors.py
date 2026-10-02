class FastrunError(Exception):
    """Base exception for expected fastrun errors."""


class ConfigError(FastrunError):
    """Raised when the fastrun configuration is invalid."""


class RunnableNotFoundError(FastrunError):
    """Raised when the requested runnable does not exist."""


class RunnableExecutionError(FastrunError):
    """Raised when a runnable cannot be started."""
