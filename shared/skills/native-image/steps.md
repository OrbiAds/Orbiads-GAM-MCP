# Steps

1. [start] Verify that `bootstrap` is complete and that the advertiser and line-item context is already stable.
2. [depends: step 1] Reconfirm the approved copy, image asset, destination URL, and target `lineItemIds`.
3. [depends: step 2] Upload or create the image asset with `create_image_creative` only when the asset is not already available in GAM.
4. [depends: step 2] Ensure the Classic Native template with `ensure_classic_native_template`.
5. [depends: steps 3-4] Create the Native creative with `create_classic_native_creative`.
6. [depends: step 5] Associate the creative to the approved line items.
7. [depends: step 6] Hand off the created creative IDs and template details to `qa-preview`.

## Abort Conditions

- stop if the copy, image asset, URL, or line-item scope is not yet approved;
- stop if template ownership is ambiguous and could overwrite an unintended setup;
- stop if the creative payload conflicts with the destination line items.