# Examples

## Check CLI version

```bash
$ orbiads --version
orbiads-cli 1.2.0
```

## Verify authentication

```bash
$ orbiads auth status --json
{"authenticated": true, "tenantId": "abc123", "email": "user@example.com"}
```

## Show active network

```bash
$ orbiads network info --json
{"networkCode": "66235823", "displayName": "My Ad Network", "currencyCode": "EUR", "timeZone": "Europe/Paris"}
```

## Switch network

```bash
$ orbiads network list --json
[{"networkCode": "66235823", "displayName": "Production"}, {"networkCode": "45515589", "displayName": "Test"}]

$ orbiads network switch --network-code 45515589 --json
{"networkCode": "45515589", "displayName": "Test", "switched": true}
```
