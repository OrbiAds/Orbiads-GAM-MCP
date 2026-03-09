# Examples

## Example User Inputs

- “Use this approved image and copy to prepare a Native creative for these line items.”
- “Ensure the Classic Native template exists, then create the creative and tell me what still needs review.”
- “Associate the approved Native creative to the selected line items and prepare the QA packet.”

## Example Response Plan

- verify advertiser and line-item context;
- prepare the image asset and template;
- create the Native creative;
- associate it to line items;
- summarize what must be reviewed next in QA and preview.

## Example Structured Output

- `creativeIds`;
- `lineItemIds`;
- `templateStatus`;
- `associationSummary`;
- `requiredReviews`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not use this skill before advertiser and line-item context is stable;
- do not skip QA and preview after the creative has been created.