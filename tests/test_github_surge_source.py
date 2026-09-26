import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class GitHubSurgeSourceTests(unittest.TestCase):
    def test_build_workflow_publishes_github_surge_file(self):
        workflow = (REPO_ROOT / ".github/workflows/build.yml").read_text()
        self.assertIn(
            "cp source/github_surge.list dist/ext/github_surge.list",
            workflow,
        )

    def test_build_workflow_publishes_ext_files_with_matching_names(self):
        # Source files under source/ must be published to dist/ext/ under
        # their own basename: a Surge module must not be published as .quanx.
        workflow = (REPO_ROOT / ".github/workflows/build.yml").read_text()
        for name in ("maintained.list", "github_surge.list", "bili.sgmodule", "bili.quanx"):
            self.assertIn(f"cp source/{name} dist/ext/{name}", workflow)
            self.assertTrue((REPO_ROOT / "source" / name).exists())

    def test_github_surge_source_format(self):
        source_file = REPO_ROOT / "source/github_surge.list"
        lines = source_file.read_text().splitlines()
        self.assertTrue(lines)
        self.assertEqual(len(lines), len(set(lines)))

        for line in lines:
            self.assertTrue(line)
            if line.startswith("# "):
                continue
            self.assertRegex(
                line,
                r"^(DOMAIN-SUFFIX|DOMAIN),[a-z0-9.-]+,PROXY$",
            )


if __name__ == "__main__":
    unittest.main()
