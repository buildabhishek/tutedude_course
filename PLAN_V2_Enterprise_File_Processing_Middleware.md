# PLAN.md V2 — Enterprise File Processing Middleware

**Project:** Application 2 — Phase 2  
**Document:** Master Engineering Plan  
**Status:** Proposed architecture — implementation blueprint  
**Primary audience:** Developer, Tester, Business Analyst, Architect, DevOps, Client/Reviewer  
**Last updated:** 13 September 2026

---

# 1. Purpose

This document is the **engineering master plan** for Phase 2.

The official assignment/PDF is the contractual baseline. Everything else in this document is classified as either:

- **MANDATORY** — explicitly required by the assignment/mentor.
- **ENHANCEMENT** — engineering improvements proposed to make the solution production/enterprise ready.
- **DECISION** — an architectural choice made in this plan.
- **OPEN** — must be confirmed by the architect/manager before being treated as a contractual requirement.

The goal is not to add technology for appearance.

The goal is:

> **Make the middleware reliable, observable, recoverable, scalable, configurable, testable and understandable to both technical and non-technical users while respecting the one-trigger Phase 2 constraint.**

---

# 2. Current Confirmed Direction

## 2.1 Phase 2 trigger constraint

**MANDATORY / CONFIRMED**

The architect/mentor clarified:

> "One function trigger."

Therefore Phase 2 must use **exactly one Azure Function trigger**.

This does NOT mean:

- one giant method;
- no services;
- no interfaces;
- no separation of concerns;
- no internal orchestration.

It means:

```text
ONE AZURE FUNCTION TRIGGER
          |
          v
APPLICATION ORCHESTRATOR
          |
   +------+-------+--------+---------+
   |              |        |         |
Validation      SQL      Blob      Outputs
State           Config   Storage    Telemetry
```

The trigger is the single event entry point.

---

# 3. Recommended One-Trigger Architecture

## 3.1 Preferred direction

**DECISION — proposed**

Use a **Service Bus Queue Trigger** as the single Azure Function trigger.

The intended flow:

```text
                    FILE PRODUCER
                         |
                         v
                 Azure Blob Storage
                    /input/*.xml
                         |
                         v
              Event / Integration Layer
                         |
                         v
                 Service Bus Queue
                         |
                         v
       +--------------------------------------+
       | ONE AZURE FUNCTION TRIGGER           |
       | Service Bus Queue Trigger             |
       +------------------+-------------------+
                          |
                          v
                Processing Orchestrator
                          |
          +---------------+----------------+
          |               |                |
          v               v                v
      Blob Read          SQL          Configuration
          |               |                |
          +---------------+----------------+
                          |
                          v
                  XML Stream / Parse
                          |
                          v
                    Validation
                          |
                          v
                   Batch Processing
                          |
                          v
              Duplicate / Business Rules
                          |
                          v
                Output Generator Factory
                          |
        +---------+------+------+------+------+
        |         |      |      |      |
        v         v      v      v      v
       TXT       CSV    JSON    XML    DAT
        |         |      |      |      |
        +---------+------+------+------+------+
                          |
                          v
                    Archive Input
                          |
                          v
                       SUCCESS
```

### Important

The event/integration mechanism that places a message onto Service Bus must be confirmed against the actual assignment infrastructure.

The architecture must not introduce a second Azure Function trigger merely to get the file onto the queue.

---

# 4. Why Service Bus Queue as the Trigger?

**DECISION — proposed**

Service Bus is useful because the system needs:

- asynchronous processing;
- retry;
- dead-letter handling;
- decoupling;
- controlled processing;
- durable messages;
- failure isolation.

The message should reference the Blob rather than carry the entire XML file.

Example message:

```json
{
  "processingJobId": "GUID",
  "correlationId": "GUID",
  "container": "input-container",
  "blobPath": "input/customer.xml",
  "fileName": "customer.xml",
  "fileHash": "SHA256"
}
```

The Function then reads the file from Blob Storage.

---

# 5. Core Engineering Principles

## 5.1 Reliability

The system must have a predictable answer for:

- duplicate messages;
- duplicate files;
- invalid files;
- transient infrastructure failures;
- permanent failures;
- partial output;
- Function restart;
- archive failure;
- configuration changes;
- concurrent processing.

## 5.2 Observability

Every important operation must answer:

```text
WHAT happened?
WHERE did it happen?
WHICH file?
WHICH job?
WHICH correlation ID?
WHICH stage?
WHEN?
HOW LONG?
WHY did it fail?
CAN it recover?
```

## 5.3 Recoverability

A crash must not force the system to guess what already happened.

Durable state + checkpoints + output state should determine recovery.

## 5.4 Scalability

Avoid:

```text
1 customer
→ 1 SQL query
→ 1 log
→ 1 transaction
```

for millions of records.

Use:

```text
Stream
→ batch
→ set-based SQL
→ checkpoint
```

---

# 6. File Identity Model

## 6.1 Filename is NOT identity

This is a fundamental rule.

These are different processing jobs:

```text
customer.xml
CustomerId = C001
```

and:

```text
customer.xml
CustomerId = C002
```

Same filename does not mean duplicate.

## 6.2 Processing identity

Each uploaded processing operation receives:

```text
ProcessingJobId
CorrelationId
OriginalFileName
InputBlobPath
FileHash
```

Recommended:

```text
ProcessingJobId = database primary key / internal identifier
CorrelationId = cross-system telemetry identifier
FileHash = content identity/idempotency aid
OriginalFileName = human-readable source name
```

## 6.3 Business duplicate

Duplicate customer detection is based on:

```text
CustomerId
```

not filename.

A database uniqueness constraint should provide the final integrity guarantee.

---

# 7. Same Filename Scenario

Input 1:

```text
customer.xml
CustomerId = 1001
OrderId = 5001
Address = A
```

Input 2:

```text
customer.xml
CustomerId = 1002
OrderId = 5002
Address = B
```

Expected:

```text
ProcessingJob A
ProcessingJob B
```

Each gets a unique internal job ID.

Storage:

```text
output/
  /{ProcessingJobId-A}/
      customer.txt
      customer.csv
      customer.json
      customer.xml
      customer.dat

  /{ProcessingJobId-B}/
      customer.txt
      customer.csv
      customer.json
      customer.xml
      customer.dat
```

No:

```text
copy-of-customer.xml
customer-1.xml
final-final.xml
```

---

# 8. State Management

## 8.1 File state machine

Recommended:

```text
RECEIVED
   |
   v
QUEUED
   |
   v
PROCESSING
   |
   +--> VALIDATING
   |
   +--> PROCESSING_RECORDS
   |
   +--> GENERATING_OUTPUT
   |
   +--> ARCHIVING
   |
   v
COMPLETED
```

Failure paths:

```text
PROCESSING
   |
   v
RETRYING
   |
   +----> PROCESSING

PROCESSING
   |
   v
FAILED
```

## 8.2 Completion statuses

Recommended:

```text
COMPLETED
COMPLETED_WITH_ERRORS
FAILED
RETRYING
DEAD_LETTERED
```

Do not use a vague status such as:

```text
SUCCESS
```

when the file actually has rejected records.

---

# 9. Per-Output State

The file state is not enough.

For five outputs:

```text
TXT  = COMPLETED
CSV  = COMPLETED
JSON = COMPLETED
XML  = COMPLETED
DAT  = FAILED
```

Dashboard:

```text
4 / 5 outputs completed
1 output failed
```

This allows targeted recovery.

---

# 10. Checkpointing

Checkpoint state should identify where the processing job can safely resume.

Example:

```text
Job: 123
Stage: RECORD_PROCESSING
Batch: 240
RecordsProcessed: 1,200,000
```

For outputs:

```text
TXT  ✓
CSV  ✓
JSON ✓
XML  ✓
DAT  ✗
```

The recovery logic should not regenerate successful work unnecessarily unless the output contract requires it.

---

# 11. Idempotency

The system must tolerate repeated delivery.

Example:

```text
Message A → Job 123
Message A delivered again
```

Expected:

```text
Existing Job 123
Already completed
→ do not duplicate processing
```

Application checks are useful, but database constraints are the final protection against concurrent duplicate writes.

---

# 12. Configuration-Driven Development

## 12.1 Objective

The output formats must be configurable.

Example:

```text
Configuration V1
TXT = true
CSV = true
JSON = true
XML = true
DAT = false
```

Another configuration:

```text
Configuration V2
TXT = true
CSV = true
JSON = true
XML = true
DAT = true
```

## 12.2 Configuration snapshot

A ProcessingJob stores:

```text
ConfigurationVersion
```

at the beginning of processing.

Therefore:

```text
Job 100 → Config V1
Job 101 → Config V1

Config changes

Job 102 → Config V2
```

An already queued job must not unexpectedly switch configuration halfway through.

## 12.3 Mixed upload scenario

If:

```text
Files 1–5 → four formats
Files 6–10 → five formats
```

the configuration is resolved per ProcessingJob.

Therefore:

```text
Job 1 → V10 → 4 outputs
Job 2 → V10 → 4 outputs
...
Job 6 → V11 → 5 outputs
```

No code modification is required.

---

# 13. Output Generator Architecture

Use a strategy/factory approach:

```text
IOutputGenerator
       |
       +-- TxtOutputGenerator
       +-- CsvOutputGenerator
       +-- JsonOutputGenerator
       +-- XmlOutputGenerator
       +-- DatOutputGenerator
       +-- PdfOutputGenerator [ENHANCEMENT]
```

The core processor should not contain:

```csharp
if (format == "TXT") ...
if (format == "CSV") ...
if (format == "JSON") ...
```

for every format.

Instead:

```text
Configuration
      |
      v
OutputGeneratorFactory
      |
      v
Required generators
```

This supports the Open/Closed Principle.

---

# 14. Output Storage

Recommended:

```text
output/
    {ProcessingJobId}/
        {base-name}.txt
        {base-name}.csv
        {base-name}.json
        {base-name}.xml
        {base-name}.dat
```

The database stores the authoritative metadata:

```text
Format
FileName
BlobPath
Status
AttemptCount
CreatedAt
CompletedAt
```

Blob Storage stores the physical output.

SQL does not need to contain the entire output file.

---

# 15. What if 4 Outputs Succeed and the 5th Fails?

Example:

```text
TXT  ✓
CSV  ✓
JSON ✓
XML  ✓
DAT  ✗
```

Database:

```text
Job = PARTIALLY_COMPLETED / FAILED_OUTPUT
```

Output table:

```text
TXT  COMPLETED
CSV  COMPLETED
JSON COMPLETED
XML  COMPLETED
DAT  FAILED
```

If DAT is retryable:

```text
Retry DAT
```

If successful:

```text
DAT COMPLETED
Job COMPLETED
```

If retry exhaustion occurs:

```text
DAT DEAD_LETTERED / FAILED
Job FAILED
```

The exact final status terminology should be confirmed.

---

# 16. XML Validation

Validation should occur in layers.

## Layer 1 — File validation

```text
File exists?
Size > 0?
Readable?
```

## Layer 2 — XML validation

```text
Well-formed XML?
Expected root?
Expected structure?
Schema valid?
```

## Layer 3 — field validation

Examples:

```text
CustomerId present?
DOB valid?
Address valid?
Required fields present?
```

## Layer 4 — business validation

Examples:

```text
Customer already exists?
Business rule violated?
Unsupported value?
```

Do not confuse:

```text
Malformed XML
```

with:

```text
Valid XML containing invalid customer data
```

---

# 17. Empty XML

A 0 KB file must not enter normal XML processing.

```text
Blob
 ↓
Size = 0
 ↓
ERROR
 ↓
Error location
```

Record:

```text
ErrorType = EMPTY_FILE
FileName
ProcessingJobId
CorrelationId
Timestamp
Reason
```

---

# 18. Invalid Record Handling

Example:

```text
1000 records
```

Results:

```text
600 valid
300 duplicate
100 invalid
```

The system should not automatically fail all 1000 unless the official business contract requires whole-file rejection.

Recommended enterprise behavior:

```text
Valid records
      ↓
normal output

Duplicate/invalid records
      ↓
error/rejection output
```

The exact error-file format must follow the assignment.

---

# 19. Large File Strategy

No arbitrary file-size assumption should be built into application logic.

Use streaming:

```text
Blob Stream
    ↓
XmlReader
    ↓
Record
    ↓
Validation
    ↓
Batch
    ↓
SQL
    ↓
Checkpoint
```

Avoid:

```text
Read entire XML
      ↓
10 million objects in memory
```

---

# 20. Batch Processing

For very large input:

```text
10,000,000 records
```

process:

```text
Batch 1 = 5,000
Batch 2 = 5,000
Batch 3 = 5,000
...
```

Batch size must be configurable and performance-tested.

---

# 21. SQL Strategy

## 21.1 Primary data-access choice

**DECISION — proposed**

Use:

> **EF Core as the primary ORM.**

Why:

- many relational tables;
- relationships;
- entity mapping;
- dashboard/API queries;
- configuration;
- state management;
- maintainability;
- migrations/model management where appropriate.

## 21.2 Stored procedures

Use stored procedures selectively for:

- high-volume batch operations;
- set-based duplicate detection;
- bulk insert/update;
- SQL-heavy operations where SQL is the better execution layer.

## 21.3 Dapper

Do not add Dapper simply because it is perceived as faster.

If the application is predominantly relational and has many entities/tables, EF Core provides a stronger default abstraction.

If profiling later demonstrates a workload where Dapper is materially beneficial, that can be introduced deliberately.

---

# 22. Database Design

Core entities:

```text
ProcessingJob
ProcessingOutput
ProcessingError
ProcessingCheckpoint
RetryHistory
AuditEvent
Customer
OutputFormat
ProcessingConfiguration
ProcessingConfigurationFormat
ValidationResult
```

---

# 23. ProcessingJob

Suggested columns:

```text
ProcessingJobId       PK
CorrelationId         UNIQUE
OriginalFileName
InputContainer
InputBlobPath
FileHash
Status
CurrentStage
TotalRecords
SuccessfulRecords
DuplicateRecords
InvalidRecords
FailedRecords
RetryCount
ConfigurationVersion
ReceivedAt
StartedAt
CompletedAt
CreatedAt
UpdatedAt
```

---

# 24. ProcessingOutput

```text
ProcessingOutputId    PK
ProcessingJobId       FK
Format
FileName
BlobPath
Status
AttemptCount
StartedAt
CompletedAt
ErrorMessage
CreatedAt
UpdatedAt
```

Recommended uniqueness:

```text
UNIQUE(ProcessingJobId, Format)
```

This prevents two logical records for the same output format within one job.

---

# 25. ProcessingError

```text
ProcessingErrorId
ProcessingJobId       FK
ProcessingOutputId    FK nullable
ErrorType
ErrorCode
Message
RecordIdentifier
Retryable
OccurredAt
```

Avoid putting sensitive customer information into logs/errors unnecessarily.

---

# 26. ProcessingCheckpoint

```text
CheckpointId
ProcessingJobId       FK
Stage
BatchNumber
RecordsProcessed
LastSuccessfulStep
CreatedAt
```

---

# 27. RetryHistory

```text
RetryHistoryId
ProcessingJobId       FK
AttemptNumber
Reason
Result
StartedAt
CompletedAt
```

---

# 28. AuditEvent

```text
AuditEventId
ProcessingJobId       FK
CorrelationId
EventType
Description
OccurredAt
```

This provides a durable business/operational timeline.

---

# 29. Customer

The exact customer schema must follow the XML/business model.

At minimum, where appropriate:

```text
CustomerId            PK / UNIQUE BUSINESS KEY
...
```

Do not assume filename is a customer identifier.

---

# 30. Configuration Model

Recommended:

```text
ProcessingConfiguration
        |
        +-- ConfigurationVersion
        +-- IsActive
        +-- CreatedAt
        |
        v
ProcessingConfigurationFormat
        |
        +-- Format
        +-- Enabled
```

This allows:

```text
Configuration V1
    TXT ✓
    CSV ✓
    JSON ✓
    XML ✓
    DAT ✗
```

---

# 31. Relationships

```text
ProcessingJob
    |
    +----< ProcessingOutput
    |
    +----< ProcessingError
    |
    +----< ProcessingCheckpoint
    |
    +----< RetryHistory
    |
    +----< AuditEvent
```

Configuration:

```text
ProcessingConfiguration
    |
    +----< ProcessingConfigurationFormat
```

Customer relationships must follow the actual business model and should not be invented solely for normalization.

---

# 32. Primary Keys

Recommended:

```text
ProcessingJobId
ProcessingOutputId
ProcessingErrorId
ProcessingCheckpointId
RetryHistoryId
AuditEventId
```

Use surrogate integer/long keys or GUIDs according to the database conventions and expected scale.

Use GUIDs where distributed correlation/identity benefits from them.

Do not use a filename as a primary key.

---

# 33. Foreign Keys

Foreign keys enforce relational integrity.

Examples:

```text
ProcessingOutput.ProcessingJobId
    → ProcessingJob.ProcessingJobId

ProcessingError.ProcessingJobId
    → ProcessingJob.ProcessingJobId

ProcessingCheckpoint.ProcessingJobId
    → ProcessingJob.ProcessingJobId
```

Use appropriate delete behavior. Avoid accidental cascading deletion of audit/history data.

---

# 34. Index Strategy

Indexes must be based on real query patterns.

Initial candidates:

```text
ProcessingJob
    UNIQUE CorrelationId
    INDEX Status
    INDEX ReceivedAt
    INDEX FileHash

ProcessingOutput
    INDEX ProcessingJobId
    INDEX Status
    UNIQUE(ProcessingJobId, Format)

ProcessingError
    INDEX ProcessingJobId
    INDEX ErrorType
    INDEX OccurredAt

AuditEvent
    INDEX ProcessingJobId
    INDEX OccurredAt

Customer
    UNIQUE CustomerId
```

Validate with execution plans and realistic load tests.

---

# 35. Database Views

Potential operational views:

```text
vw_FileProcessingSummary
vw_FileProcessingTimeline
vw_OutputProcessingStatus
vw_ErrorSummary
```

Views should simplify reporting.

The API should normally query application/repository abstractions rather than exposing arbitrary SQL directly.

---

# 36. Transactions

Use transactions where state must change atomically.

Good candidate:

```text
Batch database operation
    +
checkpoint/state update
```

Avoid holding a transaction across long Blob operations or external waits.

---

# 37. Error Taxonomy

Recommended categories:

```text
EMPTY_FILE
MALFORMED_XML
SCHEMA_VALIDATION_ERROR
MISSING_REQUIRED_FIELD
INVALID_CUSTOMER_ID
INVALID_DATE
INVALID_ADDRESS
DUPLICATE_CUSTOMER
UNSUPPORTED_FORMAT
DATABASE_ERROR
STORAGE_ERROR
SERVICE_BUS_ERROR
TIMEOUT
UNKNOWN_ERROR
```

Every error should have:

```text
ErrorType
ErrorCode
Message
Retryable
CorrelationId
ProcessingJobId
```

---

# 38. Retry Policy

## Retryable

Examples:

```text
Transient SQL error
Temporary storage failure
Temporary Service Bus failure
Network timeout
```

## Non-retryable

Examples:

```text
Empty XML
Malformed XML
Invalid DOB
Invalid address
Duplicate customer
Unsupported format
```

Retries must be bounded.

Never implement infinite retry loops.

---

# 39. Dead Letter

When a Service Bus message cannot be processed successfully after the configured retry policy, it should reach the dead-letter mechanism.

Additionally, the project has a `deadletter` directory for failed artifacts where required by the assignment/design.

Recommended metadata:

```text
ProcessingJobId
CorrelationId
FileName
FailureReason
AttemptCount
Timestamp
```

The exact interaction between Service Bus DLQ and the Blob `deadletter` directory must be explicitly documented so they are not confused.

---

# 40. Error Directory

Recommended:

```text
error/
    {ProcessingJobId}/
```

Use it for invalid input/business/data failures according to the official contract.

Examples:

```text
0 KB XML
Malformed XML
Invalid DOB
Invalid address
Invalid customer data
```

---

# 41. Archive

Successful processing should move the original input out of the input directory.

Recommended:

```text
input/
archive/
error/
deadletter/
output/
```

The trigger must only observe the intended input event/path.

---

# 42. Trigger Loop Prevention

Never configure the Blob trigger over the entire container if archive/error/output/deadletter objects can cause events.

Conceptually:

```text
container/
├── input/        ← input events
├── output/
├── archive/
├── error/
└── deadletter/
```

Only the intended input event should initiate processing.

---

# 43. Application Logging

Every major event should include:

```text
Timestamp
Level
ProcessingJobId
CorrelationId
FileName
BlobPath
Stage
Status
Attempt
Duration
```

Example:

```text
[INFO]
FileName=customer.xml
ProcessingJobId=123
CorrelationId=abc
Stage=XML_VALIDATION
Status=STARTED
```

Then:

```text
[INFO]
FileName=customer.xml
ProcessingJobId=123
CorrelationId=abc
Stage=XML_VALIDATION
Status=COMPLETED
DurationMs=180
```

---

# 44. Local Terminal Experience

When running locally in Visual Studio/terminal, logs should tell a complete story.

Example:

```text
[INFO] Blob event received
[INFO] File: customer.xml
[INFO] ProcessingJobId: 8f...
[INFO] CorrelationId: 91...
[INFO] Service Bus message received
[INFO] State: RECEIVED -> PROCESSING
[INFO] Validating XML
[INFO] XML validation completed
[INFO] Processing batch 1: 5,000 records
[INFO] Batch 1 completed: Success=4,980 Duplicate=20 Invalid=0
[INFO] Generating TXT: customer.txt
[INFO] TXT completed
[INFO] Generating CSV: customer.csv
[INFO] CSV completed
[INFO] Generating JSON: customer.json
[INFO] JSON completed
[INFO] Generating XML: customer.xml
[INFO] XML completed
[INFO] Generating DAT: customer.dat
[INFO] DAT completed
[INFO] Archiving input file
[INFO] Input removed from input directory
[INFO] File completed
[INFO] Final status: COMPLETED
```

A developer should be able to understand the flow without debugging line-by-line.

---

# 45. Application Insights

Use structured telemetry with custom dimensions:

```text
ProcessingJobId
CorrelationId
FileName
Stage
OutputFormat
Status
ErrorType
Attempt
```

Avoid high-cardinality or sensitive data where unnecessary.

---

# 46. Custom Metrics

Recommended:

```text
FilesReceived
FilesProcessing
FilesCompleted
FilesFailed
FilesRetried
FilesDeadLettered

RecordsProcessed
RecordsSuccessful
RecordsDuplicate
RecordsInvalid

OutputsGenerated
OutputsFailed

ProcessingDuration
OutputGenerationDuration
ValidationDuration
DatabaseDuration
```

---

# 47. KQL Operational Questions

The telemetry design must allow queries answering:

### Failed files

```text
Which files failed today?
```

### Stuck files

```text
Which files have been processing unusually long?
```

### Output failures

```text
Which output format fails most often?
```

### Performance

```text
What is average processing duration?
```

### Retry

```text
How many files were retried?
```

### Data quality

```text
How many invalid/duplicate records occurred?
```

---

# 48. Health Endpoints

Recommended:

```text
GET /api/health
GET /api/health/ready
```

Potential dependencies:

```text
SQL
Blob Storage
Service Bus
```

Distinguish:

```text
Liveness
Readiness
Dependency failure
```

Health checks should be lightweight.

---

# 49. REST API

Recommended operational APIs:

```text
GET /api/health

GET /api/files
GET /api/files/{processingJobId}

GET /api/files/{processingJobId}/outputs
GET /api/files/{processingJobId}/errors
GET /api/files/{processingJobId}/timeline
GET /api/files/{processingJobId}/checkpoints

GET /api/metrics/summary
```

Optional enhancement:

```text
POST /api/files/{processingJobId}/reprocess
```

Reprocessing must have safeguards and must not create duplicate business data.

---

# 50. DTO Strategy

DTOs are API contracts.

Example:

```text
ProcessingJobEntity
        |
        v
ProcessingJobDto
```

The DTO does not detect physical output files.

The application/database records output state:

```text
Format = CSV
Status = COMPLETED
FileName = customer.csv
BlobPath = output/job123/customer.csv
```

API response:

```json
{
  "format": "CSV",
  "status": "COMPLETED",
  "fileName": "customer.csv"
}
```

---

# 51. Dashboard

The dashboard should consume REST APIs.

It should not directly connect to SSMS.

## Summary

```text
Files Received       128
Processing              3
Completed             118
Failed                  5
Retrying                2
```

## File list

```text
File              Status        Records    Outputs
----------------------------------------------------
customer-001.xml  COMPLETED     10,000     5/5
customer-002.xml  PROCESSING    50,000     3/5
customer-003.xml  FAILED         2,000     0/5
```

## Detail

```text
File
ProcessingJobId
CorrelationId
Status
CurrentStage
Records
Success
Duplicate
Invalid
RetryCount

TXT  ✓
CSV  ✓
JSON ✓
XML  ✓
DAT  ⏳
```

## Timeline

```text
RECEIVED
QUEUED
PROCESSING
VALIDATING
PROCESSING_RECORDS
GENERATING_OUTPUT
ARCHIVING
COMPLETED
```

A BA or client should understand this without opening:

- SSMS;
- Application Insights;
- KQL;
- Visual Studio;
- Windows Terminal.

---

# 52. Cache Decision

No cache is required initially.

The database is the durable source of truth for processing state.

If performance testing later proves that configuration/reference data causes excessive database load, introduce caching deliberately.

Do not introduce Redis merely to make the architecture look enterprise.

---

# 53. Concurrency

Assume multiple files can arrive simultaneously.

Each job must have isolated:

```text
ProcessingJobId
CorrelationId
State
Checkpoint
Outputs
Errors
```

No processing state should depend on static/global in-memory variables.

Database constraints must protect against concurrent duplicate writes.

---

# 54. Cancellation and Timeouts

External operations need bounded execution.

Consider:

```text
CancellationToken
SQL command timeout
Blob operation timeout
Service Bus timeout
```

Never allow an infrastructure problem to create an indefinite Function invocation.

---

# 55. Security

Even if authentication is not currently required:

- never log secrets;
- never expose connection strings;
- do not put sensitive customer data into telemetry;
- validate API parameters;
- use least privilege;
- keep secrets/configuration outside source code;
- do not expose SQL directly to the dashboard.

Authentication/authorization remains **OPEN** if not specified in the official requirement.

---

# 56. Clean Architecture

Recommended structure:

```text
src/
├── Functions/
│   └── FileProcessingFunction.cs
│
├── Application/
│   ├── Services/
│   ├── Interfaces/
│   ├── DTOs/
│   └── UseCases/
│
├── Domain/
│   ├── Entities/
│   ├── Enums/
│   └── ValueObjects/
│
├── Infrastructure/
│   ├── Persistence/
│   ├── Storage/
│   ├── Messaging/
│   └── Telemetry/
│
├── Processing/
│   ├── Xml/
│   ├── Validation/
│   ├── Mapping/
│   └── OutputGenerators/
│
└── Tests/
    ├── Unit/
    └── Integration/
```

The Function trigger should remain thin.

---

# 57. One Trigger ≠ One Class Responsibility

Bad:

```text
Function
 └── 2,000 lines
```

Good:

```text
Function Trigger
       |
       v
ProcessingOrchestrator
       |
       +-- FileStateService
       +-- BlobStorageService
       +-- XmlProcessor
       +-- ValidationService
       +-- CustomerService
       +-- OutputGeneratorFactory
       +-- ConfigurationService
       +-- CheckpointService
       +-- ArchiveService
       +-- TelemetryService
```

The architect can inspect each responsibility independently.

---

# 58. Testing Strategy

## Unit tests

Test:

```text
XML parser
Validators
Duplicate rules
Output generators
Filename rules
State transitions
Configuration resolution
Error classification
```

## Integration tests

Test:

```text
Blob
Service Bus
SQL
Output storage
```

## Failure tests

Test:

```text
Empty XML
Malformed XML
Invalid DOB
Invalid address
Duplicate customer
Duplicate message
Same filename/different content
SQL failure
Blob failure
Service Bus failure
Timeout
Archive failure
Output failure
Retry exhaustion
Function restart
Checkpoint recovery
```

## Performance tests

Test:

```text
1,000 records
100,000 records
1,000,000+ records
```

where the environment permits.

---

# 59. "What If?" Catalogue

This is a core differentiator.

| What if? | Design answer |
|---|---|
| Empty XML | Reject → error |
| Malformed XML | Reject → error |
| Invalid DOB | Record validation failure |
| Invalid address | Record validation failure |
| Invalid CustomerId | Record validation failure |
| Customer already exists | Duplicate handling |
| Same filename uploaded again | New ProcessingJob |
| Same content uploaded again | Idempotency/file-hash policy |
| Same Service Bus message delivered twice | Idempotent processing |
| 1,000 records / 400 duplicate | Process valid records; track duplicates |
| 10M records | Streaming + batching |
| One output fails | Per-output state + retry |
| 4/5 outputs succeed | Preserve 4; recover 5th where safe |
| SQL temporarily unavailable | Retry |
| SQL permanently fails | Fail/dead-letter |
| Blob temporarily unavailable | Retry |
| Function crashes | Durable state/checkpoint |
| Archive fails | Retry; don't falsely complete |
| Config changes while queued | Use captured config version |
| Multiple files arrive together | Isolated jobs |
| Error file triggers Function | Trigger scope prevents it |
| Archive file triggers Function | Trigger scope prevents it |
| Database contains duplicate CustomerId | Database constraint protects integrity |
| Logs become huge | File/batch-level logging |
| Dashboard cannot find file | Correlation + indexed job lookup |
| Processing gets stuck | State + heartbeat/timestamp + dashboard/KQL |
| Output naming collision | Job-scoped storage + deterministic naming |

---

# 60. Processing Timeline

Every job should have a durable timeline:

```text
16:01:02 RECEIVED
16:01:03 QUEUED
16:01:05 PROCESSING
16:01:05 VALIDATING
16:01:06 VALIDATION_COMPLETED
16:01:06 RECORD_PROCESSING
16:01:09 OUTPUT_GENERATION
16:01:10 TXT_COMPLETED
16:01:10 CSV_COMPLETED
16:01:11 JSON_COMPLETED
16:01:11 XML_COMPLETED
16:01:12 DAT_COMPLETED
16:01:12 ARCHIVING
16:01:13 COMPLETED
```

This is more useful than raw log lines alone.

---

# 61. Stuck Processing Detection

Enhancement.

Add:

```text
LastHeartbeatAt
CurrentStage
UpdatedAt
```

Dashboard can flag:

```text
PROCESSING for 45 minutes
```

when normal processing is expected to take seconds/minutes.

This does not automatically mean the job is failed.

It means:

> **Potentially stuck — investigate.**

---

# 62. Operational State vs Technical Telemetry

Do not make Application Insights the only source of truth.

Use:

```text
SQL
    = durable processing state

Application Insights
    = diagnostic telemetry

Dashboard/API
    = operational interface
```

Each has a different responsibility.

---

# 63. Audit vs Logging

Logging:

```text
Debugging / diagnostics
```

Audit:

```text
Durable business/operational history
```

Do not assume Application Insights is a permanent business audit database.

---

# 64. Configuration and Secrets

Separate:

```text
Application configuration
```

from:

```text
Secrets
```

Configuration examples:

```text
Enabled output formats
Batch size
Retry count
Timeout
Storage paths
```

Secrets should not be committed to source control.

---

# 65. Local Development

Local environment should make the full lifecycle visible.

Example:

```text
Blob uploaded
↓
Message created
↓
Queue received
↓
Function started
↓
File identified
↓
State changed
↓
XML validated
↓
Records processed
↓
Outputs generated
↓
Database updated
↓
Archive completed
↓
Final status
```

Local logs should use the same correlation identifiers as telemetry.

---

# 66. Development Order

## Step 1 — Requirement freeze

- Extract PDF requirements.
- Mark mandatory requirements.
- Record open questions.

## Step 2 — Architecture

- Confirm one trigger.
- Confirm Service Bus role.
- Confirm Blob event mechanism.
- Draw final architecture.

## Step 3 — Database

- ERD.
- Tables.
- PK/FK.
- Constraints.
- Indexes.
- Views.
- Stored procedures.
- EF Core model.

## Step 4 — Domain

- Entities.
- Enums.
- State machine.
- Validation models.

## Step 5 — Infrastructure

- Blob.
- Service Bus.
- SQL.
- Telemetry.

## Step 6 — Processing

- Streaming XML.
- Validation.
- Mapping.
- Batching.
- Duplicate detection.

## Step 7 — Outputs

- Generator abstraction.
- Five formats.
- Config selection.
- Per-output state.

## Step 8 — Reliability

- Idempotency.
- Retry.
- Timeout.
- Checkpoint.
- Recovery.
- Dead letter.
- Archive.

## Step 9 — API

- Health.
- Files.
- Outputs.
- Errors.
- Timeline.
- Metrics.

## Step 10 — Dashboard

- Summary.
- Search.
- Detail.
- Timeline.
- Errors.
- Outputs.

## Step 11 — Testing

- Unit.
- Integration.
- Failure.
- Performance.
- Concurrency.

## Step 12 — Documentation/demo

- README.
- ERD.
- Architecture.
- ADRs.
- API documentation.
- KQL.
- Runbook.
- Demo.

---

# 67. Architecture Decision Records

Create:

```text
docs/adr/
```

Required decisions:

```text
ADR-001 One Function Trigger
ADR-002 Service Bus Queue
ADR-003 EF Core vs Dapper
ADR-004 Stored Procedure Strategy
ADR-005 ProcessingJob Identity
ADR-006 Idempotency
ADR-007 Configuration Versioning
ADR-008 Output Storage/Naming
ADR-009 Checkpoint and Recovery
ADR-010 Error vs Dead Letter
ADR-011 XML Streaming
ADR-012 Dashboard/API Boundary
```

Each ADR:

```text
Context
Problem
Options
Decision
Why
Consequences
Status
```

---

# 68. Definition of Done

A feature is not done because the happy path works.

For every significant feature:

```text
[ ] Requirement identified
[ ] Architecture identified
[ ] Code implemented
[ ] Unit tests
[ ] Error handling
[ ] Logging
[ ] Correlation ID
[ ] State transition
[ ] Database persistence
[ ] Retry behavior
[ ] Failure behavior
[ ] API visibility if applicable
[ ] Dashboard visibility if applicable
[ ] Documentation
```

---

# 69. Demonstration Strategy

Do not demonstrate only:

```text
Upload XML
→ 5 files
```

Demonstrate engineering behavior.

## Demo 1 — Happy path

```text
Upload
→ queue
→ function
→ validate
→ process
→ 5 outputs
→ archive
→ completed
```

## Demo 2 — Empty XML

```text
0 KB
→ rejected
→ error
→ dashboard
```

## Demo 3 — Duplicate records

```text
1,000 records
600 valid
400 duplicate
→ output
→ error/rejection
→ metrics
```

## Demo 4 — Partial output

```text
4 outputs succeed
5th fails
→ state
→ retry
→ recovery
```

## Demo 5 — Duplicate message

```text
same message twice
→ no duplicate business processing
```

## Demo 6 — Observability

Show one correlation ID across:

```text
Terminal
Application Insights
KQL
SQL
API
Dashboard
```

That demonstrates the architecture rather than just the conversion.

---

# 70. Business Value

The system should allow a non-technical person to answer:

> What file arrived?

> Is it processing?

> How many records were successful?

> How many were duplicates?

> How many were invalid?

> Which output failed?

> Why did it fail?

> Will it retry?

> Where is the input now?

> Where are the outputs?

> When did it finish?

> Is anything stuck?

This is the business-facing value of durable state + API + dashboard + observability.

---

# 71. Enterprise Differentiators

The solution should stand out because it demonstrates:

## Reliability

```text
Idempotency
Retry
Checkpoint
Recovery
Timeout
Dead letter
```

## Observability

```text
Correlation
Structured logging
Metrics
KQL
Health
Dashboard
```

## Scalability

```text
Streaming
Batching
Set-based SQL
Controlled concurrency
```

## Maintainability

```text
Clean Architecture
SOLID
EF Core
Selective stored procedures
Output generator abstraction
Configuration
```

## Business usability

```text
REST API
Operational dashboard
Human-readable errors
Processing timeline
```

---

# 72. Questions Still Requiring Architect Confirmation

1. Does the single trigger definitely need to be a Service Bus Queue Trigger?
2. How is the Blob event converted into a Service Bus message without a second Function trigger?
3. Is the Service Bus topology definitely Queue, or does Topic/Subscription remain part of the official architecture?
4. Are exactly five formats mandatory?
5. Are additional formats such as PDF allowed?
6. Is configurable format selection officially allowed or only an enhancement?
7. What is the exact output filename contract?
8. What is the exact XML schema?
9. What is the exact duplicate rule beyond CustomerId?
10. What is the exact error-file format?
11. What is the exact retry count?
12. Which failures are retryable?
13. What exactly should happen after partial output failure?
14. Is checkpoint/resume required or an enhancement?
15. Is the Blob `deadletter` directory separate from Service Bus DLQ?
16. Is the dashboard part of Phase 2?
17. Is API authentication required?
18. Is EF Core acceptable?
19. Are stored procedures required or optional?
20. What is the expected production database?
21. What are the production retention requirements?
22. Are there PII/security restrictions for telemetry?
23. What is the expected maximum practical file size?
24. What is the expected maximum record count?
25. What concurrency level should the solution support?
26. Should reprocessing be supported?
27. Should a configuration change affect queued files?
28. What exact status values should the client see?
29. What are the scoring-critical features for Phase 2?
30. Which enhancements are acceptable without changing the assignment scope?

---

# 73. Final Technology Position

Current recommended stack:

```text
C#
Azure Functions
Azure Blob Storage
Azure Service Bus
SQL Server / Azure SQL
EF Core
Selective Stored Procedures
Application Insights
KQL
REST API
Dashboard
```

Avoid technology for technology's sake.

The architecture should remain understandable.

---

# 74. Final Mental Model

Do not think:

> "I am building XML → five files."

Think:

> **"I am building a durable, event-driven file-processing middleware platform with one Azure Function trigger."**

The platform must make every important state and failure predictable.

```text
                         ONE TRIGGER
                              |
                              v
                       PROCESSING JOB
                              |
                              v
                       STATE MACHINE
                              |
                +-------------+-------------+
                |             |             |
                v             v             v
             STREAM         VALIDATE       CONFIG
                |             |             |
                +-------------+-------------+
                              |
                              v
                           BATCH
                              |
                              v
                    DUPLICATE / BUSINESS
                         VALIDATION
                              |
                              v
                      OUTPUT GENERATORS
                              |
          +--------+----------+----------+--------+
          |        |          |          |        |
         TXT      CSV        JSON        XML      DAT
          |        |          |          |        |
          +--------+----------+----------+--------+
                              |
                              v
                         CHECKPOINT
                              |
                              v
                           ARCHIVE
                              |
                              v
                          COMPLETED

          ┌───────────────────────────────────┐
          │         OBSERVABILITY             │
          │ Logs | Metrics | KQL | Health     │
          │ Correlation | Audit | Dashboard   │
          └───────────────────────────────────┘
```

---

# 75. Golden Rules

1. The official PDF is the requirement baseline.
2. One Function Trigger means exactly one Azure Function trigger.
3. One trigger does not mean one giant method.
4. Filename is not identity.
5. CustomerId is the business duplicate key unless the architect says otherwise.
6. Design for duplicate event/message delivery.
7. Durable state belongs in SQL, not in memory.
8. Track every output independently.
9. Stream large XML files.
10. Batch database operations.
11. Do not perform one SQL query per customer at massive scale.
12. Do not log millions of records individually.
13. EF Core is the default ORM; use stored procedures selectively.
14. Do not use Dapper without a measurable architectural reason.
15. Do not treat Application Insights as the business source of truth.
16. Separate business errors from infrastructure failures.
17. Retries must be bounded.
18. Error/archive/output paths must not create processing loops.
19. Configuration must be versioned per processing job.
20. Dashboard → API → application/data layer; never Dashboard → direct SQL.
21. A partial failure must have a recoverable state.
22. Health is not the same as file-processing status.
23. Correlation IDs must connect terminal, telemetry, SQL, API and dashboard.
24. Every important failure needs an explicit answer.
25. **Enterprise architecture is not "more components"; it is predictable behavior under normal conditions and failure.**

---

# 76. Success Criteria

The project is successful when:

```text
A developer
    → can debug it.

A tester
    → can deliberately break it and understand the result.

A DevOps engineer
    → can identify failures from telemetry.

A BA
    → can understand processing status.

A manager
    → can see operational health.

A client
    → can understand what happened to a file.

An architect
    → can explain why every major design decision exists.

And the system
    → can recover without guessing what already happened.
```

**End of PLAN.md V2**
