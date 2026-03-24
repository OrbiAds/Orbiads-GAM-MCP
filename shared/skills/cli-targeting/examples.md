# Examples

## List all targeting keys

```bash
$ orbiads inventory keys --json
[{"name": "section", "values": ["sport", "news", "tech"]}, {"name": "page_type", "values": ["article", "home", "listing"]}]
```

## Get values for a specific key

```bash
$ orbiads inventory keys --key "section" --json
{"name": "section", "values": ["sport", "news", "tech", "entertainment", "business"]}
```

## Validate ad unit targeting compatibility

```bash
$ orbiads inventory ad-units --id 12345 --json
{"id": "12345", "name": "Homepage_Leaderboard", "sizes": ["728x90"], "targetingKeys": ["section", "page_type"], "status": "ACTIVE"}
```

## Counter-Examples

- Do not use this skill to create targeting keys — use MCP or GAM web UI.
- Do not use this skill to deploy campaigns.
