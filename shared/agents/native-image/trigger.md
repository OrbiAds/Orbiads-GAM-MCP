# Agent Trigger — native-image

## Enter when

- an approved image, copy set, and destination URL must become a Classic Native creative;
- line items are ready and the next step is creative production before QA.

## Do not enter when

- assets or copy have not been approved by a human — block and request approval first;
- the creative type is HTML5, audio, or video — those use different low-level tools outside this skill;
- line items are not yet confirmed — route to `advertiser-order-line-items` first.

## Disambiguation

- "upload this image as a Native creative" → `create_image_creative` then `create_classic_native_creative`, template first;
- "ensure the Native template exists" → `ensure_classic_native_template` only, not a full skill run;
- "associate this creative to line items" → `associate_creative` only, after creative ID is already known;
- "create an HTML5 creative" → out of scope for this skill — use `create_html5_creative_from_files` directly.
