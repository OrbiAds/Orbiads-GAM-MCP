# Examples

## Full deployment workflow

```bash
# Step 1: Verify campaign is ready
$ orbiads campaigns get campaign_123 --json
{"id": "campaign_123", "name": "Summer Campaign", "status": "DRAFT", "lineItems": 5, "creatives": 3}

# Step 2: Deploy
$ orbiads campaigns deploy campaign_123 --yes --json
{"status": "deploying", "jobId": "job_456", "creditsUsed": 5}

# Step 3: Poll status
$ orbiads campaigns get campaign_123 --json
{"id": "campaign_123", "status": "deploying", "jobId": "job_456", "progress": 60}

# ... wait 10 seconds ...
$ orbiads campaigns get campaign_123 --json
{"id": "campaign_123", "status": "deployed", "jobId": "job_456", "progress": 100}

# Step 4: Check delivery
$ orbiads reporting run --type delivery --campaign campaign_123 --json
{"campaignId": "campaign_123", "impressions": 0, "clicks": 0, "status": "not_started", "startDate": "2026-04-01"}
```

## Failed deployment

```bash
$ orbiads campaigns deploy campaign_123 --yes --json
{"status": "deploying", "jobId": "job_457", "creditsUsed": 5}

$ orbiads campaigns get campaign_123 --json
{"id": "campaign_123", "status": "failed", "jobId": "job_457", "error": "Creative 3002 rejected by GAM: SSL validation failed"}
```

## Counter-Examples

- Never deploy without running `--dry-run` first via `cli-qa`.
- Never deploy without explicit user confirmation.
- Do not poll more frequently than every 5 seconds.
