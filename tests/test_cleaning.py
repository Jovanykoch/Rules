import unittest

from main import DIRECT_DOMAIN, DIRECT_DOMAIN_SUFFIX, clean_domains


class CleanDomainsTests(unittest.TestCase):
    def test_removes_domains_covered_by_suffix(self):
        domain, suffix = clean_domains(
            ["a.example.com", "keep.example.net", "a.example.com"],
            ["example.com", "example.net", "example.com"],
        )
        self.assertEqual(domain, [])
        self.assertEqual(suffix, ["example.com", "example.net"])

    def test_direct_domain_extensions_are_kept_before_cleaning(self):
        domain = ["foreign.example", *DIRECT_DOMAIN]
        suffix = ["foreign.example", *DIRECT_DOMAIN_SUFFIX]
        cleaned_domain, cleaned_suffix = clean_domains(domain, suffix)
        self.assertIn("api.github.com", cleaned_domain)
        self.assertIn("cn", cleaned_suffix)


if __name__ == "__main__":
    unittest.main()
