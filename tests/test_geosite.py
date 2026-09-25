import tempfile
import unittest
from pathlib import Path

from main import validate_binary_geosite, write_geosite_file


class GeoSiteTests(unittest.TestCase):
    def test_writes_non_empty_geosite_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "geosite.dat")
            write_geosite_file(
                str(path),
                {
                    "loc-cn": (
                        ["full.example"],
                        ["example.cn"],
                        ["keyword"],
                        ["^regex$"],
                    )
                },
            )
            self.assertTrue(path.exists())
            self.assertGreater(path.stat().st_size, 0)
            validate_binary_geosite(str(path))


if __name__ == "__main__":
    unittest.main()
