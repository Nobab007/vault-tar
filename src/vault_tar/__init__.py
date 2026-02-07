"""vault-tar — AES-256-GCM file and directory encryption."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__: str = version("vault-tar")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
