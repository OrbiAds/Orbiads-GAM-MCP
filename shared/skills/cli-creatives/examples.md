# Examples

## List all creatives

```bash
$ orbiads creatives list --json
[{"id": "3001", "name": "Summer_Banner_728x90", "advertiserId": "5001", "status": "ACTIVE"}, {"id": "3002", "name": "Summer_MPU_300x250", "advertiserId": "5001", "status": "ACTIVE"}]
```

## Get creative details

```bash
$ orbiads creatives get --id 3001 --json
{"id": "3001", "name": "Summer_Banner_728x90", "advertiserId": "5001", "size": "728x90", "status": "ACTIVE", "sslCompliant": true}
```

## Upload a new creative

```bash
$ orbiads creatives upload --file ./assets/banner_728x90.png --name "Fall_Banner_728x90" --advertiser 5001 --json
{"id": "3003", "name": "Fall_Banner_728x90", "advertiserId": "5001", "size": "728x90", "status": "ACTIVE", "creditsUsed": 5}
```

## Counter-Examples

- Do not upload without confirming the credit cost with the user.
- Do not use this skill for creative compliance checks — use `cli-qa`.
