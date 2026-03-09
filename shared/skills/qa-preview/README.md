# QA & preview

## Purpose

- Centralize the last quality gate before any real campaign action.
- Validate compliance, SSL, previews, and creative coverage.
- Return a decision packet that can safely unblock deployment or stop it.

## Prerequisites

- `bootstrap` has been completed;
- the relevant `creativeIds`, `lineItemIds`, or `orderId` are known;
- the creative payload was already business-approved before QA starts.

## Inputs

- `tenantId`;
- `creativeIds`, `lineItemIds`, or `orderId` depending on the preview scope;
- optional file content or bundle content for compliance scanning;
- the delivery context needed to interpret coverage gaps.

## Expected Output

- compliance findings;
- SSL validation summary;
- preview URLs at line-item or campaign scope;
- creative coverage status and deployment recommendation.

## Guardrails

- run this skill before any real deploy, update, or activation;
- prefer the smallest preview scope that answers the question;
- stop the flow on blocking compliance, SSL, or coverage findings;
- use batch SSL validation when multiple creatives are already known;
- never hide unresolved QA issues behind a deployment request.

## Handoff

- pass preview URLs, compliance findings, SSL status, and coverage summary;
- pass the explicit go / no-go recommendation and unresolved blockers;
- route next to `deploy-reporting` only when the QA gate is acceptable.