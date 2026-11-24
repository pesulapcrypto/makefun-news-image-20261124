#!/usr/bin/env python3
"""THE MERIDIAN POST - NI24 entry program (Akun 12, @pesulapcrypto).

Copies the pre-rendered entry.png shipped in this repository to the
grader output directory. Standard library only, no network, deterministic:
the same bytes come out on every run.

Gate enforced here before copying: entry.png must be exactly 1024x1024
(IHDR) and at most 1048576 bytes, matching the competition gate.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = "entry.png"
MAX_BYTES = 1048576
EXPECT_W = 1024
EXPECT_H = 1024


def check_png(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    if (w, h) != (EXPECT_W, EXPECT_H):
        raise SystemExit("entry.png is %dx%d, must be 1024x1024" % (w, h))
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over 1048576" % size)
    return w, h, size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    w, h, size = check_png(src)
    digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
    dst = os.path.join(outdir, ENTRY)
    shutil.copyfile(src, dst)
    print("copied entry.png %dx%d %d bytes sha256=%s -> %s" % (w, h, size, digest, dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
