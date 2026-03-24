# Examples

## Inspect campaign configuration

```bash
$ orbiads campaigns get campaign_123 --json
{"id": "campaign_123", "name": "Summer Campaign", "status": "DRAFT", "lineItems": 5, "creatives": 3, "targeting": {"keys": ["section"], "geo": ["FR"]}}
```

## Check creative SSL compliance

```bash
$ orbiads creatives get --id 3001 --json
{"id": "3001", "name": "Summer_Banner_728x90", "sslCompliant": true, "status": "ACTIVE"}
```

## Run dry-run deployment

```bash
$ orbiads campaigns deploy campaign_123 --dry-run --json
{"dryRun": true, "status": "pass", "warnings": ["Line item LI_002 has no frequency cap"], "errors": []}
```

## Dry-run with blocking errors

```bash
$ orbiads campaigns deploy campaign_123 --dry-run --json
{"dryRun": true, "status": "errors", "warnings": [], "errors": ["Creative 3002 is not SSL-compliant", "No targeting configured for LI_003"]}
```
