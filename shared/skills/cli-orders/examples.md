# Examples

## Search for an advertiser

```bash
$ orbiads advertisers list --search "acme" --json
[{"id": "5001", "name": "Acme Corp", "status": "ACTIVE"}]
```

## Create a new advertiser

```bash
$ orbiads advertisers create --name "New Brand Inc" --json
{"id": "5002", "name": "New Brand Inc", "status": "ACTIVE", "creditsUsed": 1}
```

## List orders for an advertiser

```bash
$ orbiads orders list --advertiser 5001 --json
[{"id": "8001", "name": "Q2 Campaign", "status": "DRAFT", "advertiserId": "5001"}]
```

## Create a new order

```bash
$ orbiads orders create --advertiser 5001 --name "Summer Campaign 2026" --json
{"id": "8002", "name": "Summer Campaign 2026", "status": "DRAFT", "advertiserId": "5001", "creditsUsed": 1}
```
