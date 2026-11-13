#!/usr/bin/env python3
"""Entry for make.fun bounty "cutest-picture-01" (Make the cutest picture).

The picture is the original cute artwork shipped beside this file
as cute.png: a chubby baby kitten with big bright eyes and a tiny
pink bow, head tilted, cuddling a small fluffy yellow duckling,
among hearts and flowers. This entrypoint copies it, byte for byte,
to /output/entry.png using only the Python standard library, so it
runs in the grader's sandbox with no third-party package and no
network access.

Deterministic: the same input file always produces the same output
bytes, so two runs of this program write identical files.
"""

import hashlib
import os
import shutil
import struct
import sys

ART_NAME = "cute.png"
MAX_BYTES = 1_048_576        # competition cap: image at most 1 MiB
MAX_DIMENSION = 1024         # competition cap: at most 1024 by 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Return (width, height) from a PNG IHDR chunk, stdlib only."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ART_NAME)

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        raise SystemExit("cute.png is %d bytes, over the 1 MiB cap" % size)
    width, height = png_dimensions(source)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit("cute.png is %dx%d, over the 1024x1024 cap"
                         % (width, height))

    # The brief names /output/entry.png. Fall back to a relative
    # output/ directory only if the absolute one is not usable here.
    destination = "/output/entry.png"
    try:
        os.makedirs("/output", exist_ok=True)
        shutil.copyfile(source, destination)
    except OSError:
        os.makedirs(os.path.join(here, "output"), exist_ok=True)
        destination = os.path.join(here, "output", "entry.png")
        shutil.copyfile(source, destination)

    if sha256_of(source) != sha256_of(destination):
        raise SystemExit("copy verification failed: hashes differ")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (destination, width, height, size, sha256_of(source)[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
