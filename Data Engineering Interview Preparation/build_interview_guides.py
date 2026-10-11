from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'Azure_Data_Engineering_Interview_Guides'
ROOT.mkdir(exist_ok=True)

def pairs(text):
    return [tuple(line.split('|', 1)) for line in text.strip().splitlines() if line.strip()]

# Answers are concise rehearsal guidance, not claims about client experience.
TOPICS = []
def topic(name, slug, purpose, flow, official, core, advanced, scenarios, practical, ops):
    TOPICS.append(dict(name=name, slug=slug, purpose=purpose, flow=flow,
                       official=official, core=pairs(core), advanced=pairs(advanced),
                       scenarios=pairs(scenarios), practical=pairs(practical), ops=ops))

topic('Azure Data Factory (ADF)', '01_Azure_Data_Factory_ADF',
'Source ingestion, orchestration, scheduling and controlled ETL/ELT execution.',
'Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset',
'https://learn.microsoft.com/en-us/azure/data-factory/introduction',
'''What is an ADF pipeline?|A pipeline groups activities into an orchestrated workflow. A pipeline run is one execution with a specific parameter set and run identity.
What are linked services and datasets?|A linked service defines connectivity/authentication to a data store or compute service; a dataset identifies the data structure or location used by an activity.
What is an integration runtime?|It provides the execution/connectivity bridge for integration work. Choose Azure, self-hosted or Azure-SSIS runtime based on the workload and network requirements.
When do you use Copy activity versus Mapping Data Flow?|Copy moves supported data between sources and sinks. Mapping Data Flow performs visual Spark-based transformations; external activities can invoke custom compute such as Databricks.
How do ETL and ELT differ?|ETL transforms before the analytical destination; ELT lands data and transforms within the destination platform. Select based on data volume, engine capabilities and control needs.
How do parameters differ from variables?|Parameters supply read-only run configuration. Variables hold mutable pipeline state; avoid shared mutable variables in parallel iterations.
What trigger patterns should you know?|Schedule triggers start time-based runs, tumbling windows represent bounded recurring windows, and supported event triggers respond to events. Choose based on replay, dependency and timing requirements.
How do Lookup and Get Metadata differ?|Lookup reads configuration or query results; Get Metadata reads supported object/file metadata. Their output size and connector constraints matter for large workloads.
How do you process multiple entities?|Read reviewed metadata and iterate with parameterized datasets/pipelines. Bound concurrency to protect the source and avoid conflicting target publications.
What proves a pipeline succeeded?|Execution status proves activities completed. Business success also requires manifest completeness, quality/reconciliation controls and accepted consumer publication.''',
'''How do you make incremental ingestion safe?|Use a source-consistent bounded change boundary, retain raw input and advance accepted state after publication. Timestamp-only extraction requires explicit assumptions and cannot detect hard deletes by itself.
How do you build restartable pipelines?|Persist phase state, source boundaries and manifests. Make target operations idempotent and reconcile cases where publication succeeds but state recording fails.
How do you parameterize dynamic SQL safely?|Bind values using supported parameters and allow-list object identifiers. Metadata-driven ingestion must not execute unrestricted configuration as SQL.
How do you deploy ADF across environments?|Version source definitions, produce deployable artifacts, use environment parameters and separate identities, and validate trigger behavior during promotion.
How do you tune Copy performance?|Inspect source, network, runtime and sink throughput; adjust partitioning/concurrency only at a measured bottleneck. Higher parallelism can overload the source.''',
'''An on-premises SQL connection fails while cloud copies work. What do you check?|Inspect self-hosted runtime availability, service credentials, outbound connectivity, DNS and source permissions. Reproduce with the runtime identity rather than your interactive account.
A file event starts before all delivery files arrive. How do you prevent incomplete processing?|Treat the event as a signal, then validate an expected manifest or completion marker. Publish only after the complete delivery is present.
Two runs update the same watermark. How do you fix it?|Serialize the entity or acquire a durable lease; use compare-and-set state updates. Preserve distinct run IDs and prevent competing publication.
A source hard-deletes rows. Will your timestamp query capture this?|No. Use source-supported CDC, a tombstone feed or an authoritative full-snapshot comparison with explicit deletion rules.
Copy succeeds but the notebook fails. What do you rerun?|Reuse the durable landed input and same boundary for transformation. Do not re-extract a changing source without recording a new input version.
Parallel ForEach produces incorrect shared totals. Why?|Pipeline variables are shared mutable state. Return per-iteration outputs or persist isolated results and aggregate after the parallel work.
REST pagination repeats a page after a timeout. What is your strategy?|Persist cursor/page identity, bound retries and deduplicate stable source keys. Verify whether the API supports a consistent snapshot while pages are fetched.
A tumbling-window backfill overloads the database. What changes?|Lower approved concurrency, chunk the ranges and measure database pressure. Keep backfill separate from the live freshness workload where necessary.
A Databricks activity times out after the job finished. Should you submit a new job immediately?|Inspect the external job/run status and target publication before retrying. Use correlation IDs and idempotency to avoid duplicated side effects.
Triggers run during deployment and read half-updated configuration. How do you prevent that?|Use a controlled deployment sequence for affected triggers and dependencies, validate the release, then resume scheduling and reconcile missed windows.''',
'''Design a metadata-driven ingestion pipeline.|Show entity configuration, validated identifiers, extraction boundary, Copy, notebook dispatch, controls, publication and state update. Demonstrate one failed-run replay.
Write a bounded incremental extraction query.|Use old < boundary <= new under a documented source contract. Include a deletion strategy and explain why backdated updates need more than a timestamp.
Implement a file completeness gate.|Compare expected manifest paths/counts/checksums against landed objects and preserve run evidence. Test a missing and a duplicate delivery.''',
dict(unit='one scheduled entity pipeline', artifact='pipeline JSON, linked services, trigger definitions and parameterized datasets', signal='activity output, integration-runtime diagnostics and source/sink throughput', state='source watermark, immutable delivery manifest and accepted run record', access='linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants', contract='source schema, extraction boundary and sink dataset schema', bottleneck='source query duration, Copy throughput and transformation activity duration', dependency='source system and invoked Databricks/SQL transformation', project='banking transaction ingestion and restartable lake modernization'))

topic('Azure Databricks', '02_Azure_Databricks',
'Distributed lakehouse transformations, orchestration of Spark workloads and governed analytical serving.',
'ADF or event source -> ADLS/Delta bronze -> Databricks job -> silver transformations -> gold Delta -> Databricks SQL or reporting',
'https://learn.microsoft.com/en-us/azure/databricks/introduction/',
'''What is Azure Databricks?|An Azure-integrated data/AI platform used for distributed processing and lakehouse workloads. Distinguish the platform from Apache Spark, which is one processing engine it uses.
What is the driver versus an executor?|The driver coordinates application execution and planning; executors process distributed tasks. Collecting large data to the driver defeats distributed memory scaling.
How do jobs differ from exploratory notebooks?|Jobs provide scheduled/triggered production tasks, parameters and execution controls. Notebooks support development; production requires versioning, ownership and reproducible deployment.
What is a Delta table?|A table with transaction-log metadata over data files, providing supported transactional and schema behavior. It is not merely a folder of Parquet files.
What are bronze, silver and gold layers?|Bronze preserves raw/source context, silver conforms business records, and gold serves defined analytical products. They are design conventions, not required platform names.
How do SQL warehouses differ from Spark job compute?|SQL warehouses serve SQL workloads; Spark compute executes distributed jobs/notebooks. Match compute to workload, isolation and measured concurrency.
What does lazy execution mean?|Spark transformations build a plan and actions trigger computation. Several actions can recompute the same lineage unless reuse is deliberately materialized or persisted.
What should a production notebook accept?|Validated input/output identifiers, run ID, bounded processing scope and rule/configuration version. Return meaningful status without embedding credentials.
How do you govern access?|Use Unity Catalog object grants and approved storage credentials/external locations where appropriate, plus platform identity/workspace policies.
What does the Spark UI reveal?|Stages, task duration, shuffle volume, skew, spills and execution plans help identify bottlenecks. Correlate them with job input and output evidence.''',
'''When should you broadcast a dimension?|When the actual serialized relation is small enough for executor memory and the join plan benefits. Verify size, skew and runtime behavior instead of forcing broadcasts universally.
How do you handle late dimension changes?|Maintain effective intervals, reconstruct affected key timelines and re-resolve impacted facts. Closing only the current row may mishandle out-of-order history.
How do you make foreachBatch safe?|Design the handler to be idempotent using batch/business keys and transactional target operations where supported. The function can execute more than once.
How do you tune cost and performance together?|Measure cost per accepted workload, startup/runtime, utilization, shuffle and query latency. Select compute and scaling from these measures, not only job duration.
How do you upgrade runtimes safely?|Pin dependencies, validate API/connector compatibility and run correctness/performance/replay fixtures in test. Promote with a rollback and data compatibility plan.''',
'''A Spark job spends most time in one task. What do you investigate?|Check skewed keys and partition sizes in task metrics. Filter early, redesign keys or use supported skew handling, then compare the new plan.
Executors fail after a forced broadcast. What do you do?|Confirm relation size and memory pressure, remove the forced hint if unsuitable, and evaluate a shuffle join with appropriate partitioning.
The driver crashes during collect(). What is the fix?|Remove large driver materialization. Write distributed output or use bounded samples; increasing driver size alone preserves the faulty scaling design.
A job creates thousands of tiny Delta files. How do you improve it?|Measure batch sizes and writer partitions, use suitable compaction/layout maintenance and verify retention. Avoid arbitrary repartitioning without workload evidence.
Two tasks MERGE the same target partition. How do you respond to conflicts?|Partition ownership or serialize conflicting writes, handle supported optimistic conflicts with bounded retry and verify idempotent results.
A reference change arrives after gold facts were published. What must change?|Rebuild the affected dimension timeline and identify dependent fact dates. Publish a reconciled revision rather than only changing the current dimension.
A notebook works interactively but not in a job. What do you compare?|Compare execution identity, runtime, dependencies, parameters, catalog/context and network permissions. Reproduce under the job identity.
A stream checkpoint is deleted. Is restart from latest safe?|Not automatically. Identify recoverable offsets/raw input and target idempotency; plan controlled replay instead of silently skipping data.
SQL warehouse queries slow during a batch workload. What would you isolate?|Measure concurrency and resource contention; separate serving and transformation compute where justified and tune the expensive query plan.
A runtime upgrade changes output decimal rounding. How do you detect and prevent it?|Run explicit decimal/null/timezone fixtures and financial reconciliation before promotion. Record the runtime/rule version and roll back incompatible outputs.''',
'''Create a parameterized bronze-to-silver notebook.|Use explicit schemas, bad-record handling, ordered deduplication and target controls. Prove replay produces the same business output.
Diagnose a slow Spark join from a plan.|Identify join type, shuffle boundaries, estimates and task skew; propose a measured change and explain its tradeoff.
Build a multi-task job dependency graph.|Separate independent tasks, reference dependencies and critical publication gates. Include durable run IDs and failure recovery.''',
dict(unit='one Databricks job or notebook task', artifact='job definition, notebook/package version and compute configuration', signal='Spark UI stages, task skew, job logs and Delta operation history', state='Delta table version, job run ID and streaming checkpoint where relevant', access='job identity, Unity Catalog grants, storage credential and network connectivity', contract='input schema, source keys and silver/gold table contract', bottleneck='shuffle spill, skewed tasks, scan volume and compute utilization', dependency='ADLS source, Unity Catalog metadata and upstream orchestration', project='lake modernization, banking transformations and telecom usage processing'))

topic('Azure Data Lake Storage Gen2 (ADLS)', '03_ADLS_Gen2',
'Durable lake storage, directory organization, permissions and efficient access for analytical workloads.',
'Approved producer -> immutable ADLS landing -> bronze/silver/gold storage -> governed compute -> accepted SQL/BI consumption',
'https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction',
'''What is ADLS Gen2?|Azure storage capabilities for analytical lake workloads built on Blob Storage with hierarchical namespace support. It stores files/objects; it does not execute Spark transformations.
Why does hierarchical namespace matter?|It provides directory semantics used by data-lake workloads, including directory-oriented operations and ACLs. Evaluate account configuration and feature compatibility before provisioning.
What is the abfss URI used for?|It identifies secure Azure Blob File System access to a container and path. Authentication still requires the workload's supported identity/credential configuration.
How do containers and directories differ?|A container is a top-level storage boundary; directories organize paths within it. Choose boundaries based on governance and lifecycle needs, not naming convenience alone.
How do RBAC and ACLs relate?|Azure roles and path ACLs participate in authorization through documented evaluation rules. Broad data-plane role grants can make restrictive ACL assumptions ineffective.
What are access versus default ACLs?|Access ACLs apply to existing objects; default ACLs define inheritance for newly created children. Changing defaults does not automatically rewrite every existing child's ACL.
Which file format would you choose for analytics?|Parquet suits typed columnar analytical scans; JSON/CSV may preserve source interchange; Delta adds a transaction log over data files for table semantics.
How should lake paths be organized?|Separate source/entity/date/run landing from curated datasets and restricted exceptions. Preserve manifests and avoid high-cardinality directory partitioning without evidence.
What do lifecycle policies do?|They automate supported object retention/tiering behavior. Verify compatibility with active table files, recovery needs and the account's enabled features.
What distinguishes storage encryption from authorization?|Encryption protects stored/transmitted data; authorization decides who can access it. Encrypted storage is not proof of appropriate user permissions.''',
'''Why are small files expensive for analytics?|They increase listing/opening/metadata overhead and fragmented reads. Measure actual query and write behavior before choosing compaction or file-size targets.
How do you secure network access?|Use supported firewall/private endpoint controls with correct private DNS and permitted workload routes. A valid identity can still fail through network restrictions.
How do you validate complete delivery?|Use a source manifest, expected file/row counts and checksums where appropriate. Listing currently visible files alone does not establish that the source finished writing.
How do you design recovery?|Align immutable source retention, table-log/data retention, storage protection and tested restoration with RPO/RTO. Do not equate geo-redundancy with a complete application recovery plan.
How do you delete sensitive records safely?|Find relevant raw/curated/export copies and apply the approved retention/deletion procedure. Coordinate table-level transactions and physical retention; do not manually delete active Delta files.''',
'''A user can read a file but cannot list its parent. What do you inspect?|Check RBAC and path ACL evaluation, including required traversal permissions on ancestors. Test with the actual user's token and path.
New files inherit the wrong permissions. Why?|Inspect directory default ACLs and the writer's behavior. Correct defaults for future objects and deliberately repair existing ACLs where approved.
A Databricks job gets 403 after an identity change. How do you isolate it?|Check the actual workload identity, storage data-plane roles, ACLs, catalog storage configuration and network routing.
A private endpoint exists but requests still use a public route. What is likely wrong?|Verify DNS resolution and the workload's network path. Endpoint creation alone does not ensure clients resolve/use the private endpoint.
Millions of tiny JSON files slow ingestion. What would you change?|Measure listing/opening overhead; compact or batch source deliveries and convert accepted data to columnar tables while preserving raw traceability.
A retention policy removes files still referenced by Delta. What is your response?|Hold consumers, inspect table versions and available backups, restore missing files if possible, and redesign lifecycle rules to respect table retention.
Someone deletes files directly from a gold table directory. How do you recover?|Inspect transaction-log references and storage recovery options; restore the table consistently. Restrict direct file deletion and use supported table operations.
An account is being redesigned for hierarchical namespace. What must be checked?|Validate supported enablement/migration paths, workload compatibility, ACL strategy and rollback constraints for the actual account.
A producer overwrites yesterday's source file. How do you retain auditability?|Copy deliveries to immutable run/version paths and record manifest/hash provenance. Corrections create new identified deliveries rather than erasing prior evidence.
Storage cost rises while rows remain constant. What do you investigate?|Check retained versions/raw copies, small-file counts, tier/access charges, orphaned exports and transaction-log retention before deleting anything.''',
'''Design a lake directory and permission matrix.|Show source/run landing, curated layers, quarantine, consumer scope and workload identity. Explain traversal and inheritance tests.
Build a delivery-manifest validator.|Compare expected objects, size/checksum where meaningful and source control counts; fail a partial delivery before downstream publication.
Explain a safe table retention policy.|Map raw recovery, Delta history, stream consumers and deletion obligations; show why deleting arbitrary files is unsafe.''',
dict(unit='one ingestion or curated storage path', artifact='container/path layout, role/ACL assignments and network configuration', signal='storage request failures, read/list latency, bytes and object counts', state='delivery manifest, immutable raw path and active table-log references', access='data-plane RBAC, directory traversal ACLs, workload identity and storage network route', contract='path conventions, file format, partition keys and retention policy', bottleneck='file listing, tiny-object overhead, read throughput and request rate', dependency='source producer and Spark/SQL storage reader', project='all six project landing and recovery layers'))

topic('Microsoft Fabric', '04_Microsoft_Fabric',
'Integrated ingestion, engineering, OneLake lakehouses, warehouse analytics and Power BI serving.',
'Source connection -> Fabric pipeline -> OneLake bronze -> Spark silver -> validated gold -> semantic model or SQL serving',
'https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview',
'''What is Microsoft Fabric?|A Microsoft SaaS analytics platform with integrated workloads and OneLake. Distinguish its services from separately provisioned Azure ADF, ADLS and Synapse resources.
What is OneLake?|The logical data lake for Fabric tenant data. It is not a user-created ADLS account, even though supported integration can connect to external storage.
What is a Fabric Lakehouse?|An analytical item that organizes files and tables for engineering/analytics workloads. Delta tables support Spark transformations and supported SQL/BI access.
How do Lakehouse and Warehouse choices differ?|A Lakehouse emphasizes Spark/data-file engineering; a Warehouse emphasizes relational SQL warehouse work. Choose from transformation and serving requirements.
What does the Lakehouse SQL analytics endpoint do?|It provides SQL querying over supported Lakehouse tables. Do not use its read-oriented table access as a substitute for Spark Delta mutations.
What are shortcuts?|References to supported data locations that can reduce copying. Availability, identity, freshness and source permissions still depend on the target connection.
How does Fabric Data Factory relate to ADF?|Both support integration/orchestration, but connectors, activities, execution and deployment capabilities are not guaranteed identical.
What is a semantic model?|A governed analytical model of tables, relationships and measures for BI consumption. Its security and aggregation behavior must match the business contract.
What is Direct Lake conceptually?|A Power BI storage mode designed to use lake-backed data under supported conditions. Validate the model/endpoint type and actual query behavior rather than assuming every model stays on the same path.
What should separate workspaces achieve?|Environment isolation, ownership and access boundaries. Workspace structure should follow deployment and governance needs, with tested cross-workspace dependencies.''',
'''How do you control capacity contention?|Measure capacity/workload utilization, execution patterns and consumer latency. Isolate or reschedule heavy workloads and size capacity from evidence.
How do you prevent mixed publication versions?|Use accepted boundaries/manifests and a consumer contract that selects the intended release. Independent table writes are not automatically an atomic product release.
How do you verify underlying data security?|Test OneLake/item/workload permissions and direct SQL/file access independently of Power BI row filters. The effective identity varies by access mode.
How do you deploy Fabric items?|Use supported Git/deployment/API mechanisms for the actual item types and validate dependencies/parameters. Do not assume every item supports the same promotion workflow.
How do you integrate external Azure storage?|Use supported connections/shortcuts or controlled copying according to security and freshness requirements. Verify external target permissions and network support.''',
'''The SQL endpoint will not accept your Delta MERGE. What do you do?|Run compatible Delta mutations through Spark notebooks for Lakehouse tables, or choose a SQL Warehouse implementation where the workload requires warehouse DML.
A shortcut suddenly becomes unreadable. What do you inspect?|Check external target availability, connection identity/permissions, network support and changes to the referenced location.
Power BI is slow during notebook runs. How do you diagnose it?|Correlate capacity contention, notebook timing, query workload and model behavior; isolate or schedule based on measured resource pressure.
A regional report is filtered but a user can query all gold rows. What is missing?|Underlying data permissions were not scoped as expected. Test serving modes and item/data access separately from semantic-model filters.
A schema change breaks the semantic model. How would you manage the release?|Version the table/model contract, test dependent measures/relationships and promote compatible changes together or provide a migration version.
Gold tables finish at different times and the report combines inconsistent dates. What is the fix?|Define a product publication boundary and consumer accepted-version behavior. Show table/product as-of values when separate releases are intentional.
An ADF pipeline export cannot run directly in Fabric. Why?|The integration products have different supported features/definitions. Map activities/connections and rebuild unsupported parts with tested equivalence.
A deployment omits an unsupported item. How do you handle it?|Inventory supported promotion coverage and deploy that item through an approved supported path; verify dependencies and prevent incomplete releases.
A financial report sums daily account balances over a month. What must change?|Use snapshot-aware measures and the approved as-of-date definition. Transaction sums and balance snapshots have different aggregation semantics.
The pipeline succeeds but the source data is stale. How do you make that visible?|Monitor last accepted business/source timestamp and freshness target, not only pipeline status; hold or flag the product under its contract.''',
'''Draw a Fabric banking analytical platform.|Include supported connections, pipeline, OneLake layers, Spark rules, source reconciliation, accepted publication and semantic-model access.
Design Lakehouse versus Warehouse selection.|State data shape, transformation engine, SQL write needs, BI consumers, operational tradeoffs and tested permissions.
Demonstrate a late transaction correction.|Replay a bounded source scope, resolve historical dimensions/FX, reconcile and publish an accepted replacement without duplicating facts.''',
dict(unit='one Fabric pipeline and analytical publication', artifact='workspace items, notebook/pipeline definitions and semantic-model contract', signal='Fabric run monitoring, capacity metrics and consumer query behavior', state='OneLake table versions, delivery manifests and accepted product boundary', access='connection identity, workspace/item/OneLake permissions and semantic-model security', contract='Lakehouse schema, gold product grain and semantic-model relationships', bottleneck='capacity contention, Spark processing time and model query latency', dependency='external source connection and Power BI or SQL consumers', project='Citi EMEA reference Fabric banking analytics design'))

topic('Azure Synapse Analytics', '05_Azure_Synapse_Analytics',
'SQL warehouse serving, lake queries and integrated analytical workload coordination.',
'ADLS curated files -> Synapse staging -> dimensions and facts -> reconciled warehouse publication -> SQL views and Power BI',
'https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is',
'''What workloads exist in Synapse?|Synapse includes SQL analytical engines, Spark and integration capabilities. Name the actual engine when discussing behavior or optimization.
How do dedicated and serverless SQL differ?|Dedicated pools provision distributed warehouse compute/storage; serverless SQL queries supported external data without a dedicated pool. Their syntax, tuning and billing models differ.
What is MPP?|Massively parallel processing distributes work across nodes/distributions. Data movement and skew are major performance considerations.
What distribution choices matter in a dedicated pool?|Hash, round-robin and replicated table designs address different loading/join needs. Select from observed key distribution, table size and join patterns.
Why does distribution skew matter?|Uneven rows/work cause one distribution to dominate execution. Validate key frequencies and runtime work, not only logical uniqueness.
What are staging tables for?|They isolate incoming batches for validation and controlled dimension/fact publication. Staging should not be an uncontrolled consumer interface.
How are columnar files useful for external queries?|Columnar formats support efficient selected-column reads and compatible pruning. Actual efficiency depends on layout, filters and engine capabilities.
Why are statistics important?|They inform cardinality estimates and plans. Verify freshness after substantial data changes and compare estimated versus actual workload behavior.
How do dimensional keys work?|Dimensions have stable keys and historical behavior; facts resolve them at the agreed business time. Unknown or multiple matches need explicit handling.
How does a warehouse load become accepted?|Validate source/stage/fact counts, keys and relevant totals, then expose the accepted output under a documented publication contract.''',
'''When is replication useful?|For suitably small dimensions where reducing movement improves joins. Replication cost and update behavior must be measured, not assumed appropriate for large tables.
How do you tune dedicated SQL joins?|Review distributions, join keys, movement, skew, statistics and query shape. Avoid transplanting single-node SQL tuning assumptions unchanged.
How do you control serverless scan costs?|Use suitable columnar layout, scoped paths, explicit schemas and selective queries; measure scanned bytes and confirm actual pruning.
How do you design atomic publication?|Use supported transactions and isolated staging for the selected engine, or a versioned accepted-view contract. Multi-system lake-to-warehouse operations need recovery reconciliation.
Why must SQL syntax be engine-specific?|Dedicated SQL, serverless SQL, Azure SQL and Spark SQL have different DML, external table and function support. Verify support rather than copying scripts blindly.''',
'''A hash-distributed fact has one busy distribution. What do you inspect?|Check null/hot distribution keys and the actual workload spread. Evaluate an alternative key using realistic joins and load/query evidence.
Joining two large tables causes heavy movement. How can it improve?|Evaluate compatible distributions on join keys and reduce unnecessary rows/columns before the join. Measure movement and skew before and after.
Serverless reads every date folder for a one-day request. What would you check?|Check path scoping, partition/filter expression and supported pruning behavior. Validate scanned data rather than assuming a date predicate prunes.
The same Parquet batch loads twice into staging. What prevents duplicate facts?|Record batch/source identity and use idempotent publish logic with uniqueness controls. Keep staged batches isolated and verify accepted publication IDs.
A new GL mapping changes historical reports. What is the correct model?|Use effective-dated dimensions and as-of fact resolution, or an explicitly approved restatement model. Do not silently join all history to today's mapping.
A load is quick but downstream reporting is slow. What should you tune?|Inspect reporting plans, data movement, statistics, distributions and concurrency; load throughput alone does not establish query efficiency.
Delta files were manually exported without respecting the active table version. What is the risk?|Reading arbitrary Parquet files may include obsolete/uncommitted table state. Use a supported Delta reader or export an accepted consistent table snapshot.
A closed reporting period receives a correction. What is your flow?|Follow authorized reopen/correction policy, replay the affected scope, reconcile financial totals and record the reporting revision.
A query copied from Azure SQL fails in dedicated SQL. How do you handle it?|Check supported syntax/features for the exact pool; rewrite with tested engine-supported patterns rather than asserting all T-SQL is portable.
Pausing a dedicated pool affects report availability. How do you decide the schedule?|Match pause/resume windows to consumer freshness/availability contracts and measured cost savings, including startup and cache warm-up effects.''',
'''Design a finance star schema and load order.|Specify fact grains, historical dimensions, staging, distribution candidates and source-to-fact financial controls.
Explain a slow warehouse execution plan.|Locate data movement, skew and estimate issues, then propose one change with a comparable workload benchmark.
Implement a period-based publish contract.|Isolate a batch, validate dimensions/facts/totals, apply period-state policy and expose only accepted revisions.''',
dict(unit='one dedicated-pool load or serverless analytical query', artifact='engine-specific DDL, staging load scripts and serving views', signal='query plans, data movement, distribution skew, waits and scanned bytes', state='staging batch ID, accepted warehouse revision and source control totals', access='SQL execution identity, database grants and external-storage access', contract='fact/dimension grain, external file schema and accounting period rules', bottleneck='data movement, distribution skew, load throughput and query concurrency', dependency='ADLS curated batch and finance reporting consumer', project='Barclays financial warehouse integration reference design'))

topic('PySpark', '06_PySpark',
'Distributed DataFrame transformations, join/window logic, aggregation and streaming correctness.',
'Explicit-schema input -> DataFrame transformations -> validation and ordered deduplication -> Delta/Parquet output -> reconciliation',
'https://spark.apache.org/docs/latest/api/python/index.html',
'''How do DataFrames differ from RDDs?|DataFrames provide schema-aware operations and optimizer visibility. RDDs expose lower-level transformations and may be appropriate for specialized requirements.
What is lazy evaluation?|Transformations define a plan; actions execute it. Repeated actions can repeat computation unless reuse is deliberately materialized or persisted.
What is a shuffle?|Redistribution of records across partitions for joins, grouping or sorting. It can add network, memory and disk cost.
What is the difference between repartition and coalesce?|Repartition generally redistributes data with shuffle. Coalesce can reduce partitions with less movement but may create imbalance; choose based on the workload.
How do narrow and wide transformations differ?|Narrow operations can operate within a partition lineage; wide operations require cross-partition dependencies such as shuffle.
Why prefer built-in expressions over Python UDFs?|Built-ins usually preserve optimizer visibility and avoid Python serialization overhead. Use a UDF only when suitable native expressions are unavailable.
How do window functions help deduplication?|Partition by business key and order by an authoritative source sequence, then select the latest row. Reject conflicting ties instead of choosing an arbitrary record.
What is cache/persist for?|Reusing computed data across actions when the cost and memory/storage footprint justify it. Remove persistence when no longer needed.
How do nulls behave in filters/joins?|SQL-like three-valued logic means null comparisons are not ordinary equality. Define null semantics explicitly, including null-safe equality where appropriate.
Why are explicit schemas useful?|They avoid repeated inference and ambiguous types, especially decimal/time fields. Malformed and unexpected input still needs a deliberate rejection/evolution policy.''',
'''How do you handle skew?|Measure hot keys and task imbalance; consider filtering, aggregation, supported adaptive handling or carefully designed salting that preserves semantics.
How do you implement SCD Type 2 correctly?|Define tracked attributes, effective timestamps and half-open intervals. Validate one current version and nonoverlap; rebuild timelines for late changes.
What is watermarking?|An event-time policy used by supported stateful streaming operations to manage late data/state. It is not a universal promise that all late events are retained or rejected identically.
How do you test distributed logic?|Use small explicit fixtures for nulls, ties, duplicates, decimal boundaries and late history; compare expected business outputs and test representative integration behavior.
How do you interpret an execution plan?|Identify scans, filters, exchanges, joins and aggregates, then compare estimates/task metrics with the data. An optimized plan still requires output validation.''',
'''A latest-row window returns different results on reruns. Why?|The ordering has ties or lacks an authoritative sequence. Add deterministic source semantics and reject contradictory equal-sequence payloads.
dropDuplicates removes a corrected transaction. What is wrong?|It does not select the correct latest business version automatically. Use key plus source ordering and explicit correction semantics.
An aggregation changes decimal cents. What do you inspect?|Check input casts, decimal precision/scale, rounding policy and accidental floating-point conversions. Reconcile with approved decimal totals.
A join increases row count unexpectedly. How do you diagnose it?|Check right-side key uniqueness and effective interval overlaps. Count matches per fact and fix the intended relationship before publishing.
A UDF is much slower than SQL expressions. What should change?|Translate logic to native functions where possible and benchmark the plan. Check Python serialization and row-at-a-time overhead.
A global sort slows the whole job. Is it necessary?|Determine whether ordering is required globally or only within business groups. Use the minimal supported ordering required for correctness.
Caching a large table causes spills and recomputation. What do you do?|Measure reuse and storage pressure, choose a suitable persistence level or remove caching, and materialize only genuinely reused scoped data.
A null currency slips through a not-equal filter. Why?|Null comparison yields unknown, not true. Include explicit isNull handling and test the predicate's business semantics.
A stream accepts a very old replay. Does a watermark prevent all duplicates?|No. Bounded state expires; use durable key-based idempotency and retained raw reconciliation for out-of-horizon replay.
An event-time join finds two subscriber versions. What should happen?|Treat overlapping dimension intervals as a critical integrity failure; repair the timeline rather than multiplying usage facts.''',
'''Write deterministic latest-per-key logic.|Use Window partitioning and authoritative source sequence, assert equal-sequence payload consistency and verify rerun stability.
Build a financial reconciliation aggregation.|Cast to explicit decimals, group by matching entity/date/currency grain and compare expected signed totals.
Implement a historical dimension join.|Use half-open intervals and test zero/one/multiple matches plus a late-arriving dimension update.''',
dict(unit='one distributed DataFrame transformation', artifact='PySpark module/notebook, explicit input schema and transformation tests', signal='explain plan, Spark UI exchanges, task skew and spill metrics', state='source sequence, input snapshot, output table version and checkpoint if streaming', access='execution identity and governed source/target table permissions', contract='DataFrame types, business-key uniqueness and event-time semantics', bottleneck='shuffle, serialization, skewed partitions and driver materialization', dependency='Spark runtime, source format and Delta/Parquet sink', project='all six domain transformations and telecom streaming enrichment'))

topic('SQL', '07_SQL',
'Relational querying, data modeling, transformation correctness and query performance.',
'Typed source/staging tables -> joins windows and aggregates -> integrity checks -> accepted facts/views -> consumers',
'https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql',
'''How do INNER and LEFT JOIN differ?|INNER retains matching pairs; LEFT preserves left rows with nulls for unmatched right rows. Duplicate matches can multiply rows in either join.
How do WHERE and HAVING differ?|WHERE filters input rows before grouping; HAVING filters grouped results. Avoid moving predicates if the change alters outer-join or aggregation semantics.
How do UNION and UNION ALL differ?|UNION eliminates duplicate result rows; UNION ALL preserves them. Choose from business semantics, not just speed.
What is a CTE?|A named query expression used for readability/recursion where supported. It is not inherently a cached result or guaranteed performance improvement.
How do window functions differ from GROUP BY?|Windows calculate over related rows while retaining row detail; GROUP BY changes the output grain. Specify partition and ordering carefully.
How do ROW_NUMBER, RANK and DENSE_RANK differ?|ROW_NUMBER numbers rows; RANK preserves ties with gaps; DENSE_RANK preserves ties without gaps. Deterministic ordering needs an appropriate tie-breaker.
How should nulls be tested?|Use IS NULL/IS NOT NULL and explicit null-aware business logic. Equality to NULL does not behave like ordinary value equality.
What is a primary versus foreign key?|A primary key identifies a row; a foreign key describes a reference to another key. Enforcement differs by engine, so verify actual constraint behavior.
What is normalization versus a star schema?|Normalization reduces redundant relational facts; star schemas organize dimensional analytical grains. Choose based on transaction versus reporting needs.
Why use DECIMAL for money?|It represents specified fixed decimal precision/scale, unlike binary floating point. Rounding and overflow behavior still need explicit policies.''',
'''What makes a predicate sargable?|It can support efficient access using the engine's indexing/pruning mechanisms. Avoid unnecessary functions/casts on filtered keys and verify the actual plan.
How do you diagnose query regression?|Compare plans, estimates, statistics, parameter behavior, blocking and data changes with a prior baseline. Do not add indexes without evidence.
How do isolation levels affect ingestion?|They govern visibility and concurrency behavior; a source-consistent extraction needs a documented snapshot/change boundary. Isolation names and defaults differ by engine.
How do you design idempotent upserts?|Define a unique business key and authoritative version/sequence, then use engine-supported transactional logic and concurrency controls. MERGE semantics differ by engine.
How do you query historical dimensions?|Join on business key and effective interval, then assert exactly one eligible match per fact. Late changes may require fact re-resolution.''',
'''A LEFT JOIN loses unmatched rows after a WHERE filter. Why?|A predicate on right-side values can reject the null-extended rows. Move the predicate to ON only if that matches the intended business semantics.
NOT IN returns no rows when its subquery contains NULL. How do you fix it?|Use a null-aware NOT EXISTS/anti-join design and define desired handling of null keys explicitly.
A customer join doubles revenue. What do you investigate?|Check dimension key uniqueness and effective intervals. Establish the correct relationship instead of masking the error with DISTINCT.
A query uses SELECT DISTINCT to hide duplicates. Is that sufficient?|No. Identify the duplicated grain and join/source cause; DISTINCT may remove legitimate records or conceal incorrect totals.
Two records share the same latest timestamp. Which should win?|Use an authoritative source sequence or approved tie-breaker; reject unresolved contradictory ties rather than choosing arbitrarily.
A daily balance query sums all historical dates. What should change?|Define selected-date or period-end snapshot semantics. Balances are not additive over time in the same way as transaction amounts.
A date filter wraps the indexed column in a function. What is your optimization?|Use an equivalent bounded range where correct, then compare access path and results; confirm timezone and inclusive/exclusive boundaries.
An update blocks ingestion for minutes. What do you inspect?|Inspect transaction duration, locks, access paths and isolation behavior; reduce unnecessary scope and keep correctness/concurrency requirements explicit.
OFFSET pagination skips rows during concurrent inserts. What is better?|Use a consistent extraction snapshot and deterministic keyset cursor where suitable. Keyset ordering alone does not solve backdated updates.
The same MERGE script runs differently in Spark and Azure SQL. Why?|Engines differ in SQL syntax, match semantics and transaction behavior. Implement and test an engine-specific version.''',
'''Write latest-record-per-key SQL.|Use ROW_NUMBER with authoritative ordering, and detect conflicting equal-sequence rows separately.
Write source-to-target reconciliation SQL.|Compare key sets, duplicate counts and decimal totals by the same date/entity/currency grain.
Write an as-of historical join.|Use valid_from <= event time < valid_to with explicit current-end handling and prove one match per fact.''',
dict(unit='one transformation query or stored-procedure batch', artifact='engine-specific SQL scripts, schema migrations and execution parameters', signal='execution plan, logical reads or scan bytes, waits and row estimates', state='transaction boundary, staging batch ID and accepted output revision', access='database execution identity, object grants and approved parameter binding', contract='table grain, key constraints, types and null semantics', bottleneck='join cardinality, scans, statistics, blocking and distributed data movement', dependency='selected SQL engine and upstream typed staging tables', project='financial warehouse reconciliation and banking analytical transformations'))

topic('Python', '08_Python',
'Reliable ingestion scripts, API/file processing, validation and engineering automation.',
'Configuration -> authenticated source reader -> bounded processing -> validated durable output -> logs and status',
'https://docs.python.org/3/library/index.html',
'''When is Python appropriate versus PySpark?|Use local Python for bounded scripting, API integration and automation; use distributed processing when data volume/work requires it. Python code does not become distributed merely by running in a notebook.
How do lists, tuples, sets and dictionaries differ?|Lists are ordered mutable sequences, tuples ordered immutable sequences, sets unique-value collections and dictionaries key-value mappings. Choose based on required semantics.
What are generators?|Lazy iterators that produce values on demand. They help bounded-memory processing when downstream code does not materialize everything.
What is a context manager?|A structured resource lifecycle, commonly with with, that ensures cleanup for files/connections even on exceptions.
How should exceptions be handled?|Catch specific expected failures, preserve useful context, clean up resources and surface unrecoverable errors. Broad silent catches can publish incomplete data.
Why use Decimal for financial scripting?|Decimal supports decimal arithmetic with explicit context/rounding. Construct from decimal text rather than an already-rounded binary float.
How do modules and packages help?|They organize reusable code and dependency boundaries. Avoid production scripts that rely on undocumented interactive notebook state.
What does type hinting provide?|Readable contracts and support for static tooling. It does not automatically validate every runtime value or source payload.
What makes a script idempotent?|Repeating the same business input produces the same intended state without extra side effects. Use stable keys/manifests and atomic supported target operations.
How should configuration and secrets be handled?|Separate validated configuration from code, use approved identity/secret providers and redact logs. Never check secret values into source control.''',
'''How do you process large files safely?|Stream records/chunks, bound memory and preserve schema/error policy. Do not read an entire lake-scale dataset into local memory.
How do you implement HTTP retries?|Retry appropriate transient errors with bounded exponential backoff/jitter, timeouts and rate-limit handling. Make repeated requests safe or use idempotency keys.
Threads, processes or asyncio?|Choose from I/O versus CPU work, library behavior, runtime characteristics and serialization cost. Do not assume a fixed GIL behavior across all Python builds.
How do you test an ingestion script?|Use fixtures for pagination, nulls, malformed records, decimal/time boundaries and partial failures. Mock external boundaries while testing actual parsing/business logic.
How do you make deployments reproducible?|Pin supported dependencies, use an isolated environment, build the same package artifact and validate runtime/OS compatibility.''',
'''A script runs out of memory reading a CSV. What changes?|Use chunked/streaming parsing and bounded output or move to a distributed engine when needed. Measure peak memory and test malformed records.
An API returns 429. How do you respond?|Honor supported rate-limit/retry guidance, bound concurrency and retry with backoff; record the cursor so progress is resumable.
An HTTP timeout occurs after a POST may have succeeded. Is retry safe?|Check the API's idempotency contract and use a stable request key/status lookup. Blind retries can duplicate side effects.
A decimal total differs from the ledger by cents. What do you inspect?|Check float conversion, Decimal construction, precision and rounding order; use approved decimal fixtures and reconciliation.
A timezone-naive datetime shifts a business date. How do you prevent it?|Parse the source timezone explicitly, use timezone-aware values and define business-date conversion, including daylight-saving cases.
A broad except logs success after rejecting half the rows. What is wrong?|Failure status and rejection thresholds are missing. Catch expected errors, retain exception evidence and block publication when the contract fails.
A package works locally but fails on the job host. What do you compare?|Compare Python build, dependency lock, compiled libraries, OS, environment variables and workload permissions.
Concurrent workers write the same output file. How do you fix it?|Use isolated temporary/run paths and a controlled publication step; serialize conflicting writes and verify durable output manifests.
Logs include bearer tokens from request headers. What should change?|Redact sensitive headers/payload fields centrally, restrict logs and rotate exposed credentials through the approved incident process.
An API cursor changes during the extraction. How do you keep a consistent result?|Use source snapshot/version support if available, stable keys and defined overlap/reconciliation; document limits when the API cannot offer consistency.''',
'''Build a paginated REST extraction function.|Include timeouts, bounded retries, rate-limit handling, stable output keys, cursor persistence and redacted logs.
Write a streaming CSV validator.|Parse explicit types, use Decimal/timezone-aware values and retain bad-record counts/reasons without excessive memory.
Implement a run manifest and replay test.|Record input boundaries and output hashes/counts, simulate partial failure, and prove a second attempt creates no duplicate result.''',
dict(unit='one ingestion or automation script execution', artifact='Python package, dependency lock and validated configuration', signal='structured logs, traceback, request timing, memory and accepted record counts', state='API cursor, run manifest, stable idempotency key and durable output path', access='SDK credential chain, workload identity and source/target permissions', contract='payload schema, parsing types, decimal/time rules and API behavior', bottleneck='I/O latency, local memory, concurrency limits and CPU parsing', dependency='source API/file library and target SDK/database driver', project='API integration, validation and deployment automation for the six designs'))

topic('Delta Lake', '09_Delta_Lake',
'Transactional lake tables, ordered changes, schema contracts, retention and recoverable versioned data.',
'Source records -> Delta bronze -> validated MERGE/history -> silver/gold Delta version -> accepted consumer snapshot',
'https://docs.delta.io/index.html',
'''What does Delta add to Parquet?|A transaction log and table protocol over data files that support compatible transactional reads/writes and schema behavior. Raw file scanning bypasses those semantics.
What does ACID mean here?|Atomicity, consistency, isolation and durability describe supported table transaction properties. This does not guarantee atomicity across unrelated external systems.
What is the transaction log for?|It records table state changes so compatible readers select the active snapshot. Old physical files are not automatically active rows.
What is schema enforcement versus evolution?|Enforcement rejects incompatible writes; evolution deliberately permits supported schema changes. Evolution must still follow the consumer contract.
What is time travel?|Reading an earlier retained table state using supported version/timestamp syntax. Required log and data files must remain available.
What is MERGE used for?|Matching source and target keys to apply supported inserts/updates/deletes. Deduplicate source keys and define ordering before executing it.
What does VACUUM do?|It removes eligible unneeded data files under a retention policy. Too-short retention can break time travel, replay or delayed consumers.
What is optimistic concurrency?|Writers validate whether concurrent changes conflict when committing. Handle supported conflicts without corrupting source ordering or output semantics.
What is change data feed?|A supported mechanism for reading table-level changes after ingestion. It does not automatically capture changes in an upstream system.
Why must protocol compatibility be checked?|Table features may require reader/writer support from particular engines/runtimes. A newer feature can make older consumers incompatible.''',
'''How do you prevent stale corrections?|Retain an authoritative source sequence/version and apply only newer changes. Deletes may require retained tombstone ordering to prevent resurrection.
How do you handle late SCD changes?|Reconstruct the affected entity timeline, validate nonoverlap and re-resolve impacted facts. Table ACID alone does not implement temporal business correctness.
How do you optimize layout?|Measure file size/count, filtering, join patterns and supported clustering/compaction options. Maintenance methods vary by distribution/runtime.
How do you recover a bad write?|Identify a known-good retained version, choose supported restoration/republication, and reconcile downstream state. Restoring a table can itself generate downstream changes.
How do you consume CDF reliably?|Checkpoint an accepted version range, handle retention gaps with controlled snapshots/backfills and reconcile sink idempotency. Verify the CDF mode supported by each consumer.''',
'''A MERGE fails because several source rows match one target. What should happen?|Resolve source order and select one valid latest change per key, rejecting contradictory ties. Do not arbitrarily drop duplicates.
An old insert arrives after a delete. How do you avoid resurrection?|Retain deletion sequence/tombstone or soft-deleted current state and reject stale source versions.
A BI tool reads all Parquet files and double counts rows. Why?|It bypasses the Delta transaction log and can include obsolete files. Use a compatible Delta reader or a consistent accepted export.
Time travel fails after VACUUM. What do you explain?|Historical data files may have been removed. Recover only if supported backups/retention exist and align future retention with recovery/consumer needs.
Schema evolution adds a field that breaks an export. What is missing?|A consumer compatibility check and versioned export contract. Storage acceptance is not proof that all consumers support the change.
Two writers conflict on the same target keys. How do you handle it?|Isolate write scopes or serialize conflicting jobs, then apply bounded safe retry with idempotent source semantics.
A CDF consumer falls behind retention. What is the recovery path?|Detect the gap, perform a consistent snapshot/backfill and re-establish an accepted change boundary; do not silently skip lost versions.
A new table feature prevents an older engine from reading. What do you do?|Validate protocol/runtime compatibility before enabling it; plan migration or use a supported compatible serving copy.
Restoring a table changes downstream reports unexpectedly. Why?|Consumers may see restoration as new changes or retain prior derived state. Reconcile and republish affected downstream datasets.
A partition overwrite removes good records outside the correction scope. What is wrong?|The replacement input/scope is incomplete. Validate the exact predicate and full affected partition before using overwrite.''',
'''Implement ordered transaction upsert.|Deduplicate keys by source sequence, detect ties, create a compatible target and test insert/update/delete/stale replay behavior.
Design retention for three consumers.|Include delayed stream reader, audit/time-travel use and operational recovery. Show the failure path when a retained boundary expires.
Prove a replay is idempotent.|Apply the same bounded batch twice and compare keys, totals, active row state and accepted publication metadata.''',
dict(unit='one Delta table write or retained-version read', artifact='table DDL/protocol, writer logic and retention configuration', signal='table history, operation metrics, conflicting commits and active file counts', state='Delta commit version, source sequence, tombstone history and consumer checkpoint', access='catalog grants, approved writer identity and table storage permissions', contract='table schema/protocol, business keys and change ordering', bottleneck='target scan scope, write conflicts, file fragmentation and maintenance', dependency='compatible runtime reader/writer and downstream CDF/export consumer', project='transactional silver/gold layers across the six reference projects'))

topic('Unity Catalog', '10_Unity_Catalog',
'Governed Databricks objects, workload access, storage abstraction and metadata/lineage visibility.',
'Entra workload/user identity -> catalog and schema privileges -> governed table/volume -> approved storage access -> audited consumption',
'https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/',
'''What is Unity Catalog?|The Databricks governance layer for supported data/AI assets. It manages securable objects, grants and governance capabilities; Azure storage authorization remains relevant.
What is the object hierarchy?|Common table addressing uses catalog.schema.table within a metastore governance context. Different securable object types have their own privileges.
How do managed and external tables differ?|Managed tables let the platform manage relevant data lifecycle; external tables reference externally managed storage. Verify drop/data-retention behavior for the actual table type.
What is a storage credential?|An approved credential abstraction used by governed access to external storage. Its backing identity must have appropriate cloud permissions.
What is an external location?|A governed storage path associated with a storage credential. It scopes supported external data access without distributing raw secrets.
What are volumes for?|Governed access to supported non-tabular files. Do not confuse file access through a volume with querying a table.
Why do users need USE privileges?|Object selection/access involves parent catalog/schema usage as well as the object permission. Diagnose the full privilege path.
How does ownership differ from reading?|Ownership confers management authority under the governance model; SELECT is a data-read privilege. Assign ownership to accountable groups, not casually to every reader.
What is lineage useful for?|Tracing supported upstream/downstream relationships and impact. Validate capture coverage for actual execution paths rather than assuming all external movement is captured.
What does workspace access establish?|It allows platform workspace use subject to controls; it is not automatic permission to every governed data object.''',
'''How do you design least privilege?|Separate producer, engineer, steward and consumer groups; grant required parent/object permissions and control direct cloud access that could bypass governance.
How do you migrate legacy access?|Inventory tables/paths/identities, map ownership/grants and compatible compute access, test workload identities, then cut over with traceable reconciliation.
How do masking and row filtering help?|Supported policies restrict exposed values/rows for applicable query paths. Verify function/policy compatibility and bypass routes for the actual runtime.
How do you govern production jobs?|Use approved service/workload identities, narrowly scoped grants and reviewed deployment permissions. Test jobs under their production identity.
How do you audit access effectively?|Correlate supported audit events with identities, object names and execution context; protect logs and retain them under the approved policy.''',
'''SELECT is granted but the user still cannot query. What do you inspect?|Check catalog/schema USE privileges, workspace/compute eligibility, object name and the effective identity.
A storage credential exists but a job gets a storage error. What might be wrong?|Verify backing cloud identity permissions, external-location path, network access and the job's object privileges.
An engineer can bypass filters by opening raw ADLS files. What is the gap?|Direct storage access bypasses the intended catalog path. Review cloud roles/ACLs and permitted external-location access alongside table policies.
A job succeeds for its author but fails as a service identity. What changes?|Grant the service identity the specific parent/object privileges and approved execution/storage path; avoid reusing the author's broad grants.
A table is dropped and its files remain. Is that always wrong?|External versus managed lifecycle behavior differs. Check table type and retention contracts before cleanup; do not delete data still used elsewhere.
Several teams need the same data with separate ownership. How do you organize it?|Define catalogs/schemas and consumer grants around accountable domains, with shared approved products and explicit ownership.
Lineage is missing for an external export. What do you do?|Verify supported lineage capture for that path and record/document/custom-register the missing relationship through an approved mechanism.
Granting a catalog-wide privilege exposes unintended objects. How do you prevent recurrence?|Review inherited/broad grants and group membership, narrow scope and test representative restricted objects.
A masking policy fails on one compute/runtime. What do you check?|Validate policy support and execution compatibility for the actual compute/runtime, then use a supported controlled path.
A legacy notebook uses direct secret-backed storage paths. How would you modernize it?|Migrate to approved storage credentials/external locations or volumes/tables, remove unnecessary direct secrets and validate equivalent output/access.''',
'''Design a catalog/schema/grant matrix.|Include owner, production writer, steward and consumer with required parent/object privileges and cloud-bypass review.
Trace an access-denied incident.|Show effective identity, workspace/compute context, object grants, external location and cloud/network authorization checks.
Plan a legacy table migration.|Inventory location/type/history, recreate governance, validate data/grants and cut over consumers with recovery evidence.''',
dict(unit='one governed object access or grant change', artifact='catalog/schema definitions, reviewed grants and storage-location configuration', signal='effective privileges, audit events, query identity and supported lineage', state='approved grant matrix, ownership record and migration acceptance boundary', access='USE and object privileges, backing storage identity and workspace/compute eligibility', contract='object ownership, data classification and permitted consumer paths', bottleneck='authorization resolution, storage connectivity and unsupported execution paths', dependency='Microsoft Entra identities, Databricks compute and Azure storage', project='governed Databricks domains and production workload access'))

topic('Azure SQL Database', '11_Azure_SQL_Database',
'Managed relational storage, metadata control, transactional serving and query optimization.',
'Approved client identity -> parameterized SQL -> relational tables and transaction -> accepted result -> application or orchestration consumer',
'https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview',
'''What is Azure SQL Database?|A managed relational database service that handles platform functions such as patching and supported backups. Application schemas, queries and access still require design.
How does it differ from SQL Server on a VM?|The managed service removes much infrastructure administration but has service-specific feature/configuration boundaries. A VM provides broader instance/OS control with more operational ownership.
What is an elastic pool?|A set of databases sharing configured resources. It can suit variable database usage, but noisy neighbors and per-database limits must be considered.
How do provisioned and serverless compute differ?|Provisioned compute supplies configured capacity; supported serverless configurations scale compute according to the service model. Validate tier eligibility, resume latency and billing behavior.
What is Query Store?|A database feature for retaining query/plan/runtime information useful in regression analysis. It helps compare observed execution behavior over time.
How do indexes affect reads and writes?|They can improve selected access paths but add storage and write maintenance. Choose from query predicates/joins and measured plans.
What are transactions used for?|Grouping compatible changes with atomic commit/rollback and isolation semantics. External storage writes are not automatically included in a database transaction.
How do you authenticate securely?|Use supported Microsoft Entra/workload identity patterns and least-privilege database grants; store necessary secrets securely when identity-based access is unavailable.
What are source consistency requirements for extraction?|The extraction must read a defined snapshot/change boundary. Concurrent updates can make arbitrary paginated reads inconsistent.
How are automated backups different from tested recovery?|Backups provide recovery capabilities under service settings; tested recovery proves the application, identities and consumers can resume within agreed objectives.''',
'''How do you diagnose CPU versus blocking issues?|Compare resource metrics with Query Store, waits and active transactions. Query inefficiency and lock contention need different fixes.
How do you coordinate an orchestration watermark?|Use an entity lease or serialized owner and compare-and-set updates, preserving run/publication evidence. Reconcile cross-system commits after failures.
How should an API paginate mutable records?|Use a documented consistency contract and stable keyset cursor where appropriate. Cursor order does not capture all backdated changes automatically.
How do you choose a service tier?|Measure workload latency, concurrency, resource pressure, recovery and cost needs, then validate supported tier features. Avoid quoting unverified current limits.
How do you make schema migrations safe?|Deploy compatible changes, validate data/backfills and coordinate consumer versions. DDL rollback alone may not restore transformed data.''',
'''A metadata lookup becomes slow as pipeline runs accumulate. What do you inspect?|Check filters/indexes, execution plan and table retention. Keep active state small while preserving appropriately indexed run history.
Two pipelines claim the same entity. How do you prevent it?|Use a transactional claim/lease or approved serialization and an ownership token; expire/recover abandoned leases safely.
CPU is high but adding capacity barely helps. Why?|Inspect query plans, scan volume, expensive expressions and contention. Scaling does not remove inefficient access or incorrect join grain.
A procedure works for an administrator but not a workload identity. What do you test?|Check the effective contained identity and required object/execute privileges, connection token and network route.
The database is reachable publicly but not through a private route. What is likely missing?|Validate endpoint/DNS configuration and workload connectivity; authentication alone does not fix routing.
A watermark update succeeds although gold publication failed. What is wrong?|The acceptance sequence is incorrect. Restore/reconcile the accepted source boundary and advance only after validated publication evidence.
An API request retries an insert and creates two rows. What prevents it?|Use a stable idempotency/business key with a supported unique constraint and transaction-aware request handling.
A point-in-time restore produces a new database. What else needs recovery?|Validate connection routing, identities/grants, schema version, application state and downstream reconciliation before consumer switch.
Reporting queries block metadata updates. What can you change?|Review query duration/access paths and isolation behavior; isolate workloads or use suitable serving architecture without compromising transaction correctness.
A scale-down causes unacceptable latency. How do you evaluate it?|Benchmark representative concurrency and active resource pressure, then match tier/capacity to the agreed service target rather than average utilization.''',
'''Build a safe entity-state update procedure.|Require expected previous state/version and an owning run token; transactionally record the new accepted boundary and run result.
Analyze a query regression with Query Store.|Compare historical/current plan/runtime, data changes, waits and indexes; validate one corrective change with equivalent parameters.
Design a restore-and-cutover rehearsal.|Specify restore boundary, connection/identity validation, application checks, downstream reconciliation and measured recovery time.''',
dict(unit='one transactional SQL operation or control-state update', artifact='database schema, procedures, connection configuration and migration scripts', signal='Query Store plans, database resource metrics, waits and transaction state', state='transaction commit, entity-state version and accepted run/publication record', access='Entra/database identity, object grants, firewall/private-route configuration', contract='relational schema, unique keys, isolation and API/metadata semantics', bottleneck='CPU, I/O, plan regression, blocking and connection pressure', dependency='application/ADF caller and source or consumer contract', project='Azure orchestration metadata and governed relational serving'))

topic('Azure Event Hubs', '12_Azure_Event_Hubs',
'Managed event ingestion, partitioned consumption, replay boundaries and durable streaming integration.',
'Producer -> Event Hubs partition -> consumer group -> checkpointed processor -> durable bronze -> validated analytical output',
'https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-apache-kafka-overview',
'''What is Event Hubs for?|High-throughput event ingestion and consumption. It is not a relational query engine or a general substitute for every messaging pattern.
What is a partition?|An ordered event sequence within the hub. Ordering is partition-scoped, not automatically global across the hub.
What is a partition key?|A producer key used to route related events consistently under supported partition behavior. Hot keys can create uneven throughput.
What is a consumer group?|An independent consumption view for an application. Use separate groups for independent applications and coordinate workers within each group.
What are offsets/checkpoints?|Offsets identify positions in partition streams; a checkpoint records consumer progress. Sink side effects still need replay-safe handling.
What does retention imply?|Events remain available within the configured supported retention window. A stalled consumer beyond that window needs another recovery source.
What is Event Hubs Capture?|A supported archival delivery capability to configured storage. Validate output layout, identity and retention rather than treating it as a complete curated dataset.
How does the Kafka endpoint fit?|Event Hubs supports compatible Kafka protocol clients for documented features. It is a managed service endpoint, not an Apache Kafka broker cluster you administer.
How do you handle event schema?|Use an approved schema/contract, versioning and explicit parsing with failed-payload handling. A broker accepting bytes does not validate business semantics automatically.
What proves streaming freshness?|Measure accepted source event age and consumer lag as well as processing success. A running consumer can still be far behind.''',
'''How do you design idempotent consumption?|Persist stable event keys and source ordering in durable targets and handle replay. Checkpointing alone does not guarantee exactly-once external side effects.
How do you scale consumption?|Match worker/partition parallelism and supported service capacity to measured producer rate and processor cost. Idle partitions do not solve a hot key.
How do you use Kafka clients safely?|Verify supported APIs/configuration, authentication, partition behavior and transaction semantics for the actual service tier rather than assuming full Kafka parity.
How do you recover from retention gaps?|Detect missing boundaries, restore from retained raw/capture/source replay and reconcile target keys before continuing from a known accepted point.
How do you distinguish transport and business ordering?|Partition offsets order transport events; business corrections may require a producer sequence/effective timestamp. Do not overwrite newer state using an older event.''',
'''One partition is overloaded while others are idle. What do you investigate?|Inspect partition-key frequency and per-partition traffic, then redesign routing or business-key distribution with an ordering-aware migration.
Two independent applications steal each other's work. What is wrong?|They may share a consumer group unintentionally. Give independent applications separate groups and coordinate replicas only within an application.
A consumer restarts and duplicates usage rows. How do you fix it?|Reuse valid durable checkpoints and enforce target event-key idempotency. Reconcile already accepted events before replay.
A producer retries after an uncertain send. Can consumers see duplicates?|Yes, unless supported end-to-end semantics prevent them. Use stable business event IDs and durable sink deduplication.
An outage exceeds event retention. What is the recovery plan?|Replay from approved retained raw/capture/source history and establish a consistent new boundary; do not assume expired offsets remain readable.
Kafka client configuration works on Kafka but fails here. Why?|Event Hubs Kafka compatibility is feature/configuration-specific. Validate supported APIs, authentication and documented service behavior.
A poison event repeatedly crashes a partition processor. What do you do?|Persist restricted payload/error evidence, apply an approved quarantine policy and continue only when integrity/completeness rules permit.
Adding consumers does not reduce lag. What else matters?|Check partition parallelism, hot keys, throttling, sink throughput and per-event processing cost; worker count alone may not address the bottleneck.
Capture files exist but analytics missed events. What do you inspect?|Compare capture boundaries/manifests with processed offsets and source IDs. Validate ingestion of all relevant files and duplicate handling.
Events arrive out of business order. How do you update account state?|Use authoritative source sequence/correction rules and reject stale events; partition arrival order alone may not establish latest business state.''',
'''Design a telecom event ingestion pipeline.|Include event IDs, partition key, consumer group, checkpoint, raw archive, late policy and durable silver deduplication.
Build a lag and freshness dashboard.|Show producer/consumer rate, per-partition lag, accepted event age, throttling and sink errors with owner alerts.
Rehearse recovery beyond retention.|Use retained raw input, reconcile existing target keys and establish a supported replay boundary without data loss or double counting.''',
dict(unit='one event partition processing window', artifact='hub/consumer configuration, client authentication and processor deployment', signal='per-partition traffic, consumer lag, throttling and processor errors', state='partition offsets, durable checkpoint, raw archive and stable event keys', access='producer/consumer identity, service permissions and network connectivity', contract='event schema, partition key, business ordering and retention', bottleneck='hot partitions, ingestion limits, processor rate and sink throughput', dependency='event producers and checkpointed Databricks/Functions consumer', project='Mobistar reference streaming ingestion and datahub event integration'))

topic('Apache Kafka', '13_Apache_Kafka',
'Partitioned event logs, producers, consumer groups, offsets and streaming reliability.',
'Producer -> topic partition and replicated log -> consumer group -> accepted processing -> transactional or idempotent sink',
'https://kafka.apache.org/documentation/',
'''What is a Kafka topic?|A named logical stream divided into partitions. Retention/replay and consumer progress are separate concerns.
What ordering does Kafka provide?|Record order within a partition. Global ordering across partitions requires a separate design and can constrain scale.
What does a consumer group do?|Distributes partition ownership across group members for an application. Separate groups read independently.
What are committed offsets?|Recorded next-progress positions for group consumption. Commit timing relative to processing determines replay or loss risks.
What do producer acknowledgments affect?|They influence durability/latency tradeoffs with broker replication settings. Explain the full failure model rather than treating one setting as a universal guarantee.
What is the ISR concept?|In-sync replicas describe replicas sufficiently caught up under broker rules. Replication and minimum ISR settings participate in write availability/durability tradeoffs.
What does producer idempotence address?|Supported producer retry duplication within Kafka's documented semantics. It does not automatically deduplicate every business event or external sink side effect.
What is log compaction?|Retention of latest values by key under compaction semantics, with tombstone behavior. It is not instant uniqueness enforcement or complete event history.
What is a rebalance?|A reassignment of partition ownership in a consumer group. Consumers must manage in-flight work and offset handling safely.
How do schemas affect event compatibility?|Define versioned producer/consumer contracts and compatibility rules. Broker byte transport does not establish that a field change is safe.''',
'''What does exactly-once mean in Kafka processing?|Supported transactions can coordinate Kafka records/offsets under specified conditions. Arbitrary external databases/APIs still require an explicit transactional/idempotent integration design.
How do you avoid offset loss?|Process safely, then commit an appropriate accepted boundary; preserve replay-safe targets and handle partial-batch/rebalance cases.
How do you troubleshoot lag?|Compare per-partition input rate, consumer work, rebalance frequency and sink latency; distinguish hot keys from general undercapacity.
How do you plan partition increases?|Evaluate routing/key ordering impacts, producer mapping and downstream assumptions. Existing and future records may not map identically under a changed partition count.
How does Event Hubs compare?|It provides a managed Kafka-compatible endpoint with documented service support. Native broker operations/features and limits cannot be assumed identical.''',
'''You commit offsets before writing the database and then crash. What happens?|The consumer may resume after unpersisted records, causing loss. Coordinate the accepted write boundary and offset or use durable replay-safe processing.
You commit after database writes and then crash before commit. What happens?|Records can replay. Make database writes idempotent with stable keys or use an explicit supported coordinated design.
A rebalance duplicates external API calls. What prevents that?|Handle partition revocation/in-flight work and use external request idempotency keys; broker offset coordination alone cannot undo an API call.
One customer key dominates a partition. How would you redesign?|Measure key skew and ordering needs; consider a revised routing/business aggregation design while preserving required per-entity sequencing.
A partition increase changes key routing. What risk follows?|Per-key history may span old/new partitions, complicating ordering and state. Plan the migration and downstream state handling explicitly.
Compaction removes data needed for audits. What should change?|Separate compacted current-state topics from retained audit/raw history and align retention with approved evidence needs.
A poison payload stops a consumer group. What is your approach?|Capture restricted error evidence, route to an approved exception path and advance only under a defined completeness policy.
A producer times out despite broker acceptance. How do you handle duplicates?|Use supported idempotent producer configuration and stable business event IDs; validate downstream replay handling.
Consumer lag grows while CPU is low. What do you inspect?|Inspect slow sink/API calls, throttling, fetch behavior and partition ownership before adding CPU.
A team claims Kafka transactions make a REST side effect exactly once. How do you respond?|Kafka transactions do not automatically include an external REST operation. Require the API's idempotency/status contract or a durable outbox/workflow design.''',
'''Draw an offset commit failure timeline.|Show crashes before write, after write and after commit; explain lost/replayed records and target idempotency.
Design a keyed event contract.|Specify stable event ID, partition/business key, source sequence, schema version, correction rules and retention.
Create a consumer recovery rehearsal.|Simulate rebalance and replay, then verify accepted database/output keys and compare consumer offset boundaries.''',
dict(unit='one topic partition consumption batch', artifact='producer/consumer configuration, schema contract and processing code', signal='consumer-group lag, rebalance events, broker/client errors and sink latency', state='committed offsets, producer sequence, transaction boundary and target idempotency keys', access='client authentication, topic/group authorization and broker network route', contract='topic schema, partition routing, retention and business ordering', bottleneck='hot partitions, consumer processing rate, rebalance churn and external sink delays', dependency='Kafka producer/broker/consumer and downstream database or lake', project='streaming concepts for telecom and enterprise datahub integrations'))

topic('Azure DevOps', '14_Azure_DevOps',
'Reviewed source changes, CI/CD artifacts, environment promotion and deployment evidence.',
'Git change -> pull request -> validation -> immutable build artifact -> test deployment -> accepted production promotion -> monitoring and recovery',
'https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines',
'''What are the main CI/CD concepts?|CI validates integrated changes; CD promotes reviewed artifacts through environments. A deployment must include configuration/dependency handling and evidence, not just file copying.
What are stages, jobs and steps?|Stages group deployment/validation phases; jobs execute units of work on agents; steps are tasks/scripts within jobs.
What is an agent?|The execution host for a pipeline job. Hosted or self-hosted selection affects networking, dependencies, isolation and maintenance.
What is a service connection?|A pipeline's configured authentication/access path to an external service. Scope it to required deployment operations and environments.
What are build artifacts?|Versioned outputs produced by a build for deployment/use. Promote the same reviewed artifact rather than rebuilding different code in each environment.
How do variables differ from runtime parameters?|Variables hold pipeline/configuration values with defined expansion scopes; parameters support template/run configuration. Do not expose secrets through expansion/logging.
What does a PR policy protect?|Review and validation requirements before integration. It should include meaningful contract/tests and control of production-impacting changes.
What is infrastructure as code?|Reviewed definitions for infrastructure/configuration using tools such as Bicep/Terraform. State, identities and environment parameters need deliberate management.
How do you separate environments?|Use distinct resources/configuration/identities and controlled deployment permissions. Development author access should not imply unrestricted production modification.
What should release evidence include?|Commit/artifact IDs, deployment parameters, migration outcome, validation results, actor and accepted consumer/recovery state.''',
'''How do you deploy data schemas safely?|Use versioned migrations with compatibility/backfill checks and a data recovery plan. Reverting pipeline code may not reverse schema/data changes.
How do you secure pipeline dependencies?|Review tasks/packages and pin appropriate versions, scope tokens, protect secrets and verify artifact integrity. Avoid untrusted code with broad production credentials.
How do you handle private Azure resources?|Run deployment from an approved agent/network path with correct DNS and identity. Public hosted agents cannot be assumed to reach private endpoints.
How do you prevent concurrent releases?|Serialize environment/resource deployments or use supported locks; record ownership and state so one release does not overwrite another.
What is a good rollback strategy?|Restore compatible code/configuration and any affected data/consumer boundary, validate correctness, then resume traffic. Define rollback triggers before release.''',
'''A release deploys different code in test and production. What is the flaw?|The artifact is rebuilt or fetched inconsistently. Build once, identify the immutable artifact and promote it with environment-specific parameters.
A hosted agent cannot reach private ADLS. What do you change?|Use an approved reachable agent/network route and validate DNS/identity; do not weaken storage access just to make deployment pass.
A secret is printed by an echoed command. How do you respond?|Stop exposure, restrict/remove log access as appropriate, rotate the credential and remove unsafe logging/interpolation patterns.
A successful code rollback leaves the new table schema. What is missing?|A compatible schema/data migration recovery plan and validation of downstream consumers.
Two releases overwrite production configuration. What prevents it?|Environment/resource locking, immutable artifacts, release ownership and compare/check deployment state before mutation.
A production notebook depends on an unpinned package. Why is that risky?|The deployed behavior can change without a source change. Pin/validate dependencies and retain the package/runtime identity.
A test pipeline passes because it tests only syntax. What should be added?|Meaningful transformation fixtures and integration/replay/reconciliation/access checks appropriate to the change.
A service connection has subscription-wide rights. How would you reduce them?|Map actual deployment operations and scope identities/roles to required resources and environments with tested permissions.
ADF triggers fire during resource promotion. How do you handle it?|Use a controlled trigger/dependency deployment sequence and reconcile missed/overlapping windows before resuming live schedules.
A failed release has partially applied infrastructure changes. What do you do?|Inspect actual resource state and deployment evidence, then reconcile through a reviewed idempotent update or tested recovery rather than assuming no change occurred.''',
'''Design a data-platform YAML pipeline.|Show validation, immutable artifacts, test deploy, meaningful checks, controlled production promotion and recovery evidence.
Build an environment parameter contract.|Separate resource names/paths/identity references, validate required values and keep secrets out of repository files.
Write a schema-change rollback exercise.|Include compatibility checks, backfill scope, data recovery and downstream accepted publication validation.''',
dict(unit='one CI/CD deployment stage', artifact='YAML/templates, build artifact, IaC and environment parameters', signal='pipeline logs, task exit status, deployment state and integration evidence', state='commit/artifact ID, migration version and accepted release record', access='agent identity, service connection scope, environment controls and private route', contract='deployable artifact, configuration schema and consumer compatibility', bottleneck='agent queue, dependency restore, deployment duration and integration runtime', dependency='Git repository, Azure deployment APIs and target workload', project='promotion of ADF, Databricks, SQL and supported Fabric artifacts'))

topic('Git / GitHub', '15_Git_GitHub',
'Versioned engineering changes, pull requests, collaboration and recoverable source history.',
'Working tree -> staged changes -> commit -> reviewed branch/PR -> integrated history -> versioned deployment artifact',
'https://git-scm.com/docs',
'''How do Git and GitHub differ?|Git is distributed version control; GitHub hosts repositories and collaboration/automation services. Local Git operations do not require GitHub.
What are working tree, index and repository?|The working tree holds edited files, the index stages the next commit, and the repository stores history/objects/references.
What is a commit?|A versioned snapshot with parent history and metadata. Clear scope/messages help review and later recovery.
What is a branch?|A reference to a line of commits. Use short-lived reviewed branches for scoped engineering changes where the team workflow supports it.
How do fetch and pull differ?|Fetch retrieves remote refs/objects; pull integrates fetched work using configured merge/rebase behavior. Inspect integration mode and local changes first.
How do merge and rebase differ?|Merge integrates histories with a merge result; rebase rewrites a commit sequence onto a new base. Avoid rewriting shared history without agreed coordination.
What is a pull request?|A review/integration proposal around a branch diff. It should explain the concrete behavior change and relevant validation.
How do revert and reset differ?|Revert creates a new inverse commit; reset moves local refs/index/worktree depending on mode. Revert is usually more appropriate for undoing shared committed changes.
What does .gitignore do?|It prevents matching untracked files from being included by default. It does not remove already tracked files or purge secrets from history.
What does a tag provide?|A named reference useful for releases/version points. Deployment should still identify the actual commit/artifact and validated data compatibility.''',
'''How do you resolve meaningful merge conflicts?|Understand both intended changes and dependency effects, resolve the final behavior and rerun affected checks. Accepting one entire file may silently discard valid work.
How do you review notebook changes?|Prefer reviewable source/export forms, strip sensitive/generated output and verify parameters/business logic. A notebook binary/JSON diff alone can obscure behavior.
How do protected branches help?|They enforce selected review/check/integration rules. Protect production-impacting paths and keep bypass authority narrow.
How do you handle a committed secret?|Revoke/rotate it immediately through the approved incident process, then coordinate history cleanup and remove derived copies. A later deletion does not invalidate the secret.
How do GitHub Actions and Azure Pipelines relate?|Both can automate CI/CD; execution identity, permissions, runners/agents and artifact handling require explicit configuration. Git versioning alone does not deploy data safely.''',
'''Two engineers change the same SQL business rule. How do you resolve the conflict?|Agree the intended final rule with the owner, inspect both diffs and validate fixtures/reconciliation. A textual resolution is not sufficient evidence of semantic correctness.
A notebook commit includes customer data in outputs. What do you do?|Remove/restrict sensitive output and follow the approved exposure response; sanitize exports and add prevention to the workflow.
A password was removed in the latest commit. Is it safe now?|No. It can remain in history/copies; rotate/revoke it and coordinate cleanup with affected collaborators.
An engineer force-pushes a shared branch. How do you recover?|Identify expected commits using available reflogs/refs, coordinate recovery without overwriting others, and restore agreed history under team policy.
A release tag points to code without its schema migration. What is missing?|A reviewed compatible release unit and migration evidence; tag code and deployable artifacts only with the required schema/configuration scope.
A large generated dataset bloats the repository. What should change?|Keep data artifacts in approved storage, retain small synthetic fixtures and use suitable artifact pointers where appropriate.
A PR modifies ingestion and unrelated dashboards. How would you improve review?|Separate independently reviewable changes or clearly justify dependencies; give each scope concrete behavior and validation evidence.
A cherry-pick applies cleanly but breaks a pipeline. Why?|Text compatibility does not prove dependency compatibility. Check required schema/configuration commits and test the target branch.
A rollback needs to preserve later valid commits. What operation would you consider?|Use an appropriate inverse/revert change and validate interactions rather than resetting shared history blindly.
A PR check runs untrusted contributor code with production secrets. What is wrong?|The trust boundary is unsafe. Use restricted validation contexts and scope secrets/deployment permission to reviewed trusted execution.''',
'''Resolve a transformation merge conflict.|Explain both rules, build the intended final query and validate null/tie/financial fixtures.
Create a reviewable release change.|Include scoped commits, PR description, schema/configuration dependencies and relevant acceptance evidence.
Rehearse source rollback without losing valid work.|Identify the faulty commit/artifact, create a safe inverse or corrected change and validate downstream compatibility.''',
dict(unit='one reviewed change and release commit', artifact='commits, branch diff, pull request and versioned release reference', signal='diff/review history, required-check results and deployment commit identity', state='commit graph, release artifact mapping and migration version', access='repository permissions, protected-branch rules and automation token scope', contract='review scope, source format and code/schema/configuration compatibility', bottleneck='oversized diffs, generated files, conflicted changes and slow validation', dependency='collaborators, CI runner and deployment artifact consumer', project='review and release history for all six Azure project designs'))

topic('Power BI', '16_Power_BI',
'Business semantic models, measures, dashboards, refresh behavior and governed reporting.',
'Accepted facts and dimensions -> semantic model -> relationships and DAX measures -> secured report -> consumer decision',
'https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-overview',
'''What is a semantic model?|A defined analytical model of data, relationships and measures used by reports. Its grain and calculations must reflect the business contract.
What is a star schema useful for?|Dimensions filter facts with clear relationships and grains. It simplifies analytical reasoning and avoids accidental many-to-many multiplication.
How do Import and DirectQuery differ?|Import stores model data for query use; DirectQuery sends queries to the source under supported behavior. Freshness, latency and source load differ.
Where does Direct Lake fit?|A supported lake-oriented model mode for compatible Fabric scenarios. Validate the actual model/endpoint implementation and query path.
How do measures and calculated columns differ?|Measures evaluate in query/filter context; calculated columns store/evaluate row-derived values under model processing behavior. Choose based on semantics and resource impact.
What are filter context and row context?|Filter context defines selected rows for evaluation; row context iterates/current-row evaluation. DAX behavior depends on context transitions and relationships.
What is CALCULATE used for?|Evaluating an expression under modified filter context. The specific filter changes must be intentional and tested.
What is row-level security?|Model security rules limiting rows for applicable consumers. Underlying storage/source access and elevated workspace roles require separate review.
What is incremental refresh for?|Processing defined date ranges/partitions rather than all historical data, subject to supported configuration. Verify filtering/query folding and late-correction policy.
Why are dates and relationships important?|Consistent calendars, active relationships and fact dates determine correct time analysis. Multiple date roles need explicit modeling.''',
'''How do you model semi-additive balances?|Aggregate across approved entity dimensions but use selected-date/period-end behavior across time. Do not sum all daily snapshots as current balance.
How do you diagnose slow reports?|Measure expensive visuals/measures and source/model queries, then inspect cardinality, relationships and filter paths. Do not start by adding every column to the model.
How do you handle late fact corrections?|Refresh/reprocess affected partitions or use a supported current serving mode, then reconcile the revised accepted product and report measures.
How do you validate RLS?|Test actual user/group paths and elevated/direct-data access separately; compare allowed/forbidden rows and exports.
How do you deploy model changes?|Version model/report dependencies, test relationships/measures/security and promote compatible sources/contracts with environment settings.''',
'''Revenue doubles after adding a customer table. What do you inspect?|Check relationship cardinality, duplicated dimension keys, filtering and fact grain; fix the model instead of masking totals.
A monthly chart adds daily closing balances. What is wrong?|The measure treats snapshot values as fully additive. Implement the approved month-end/selected-date definition.
RLS works in testing but an admin sees every region. Is that unexpected?|Elevated roles/access can have different effective security behavior. Validate each real consumer role and underlying data path.
Refresh succeeds but the report has yesterday's business data. What should be monitored?|The accepted source/product as-of boundary and freshness target, not just model refresh completion.
DirectQuery slows an operational database. What options would you evaluate?|Measure query/concurrency pressure, tune the model/source and consider an appropriate analytical serving/import strategy aligned with freshness needs.
An incremental-refresh report misses a historical correction. Why?|The correction falls outside reprocessed scope or filtering policy. Reprocess affected partitions and define a late-correction mechanism.
A DAX measure returns the same value for every product. What do you inspect?|Check relationship paths, removed filters and CALCULATE/filter context behavior with small known examples.
One visual is fast while a page is slow. Why?|Multiple visuals/queries, expensive measures and interactions can create cumulative load. Measure the full page behavior and simplify the actual bottleneck.
A schema rename breaks refresh and measures. How do you release safely?|Use compatibility/versioning, dependency impact checks and coordinated source/model deployment with rollback.
A user downloads sensitive details from a permitted report. What controls matter?|Review report/model/export permissions and data minimization alongside row filters; validate the permitted consumer and underlying source paths.''',
'''Build a transaction-and-balance model.|Specify separate fact grains, dimensions and a date-aware balance measure; validate with known daily snapshots.
Design and test regional RLS.|Map users/groups to allowed regions, test real role paths and examine elevated/direct data access separately.
Diagnose one expensive visual.|Capture query/measure evidence, inspect model relationships and choose a measured optimization without changing totals.''',
dict(unit='one semantic-model refresh or report query', artifact='model relationships, DAX measures, report definition and refresh settings', signal='refresh history, visual/query timings, source queries and accepted-data age', state='model refresh boundary, accepted fact revision and date partition scope', access='workspace/model/report roles, row security and direct source permissions', contract='fact grains, measure definitions, relationship cardinality and date semantics', bottleneck='high cardinality, expensive DAX, source query latency and visual concurrency', dependency='accepted lakehouse/warehouse tables and report consumers', project='banking balances, finance reporting and enterprise quality dashboards'))

topic('Azure Key Vault', '17_Azure_Key_Vault',
'Controlled secrets, keys and certificates with workload access, rotation and auditability.',
'Approved workload identity -> vault authorization and network route -> required secret/key operation -> dependent connection -> audited access',
'https://learn.microsoft.com/en-us/azure/key-vault/general/overview',
'''What does Key Vault manage?|Supported secrets, cryptographic keys and certificates. Identify the object type and allowed operation for each integration.
How is a secret different from a key?|A secret stores a retrievable value; a key supports cryptographic operations under supported key rules. A key need not be exposed as plaintext to the caller.
Why prefer workload identity when supported?|It reduces the need to distribute reusable credentials. The workload still needs scoped permissions and a valid supported authentication flow.
What are authorization models?|Supported Azure RBAC and vault access-policy models govern data access differently. Configure/test the actual model and avoid assuming management access grants secret read.
How do management and data-plane permissions differ?|Resource administration and reading/using vault objects are different actions. Scope each separately.
Why do secret versions matter?|They preserve distinct values/metadata during updates. A pinned reference and a latest-version reference have different rotation behavior.
How should applications cache secrets?|Use bounded appropriate caching and refresh/rotation behavior, not a request to the vault for every data record. Never log cached values.
What is soft delete useful for?|Recovering supported deleted objects within configured retention. Verify purge protection and recovery procedures separately.
What do private endpoints change?|They provide a supported private access route when DNS/network configuration is correct. Permissions are still required.
What belongs in audit logs?|Identity, object operation, time and result without secret values. Restrict and retain logs under the approved policy.''',
'''How do you rotate a credential safely?|Coordinate source credential validity, new secret version, consumer refresh and rollback window; validate actual connections before retiring the old credential.
How do you avoid broad secret access?|Use narrowly scoped workload identities/object access where supported and separate environments/vaults as appropriate.
How do you distinguish 401/403/network errors?|Check token/identity first for authentication, effective permission for authorization and DNS/route/firewall for connectivity. Use the actual workload path.
How do keys relate to encryption at rest?|A key may be used by a supported service encryption integration. Key availability/permissions/rotation must be validated; encryption is not a replacement for data access controls.
How do you handle vault throttling?|Reduce excessive retrieval with safe caching, bounded retry/backoff and measured concurrency. Keep rotation refresh behavior explicit.''',
'''ADF cannot retrieve a secret but your portal account can. Why?|The factory's identity and vault permission/network path differ from yours. Test the linked-service/workload identity and required operation.
A rotated password is in the vault but jobs still use the old value. What do you inspect?|Check pinned secret version, connection caching and consumer refresh; validate source credential overlap/expiry.
A vault administrator cannot read secret values. Is that necessarily wrong?|Management and data-plane permissions differ. Grant only the required approved data access, not blanket privileges.
A private endpoint is configured but resolution is public. What should change?|Fix approved DNS/routing for the calling workload and validate network access without widening the vault unnecessarily.
A secret appears in notebook output. What is the response?|Restrict exposure, rotate/revoke the affected credential, sanitize outputs and prevent value logging through reviewed patterns.
An application retrieves a secret for every event and gets throttled. How do you improve it?|Cache safely with defined refresh/rotation behavior and bounded retries; secret lookup should not be per data record.
A deleted secret is needed for recovery. What do you check?|Inspect supported soft-delete retention and object recovery permissions; test the recovered consumer connection and current validity.
A disabled key breaks an encrypted service. What should be restored?|Identify the service's key/version dependency and approved recovery operation, restore supported access/availability and validate the service.
An expired credential causes only some workers to fail. Why?|Workers may have different cached versions/refresh timing. Inspect effective secret version and rotation rollout across consumers.
The same secret is copied into all environments. What is the concern?|It weakens isolation and broadens impact. Use environment-specific identities/credentials and validated rotation/access paths.''',
'''Design a secret rotation timeline.|Show source update, vault version, consumer refresh, validation, overlap and retirement with a rollback condition.
Diagnose a failed secret retrieval.|Separate authentication, data authorization and network route; use identity/object/version evidence without exposing values.
Build a secret-free deployment configuration.|Store identity/object references and parameters, retrieve only in supported runtime paths and test redacted logs.''',
dict(unit='one vault retrieval or cryptographic operation', artifact='vault authorization, object references, rotation policy and consumer configuration', signal='vault operation result, identity audit, DNS route and retry/throttling metrics', state='secret/key version, validity interval and consumer refresh state', access='effective workload identity, vault data-plane permission and network route', contract='required object operation, version pinning, caching and rotation behavior', bottleneck='excessive retrieval, throttling, network delay and refresh failures', dependency='credential issuer and dependent ADF/Databricks/application connection', project='secure supported connection credentials across Azure project designs'))

topic('Azure Monitor', '18_Azure_Monitor',
'Operational telemetry, log queries, metrics, meaningful alerts and incident investigation.',
'Workload diagnostics and metrics -> telemetry collection -> logs/metrics analysis -> alert rule -> action group -> owner investigation',
'https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview',
'''What does Azure Monitor provide?|Platform monitoring capabilities for metrics, logs and related operational analysis. Actual telemetry availability depends on each resource and configured collection.
How do metrics and logs differ?|Metrics are numeric time-series signals; logs are records queried for detailed context. Choose based on the question and signal availability.
What is Log Analytics?|A workspace/query experience for collected logs using supported schemas and KQL. Enabling a workspace alone does not collect every resource log.
What are diagnostic settings for?|Routing supported resource telemetry to configured destinations. Verify enabled categories, destination and retention.
What is an action group?|A configured set of actions invoked by supported alert rules. It routes notification/automation; it does not establish the alert's correctness.
What is KQL used for?|Querying supported telemetry tables with filtering, aggregation and correlation. It is not T-SQL and table schemas must be inspected.
What is Application Insights used for?|Application-oriented telemetry/tracing for supported integrations. Configure collection, correlation and sensitive-data handling.
What makes a useful alert?|An actionable condition with severity, owner, context and a runbook. Alert on accepted product freshness, not only technical task failures.
What is a correlation ID?|An identifier linking operations across telemetry sources. Keep it consistent with pipeline/job/publication IDs where possible.
How do telemetry cost and retention relate?|Collection volume, query use and retention affect cost. Keep necessary evidence and reduce unnecessary/sensitive high-volume payloads.''',
'''How do you distinguish no data from no failures?|Monitor collection heartbeat/expected telemetry and explicit success/freshness signals. An empty error query can mean ingestion stopped.
How do you reduce alert fatigue?|Use thresholds/windows tied to business impact, deduplication/grouping and clear ownership. Test missed incidents as well as noisy alerts.
How do you measure end-to-end freshness?|Compare accepted source business timestamps/publication boundaries to the current evaluation time and target, not just latest job end time.
How do you investigate a cross-service incident?|Correlate source, ADF, processing, storage and serving telemetry by run/boundary IDs, then identify the first failed/stale phase.
How do you monitor Fabric alongside Azure?|Use available Fabric monitoring/capacity signals and Azure telemetry for integrated services; do not assume every Fabric internal event lands automatically in Log Analytics.''',
'''A dashboard shows no pipeline failures but data is two days old. What is missing?|An accepted-data freshness signal and expected-run/source heartbeat. Successful or absent jobs are not proof of current data.
No logs arrive after a deployment. What do you check?|Diagnostic categories/settings, destination/workspace, identity where applicable, query scope and ingestion delay; test a known event.
A log query alerts on every retry. How do you improve it?|Correlate attempts to the final accepted run result and impact window; suppress only documented non-actionable transient events.
An alert fires but nobody receives it. What do you inspect?|Validate action group configuration, receiver availability and alert action execution; rehearse the routing path.
KQL returns no rows after a table schema change. What should change?|Inspect actual table/column types and collection context, update the query and validate known incident fixtures.
Telemetry costs spike during a backfill. What do you evaluate?|Identify high-volume categories/payloads and retention, reduce redundant detail while preserving run controls and required audit evidence.
Logs expose customer records from exceptions. How do you fix it?|Redact/minimize payloads, use restricted record references and separate exception storage; apply the approved exposure response.
Averages hide severe p95 latency. What should be monitored?|Use tail latency and appropriate business windows with volume/context, not just average duration.
An action-group webhook creates repeated incidents. What prevents it?|Use stable alert/incident keys and idempotent action handling with retry/correlation state.
A source outage and a slow Spark job look similar in freshness alerts. How do you isolate them?|Trace source boundary, landing manifest, processing lag and accepted publication IDs to locate the earliest stale phase.''',
'''Write a failure-trend KQL query.|Use the actual diagnostic table schema, filter by time/resource, summarize final failed runs and include run IDs for drill-down.
Design a data-product freshness alert.|Define accepted business timestamp, target, evaluation window, owner, missing-telemetry behavior and recovery condition.
Build an incident correlation view.|Join or link source delivery, pipeline/job run, control status and publication identity without exposing sensitive payloads.''',
dict(unit='one telemetry collection and alert evaluation cycle', artifact='diagnostic settings, KQL queries, alert rules and action groups', signal='collection heartbeat, log/metric time, alert state and action delivery outcome', state='evaluation window, correlation ID, alert/incident key and accepted product timestamp', access='telemetry writer/query roles, workspace scope and action endpoint identity', contract='telemetry schema, time semantics, freshness target and incident-routing policy', bottleneck='ingestion latency, query scan volume, alert noise and telemetry cost', dependency='resource diagnostics and owner/action-group response path', project='end-to-end health and accepted-data freshness across six projects'))

topic('Azure Functions', '19_Azure_Functions',
'Serverless event handlers, lightweight validation, integration and asynchronous processing.',
'HTTP or supported event trigger -> function identity/binding -> bounded business operation -> durable target -> status and telemetry',
'https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview',
'''What is Azure Functions?|A serverless application execution platform for supported triggers and bindings. Hosting/runtime choices affect scaling, execution and networking behavior.
What is a trigger versus a binding?|A trigger starts an invocation; bindings provide supported input/output integrations. Bindings do not automatically establish all business correctness guarantees.
When is a function suitable for data engineering?|For bounded event validation, API adapters and lightweight automation. Large historical Spark transformations usually need a suitable analytical engine.
What makes a function stateless?|It does not rely on local process memory/files for durable business state across invocations. Persist necessary progress in supported external storage.
What are cold starts?|Initialization effects when an instance/runtime must become ready. Their impact depends on hosting, configuration and actual traffic pattern.
What is idempotency for an event handler?|Repeated delivery of the same business operation has no extra effect. Use stable event/request keys and durable target safeguards.
How do you authenticate dependencies?|Prefer supported workload identities and scoped permissions; configure required secrets through approved mechanisms when necessary.
What is Durable Functions for?|Supported stateful workflow/orchestration patterns using its runtime model. Orchestrator code must follow replay/determinism requirements.
How do you monitor invocations?|Record correlation IDs, results, durations and dependency failures using supported telemetry without sensitive payloads.
How do you choose hosting?|Evaluate execution pattern, latency, scale, network requirements and supported plan capabilities. Do not assume one universal timeout/network feature set.''',
'''How do retries differ by trigger?|Retry/delivery behavior depends on trigger extension and configuration. Define poison-event handling, accepted progress and idempotent targets explicitly.
How do you coordinate external side effects?|Use API idempotency keys, durable operation state or a supported outbox/workflow design. Process restart can occur after the side effect but before status recording.
How do you tune concurrency?|Measure per-instance processing and downstream limits, then use supported trigger/host controls. Scaling up can overwhelm the target database/API.
How do you deploy safely?|Version package/runtime/configuration, validate trigger bindings and identity/network access, and coordinate supported deployment slots/routes where applicable.
How do you design long-running work?|Use asynchronous work handoff or supported durable orchestration rather than holding an HTTP request for large processing; keep replay-safe activities.''',
'''A blob-triggered function processes the same file twice. What should happen?|Use a stable delivery/object-version key and durable target idempotency. Verify trigger behavior rather than assuming exactly-once delivery.
An HTTP function times out during a full data backfill. What redesign fits?|Return an accepted asynchronous job reference and dispatch suitable analytical work; track status externally rather than doing lake-scale work synchronously.
Scaling creates too many database connections. What do you tune?|Use appropriate connection reuse/pooling and bounded concurrency while checking database limits and request throughput.
A function succeeds locally but cannot access Key Vault in Azure. Why?|The deployed identity, configuration and network route differ. Test the actual managed/workload identity and vault data-plane access.
An Event Hubs poison event retries repeatedly. What is the policy?|Capture restricted exception evidence and apply documented trigger/checkpoint/quarantine semantics, ensuring the accepted stream remains reconcilable.
A durable orchestrator makes random external calls during replay. What is wrong?|Orchestrator logic must follow determinism constraints; put external side effects in supported activities with idempotent handling.
A function writes data then crashes before returning. Can retry duplicate it?|Yes. Use durable idempotency keys/target constraints and reconcile completed operation state.
An API consumer complains about intermittent cold latency. What do you evaluate?|Measure initialization versus dependency latency and assess supported hosting/runtime configuration against cost and response targets.
Local temporary files disappear between invocations. Why?|Instance-local storage is not a durable cross-invocation business store. Use approved external storage and explicit manifests.
A deployment starts processing with mismatched schema/configuration. How do you avoid it?|Promote a compatible package/configuration/binding set, validate in test and control activation/traffic with a tested recovery path.''',
'''Design an idempotent event handler.|Use event key, validation, durable operation state, target write and accepted completion; test a crash after the side effect.
Build an asynchronous API pattern.|Return operation ID, dispatch bounded/suitable work and expose secure durable status with retry/correlation handling.
Plan a function deployment check.|Validate runtime/extensions, bindings, identity, network route, one synthetic event and redacted telemetry.''',
dict(unit='one event-triggered function invocation', artifact='function package, trigger/binding configuration and hosting settings', signal='invocation trace, dependency timing, retries and host scaling metrics', state='event/request idempotency key, durable operation record and trigger checkpoint', access='function identity, dependency permissions and hosting/network route', contract='trigger payload, response semantics, retry policy and execution scope', bottleneck='cold initialization, dependency latency, concurrency and connection pressure', dependency='trigger source and target API/database/storage operation', project='bounded datahub API adapters and event-driven automation'))

topic('Azure Logic Apps', '20_Azure_Logic_Apps',
'Connector-based workflows, external integration, notifications and accountable remediation orchestration.',
'Trigger -> validate workflow input -> connector/action steps -> scoped error handling -> external outcome -> durable run evidence',
'https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview',
'''What is a Logic App?|A workflow integration service using supported triggers, actions and connectors. It coordinates business/integration steps rather than serving as a distributed Spark engine.
What is a connector?|An integration interface to supported services. Authentication, limits, pagination and retry semantics vary by connector and operation.
How do triggers and actions differ?|A trigger initiates the workflow; actions perform work. The trigger's delivery behavior and action side effects need separate correctness handling.
How do Consumption and Standard differ conceptually?|They have different hosting/resource models and capabilities. Verify the actual connector, networking, scaling and billing support for the chosen model.
What are scopes and run-after conditions?|Scopes group steps; run-after conditions select follow-up behavior based on supported action outcomes. They support explicit success/error cleanup paths.
What is a workflow definition?|The versioned structure of triggers, actions and expressions. Connections and environment configuration must also be deployed correctly.
What is a recurrence trigger used for?|Time-based scheduling. Define timezone/window boundaries and duplicate/missed-run behavior under the workflow contract.
How do you secure connections?|Use supported managed/workload identity where possible and scope connector credentials/permissions. Do not embed secret values in definitions.
Why can loops be dangerous?|High concurrency can overload external services or conflict on shared state. Bound concurrency and keep per-item operation identities.
What is run history useful for?|Tracing action input/output/status and timing. Protect/redact sensitive payloads rather than exposing them to all workflow readers.''',
'''How do you make workflows idempotent?|Use stable business operation keys and durable outcome state; validate connector/API idempotency before retrying side-effecting actions.
How do you handle connector throttling?|Respect supported rate-limit guidance, bound parallelism and use appropriate retries/backoff with an accepted progress record.
How do you integrate data pipelines?|Receive a validated incident/event payload and route approved workflow actions. Keep bulk transformation in ADF/Databricks and preserve correlation IDs.
How do you deploy workflows?|Version definitions, connection references and environment parameters, verify permissions and activation behavior, then test normal/error paths.
How do you separate business failure from technical failure?|A valid action response can still report a failed business outcome. Parse agreed status semantics and route owner remediation, not just transport errors.''',
'''A quality incident opens three duplicate tickets. What prevents it?|Use a stable incident/business key and durable create-or-update outcome tracking; validate the external system's idempotency support.
A connector returns 429 during a parallel loop. What should change?|Reduce concurrency, use supported backoff/rate guidance and preserve per-item progress without duplicating accepted actions.
A failed action does not invoke cleanup. What do you inspect?|Check scope boundaries and run-after settings for failure, timeout and skipped states; test the actual error path.
An approval waits longer than the workflow permits. What design fits?|Use supported durable/stateful behavior and external business status, with explicit expiry/escalation; verify hosting/connector constraints.
Run history contains customer account details. How do you protect it?|Use supported secure-input/output settings where applicable, minimize payloads and restrict run-history access.
A workflow succeeds after an API returns a business rejection. What is missing?|Explicit response/body business-status validation; HTTP success alone does not establish accepted processing.
Deployment creates a workflow but its connection is invalid. What do you check?|Validate environment connection references, authentication, connector availability and network access before activating the trigger.
An ADF retry sends the same failure notification again. How do you handle it?|Correlate attempts to the same final incident key and update existing status rather than creating a new notification/incident each time.
A workflow tries to transform millions of lake records in loops. What would you change?|Dispatch a suitable data processing job and orchestrate its status/result; connectors/loops are not a replacement for distributed analytics.
A recurrence schedule crosses daylight-saving boundaries. What should be specified?|Use explicit supported timezone/schedule semantics and record bounded business windows; test skipped/repeated local times.''',
'''Design a data-quality remediation workflow.|Use a validated incident key, owner routing, create/update action, controlled retries, approved escalation and revalidation status.
Build a success/error scope graph.|Define normal actions, business response checks, failure/timeout handling and cleanup with tested run-after outcomes.
Create a portable workflow release.|Parameterize connections and environment references, validate identity/network routes and test activation plus one synthetic incident.''',
dict(unit='one workflow run and connector action sequence', artifact='workflow definition, connection references and environment parameters', signal='run history, action response/body, connector timing and retry status', state='workflow run ID, incident/operation key and durable external outcome', access='connector identity, external system permissions and supported network route', contract='trigger payload, business response status, retry and escalation policy', bottleneck='connector throttling, loop concurrency, external latency and long waits', dependency='upstream pipeline incident and approved external workflow system', project='data-quality owner routing and operational workflow automation'))

def operational_scenarios(t):
    o, name = t['ops'], t['name']
    return [
        (f"After moving {o['unit']} to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?",
         f"Capture the effective caller and exact error, then validate {o['access']}. Compare production with the working configuration using {o['signal']}; do not resolve the incident by giving every identity broad access.",
         'Demonstrate the required identity succeeding and an unauthorized identity remaining denied.'),
        (f"The health page says {name} is available, but the business result has not advanced. What would you check?",
         f"Trace the expected operation through {o['dependency']} and compare progress in {o['state']}. Inspect {o['signal']} to distinguish a service being reachable from an accepted business operation actually completing.",
         'Identify the last accepted business/release boundary and the earliest phase that stopped advancing.'),
        (f"A new release of {o['artifact']} works in test but breaks a dependent production consumer. How do you diagnose it?",
         f"Compare versions, environment settings and the actual {o['contract']}. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.",
         'Run the affected consumer contract test under production-equivalent identity and inputs.'),
        (f"Latency doubles for {o['unit']} although the request or data volume is unchanged. What is your investigation sequence?",
         f"Compare a known-good baseline with {o['signal']} and inspect {o['bottleneck']}. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.",
         'Compare representative latency distribution, throughput and correctness before and after the change.'),
        (f"An operation involving {name} may have completed, but the caller timed out before receiving confirmation. How do you retry safely?",
         f"Inspect the durable outcome in {o['state']} before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.",
         'Simulate the timeout after completion and prove the retry does not create an extra business side effect.'),
        (f"Two automated callers perform conflicting changes to {o['unit']} at the same time. How do you prevent lost or inconsistent state?",
         f"Identify the shared resource and ownership boundary in {o['state']}. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.",
         'Execute the conflicting requests and verify one accepted outcome with auditable ownership.'),
        (f"An upstream contract change reaches {name} without prior notice. How do you contain the impact?",
         f"Validate against {o['contract']} and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.",
         'Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.'),
        (f"You need to investigate last month's incident, but some {o['state']} evidence has expired. What can you recover and what should change?",
         f"Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of {o['state']} and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.",
         'Reconstruct one retained incident end to end and document the tested retention/recovery boundary.'),
        (f"Sensitive identifiers appear in {o['signal']}. How would you fix the logging and access design?",
         f"Minimize/redact payload values and use restricted references/correlation IDs. Review {o['access']} for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.",
         'Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.'),
        (f"An automation for {name} accidentally points to production while rehearsing in development. What controls would you add?",
         f"Validate environment/resource identifiers in {o['artifact']}, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against {o['state']} before restoring normal processing.",
         'Demonstrate the development identity/configuration cannot perform the unintended production action.'),
        (f"{o['dependency'].capitalize()} is temporarily unavailable. What retry and recovery policy fits {name}?",
         f"Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved {o['state']}; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.",
         'Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.'),
        (f"Costs associated with {name} rise while accepted business volume stays flat. How do you investigate without losing recovery capability?",
         f"Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect {o['bottleneck']}. Remove demonstrated waste while preserving required {o['state']} and correctness/access controls.",
         'Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.'),
        (f"During a recovery exercise, {o['artifact']} is restored but the business path still fails. What else is required?",
         f"Restore/validate {o['access']}, {o['dependency']} and the appropriate {o['state']}. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.",
         'Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.'),
        (f"Only a small subset of records, requests or objects fails in {name}. How do you isolate it without silently accepting incomplete results?",
         f"Correlate failing business keys/objects with {o['signal']} and validate their {o['contract']}. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.",
         'Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.'),
        (f"You must change {o['artifact']} while dependent workloads remain active. What release sequence would you use?",
         f"Inventory consumers and {o['contract']} compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain {o['state']} and define a tested rollback/correction route for incompatible behavior.",
         'Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.'),
    ]

def question_block(prefix, number, question, answer, evidence=None):
    block = f'### {prefix}{number:02d}. {question.strip()}\n\n**Model answer:** {answer.strip()}\n'
    if evidence:
        block += f'\n**Verification:** {evidence}\n'
    return block+'\n'

def system_questions(t):
    o = t['ops']
    return [
        (f"Where does {t['name']} fit in an end-to-end Azure data platform?",
         f"Use this specific flow: {t['flow']}. Explain what this component owns, how {o['dependency']} connects, and what the accepted consumer/result boundary is."),
        (f"How would you justify using {t['name']} for {o['project']}?",
         f"Start with actual volume, freshness, correctness, access and support requirements. Explain how {o['unit']} meets them, compare a credible alternative and validate using {o['signal']} rather than choosing a tool merely because it is on the stack."),
        (f"What controls must surround {t['name']} in a financial or telecom project?",
         f"Tie {o['contract']} to accountable business ownership, verify {o['access']}, preserve {o['state']} and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed."),
        (f"Which measures would prove your {t['name']} optimization helped?",
         f"Record the old/new configuration and comparable workload, measure {o['bottleneck']} with {o['signal']}, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement."),
        (f"How would you explain your own contribution to a {t['name']} interview project?",
         f"Identify which {o['artifact']} you personally built/reviewed/operated, one specific failure you resolved, the evidence in {o['state']} and a verified outcome. State team-owned components separately and do not invent scale or savings."),
    ]

extra_sources = {
 '01_Azure_Data_Factory_ADF': [('Integration runtime concepts','https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime')],
 '02_Azure_Databricks': [('Structured Streaming with Unity Catalog','https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/unity-catalog')],
 '04_Microsoft_Fabric': [('Enterprise BI architecture','https://learn.microsoft.com/en-us/azure/architecture/example-scenario/analytics/enterprise-bi-microsoft-fabric')],
 '09_Delta_Lake': [('Databricks Delta MERGE','https://learn.microsoft.com/en-us/azure/databricks/delta/merge'),('Delta best practices','https://learn.microsoft.com/en-us/azure/databricks/delta/best-practices')],
 '13_Apache_Kafka': [('Kafka 4.1 delivery and transaction design','https://kafka.apache.org/41/design/design/')],
 '15_Git_GitHub': [('git revert reference','https://git-scm.com/docs/git-revert.html')],
 '17_Azure_Key_Vault': [('Key Vault monitoring','https://learn.microsoft.com/en-us/azure/key-vault/general/monitor-key-vault')],
 '19_Azure_Functions': [('Durable orchestrations','https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-orchestrations')],
}

for t in TOPICS:
    o = t['ops']
    assert (len(t['core']),len(t['advanced']),len(t['scenarios']),len(t['practical'])) == (10,5,10,3), t['name']
    doc = f'''# {t['name']} — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** {t['purpose']}

**Audience:** Azure data engineering interviews, from fundamentals through production troubleshooting and design. The model answers are concise starting points; expand them with the actual source semantics, engine/runtime, workload identity and acceptance evidence. Practice scenarios are hypothetical and are not claims about the named client projects.

## Contents

- A. Core interview questions — C01–C10.
- B. Advanced implementation questions — A01–A05.
- C. Scenario-based interview questions — S01–S25.
- D. Practical implementation exercises — P01–P05.
- E. Architecture and project discussion — D01–D05.
- Revision notes, scoring and official references.

## Role in the full project flow

```text
{t['flow']}
```

For this guide, the primary unit is **{o['unit']}**. The engineering artifacts are {o['artifact']}. Troubleshooting starts with {o['signal']}; durable progress/evidence is represented by {o['state']}. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

'''
    for i,(q,a) in enumerate(t['core'],1): doc += question_block('C',i,q,a)
    doc += '## B. Advanced implementation questions\n\n'
    for i,(q,a) in enumerate(t['advanced'],1): doc += question_block('A',i,q,a)
    doc += '''## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

'''
    for i,(q,a) in enumerate(t['scenarios'],1):
        doc += question_block('S',i,q,a,
            f"Use relevant {o['signal']} and confirm the intended {o['contract']}. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.")
    doc += '### Production integration, recovery and operational scenarios\n\n'
    for i,(q,a,e) in enumerate(operational_scenarios(t),11): doc += question_block('S',i,q,a,e)
    doc += '''## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

'''
    practical=t['practical']+[
        (f"Create a failing-and-recovered test for {o['unit']}.",
         f"Capture the initial {o['state']}, introduce one realistic dependency or validation failure and use {o['signal']} to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access."),
        (f"Prepare the operating handoff for {t['name']}.",
         f"Document {o['artifact']}, the {o['contract']}, required {o['access']}, owner, normal/failure signals and recovery instructions using {o['state']}. Include one normal and one failure example plus actual service targets and retention assumptions."),
    ]
    for i,(q,a) in enumerate(practical,1): doc += question_block('P',i,q,a)
    doc += '## E. Architecture and project discussion\n\n'
    for i,(q,a) in enumerate(system_questions(t),1): doc += question_block('D',i,q,a)
    doc += f'''## Revision notes and common mistakes

- Explain {t['name']}'s specific responsibility in the flow before naming surrounding tools.
- Use the real {o['contract']}; an accepted request/job does not establish a correct business result.
- Validate {o['access']} under the actual execution identity, rather than your administrator account.
- Preserve {o['state']} and inspect it before retrying uncertain side effects.
- Tune {o['bottleneck']} from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [{t['name']} official documentation]({t['official']}).
'''
    for label,url in extra_sources.get(t['slug'],[]): doc+=f'- [{label}]({url}).\n'
    doc+='\n[Back to all 20 interview guides](README.md).\n'
    (ROOT/f"{t['slug']}_Interview_Questions.md").write_text(doc,encoding='utf-8')

readme = '''# Azure Data Engineering — 20 Separate Interview Guides

**1,000 questions with model answers, including 500 scenario-based questions.** Every technology has its own Markdown file with exactly 50 questions: 10 core, 5 advanced, 25 scenarios, 5 practical exercises and 5 architecture/project questions.

These are original interview preparation questions, not leaked interview/exam material. Model answers are concise outlines; exact APIs, feature availability and runtime/service limits require checking the relevant official documentation. Scenario questions are hypothetical and must not be presented as work actually performed for a client.

## Files

| No. | Technology | Questions | Scenarios | Separate Markdown file |
|---|---|---:|---:|---|
'''
for i,t in enumerate(TOPICS,1):
    readme+=f"| {i} | {t['name']} | 50 | 25 | [Open guide]({t['slug']}_Interview_Questions.md) |\n"
readme+='''
## How to use each file

1. Read the role-in-project flow and core questions to establish terminology.
2. Practice advanced implementation answers with a diagram and an explicit engine/runtime.
3. Work through all 25 scenarios. State impact, evidence, correction, safe recovery and verification.
4. Complete the practical exercises using synthetic/approved data; retain expected outputs and test evidence.
5. Use the architecture questions to connect the technology to a real project contribution and verified result.

Each question has a stable ID: C01–C10 (core), A01–A05 (advanced), S01–S25 (scenarios), P01–P05 (practical), D01–D05 (architecture/project). Scenario questions include verification guidance. The first ten scenarios target technology-specific behavior; the remaining fifteen address production integration, security, release, observability, cost and recovery with technology-specific artifacts and evidence.

## Suggested preparation order

- Foundations: SQL, Python, ADLS Gen2, ADF.
- Distributed engineering: PySpark, Azure Databricks, Delta Lake, Unity Catalog.
- Analytics: Azure Synapse, Microsoft Fabric, Azure SQL, Power BI.
- Streaming: Event Hubs, Apache Kafka.
- Delivery and operations: Git/GitHub, Azure DevOps, Key Vault, Azure Monitor.
- Event-driven integration: Azure Functions, Azure Logic Apps.

## Use with the existing project documents

The [project portfolio](../Azure_Data_Engineering_Portfolio/README.md) and [full flow diagrams](../Azure_Data_Engineering_Portfolio/FULL_PROJECT_FLOW_DIAGRAMS.md) provide six reference architectures. Match interview practice to the actual project technology: Fabric banking analytics, Azure lake modernization, enterprise datahub, quality/governance, financial warehouse integration and telecom streaming. Do not force all twenty technologies into every project.

Documents contain questions, model answers and exercise outlines. They do not provision cloud resources or demonstrate that production configurations have been executed. Retain only verified personal experience in resume/project answers.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print(f'Created {len(TOPICS)} separate technology guides: 1,000 questions, including 500 scenarios.')
