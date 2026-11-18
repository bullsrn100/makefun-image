"""make.fun entry: news-image-20261117.

Writes the bundled news-summary image to /output/entry.png.
The image is stored in this repository as entry.png; the program
simply copies it, byte for byte, so every run produces identical
output. No network access is used.
"""

import shutil
from pathlib import Path


def main() -> None:
    src = Path(__file__).resolve().with_name("entry.png")
    out = Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)


if __name__ == "__main__":
    main()
