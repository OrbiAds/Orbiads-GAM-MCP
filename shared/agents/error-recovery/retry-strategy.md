# Retry Strategy

- retry only idempotent reads or explicit preview paths when the failure looks transient;
- do not silently retry destructive or billed actions;
- after one failed retry, return the observed error and the safest next option.