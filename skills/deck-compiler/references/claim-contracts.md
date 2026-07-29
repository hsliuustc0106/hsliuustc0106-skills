# Claim Contracts

Define claims once under `claims` and reference them from slides by stable ID.
Attach evidence to claims rather than duplicating evidence on each slide.

## Claim Classes

- `fact`: Require at least one source.
- `inference`: Require confidence plus a source or supporting claim.
- `proposal`: State a recommended action; evidence is optional unless the
  proposal also uses another class.
- `target`: Require an owner, timeline, and measurable gates.
- `comparative`: Require a baseline and comparison conditions.
- `quantitative`: Require a metric, unit, and measurement conditions.
- `illustrative`: Require a visible display label such as `Illustrative data`.

A claim may have multiple classes. Apply every relevant contract.

## Example

```yaml
claims:
  launch-target:
    statement: Launch the service within two quarters.
    classes: [target]
    acceptance:
      owner: Platform team
      timeline: End of Q2
      gates:
        - Required workflows pass acceptance testing.
        - Production readiness review is complete.

  throughput-comparison:
    statement: The proposed design doubles throughput.
    classes: [comparative, quantitative]
    measurement:
      metric: completed operations
      unit: operations per second
      conditions:
        - Same workload and quality threshold
        - Same resource envelope
    acceptance:
      baseline: Current production release
      conditions:
        - Compare repeatable median results.
```

## Configurable Claim Terms

Use `qa.claim_term_rules` to require a claim class when selected vocabulary
appears on a slide:

```yaml
qa:
  claim_term_rules:
    - pattern: "(?i)best|leading|state[- ]of[- ]the[- ]art"
      required_class: comparative
```

Keep these rules in the deck or a profile. Do not hard-code one domain's slogans
in the compiler.
