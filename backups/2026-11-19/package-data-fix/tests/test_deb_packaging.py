import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_deb import build

class DebPackagingTests(unittest.TestCase):
    def test_builds_debian_package_with_expected_files(self):
        import shutil
        import subprocess
        if not shutil.which("dpkg-deb"):
            self.skipTest("dpkg-deb unavailable on this host")
        with tempfile.TemporaryDirectory() as temp:
            output = build(ROOT, pathlib.Path(temp))
            self.assertTrue(output.is_file())
            listing = subprocess.check_output(["dpkg-deb", "--contents", str(output)], text=True)
            self.assertIn("./usr/bin/ci-master-control-community", listing)
            self.assertIn("./usr/share/ci-master-control-community/demo_server.py", listing)
            self.assertNotIn("DEBIAN/control", listing)
            control = subprocess.check_output(["dpkg-deb", "--field", str(output), "Architecture"], text=True)
            self.assertEqual(control.strip(), "all")
            with tempfile.TemporaryDirectory() as extracted:
                subprocess.run(["dpkg-deb", "-x", str(output), extracted], check=True)
                launcher = pathlib.Path(extracted) / "usr/bin/ci-master-control-community"
                self.assertTrue(launcher.is_file())
                self.assertTrue(bool(launcher.stat().st_mode & 0o111))

    def test_invalid_version_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            (root / "VERSION").write_text("invalid\n")
            with self.assertRaises(ValueError):
                build(root, root / "dist")

if __name__ == "__main__":
    unittest.main()
