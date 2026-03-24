import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import custom_plugins


class StubBaseModule:
    def __init__(self):
        self.calls = []

    def copy_sdkjs_plugin(self, src_dir, dst_dir, name, is_name_as_guid=False, is_desktop_local=False):
        self.calls.append({
            "src_dir": src_dir,
            "dst_dir": dst_dir,
            "name": name,
            "is_name_as_guid": is_name_as_guid,
            "is_desktop_local": is_desktop_local,
        })


class CustomPluginsTests(unittest.TestCase):
    def test_find_local_sdkjs_plugins_returns_only_configured_plugins(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "sdkjs-plugins" / "agent-plugin").mkdir(parents=True)
            (root / "sdkjs-plugins" / "agent-plugin" / "config.json").write_text("{}", encoding="utf-8")
            (root / "sdkjs-plugins" / "ignored").mkdir(parents=True)

            self.assertEqual(
                custom_plugins.find_local_sdkjs_plugins(str(root)),
                ["agent-plugin"],
            )

    def test_copy_local_sdkjs_plugins_uses_existing_base_copy_helper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plugins_root = root / "sdkjs-plugins"
            (plugins_root / "agent-plugin").mkdir(parents=True)
            (plugins_root / "agent-plugin" / "config.json").write_text("{}", encoding="utf-8")
            stub = StubBaseModule()

            copied = custom_plugins.copy_local_sdkjs_plugins(
                str(root),
                "/tmp/output/sdkjs-plugins",
                base_module=stub,
                is_name_as_guid=False,
                is_desktop_local=True,
            )

            self.assertEqual(copied, ["agent-plugin"])
            self.assertEqual(stub.calls, [{
                "src_dir": str(plugins_root),
                "dst_dir": "/tmp/output/sdkjs-plugins",
                "name": "agent-plugin",
                "is_name_as_guid": False,
                "is_desktop_local": True,
            }])


if __name__ == "__main__":
    unittest.main()
