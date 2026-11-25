#!/usr/bin/env python3
"""Carrier for THE BULLION POST (NI24, Akun 12 G2).

The artwork itself ships beside this file as entry.png; the harness
expects the program to place that picture at /output/entry.png.
This carrier is deliberately boring: standard library only, no
network, no image decoding - it copies bytes and nothing else, so
two runs always produce byte-identical output.
"""
import os
import shutil
import sys


def source_picture():
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, "entry.png")
    if os.path.isfile(candidate):
        return candidate
    return os.path.join(os.getcwd(), "entry.png")


def main():
    src = source_picture()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        payload = fh.read()
    with open(dst, "wb") as fh:
        fh.write(payload)
    print(f"copied {len(payload)} bytes -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
