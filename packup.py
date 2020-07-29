#!/usr/bin/env python
import subprocess
import tarfile
from io import BytesIO
from pathlib import Path
from tarfile import TarFile, TarInfo
from typing import List

HOMEDIR = Path.home()


def get_cmd_output(cmd: List[str]) -> bytes:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
    return proc.stdout


def add_bytes(name: str, data: bytes, tarball: TarFile):
    handle = BytesIO(data)
    info = TarInfo(name=name)
    info.size = len(handle.getbuffer())
    tarball.addfile(tarinfo=info, fileobj=handle)


def main():
    packages = get_cmd_output(["pacman", "-Qqent"])
    aur = get_cmd_output(["pacman", "-Qqem"])
    vscode = get_cmd_output(["code", "--list-extensions"])

    tarball = tarfile.open("out.tar.xz", "w:xz")

    add_bytes("packages.txt", packages, tarball)
    add_bytes("aur-packages.txt", aur, tarball)
    add_bytes("vscode-extensions.txt", vscode, tarball)

    tarball.close()


if __name__ == "__main__":
    main()
