import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "core_common" / "modules"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "core_common" / "modules" / "android"))

import openssl


class StubBaseModule:
    def __init__(self):
        self.calls = []

    def replaceInFile(self, path, old, new):
        self.calls.append((path, old, new))


class OpensslSysrootTests(unittest.TestCase):
    def test_apply_linux_sysroot_makefile_patches_sets_linker_sysroot(self):
        stub = StubBaseModule()

        openssl.apply_linux_sysroot_makefile_patches(
            "./Makefile",
            "/opt/sysroot/usr/bin",
            "/opt/sysroot",
            base_module=stub,
        )

        self.assertEqual(
            stub.calls,
            [
                ("./Makefile", "CROSS_COMPILE=", "CROSS_COMPILE=/opt/sysroot/usr/bin/"),
                ("./Makefile", "CFLAGS=-Wall -O3", "CFLAGS=-Wall -O3 -fvisibility=hidden --sysroot=/opt/sysroot"),
                ("./Makefile", "CXXFLAGS=-Wall -O3", "CXXFLAGS=-Wall -O3 -fvisibility=hidden --sysroot=/opt/sysroot"),
                ("./Makefile", "LDFLAGS=", "LDFLAGS=--sysroot=/opt/sysroot"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
