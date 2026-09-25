# rules

An automated rule-generation repository for proxy tools. The project fetches `domain-list-community` and `GFWList`, parses the upstream data, and generates artifacts for Surge, Clash, Quantumult X, sing-box, and V2Ray GeoSite.

## Update Schedule

- Automatic builds run daily at 00:00 UTC.
- Pushing to `main` triggers a build.
- Workflows can also be triggered manually.

## Local Build

Prerequisites:

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- sing-box, available as the `sing-box` executable

```bash
uv sync
uv run generate
```

Run tests:

```bash
uv run python -m unittest discover -s tests
```

## Rule Tags

- `reject`: Advertising and blocking rules
- `loc-cn`: Rules for direct connections in mainland China
- `loc-!cn`: Rules for destinations outside mainland China
- `gfw`: Proxy rules derived from GFWList
- `gfw-skip`: Direct-connection allowlist rules derived from GFWList

## `rel` Branch Artifacts

Main artifacts include:

- `*.list`: Surge DOMAIN-SET files
- `*.yaml`: Clash payload files
- `*.quanx`: Quantumult X `filter_remote` files
- `*.srs`: sing-box binary rule-set files
- `geosite.dat`, `geosite-cn.dat`, and `geosite-gfw.dat`: V2Ray GeoSite data
- `ext/*`: Extension files maintained under `source/`

The `rel` branch is published automatically and may be force-pushed by the workflow. Do not edit it manually.

## Common Download URLs

- https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/loc-cn.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/loc-!cn.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/gfw.list
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.srs
- https://raw.githubusercontent.com/Jovanykoch/rules/rel/geosite.dat

## Client Configuration Examples

- Surge: `DOMAIN-SET,https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.list,REJECT`
- Clash: Set a `rule-providers` entry to `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.yaml`
- Quantumult X: Set a `filter_remote` entry to `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.quanx`
- sing-box: Set a remote rule-set URL to `https://raw.githubusercontent.com/Jovanykoch/rules/rel/reject.srs`

## Generation Pipeline

1. Download DLC and GFWList data.
2. Parse and normalize the rules, including deduplication and parent-domain consolidation.
3. Generate files in multiple formats in parallel.
4. Compile sing-box `.srs` files.
5. Generate GeoSite protobuf data.
6. Validate the output formats and publish the artifacts to `rel`.

## License and Upstream Attribution

The code in this repository is released under the MIT License (see `LICENSE`).

Upstream rule data, including `domain-list-community`, `GFWList`, and other third-party sources, remains subject to the licenses and terms of use of the respective upstream repositories. This repository only aggregates, converts, and distributes that data.
