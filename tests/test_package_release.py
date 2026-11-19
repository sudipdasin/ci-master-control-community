import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_release import build, FILES


class PackageReleaseTests(unittest.TestCase):
    def test_archive_contains_installable_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build(ROOT, Path(directory))
            with zipfile.ZipFile(result) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), len(FILES))
                self.assertTrue(any(n.endswith("/install.sh") for n in names))
                self.assertTrue(any(n.endswith("/scripts/demo_server.py") for n in names))
                self.assertTrue(all(".." not in Path(n).parts for n in names))

    def test_archive_reproducible(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self.assertEqual(build(ROOT, Path(a)).read_bytes(), build(ROOT, Path(b)).read_bytes())


if __name__ == "__main__":
    unittest.main()
