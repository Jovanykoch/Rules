import tempfile
import unittest
from pathlib import Path

from main import validate_binary_geosite, write_geosite_file


def _read_varint(data: bytes, index: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        byte = data[index]
        index += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, index
        shift += 7


def _read_fields(data: bytes) -> list[tuple[int, int, bytes]]:
    """Minimal protobuf reader: returns (field_number, wire_type, raw) fields."""
    fields = []
    index = 0
    while index < len(data):
        key, index = _read_varint(data, index)
        field_number, wire_type = key >> 3, key & 0x07
        if wire_type == 0:
            value, index = _read_varint(data, index)
            fields.append((field_number, wire_type, str(value).encode()))
        elif wire_type == 2:
            length, index = _read_varint(data, index)
            fields.append((field_number, wire_type, data[index : index + length]))
            index += length
        else:
            raise ValueError(f"Unsupported wire type {wire_type}")
    return fields


def decode_geosite_file(path: str) -> dict[str, list[tuple[int, str]]]:
    """Decode a GeoSiteList file into {tag: [(domain_type, value), ...]}."""
    data = Path(path).read_bytes()
    result: dict[str, list[tuple[int, str]]] = {}
    for field_number, wire_type, entry in _read_fields(data):
        assert (field_number, wire_type) == (1, 2)  # GeoSiteList.entry
        tag = ""
        domains: list[tuple[int, str]] = []
        for fnum, wtype, value in _read_fields(entry):
            if (fnum, wtype) == (1, 2):  # GeoSite.country_code
                tag = value.decode()
            elif (fnum, wtype) == (2, 2):  # GeoSite.domain
                domain_type = value_text = None
                for dnum, dwtype, dvalue in _read_fields(value):
                    if (dnum, dwtype) == (1, 0):  # Domain.type
                        domain_type = int(dvalue.decode())
                    elif (dnum, dwtype) == (2, 2):  # Domain.value
                        value_text = dvalue.decode()
                assert domain_type is not None and value_text is not None
                domains.append((domain_type, value_text))
            else:
                raise ValueError(f"Unexpected GeoSite field {fnum}")
        assert tag
        result[tag] = domains
    return result


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

    def test_geosite_round_trip_preserves_tags_and_types(self):
        rules = {
            "loc-cn": (
                ["full.example"],
                ["example.cn"],
                ["keyword"],
                ["^regex$"],
            ),
            "gfw": (
                [],
                ["blocked.example"],
                [],
                [],
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "geosite.dat")
            write_geosite_file(str(path), rules)
            decoded = decode_geosite_file(str(path))
        self.assertEqual(
            decoded["LOC-CN"],
            [
                (3, "full.example"),  # Full
                (2, "example.cn"),  # RootDomain
                (0, "keyword"),  # Plain
                (1, "^regex$"),  # Regex
            ],
        )
        self.assertEqual(decoded["GFW"], [(2, "blocked.example")])

    def test_geosite_deduplicates_within_type(self):
        rules = {"tag": (["dup.example", "dup.example"], [], [], [])}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "geosite.dat")
            write_geosite_file(str(path), rules)
            decoded = decode_geosite_file(str(path))
        self.assertEqual(decoded["TAG"], [(3, "dup.example")])


if __name__ == "__main__":
    unittest.main()
