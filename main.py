"""make.fun entry: news-image-20261117.

Writes the bundled news-summary image to /output/entry.png.
The image is stored in this repository as entry.png; the program
copies it byte for byte, so every run produces identical output.
No network access is used.

Revision 1: validate that the bundled file really is a PNG image
before copying, and copy in chunks while counting the bytes, so a
truncated copy is detected instead of silently accepted.

Revision 2: after copying, verify the output's SHA-256 digest
against the source image, so any corruption in the written file
fails the run instead of producing a silently wrong entry.
"""

import hashlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK_SIZE = 64 * 1024


def bundled_image() -> Path:
    """Return the path of the image stored next to this program."""
    return Path(__file__).resolve().with_name("entry.png")


def check_png(path: Path) -> int:
    """Return the file size, raising ValueError if it is not a PNG."""
    with path.open("rb") as fh:
        header = fh.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise ValueError(f"{path} is not a PNG image")
    return path.stat().st_size


def copy_image(src: Path, dst: Path) -> int:
    """Copy src to dst in chunks; return the number of bytes written."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with src.open("rb") as fin, dst.open("wb") as fout:
        while chunk := fin.read(CHUNK_SIZE):
            fout.write(chunk)
            written += len(chunk)
    return written


def digest(path: Path) -> str:
    """Return the SHA-256 hex digest of a file, read in chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> None:
    src = bundled_image()
    expected = check_png(src)
    out = Path("/output/entry.png")
    written = copy_image(src, out)
    if written != expected:
        raise IOError(f"copy incomplete: wrote {written} of {expected} bytes")
    if digest(out) != digest(src):
        raise IOError("copy verification failed: output differs from source")
    print(f"wrote {out} ({written} bytes, sha256 {digest(out)})")


if __name__ == "__main__":
    main()
