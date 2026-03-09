# Claude Skill Wrapper — native-image

- load `../../shared/agents/native-image/`;
- execute `../../shared/skills/native-image/`;
- use this skill for approved image assets that must become Classic Native creatives.

## Claude-Specific Hints

- show the creative payload (headline, body, CTA, URL, image reference) as an artifact before creation — one human approval required;
- use `<handoff>` tags to pass `creativeIds`, `templateStatus`, and `lineItemIds` to `qa-preview`;
- never create the creative until the asset, copy, and destination URL are explicitly confirmed in the conversation;
- flag template recreation risk inline if `ensure_classic_native_template` returns a mismatch.
