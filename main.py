#!/usr/bin/env python3
"""Copy the pre-drawn front page to the grader's output directory.

The entry image lives next to this file as entry.png. The grader runs this
program with a read-only repository and a writable MAKEFUN_OUTPUT_DIR, so
nothing is ever written next to this file: the destination is always inside
MAKEFUN_OUTPUT_DIR.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print(f"missing source image: {src}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        print(f"bad output size: {w}x{h}", file=sys.stderr)
        return 1
    if sha256(dst) != sha256(src):
        print("output hash mismatch", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} ({w}x{h}, {os.path.getsize(dst)} bytes, "
          f"sha256 {sha256(dst)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
