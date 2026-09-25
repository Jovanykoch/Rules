import json
import tempfile
import unittest
from pathlib import Path

import yaml

from main import (
    release_clash_file,
    release_quanx_file,
    release_surge_file,
    validate_clash_yaml,
    validate_quanx_file,
    validate_singbox_json,
    validate_surge_file,
)


class OutputFormatTests(unittest.TestCase):
    def test_surge_output_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            current = Path.cwd()
            try:
                Path(directory, "dist").mkdir()
                Path(directory).joinpath("tmp").mkdir()
                import os

                os.chdir(directory)
                release_surge_file("tag", ["a.example"], ["example.com"])
                validate_surge_file("dist/tag.list")
                content = Path("dist/tag.list").read_text()
                self.assertEqual(content, "a.example\n.example.com\n")
            finally:
                os.chdir(current)

    def test_clash_output_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            current = Path.cwd()
            try:
                Path(directory, "dist").mkdir()
                import os

                os.chdir(directory)
                release_clash_file("tag", ["a.example"], ["example.com"])
                validate_clash_yaml("dist/tag.yaml")
                payload = yaml.safe_load(Path("dist/tag.yaml").read_text())["payload"]
                self.assertEqual(payload, ["a.example", ".example.com"])
            finally:
                os.chdir(current)

    def test_quanx_output_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            current = Path.cwd()
            try:
                Path(directory, "dist").mkdir()
                import os

                os.chdir(directory)
                release_quanx_file("tag", ["a.example"], ["example.com"], ["foo"], "direct")
                validate_quanx_file("dist/tag.quanx")
                content = Path("dist/tag.quanx").read_text().splitlines()
                self.assertEqual(content[0], "host, a.example, direct")
            finally:
                os.chdir(current)

    def test_singbox_json_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "tag.json")
            path.write_text(json.dumps({"version": 2, "rules": [{"domain": ["a.example"]}]}))
            validate_singbox_json(str(path))


if __name__ == "__main__":
    unittest.main()
