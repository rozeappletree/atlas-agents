---
name: data-pipeline
description: Design, build, or debug data processing pipelines. Use when asked to process a dataset, transform data, build an ETL pipeline, schedule batch jobs, or fix data quality issues.
license: MIT
compatibility: Requires python 3.10+
---

## Overview

Data pipelines fail silently and corrupt downstream systems. Every pipeline must be observable, idempotent, and validated at the boundary.

## Process

1. **Define the contract.** Before writing any transformation code, specify:
   - **Input schema:** What fields, types, and constraints does the data arrive with?
   - **Output schema:** What fields, types, and constraints must the output satisfy?
   - **Volume:** How many records? Per-run? Per-day?
   - **Frequency:** One-time, scheduled, or event-driven?

2. **Validate at the boundary.** The first thing any pipeline stage does is validate its input:
   ```python
   from pydantic import BaseModel, ValidationError

   class InputRecord(BaseModel):
       user_id: int
       event_type: str
       timestamp: str  # ISO 8601
       value: float | None = None

   def process(raw_records: list[dict]) -> list[dict]:
       valid, invalid = [], []
       for r in raw_records:
           try:
               valid.append(InputRecord(**r).model_dump())
           except ValidationError as e:
               invalid.append({"record": r, "error": str(e)})
       if invalid:
           log_invalid_records(invalid)  # Never silently drop
       return transform(valid)
   ```

3. **Make it idempotent.** Running the pipeline twice on the same input must produce the same output. Use upserts, not inserts. Use deterministic IDs based on input content, not auto-increment.

4. **Log progress at meaningful checkpoints.** After every major stage (extract, validate, transform, load), log the record count and any failures.

5. **Test with a sample.** Before running on the full dataset, run on 100 records. Confirm the output schema, record count, and that no records were silently dropped.

6. **Run on the full dataset.** Monitor progress. On completion, report: records in, records out, records failed, and time elapsed.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "I'll add validation later" | Invalid data corrupts your database. Validate at the boundary now. |
| "Logging slows the pipeline down" | A pipeline that fails without logs requires a full rerun to debug. Log it. |
| "It worked on the sample" | Test samples are not representative. Always run a full-dataset dry run before writing to the destination. |

## Verification

- [ ] Input and output schemas are defined before any code is written
- [ ] Invalid records are logged, not silently dropped
- [ ] Pipeline was tested on a 100-record sample before full run
- [ ] Final report includes: records in, records out, records failed
