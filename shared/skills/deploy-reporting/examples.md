# Examples

## Example User Inputs

- “Before deploying this job, give me the previews and creative coverage.”
- “Run a deployment dry run for job `abc123`, then summarize what still needs confirmation.”
- “After the push, give me the delivery report, underdelivery alerts, and latest audit traces.”

## Example Response Plan

- verify coverage and previews;
- produce the campaign action preview;
- confirm whether human validation is still required;
- read delivery state;
- run the requested reporting;
- summarize the next step.

## Example Structured Output

- `previewUrls`;
- `coverageStatus`;
- `campaignActionPreview` or `campaignActionStatus`;
- `deliveryStatus`;
- `reportResults`;
- `recommendedNextAction`.

## Counter-Examples

- do not trigger a real deployment without a preview and explicit confirmation;
- do not jump straight to heavy reports when `check_delivery_status` or alerts can answer the first question.