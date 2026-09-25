from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


OUTPUT = Path(__file__).with_name("25_Day_PySpark_Learning_Plan.ipynb")


def clean(text: str) -> str:
    return dedent(text).strip()


def md(text: str):
    return nbf.v4.new_markdown_cell(clean(text))


def code(text: str):
    return nbf.v4.new_code_cell(clean(text))


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def functions_table(rows: list[tuple[str, str, str, str]]) -> str:
    lines = [
        "| Function | Purpose | Syntax | Common use |",
        "|---|---|---|---|",
    ]
    for name, purpose, syntax, common_use in rows:
        lines.append(f"| `{name}` | {purpose} | `{syntax}` | {common_use} |")
    return "\n".join(lines)


def errors_table(rows: list[tuple[str, str, str]]) -> str:
    lines = [
        "| Error / problem | Why it happens | How to fix it |",
        "|---|---|---|",
    ]
    for problem, why, fix in rows:
        lines.append(f"| {problem} | {why} | {fix} |")
    return "\n".join(lines)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))


def objectives(spec: dict) -> list[str]:
    fn_names = ", ".join(f"`{row[0]}`" for row in spec["functions"][:4])
    return [
        f"Explain {spec['topic'].lower()} in plain language and say why a data engineer needs it.",
        f"Recognize the core ideas: {', '.join(spec['concepts'])}.",
        f"Use the main APIs safely: {fn_names}.",
        f"Implement the retail requirement: {spec['retail_requirement']}",
        f"Apply the same idea independently to {spec['bank_focus']}.",
        "Predict the schema and result before running a transformation.",
        f"Describe Spark's internal behavior: {spec['internal']}",
        f"Answer interview questions about {spec['compare']} and production trade-offs.",
    ]


def practice_questions(spec: dict) -> list[str]:
    concepts = spec["concepts"]
    primary = concepts[0]
    secondary = concepts[min(1, len(concepts) - 1)]
    dataset = spec["retail_df"]
    return [
        f"[Beginner] Display five rows from `{dataset}` and describe each column used today.",
        f"[Beginner] Use {primary} to answer a simple business question on `{dataset}`.",
        f"[Beginner] Re-create the instructor result with one changed value or condition.",
        f"[Intermediate] Combine {primary} with a column selection learned earlier and give columns business-friendly aliases.",
        f"[Intermediate] Use {secondary} and verify the output schema before accepting the result.",
        f"[Intermediate] Add a data-quality check for null, duplicate, or invalid values relevant to today's result.",
        f"[Intermediate] Produce a second result at a different business grain and explain why its row count changes.",
        f"[Advanced] Solve the retail requirement in a second valid way and compare readability and execution plans.",
        f"[Advanced] Explain how today's transformation behaves with 500 million rows and one highly skewed value.",
        f"[Advanced] Turn today's work into an idempotent pipeline step with named inputs, output columns, and validation rules.",
    ]


def bank_questions(spec: dict) -> list[str]:
    explicit = spec.get("bank_tasks")
    if explicit:
        return split_items(explicit)
    topic = spec["topic"].lower()
    return [
        f"Inspect the banking input schema and identify columns needed for {spec['bank_focus']}.",
        f"Create a small, readable result that demonstrates {topic}.",
        "Preserve identifiers and give all derived columns clear business names.",
        "Add one realistic condition supplied as a variable rather than hard-coded throughout the code.",
        "Reuse at least one transformation learned on an earlier day.",
        "Check nulls and duplicates at the business key before producing the result.",
        "Show the result in a stable, reviewable order without collecting the full dataset to Python.",
        "State the expected row grain and the columns that make a row unique.",
        "Write two assertions or reconciliation checks for the result.",
        "Explain one scale, skew, or security concern a bank would review before production release.",
    ]


def interview_section(spec: dict) -> str:
    fns = ", ".join(f"`{x[0]}`" for x in spec["functions"])
    first_error = spec["errors"][0]
    sections = {
        "Beginner": [
            (f"What is {spec['topic']}?", spec["what"]),
            ("Why do we need it?", spec["why"]),
            ("Which PySpark functions are most relevant?", f"The main APIs here are {fns}. I choose among them based on the required output grain and schema."),
            ("Where would you use this in a real project?", spec["production"]),
            ("Can you give a simple analogy?", spec["analogy"]),
        ],
        "Intermediate": [
            ("What does Spark do internally?", spec["internal"]),
            ("What is the main performance consideration?", spec["performance"]),
            ("How do you validate the result?", "I verify schema, row grain, key uniqueness, null rates, record counts, and a small set of known business totals."),
            (f"How do you compare {spec['compare']}?", spec["comparison_answer"]),
            ("What common mistake would you watch for?", f"I watch for {first_error[0].lower()}. It happens because {first_error[1].lower()} I prevent it by {first_error[2].lower()}"),
        ],
        "Scenario-based": [
            ("How would you solve today's retail requirement?", spec["approach"]),
            ("How would you adapt it to banking data?", f"I would start from the declared banking keys, apply the same {spec['topic'].lower()} principle, and validate {spec['bank_focus']} without copying retail-specific assumptions."),
            ("What changes when the table grows to hundreds of millions of rows?", spec["performance"]),
            ("How would you productionize this notebook code?", "I would move transformations into tested functions, parameterize paths and dates, add data-quality checks, log counts and metrics, and write atomically to a governed target."),
            ("The result is unexpectedly wrong. How do you debug it?", "I check the schema and grain at every step, isolate the earliest step where counts or totals diverge, inspect the physical plan, and reproduce the issue with a minimal sample."),
        ],
    }
    blocks = []
    for label, questions in sections.items():
        blocks.append(f"#### {label}")
        for i, (question, answer) in enumerate(questions, 1):
            blocks.append(f"**{i}. {question}**  \n{answer}")
    return "\n\n".join(blocks)


COMMON_ERRORS = [
    ("Using Python boolean operators", "Spark Columns are expressions, not Python booleans.", "Use `&`, `|`, and `~`, with each condition in parentheses."),
    ("Calling `collect()` on large data", "All matching rows are moved to the driver.", "Use `show`, `limit`, aggregations, or write the distributed result."),
    ("Assuming row order", "Distributed DataFrames have no guaranteed order.", "Use an explicit `orderBy` only when deterministic presentation is required."),
    ("Ignoring the schema", "Inferred or drifting types can silently change results.", "Declare schemas for production inputs and validate types at boundaries."),
]


SPECS = [
    dict(
        day=1, topic="Introduction to PySpark",
        concepts=["Spark", "PySpark", "distributed computing", "driver", "executors"],
        what="PySpark is the Python interface to Apache Spark, a distributed engine that processes data by dividing work across machines.",
        why="It lets a familiar Python program process data that is too large or too slow for one machine while keeping high-level DataFrame APIs.",
        how="The Python driver builds a logical plan. Spark schedules distributed tasks, executors process partitions, and the driver coordinates the result.",
        internal="The driver creates a Spark application; executors run tasks over partitions and report status and small results back to the driver.",
        production="Teams use PySpark for batch ETL, lakehouse transformations, data-quality checks, feature preparation, and large analytical jobs.",
        analogy="Think of the driver as a restaurant manager who divides a large order among several cooks, the executors.",
        performance="Keep computation distributed and avoid pulling large datasets to the driver.",
        compare="PySpark, pandas, and SQL", comparison_answer="PySpark is distributed, pandas is normally single-machine, and SQL is a language that Spark can execute through the same engine.",
        functions=[
            ("SparkSession.builder.getOrCreate", "Create or reuse a Spark session", "SparkSession.builder.appName('name').getOrCreate()", "Application entry point"),
            ("createDataFrame", "Build a DataFrame", "spark.createDataFrame(data, schema)", "Small samples and tests"),
            ("show", "Display a limited preview", "df.show(5, truncate=False)", "Interactive inspection"),
            ("spark.version", "Read Spark version", "spark.version", "Environment verification"),
        ],
        retail_df="retail_customers", retail_dataset="Retail customers",
        retail_requirement="create the retail Spark session, load customers, and verify the first five records.",
        retail_code="""
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .appName("RetailSalesAnalytics")
         .getOrCreate())

print("Spark version:", spark.version)
retail_customers.show(5, truncate=False)
print("Customer rows:", retail_customers.count())
""",
        approach="Create or reuse a SparkSession, construct the customer DataFrame with a known schema, preview a few rows, and count only because this teaching dataset is small.",
        expected="The preview begins with customer IDs `C001`–`C005`, and the full sample contains **12 customers**.",
        interpretation="The Spark application is ready, customer records are distributed as a DataFrame, and later retail steps can reuse the same session.",
        bank_focus="creating and inspecting a banking customer DataFrame",
        bank_tasks="Create `bank_customers` from the supplied records and schema.|Display the first five customers without truncating names.|Print the DataFrame schema.|Count the customer records.|Select only customer ID, name, and type.|Explain which process is the driver in this notebook.|Explain what an executor would do for the count action.|Change the application name and verify it from `spark.sparkContext.appName`.|Compare a Python list with a Spark DataFrame in one paragraph.|Write three checks proving the sample loaded correctly.",
        challenge="A bank receives 50 million customer rows daily. Describe how the driver, executors, and partitions cooperate to validate the file without collecting every record.",
        errors=COMMON_ERRORS,
    ),
    dict(
        day=2, topic="Spark Architecture",
        concepts=["driver", "executor", "cluster manager", "job", "stage", "task"],
        what="Spark architecture is the set of processes and scheduling units that turn DataFrame code into parallel work.",
        why="Knowing the architecture helps you read the Spark UI, explain failures, and locate bottlenecks instead of treating Spark as a black box.",
        how="An action creates a job. Shuffle boundaries split the job into stages, and each stage launches one task per input partition.",
        internal="The driver asks a cluster manager for executors, builds a DAG, divides it at exchanges, and schedules tasks close to their input data when possible.",
        production="Engineers use the Spark UI to inspect jobs, stages, task skew, shuffle volume, executor loss, and memory pressure.",
        analogy="A job is a delivery order, stages are route segments separated by depots, and tasks are the individual vans serving partitions.",
        performance="Large shuffles, uneven partitions, and too many tiny tasks are common architectural performance signals.",
        compare="jobs, stages, and tasks", comparison_answer="An action starts a job; shuffle boundaries divide it into stages; tasks are the parallel units, usually one per partition in a stage.",
        functions=[
            ("explain", "Show logical and physical plans", "df.explain('formatted')", "Understand execution"),
            ("getNumPartitions", "Return partition count", "df.rdd.getNumPartitions()", "Estimate task parallelism"),
            ("count", "Count rows and trigger a job", "df.count()", "Demonstrate an action"),
            ("sparkContext.applicationId", "Identify the application", "spark.sparkContext.applicationId", "Spark UI and logs"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders",
        retail_requirement="trace how Spark filters completed orders and calculates their total value.",
        retail_code="""
completed_orders = retail_orders.filter("order_status = 'COMPLETE'")
completed_total = completed_orders.groupBy().sum("total_amount")

print("Input partitions:", retail_orders.rdd.getNumPartitions())
completed_total.explain("formatted")
completed_total.show()
""",
        approach="Build a filter and global aggregation, inspect the physical plan before the action, then call `show()` to trigger the job.",
        expected="The physical plan contains a filter plus aggregate/exchange steps; the completed-order total is **₹160,248.00**.",
        interpretation="Filtering can happen before the global exchange, reducing the data that must be combined for the final total.",
        bank_focus="identifying jobs, stages, and tasks in transaction processing",
        bank_tasks="Filter successful debit transactions and call `explain('formatted')`.|Predict how many jobs `show()` can trigger and verify in the Spark UI if available.|Count the input partitions.|Explain where a shuffle appears in a transaction-type aggregation.|State how many tasks a stage normally receives from ten partitions.|Identify the driver process in local mode.|Describe the cluster manager's role in a real cluster.|Run `count()` and label it as a transformation or action.|Draw a DAG for filter → groupBy → sum.|Record two Spark UI metrics useful for diagnosing a slow stage.",
        challenge="A transaction aggregation has one task running for 20 minutes while 199 tasks finish in seconds. Use architecture terms to explain the likely issue and the evidence you would inspect.",
        errors=[
            ("Calling every code line a job", "Transformations are lazy and only actions create jobs.", "Mark actions first, then inspect jobs and stages in the UI."),
            ("Equating partitions with executors", "An executor can process many partitions over time.", "Treat tasks as partition work and executors as worker processes."),
            ("Missing shuffle boundaries", "Wide transformations exchange data across executors.", "Look for `Exchange` nodes in the plan."),
            ("Assuming local mode equals a cluster", "Processes and resource allocation differ.", "Use local mode to learn APIs, but interpret production metrics in the real cluster."),
        ],
    ),
    dict(
        day=3, topic="DataFrame Basics",
        concepts=["DataFrame", "row", "column", "schema", "data type"],
        what="A Spark DataFrame is a distributed table with named columns and a schema that Spark can optimize.",
        why="Schemas make transformations safer and give Spark enough type information to plan efficient execution.",
        how="Spark stores a logical description of rows split into partitions; DataFrame operations build new immutable plans rather than changing data in place.",
        internal="Catalyst analyzes column names and types, optimizes the logical plan, and produces a physical plan executed over partitions.",
        production="Production ingestion usually declares a schema, validates required columns, and quarantines records that cannot satisfy the contract.",
        analogy="A DataFrame is a distributed spreadsheet whose column rules are written on a blueprint called the schema.",
        performance="Explicit schemas avoid repeated inference and prevent accidental string processing for numeric or date fields.",
        compare="DataFrames and Python collections", comparison_answer="A DataFrame is distributed, lazy, schema-aware, and optimized; Python lists are local, eager objects managed by the driver.",
        functions=[
            ("createDataFrame", "Create a DataFrame", "spark.createDataFrame(rows, schema)", "Tests and structured inputs"),
            ("printSchema", "Print the schema tree", "df.printSchema()", "Type inspection"),
            ("show", "Preview rows", "df.show(n, truncate=False)", "Data inspection"),
            ("columns", "List column names", "df.columns", "Schema validation"),
            ("dtypes", "List names and simple types", "df.dtypes", "Type checks"),
        ],
        retail_df="retail_products", retail_dataset="Retail products and orders",
        retail_requirement="create product and order DataFrames with explicit schemas and inspect their structure.",
        retail_code="""
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

product_schema_demo = StructType([
    StructField("product_id", StringType(), False),
    StructField("product_name", StringType(), False),
    StructField("category", StringType(), True),
    StructField("price", DoubleType(), True),
])

product_demo = spark.createDataFrame(
    [("PX1", "Demo Keyboard", "Electronics", 1999.0),
     ("PX2", "Demo Chair", "Furniture", 7499.0)],
    product_schema_demo,
)
product_demo.printSchema()
product_demo.show(truncate=False)
print("Columns:", product_demo.columns)
""",
        approach="Define a strict StructType, create rows that match it, then inspect schema and data separately.",
        expected="The schema shows non-null string IDs/names plus nullable category and double price; two demonstration products are displayed.",
        interpretation="The product contract is explicit, so later arithmetic on price and joins on product ID have predictable types.",
        bank_focus="creating accounts and transactions DataFrames with explicit schemas",
        bank_tasks="Declare an accounts schema with non-null `account_id`.|Create the accounts DataFrame from the supplied sample.|Declare a transactions schema including date and amount.|Create the transactions DataFrame.|Print both schemas.|Show three rows from each DataFrame.|List each DataFrame's columns.|Explain the row grain of both tables.|Identify primary and foreign key candidates.|Add assertions for required columns and expected types.",
        challenge="A transaction file suddenly sends `amount` as text and omits `transaction_type`. Design a schema-contract check and quarantine approach without silently changing valid records.",
        errors=[
            ("Row length does not match schema", "The tuple has too few or too many values.", "Align every row with the declared field order."),
            ("Wrong Python value type", "A value cannot be converted to the declared Spark type.", "Normalize input or choose the correct type before creation."),
            ("Nullable keys", "The schema permits missing business identifiers.", "Declare required keys non-nullable and validate them."),
            ("Confusing schema order", "Tuple values are positional.", "Prefer named `Row` objects or carefully documented schema order."),
        ],
    ),
    dict(
        day=4, topic="Reading Data",
        concepts=["CSV", "JSON", "Parquet", "schema inference", "read options"],
        what="Reading data converts files from a storage format into a DataFrame with columns, types, and partitions.",
        why="Every pipeline begins at a boundary; correct schemas, options, and bad-record handling prevent downstream corruption.",
        how="Spark lists input files, creates file partitions, parses records with the selected data source, and applies projection or filter pushdown where supported.",
        internal="Text formats require parsing; Parquet supplies schema and column metadata, allowing Spark to read only required columns and sometimes skip row groups.",
        production="Pipelines read immutable landing files, record ingestion metadata, validate counts and schema, and separate malformed records.",
        analogy="CSV is a labeled stack of plain paper, JSON is a flexible form, and Parquet is a cabinet organized by column.",
        performance="Prefer explicit schemas and columnar formats such as Parquet for repeated analytical reads.",
        compare="CSV, JSON, and Parquet", comparison_answer="CSV is simple but weakly typed, JSON handles nested data but is verbose, and Parquet is typed, compressed, and columnar for analytics.",
        functions=[
            ("spark.read.csv", "Read CSV", "spark.read.schema(s).option('header', True).csv(path)", "Delimited files"),
            ("spark.read.json", "Read JSON", "spark.read.schema(s).json(path)", "Nested or event data"),
            ("spark.read.parquet", "Read Parquet", "spark.read.parquet(path)", "Lake analytics"),
            ("option", "Set data-source option", "reader.option('mode', 'PERMISSIVE')", "Parser configuration"),
            ("schema", "Supply input schema", "reader.schema(my_schema)", "Stable production contracts"),
        ],
        retail_df="retail_orders", retail_dataset="Retail customers and orders files",
        retail_requirement="write classroom source files, then read customers from CSV and orders from Parquet with controlled schemas.",
        retail_code="""
from pathlib import Path

lab_root = str(Path.cwd() / "pyspark_course_data")
retail_customers.write.mode("overwrite").option("header", True).csv(f"{lab_root}/customers_csv")
retail_orders.write.mode("overwrite").parquet(f"{lab_root}/orders_parquet")
retail_products.write.mode("overwrite").json(f"{lab_root}/products_json")

customers_from_csv = (spark.read
    .schema(retail_customers.schema)
    .option("header", True)
    .csv(f"{lab_root}/customers_csv"))
orders_from_parquet = spark.read.parquet(f"{lab_root}/orders_parquet")

customers_from_csv.show(3, truncate=False)
orders_from_parquet.printSchema()
""",
        approach="Create reproducible local source folders, use the known customer schema for CSV, and allow Parquet to supply its stored schema.",
        expected="Three customer rows display correctly; the Parquet schema preserves date and double types from `retail_orders`.",
        interpretation="The pipeline has a reproducible raw input boundary and avoids expensive or unstable CSV type inference.",
        bank_focus="reading banking customers and accounts from governed file paths",
        bank_tasks="Write banking customers to a classroom CSV folder.|Read them back with the declared schema.|Write accounts to Parquet.|Read only account ID, type, and balance from Parquet.|Write three transactions as JSON and read them back.|Compare inferred CSV types with declared types.|Use a wrong delimiter once and diagnose the resulting schema.|Create a corrupt record and describe the chosen parse mode.|Validate file row counts against the in-memory samples.|Recommend a production format for repeated bank analytics and justify it.",
        challenge="A daily bank landing zone contains late files, duplicated files, and one malformed CSV. Design an idempotent ingestion contract with file-level audit columns and quarantine behavior.",
        errors=[
            ("All CSV columns become strings", "No schema was supplied or inference was disabled.", "Declare the production schema explicitly."),
            ("Header becomes a data row", "The header option was omitted or wrong.", "Set `header=True` and verify the first record."),
            ("Path not found", "The driver resolves a different or misspelled storage path.", "Print the configured path and validate storage permissions."),
            ("Many tiny input files", "Each small file adds listing and task overhead.", "Compact upstream or periodically optimize file layout."),
        ],
    ),
    dict(
        day=5, topic="Selecting Columns",
        concepts=["select", "alias", "column expressions", "projection"],
        what="Column selection chooses the fields and expressions that belong in the next DataFrame.",
        why="Narrow schemas improve readability, reduce data movement, and create clear contracts between pipeline steps.",
        how="`select` builds a projection containing existing columns or expressions; `alias` names derived outputs without changing the source DataFrame.",
        internal="Catalyst can prune unused columns so columnar readers and later operators handle less data.",
        production="Silver and Gold tables select, rename, cast, and order only the fields required by downstream consumers.",
        analogy="Selecting columns is packing only the tools needed for a job instead of carrying the whole workshop.",
        performance="Project columns early, especially when reading wide Parquet or Delta tables.",
        compare="column names and Column expressions", comparison_answer="A string names an existing field; a Column expression can calculate, cast, rename, or combine values in the execution plan.",
        functions=[
            ("select", "Project columns or expressions", "df.select('a', F.col('b'))", "Choose output schema"),
            ("col", "Reference a column", "F.col('price')", "Build expressions"),
            ("alias", "Rename an output expression", "F.col('price').alias('unit_price')", "Business names"),
            ("expr", "Use a SQL expression", "F.expr('price * 0.9')", "Concise calculations"),
            ("selectExpr", "Select with SQL strings", "df.selectExpr('price * 0.9 AS sale_price')", "SQL-style projection"),
        ],
        retail_df="retail_products", retail_dataset="Retail products",
        retail_requirement="show a product catalogue containing product name, category, list price, and price including 18% tax.",
        retail_code="""
from pyspark.sql import functions as F

product_catalogue = retail_products.select(
    F.col("product_id"),
    F.col("product_name").alias("item_name"),
    "category",
    F.col("price").alias("list_price"),
    F.round(F.col("price") * F.lit(1.18), 2).alias("price_with_tax"),
)
product_catalogue.show(12, truncate=False)
""",
        approach="Reference only required columns, give presentation-friendly aliases, and calculate tax as a Column expression.",
        expected="The result has five columns; for `Laptop Pro`, list price is ₹65,000 and price with tax is **₹76,700**.",
        interpretation="Consumers receive a narrow catalogue with clear names and a reproducible tax calculation.",
        bank_focus="selecting account ID, account type, balance, and a derived available-view field",
        bank_tasks="Select account ID, account type, and balance.|Alias `balance` as `current_balance`.|Add a literal currency column with value `INR`.|Create `balance_in_thousands` rounded to two decimals.|Use `selectExpr` to reproduce the calculation.|Return customer ID without exposing customer name.|Arrange output columns in a documented order.|Select transaction amount as `transaction_amount`.|Compare the schemas before and after projection.|Explain why early projection matters for a wide account table.",
        challenge="Create a privacy-safe account extract for analytics that keeps join keys and financial measures but excludes direct customer identifiers and unnecessary operational columns.",
        errors=[
            ("Selecting a missing column", "The name is misspelled or removed earlier.", "Check `df.columns` and use analyzed errors to find the first bad step."),
            ("Using a Python value without `lit`", "Spark expects a Column expression in many APIs.", "Wrap constants with `F.lit` when needed."),
            ("Overwriting meaning with a poor alias", "The new name hides unit or calculation semantics.", "Use business names that include units or meaning."),
            ("Keeping every column", "Wide rows increase I/O and make contracts unclear.", "Select only required fields near the source."),
        ],
    ),
    dict(
        day=6, topic="Filtering Data",
        concepts=["filter", "where", "boolean conditions", "operator precedence"],
        what="Filtering keeps only rows whose condition evaluates to true.",
        why="Most business rules target a relevant subset, such as completed high-value orders or successful debits.",
        how="PySpark builds boolean Column expressions with comparisons, `&`, `|`, `~`, `isin`, and null checks; `filter` and `where` are aliases.",
        internal="Filters are added to the logical plan and may be pushed into Parquet or Delta scans, reducing rows read or processed.",
        production="Pipelines filter by processing date, valid status, geography, consent, and incremental-watermark ranges.",
        analogy="A filter is a security gate: every row must satisfy the written entry rule.",
        performance="Filter early with selective predicates and inspect plans for pushdown, while preserving required reconciliation data.",
        compare="filter and where", comparison_answer="They are API aliases in PySpark; teams choose the spelling that reads best with DataFrame or SQL-style code.",
        functions=[
            ("filter", "Keep matching rows", "df.filter(F.col('amount') > 1000)", "Business subsets"),
            ("where", "Alias for filter", "df.where('status = \'OK\'')", "SQL-style conditions"),
            ("isin", "Match a value set", "F.col('status').isin('A', 'B')", "Status lists"),
            ("between", "Inclusive range", "F.col('amount').between(100, 500)", "Range rules"),
            ("isNull", "Test missing value", "F.col('x').isNull()", "Data quality"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders",
        retail_requirement="find completed retail orders worth at least ₹10,000 placed from 1 February 2026 onward.",
        retail_code="""
high_value_orders = (retail_orders
    .filter(
        (F.col("order_status") == "COMPLETE") &
        (F.col("total_amount") >= 10000) &
        (F.col("order_date") >= F.lit("2026-02-01").cast("date"))
    )
    .select("order_id", "customer_id", "order_date", "total_amount"))

high_value_orders.orderBy("order_id").show(truncate=False)
""",
        approach="Combine three parenthesized Column conditions, then project only review fields and order the small display.",
        expected="Orders **O1007, O1008, O1011, and O1013** qualify; their amounts are ₹12,499, ₹18,500, ₹12,999.50, and ₹65,000.",
        interpretation="Management can focus on recent, completed, high-value sales without mixing cancelled or pending orders.",
        bank_focus="finding successful high-value banking transactions above a configurable threshold",
        bank_tasks="Filter transactions above ₹50,000.|Keep only successful transactions.|Return only debit transactions.|Find credits between ₹10,000 and ₹75,000.|Filter two transaction types with `isin`.|Find transactions on or after 1 February 2026.|Combine date, type, status, and amount conditions.|Write the same rule once with `filter` and once with `where`.|Count rejected rows separately for reconciliation.|Parameterize the threshold in one variable.",
        challenge="Fraud analysts need successful debit transactions above ₹75,000 made during a seven-day review window, excluding approved corporate accounts. Write the row-level filtering design and reconciliation totals.",
        errors=[
            ("Using `and` or `or`", "Python tries to reduce a distributed Column to one boolean.", "Use `&` or `|` with parenthesized expressions."),
            ("Missing parentheses", "Python operator precedence changes the expression.", "Wrap every comparison before combining conditions."),
            ("Comparing incompatible types", "A date or amount is still a string.", "Cast deliberately and inspect the schema."),
            ("Dropping rejected rows silently", "Filtered-out data is not reconciled.", "Count or quarantine rejected records as part of pipeline metrics."),
        ],
    ),
    dict(
        day=7, topic="Column Transformations",
        concepts=["withColumn", "cast", "when", "otherwise", "derived columns"],
        what="Column transformations create or replace fields using expressions while keeping the DataFrame immutable.",
        why="Raw values rarely match business meaning; pipelines standardize types, derive measures, and classify records.",
        how="`withColumn` attaches a named expression. `cast` changes type, and chained `when` clauses implement ordered conditional logic.",
        internal="Expressions remain inside Spark's optimized plan and are evaluated on executors, avoiding Python row-by-row loops.",
        production="Silver layers standardize data types and statuses; Gold layers add governed measures and dimensions.",
        analogy="A transformation is an assembly-line station that adds a label or reshapes one part without changing the original shipment.",
        performance="Prefer built-in Column expressions; collapse clear transformations and avoid repeated expensive expressions.",
        compare="withColumn and select", comparison_answer="`withColumn` is convenient for adding or replacing fields; `select` makes the entire output schema explicit and can be clearer for many columns.",
        functions=[
            ("withColumn", "Add or replace a column", "df.withColumn('x', expression)", "Derived fields"),
            ("cast", "Convert data type", "F.col('x').cast('double')", "Type standardization"),
            ("when", "Start conditional expression", "F.when(condition, value)", "Classification"),
            ("otherwise", "Set fallback value", "expr.otherwise(value)", "Complete conditions"),
            ("round", "Round numeric output", "F.round('amount', 2)", "Financial presentation"),
        ],
        retail_df="retail_products", retail_dataset="Retail products",
        retail_requirement="calculate a 10% promotional price and classify products into budget, standard, and premium price bands.",
        retail_code="""
enriched_products = (retail_products
    .withColumn("promo_price", F.round(F.col("price") * F.lit(0.90), 2))
    .withColumn(
        "price_band",
        F.when(F.col("price") < 1000, "BUDGET")
         .when(F.col("price") < 10000, "STANDARD")
         .otherwise("PREMIUM")
    ))

enriched_products.select(
    "product_id", "product_name", "price", "promo_price", "price_band"
).orderBy("product_id").show(12, truncate=False)
""",
        approach="Calculate price with a built-in expression, then evaluate price-band conditions from narrowest threshold to final fallback.",
        expected="`P001 Laptop Pro` has promo price **₹58,500** and band **PREMIUM**; `P012 Coffee Pack` is **BUDGET**.",
        interpretation="Merchandising receives consistent promotion values and segments that can drive catalogue campaigns.",
        bank_focus="categorizing customers or accounts by balance with explicit numeric types",
        bank_tasks="Cast account balance to double in a demo copy.|Create `balance_band` for negative, low, medium, and high balances.|Create an `is_overdrawn` boolean.|Round balances to two decimals.|Add a literal currency code.|Replace the original balance only after comparing results.|Classify loan interest rates into three bands.|Use `otherwise` for unexpected values.|Count records in each balance band using only concepts learned so far where possible.|Document boundary behavior for exactly ₹10,000 and ₹100,000.",
        challenge="Create an account health classification using balance and account type. The rules overlap; document priority so every account receives exactly one label.",
        errors=[
            ("Forgetting `otherwise`", "Unmatched rows become null.", "Provide an explicit fallback or intentionally validate null outcomes."),
            ("Incorrect condition order", "A broad earlier rule captures rows before a specific rule.", "Order rules from specific/high priority to general."),
            ("Accidental type loss", "A cast fails and produces null values.", "Compare null counts before and after casting."),
            ("Long withColumn chains", "Repeated plan growth becomes hard to read.", "Use a clear `select` for many independent derived fields."),
        ],
    ),
    dict(
        day=8, topic="String Functions",
        concepts=["trim", "upper", "lower", "concat", "substring", "split"],
        what="String functions clean, standardize, parse, and combine text columns using Spark-native expressions.",
        why="Whitespace, casing, embedded codes, and inconsistent identifiers cause failed joins and misleading groups.",
        how="Built-in string functions operate on each row inside executors and return new Columns without moving data to Python.",
        internal="Catalyst represents string functions as JVM expressions and can optimize them together with projections and filters.",
        production="Teams normalize keys, parse source codes, create display labels, and validate identifier patterns in Silver data.",
        analogy="String cleaning is preparing mailing labels: trim edges, standardize capitalization, and separate address parts.",
        performance="Use built-in functions instead of Python UDFs and avoid regex when simpler functions are sufficient.",
        compare="split and substring", comparison_answer="`split` uses a delimiter or regex to make an array; `substring` extracts characters from fixed positions.",
        functions=[
            ("trim", "Remove surrounding spaces", "F.trim('name')", "Clean text"),
            ("upper", "Convert to uppercase", "F.upper('code')", "Canonical codes"),
            ("lower", "Convert to lowercase", "F.lower('email')", "Case normalization"),
            ("concat_ws", "Join values with separator", "F.concat_ws(' - ', 'id', 'name')", "Labels"),
            ("substring", "Extract character range", "F.substring('id', 1, 3)", "Fixed-format codes"),
            ("split", "Split text to array", "F.split('value', '-')", "Delimited identifiers"),
        ],
        retail_df="retail_customers", retail_dataset="Retail customers and products",
        retail_requirement="clean padded customer names and build standardized product labels.",
        retail_code="""
dirty_customers = retail_customers.withColumn(
    "customer_name", F.concat(F.lit("  "), F.col("customer_name"), F.lit(" "))
)

clean_customers = dirty_customers.select(
    "customer_id",
    F.upper(F.trim("customer_name")).alias("customer_name_clean"),
    F.concat_ws("-", F.upper("state"), F.substring("customer_id", 2, 3)).alias("customer_label"),
)
clean_customers.show(5, truncate=False)
""",
        approach="Create a controlled dirty input, trim before uppercasing, and combine normalized state with an ID fragment.",
        expected="`C001 / Aarav Sharma / KA` becomes name **AARAV SHARMA** and label **KA-001**.",
        interpretation="Consistent text improves matching, grouping, exports, and downstream customer search.",
        bank_focus="cleaning banking customer names and parsing structured account identifiers",
        bank_tasks="Trim banking customer names.|Create an uppercase customer type.|Create a lowercase display version of city.|Build `customer_id - customer_name` labels.|Extract the numeric part of customer IDs.|Split a demo branch code such as `KA-BLR-001`.|Standardize account types to uppercase.|Find names whose cleaned length is under three characters.|Compare distinct counts before and after normalization.|Define rules that prevent accidental changes to case-sensitive identifiers.",
        challenge="Two bank systems represent names and branch codes differently. Create a canonical matching key while retaining original fields and explain collision risks.",
        errors=[
            ("Joining dirty strings", "Spaces or case differences prevent equality.", "Create and validate canonical keys before the join."),
            ("Wrong substring position", "Spark substring positions start at 1.", "Test boundary cases with short sample strings."),
            ("Regex overuse", "Complex expressions are slower and harder to maintain.", "Use trim, split, replace, or substring when possible."),
            ("Destroying original text", "Cleaning overwrites audit evidence.", "Retain raw and cleaned columns through the quality layer."),
        ],
    ),
    dict(
        day=9, topic="Date Functions",
        concepts=["date types", "current_date", "datediff", "date_add", "months_between", "year", "month"],
        what="Date functions represent calendar values with real date types and derive periods, ages, and relative dates.",
        why="Business reporting depends on correct day and month boundaries; strings cannot safely provide calendar arithmetic.",
        how="Spark parses strings with an explicit pattern and applies calendar-aware expressions such as difference, addition, and extraction.",
        internal="Typed date values are stored compactly and evaluated by Spark expressions; partition filters can be pushed down when types align.",
        production="Incremental loads, retention rules, month-end reports, and service-level checks all depend on governed timestamps and time zones.",
        analogy="A date type is a real calendar; a date string is only a label that may or may not follow the calendar's rules.",
        performance="Filter typed partition columns with typed literals and avoid wrapping them unnecessarily in functions during pruning.",
        compare="date and timestamp", comparison_answer="A date stores a calendar day; a timestamp stores an instant or local date-time and requires explicit timezone handling.",
        functions=[
            ("to_date", "Parse or cast to date", "F.to_date('text', 'yyyy-MM-dd')", "Input standardization"),
            ("current_date", "Current session date", "F.current_date()", "Age and SLA logic"),
            ("datediff", "Difference in days", "F.datediff('end', 'start')", "Elapsed days"),
            ("date_add", "Add calendar days", "F.date_add('date', 7)", "Due dates"),
            ("months_between", "Fractional months", "F.months_between('end', 'start')", "Tenure"),
            ("year / month", "Extract period", "F.year('date')", "Reporting dimensions"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders",
        retail_requirement="summarize orders by year and month and calculate days from order to a fixed classroom review date.",
        retail_code="""
review_date = F.lit("2026-03-01").cast("date")

dated_orders = retail_orders.select(
    "order_id", "order_date", "total_amount",
    F.year("order_date").alias("order_year"),
    F.month("order_date").alias("order_month"),
    F.datediff(review_date, F.col("order_date")).alias("days_to_review"),
    F.date_add("order_date", 7).alias("follow_up_date"),
)
dated_orders.orderBy("order_date").show(15, truncate=False)
""",
        approach="Use a fixed review date for reproducible output, extract reporting periods, and calculate elapsed and follow-up days.",
        expected="Order `O1001` on 2026-01-03 has review age **57 days** and follow-up date **2026-01-10**.",
        interpretation="Retail teams can create stable monthly partitions, age orders, and schedule follow-up activities.",
        bank_focus="analyzing banking transactions by month and computing account/customer tenure",
        bank_tasks="Extract transaction year and month.|Create a `yyyy-MM` reporting label.|Calculate days from transaction to 1 March 2026.|Add seven days to create a review deadline.|Calculate customer tenure in months.|Filter February 2026 transactions.|Identify transactions older than 30 days at the fixed review date.|Explain date versus timestamp for ATM events.|Create a month-start column.|Validate that every transaction date is on or after account opening in a joined production design.",
        challenge="Design a timezone-safe daily transaction report for events produced in multiple countries, including the business date used for branch reporting.",
        errors=[
            ("Date remains a string", "Parsing or casting was skipped.", "Use `to_date` with an explicit expected pattern."),
            ("Wrong parsing pattern", "`dd-MM` and `MM-dd` are confused.", "Document source formats and quarantine invalid parses."),
            ("Using current date in tests", "Expected output changes each day.", "Inject a fixed as-of date for reproducible tests."),
            ("Ignoring time zones", "Timestamp boundaries move across regions.", "Set session timezone and define the business timezone explicitly."),
        ],
    ),
    dict(
        day=10, topic="Aggregations",
        concepts=["count", "sum", "average", "minimum", "maximum", "global aggregation"],
        what="An aggregation reduces many input rows to summary measures such as count, total, average, minimum, or maximum.",
        why="KPIs and reconciliation controls summarize detailed events into information that people and systems can compare.",
        how="Aggregate functions collect partial results inside partitions, shuffle or merge them, and produce final values.",
        internal="Spark commonly uses partial and final aggregate operators so each executor reduces data before network transfer.",
        production="Pipelines calculate file counts, financial totals, data-quality metrics, and dashboard measures at declared grains.",
        analogy="Instead of carrying every receipt to head office, each store totals its receipts and sends one subtotal for final addition.",
        performance="Use mergeable built-in aggregates, avoid unnecessary distinct counts, and keep the result grain explicit.",
        compare="count, countDistinct, and approximate distinct", comparison_answer="`count` counts rows or non-null values, `countDistinct` gives exact unique counts with shuffle cost, and approximate methods trade small error for scale.",
        functions=[
            ("count", "Count rows/non-null values", "F.count('*')", "Volume KPI"),
            ("sum", "Add numeric values", "F.sum('amount')", "Revenue"),
            ("avg", "Arithmetic mean", "F.avg('amount')", "Average order value"),
            ("min", "Smallest value", "F.min('amount')", "Range check"),
            ("max", "Largest value", "F.max('amount')", "Peak transaction"),
            ("agg", "Calculate several aggregates", "df.agg(F.sum('x'), F.avg('x'))", "One summary row"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders",
        retail_requirement="calculate completed-order count, revenue, average order value, minimum, and maximum order values.",
        retail_code="""
order_kpis = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .agg(
        F.count("*").alias("completed_orders"),
        F.round(F.sum("total_amount"), 2).alias("total_revenue"),
        F.round(F.avg("total_amount"), 2).alias("average_order_value"),
        F.min("total_amount").alias("minimum_order_value"),
        F.max("total_amount").alias("maximum_order_value"),
    ))
order_kpis.show(truncate=False)
""",
        approach="Filter the correct business population first, then compute five named measures in one aggregation.",
        expected="There are **13** completed orders, total revenue **₹160,248.00**, average **₹12,326.77**, minimum **₹1,000**, and maximum **₹65,000**.",
        interpretation="The KPI row reconciles completed business only; cancelled and pending demand remain outside recognized revenue.",
        bank_focus="calculating transaction totals and averages by the intended status population",
        bank_tasks="Count all transaction rows.|Count successful transaction rows.|Sum successful transaction amount.|Calculate average successful debit amount.|Find minimum and maximum credit amounts.|Count distinct accounts with activity.|Explain null behavior in `count(column)`.|Create one KPI row with five measures.|Reconcile successful plus failed counts to total count.|Document whether amounts are signed or separated by transaction type.",
        challenge="Create auditable daily control totals for a payment file: record count, amount total, unique accounts, rejected count, and min/max event time, with a stated status population.",
        errors=[
            ("Aggregating the wrong population", "Status or date filters were omitted.", "Define the KPI population before writing expressions."),
            ("Using floating point blindly", "Binary doubles can introduce financial rounding artifacts.", "Use appropriate decimal types for production money."),
            ("Misreading count(column)", "Null values in that column are skipped.", "Use `count('*')` for row count and name both metrics clearly."),
            ("Losing the business grain", "A global total is compared with grouped totals.", "Document one row per what for every result."),
        ],
    ),
    dict(
        day=11, topic="GroupBy and Multiple Aggregations",
        concepts=["groupBy", "grouping key", "multiple aggregates", "result grain"],
        what="Grouped aggregation creates one summary row for each unique combination of grouping keys.",
        why="Businesses need KPIs by store, category, branch, month, customer segment, and other dimensions.",
        how="Rows with the same key are brought together logically; Spark calculates partial summaries and shuffles by key for final aggregation.",
        internal="A hash or sort aggregate usually surrounds an exchange partitioned by the grouping columns.",
        production="Gold tables define stable dimensions and measures, then test uniqueness at the declared grain.",
        analogy="Receipts are sorted into labeled baskets by store and category before each basket is counted and totaled.",
        performance="Choose low-to-moderate-cardinality grouping keys, handle skew, and avoid grouping by unnecessary high-cardinality text.",
        compare="global and grouped aggregation", comparison_answer="A global aggregation returns one summary row; grouped aggregation returns one row per distinct key combination.",
        functions=[
            ("groupBy", "Define grouping keys", "df.groupBy('store_id')", "Dimensional KPIs"),
            ("agg", "Apply named measures", "grouped.agg(F.sum('amount'))", "Multiple KPIs"),
            ("countDistinct", "Exact unique count", "F.countDistinct('order_id')", "Unique orders"),
            ("orderBy", "Sort final presentation", "df.orderBy(F.desc('revenue'))", "Ranked report display"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders by store",
        retail_requirement="calculate completed-order revenue, order count, and average order value for each store.",
        retail_code="""
store_sales = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .groupBy("store_id")
    .agg(
        F.countDistinct("order_id").alias("order_count"),
        F.round(F.sum("total_amount"), 2).alias("revenue"),
        F.round(F.avg("total_amount"), 2).alias("avg_order_value"),
    )
    .orderBy(F.desc("revenue")))
store_sales.show(truncate=False)
""",
        approach="Filter recognized sales, group at one row per store, calculate three measures, and sort only for presentation.",
        expected="Store `S001` leads with revenue **₹100,648.50** from 5 completed orders; `S002` follows with **₹41,499.50**.",
        interpretation="Store managers can compare both volume and value; revenue alone would hide different order patterns.",
        bank_focus="summarizing transaction count and amount by branch and transaction type",
        bank_tasks="Join-free warm-up: group transactions by transaction type.|Calculate count, sum, and average amount by type.|Group accounts by branch and account type.|Calculate total and average balance by branch.|Use two grouping columns.|Order groups by total amount descending.|Add a distinct-account measure.|Reconcile grouped totals to the global total.|State the row grain in a markdown cell.|Identify a grouping key likely to cause high cardinality.",
        challenge="Create a branch control report with account counts and balances, then describe how transaction facts would later be integrated without double-counting account balances.",
        errors=[
            ("Selecting ungrouped detail columns", "They are neither grouping keys nor aggregates.", "Add them to the group only if they belong to the intended grain."),
            ("Grouping by too many columns", "The result approaches detail-level cardinality.", "Define the business grain first."),
            ("Double-counting after a later join", "A one-to-many relationship repeats measures.", "Aggregate each fact at compatible grain before joining."),
            ("Sorting huge intermediate data", "Global order requires expensive movement.", "Sort only final bounded results when required."),
        ],
    ),
    dict(
        day=12, topic="Joins",
        concepts=["inner join", "left join", "right join", "full join", "semi join", "anti join"],
        what="A join combines rows from two DataFrames by matching key expressions.",
        why="Business facts and dimensions live in separate tables; joins integrate customers, orders, products, stores, and accounts.",
        how="Spark matches keys using a physical strategy such as broadcast hash, shuffled hash, or sort-merge join, while join type controls unmatched rows.",
        internal="Large joins usually exchange both sides by key; small-side broadcast can avoid that shuffle. Catalyst selects a strategy from statistics and hints.",
        production="Engineers validate key uniqueness and relationship cardinality before joining, then reconcile row counts and unmatched keys.",
        analogy="A join is matching claim tickets: the join type decides whether unmatched people, unmatched items, or both remain in the report.",
        performance="Project and filter early, broadcast genuinely small dimensions, and measure key skew and match rates.",
        compare="inner, left, semi, and anti joins", comparison_answer="Inner keeps matches, left keeps every left row, semi keeps left rows that have a match without right columns, and anti keeps left rows with no match.",
        functions=[
            ("join", "Combine DataFrames", "left.join(right, 'key', 'left')", "Fact-dimension integration"),
            ("alias", "Qualify DataFrames", "df.alias('o')", "Resolve ambiguous columns"),
            ("left_semi", "Keep left matches", "df.join(dim, key, 'left_semi')", "Existence filter"),
            ("left_anti", "Keep left non-matches", "df.join(dim, key, 'left_anti')", "Data-quality exceptions"),
        ],
        retail_df="retail_orders", retail_dataset="Retail customers, orders, and stores",
        retail_requirement="produce completed-order details with customer and store names, while preserving and reporting unmatched keys.",
        retail_code="""
order_details = (retail_orders.alias("o")
    .filter(F.col("o.order_status") == "COMPLETE")
    .join(retail_customers.alias("c"), F.col("o.customer_id") == F.col("c.customer_id"), "left")
    .join(retail_stores.alias("s"), F.col("o.store_id") == F.col("s.store_id"), "left")
    .select(
        F.col("o.order_id"), F.col("o.order_date"),
        F.col("c.customer_name"), F.col("s.store_name"),
        F.col("o.total_amount"),
    ))

order_details.orderBy("order_id").show(20, truncate=False)

unmatched_customers = retail_orders.join(retail_customers, "customer_id", "left_anti")
print("Orders with unknown customer:", unmatched_customers.count())
""",
        approach="Filter the fact first, left-join two dimensions on qualified keys, select a narrow schema, and audit unmatched customers with an anti join.",
        expected="All 13 completed orders receive names; the unmatched-customer audit count is **0**.",
        interpretation="The integrated result is human-readable, while the anti-join control protects against silently losing invalid foreign keys.",
        bank_focus="joining customers to accounts and integrating branches without duplicating account balances",
        bank_tasks="Inner-join customers with accounts.|Left-join customers with accounts and find customers without accounts.|Join accounts to branches.|Select qualified columns after a three-table join.|Count accounts before and after dimension joins.|Use a left-semi join to find customers with loans.|Use a left-anti join to find customers without loans.|Explain why joining transactions changes account row counts.|Check customer-key uniqueness before joining.|Produce a match-rate metric for branch IDs.",
        challenge="Build a customer-account-branch view and a separate unmatched-key exception table. State relationship cardinalities and prove balances are not double-counted.",
        errors=[
            ("Ambiguous column error", "Both sides contain the same non-key name.", "Alias DataFrames and select qualified columns."),
            ("Unexpected row multiplication", "The key is duplicated on one or both sides.", "Profile key uniqueness and declare join cardinality."),
            ("Lost unmatched records", "An inner join was used without business approval.", "Choose join type from requirements and audit anti-join rows."),
            ("Null join keys do not match", "Standard equality does not match nulls.", "Validate or intentionally use null-safe equality where appropriate."),
        ],
    ),
    dict(
        day=13, topic="Union and Data Combination",
        concepts=["union", "unionByName", "schema alignment", "distinct", "deduplication"],
        what="A union stacks rows from compatible DataFrames into one result.",
        why="Pipelines combine channels, regions, daily batches, or source systems before common processing.",
        how="`union` aligns columns by position; `unionByName` aligns by name and can fill missing columns when explicitly allowed.",
        internal="Union is usually narrow because partitions are concatenated; a following `distinct` requires a wide shuffle to find duplicates.",
        production="Bronze tables append source batches with lineage columns, and controlled deduplication uses documented business keys.",
        analogy="Union is stacking two decks of cards; they must use the same fields, and duplicate removal means comparing the entire stack.",
        performance="Prefer `unionByName`, align types deliberately, and avoid full-row distinct when a business-key strategy is available.",
        compare="union and unionByName", comparison_answer="`union` matches by position and can silently misplace values; `unionByName` matches names and is safer for evolving schemas.",
        functions=[
            ("union", "Stack by position", "df1.union(df2)", "Identical schemas"),
            ("unionByName", "Stack by column name", "df1.unionByName(df2)", "Safer batch combination"),
            ("distinct", "Remove duplicate rows", "df.distinct()", "Exact full-row deduplication"),
            ("dropDuplicates", "Deduplicate by keys", "df.dropDuplicates(['order_id'])", "Business-key cleanup"),
        ],
        retail_df="retail_orders", retail_dataset="Online and store retail orders",
        retail_requirement="combine online and offline order feeds safely and remove an intentionally duplicated order by business key.",
        retail_code="""
online_orders = (retail_orders
    .filter(F.col("store_id") == "S004")
    .withColumn("sales_channel", F.lit("ONLINE")))
offline_orders = (retail_orders
    .filter(F.col("store_id") != "S004")
    .withColumn("sales_channel", F.lit("STORE"))
    .select("sales_channel", *retail_orders.columns))  # deliberately different order

combined_orders = (online_orders
    .unionByName(offline_orders)
    .unionByName(online_orders.filter(F.col("order_id") == "O1003"))
    .dropDuplicates(["order_id"]))

print("Combined unique orders:", combined_orders.count())
combined_orders.groupBy("sales_channel").count().show()
""",
        approach="Add a lineage column, intentionally vary column order, combine by name, inject a duplicate, then deduplicate by order ID.",
        expected="The final result has **15 unique orders**: 3 online and 12 store orders.",
        interpretation="Channel feeds can evolve in column order without corrupting values, and replayed order IDs do not duplicate the table.",
        bank_focus="combining NEFT and UPI transaction feeds with lineage and business-key deduplication",
        bank_tasks="Split supplied transactions into two type-based feeds.|Add a `source_system` column to both feeds.|Reorder one feed's columns.|Combine feeds with `unionByName`.|Explain why positional `union` is risky.|Add one replayed transaction record.|Remove duplicates by transaction ID.|Compare row counts before and after deduplication.|Create a schema-difference check before union.|State how you would handle a new optional source column.",
        challenge="Three payment feeds arrive with evolving schemas and occasional replayed files. Design schema alignment, lineage, and deterministic deduplication rules.",
        errors=[
            ("Values appear under wrong columns", "Positional union used different column order.", "Use `unionByName` and validate schemas."),
            ("Union type mismatch", "Same-name columns have incompatible types.", "Cast to a canonical contract before combining."),
            ("Distinct is unexpectedly expensive", "It shuffles and compares full rows.", "Deduplicate on documented keys with deterministic rules."),
            ("Legitimate repeats removed", "The chosen key was too broad.", "Define event identity with business owners."),
        ],
    ),
    dict(
        day=14, topic="Null Handling",
        concepts=["null", "isNull", "fillna", "dropna", "replace", "three-valued logic"],
        what="Null represents an unknown or missing value, not zero, blank text, or false.",
        why="Missing values affect comparisons, aggregates, joins, and business decisions, so each column needs an explicit policy.",
        how="Spark uses SQL three-valued logic. Functions can detect, fill, drop, or replace values, but the correct action depends on business meaning.",
        internal="Nullability is part of the schema; Spark expressions propagate nulls unless a function or condition defines another outcome.",
        production="Data-quality rules classify missing fields as reject, default, impute, preserve, or escalate, with metrics by source and date.",
        analogy="Null is an unanswered question, while zero is a clear answer; replacing every unanswered question with zero changes the story.",
        performance="Apply targeted column policies and avoid repeated full scans solely for ad hoc null counts.",
        compare="null, blank, and zero", comparison_answer="Null means unknown, blank is a known empty string, and zero is a numeric value; they require different business treatment.",
        functions=[
            ("isNull / isNotNull", "Test null state", "F.col('x').isNull()", "Quality rules"),
            ("fillna", "Fill null values", "df.fillna({'city': 'UNKNOWN'})", "Approved defaults"),
            ("dropna", "Drop rows with nulls", "df.dropna(subset=['id'])", "Reject invalid keys"),
            ("replace", "Replace known values", "df.replace('N/A', None, ['city'])", "Sentinel cleanup"),
            ("coalesce", "First non-null expression", "F.coalesce('a', 'b')", "Fallback logic"),
        ],
        retail_df="retail_products", retail_dataset="Retail products with controlled missing values",
        retail_requirement="standardize missing category values, reject rows without product IDs, and preserve an auditable quality flag.",
        retail_code="""
quality_input = spark.createDataFrame([
    ("P900", "Sample Cable", None, 399.0),
    (None, "Unknown Item", "N/A", 100.0),
    ("P901", None, "Accessories", None),
], ["product_id", "product_name", "category", "price"])

standardized = (quality_input
    .replace("N/A", None, subset=["category"])
    .withColumn("had_missing_value",
                F.col("product_name").isNull() | F.col("category").isNull() | F.col("price").isNull())
    .fillna({"product_name": "UNKNOWN PRODUCT", "category": "UNCATEGORIZED"})
    .dropna(subset=["product_id"]))

standardized.show(truncate=False)
""",
        approach="Convert a sentinel to real null, flag quality before filling, apply approved text defaults, and reject missing keys.",
        expected="Two rows remain (`P900`, `P901`); both keep `had_missing_value=true`, and the row with missing product ID is rejected.",
        interpretation="The curated table is usable without pretending that missing source values were originally known.",
        bank_focus="handling missing account and transaction values under financial data-quality policies",
        bank_tasks="Count nulls in each account column.|Replace blank account types with null.|Reject rows missing account ID.|Do not replace missing financial amounts with zero; explain why.|Fill missing branch ID only if an approved `UNKNOWN` member exists.|Create a missing-value flag before filling.|Use `coalesce` for preferred and fallback city.|Compare `count('*')` with `count('amount')`.|Create accepted and rejected DataFrames.|Report null rates as data-quality metrics.",
        challenge="Design null policies for account ID, branch ID, transaction amount, customer city, and loan interest rate, including which records are rejected versus preserved.",
        errors=[
            ("Using `== None`", "SQL null comparison does not behave like Python equality.", "Use `isNull` or `isNotNull`."),
            ("Filling every numeric null with zero", "Unknown money becomes a real amount.", "Use a field-specific business policy."),
            ("Dropping rows without metrics", "Data loss becomes invisible.", "Split accepted/rejected data and report counts."),
            ("Losing the original quality state", "Filling removes evidence of missingness.", "Create flags or retain raw fields before remediation."),
        ],
    ),
    dict(
        day=15, topic="Window Functions",
        concepts=["Window specification", "partitionBy", "orderBy", "row_number", "rank", "dense_rank"],
        what="A window function calculates across related rows while keeping each row in the result.",
        why="Ranking, top-N, running context, and within-group comparisons cannot be expressed by ordinary groupBy without losing detail.",
        how="A Window specification defines the group and order; ranking functions assign positions according to tie behavior.",
        internal="Spark exchanges rows by window partition and sorts within each partition before evaluating window expressions.",
        production="Gold analytics use windows for top products, latest records, customer sequences, deduplication, and percentile analysis.",
        analogy="A race awards places within each age group while keeping every runner's row visible.",
        performance="Partition on meaningful keys, limit window width, avoid single global partitions, and reduce rows before expensive sorts.",
        compare="row_number, rank, and dense_rank", comparison_answer="`row_number` is always unique, `rank` leaves gaps after ties, and `dense_rank` gives tied rows the same rank without gaps.",
        functions=[
            ("Window.partitionBy", "Define independent groups", "Window.partitionBy('category')", "Per-group analytics"),
            ("orderBy", "Define row sequence", "window.orderBy(F.desc('sales'))", "Ranking order"),
            ("row_number", "Unique sequential number", "F.row_number().over(w)", "Latest-row selection"),
            ("rank", "Rank with gaps", "F.rank().over(w)", "Competition ranking"),
            ("dense_rank", "Rank without gaps", "F.dense_rank().over(w)", "Top distinct values"),
        ],
        retail_df="retail_order_items", retail_dataset="Retail order items joined to products",
        retail_requirement="rank products by completed sales value within each category and keep the top two.",
        retail_code="""
from pyspark.sql.window import Window

product_sales = (retail_order_items.alias("i")
    .join(retail_orders.select("order_id", "order_status"), "order_id", "inner")
    .filter(F.col("order_status") == "COMPLETE")
    .join(retail_products.select("product_id", "product_name", "category"), "product_id", "inner")
    .withColumn("line_sales", F.col("quantity") * F.col("unit_price") * (1 - F.col("discount")))
    .groupBy("category", "product_id", "product_name")
    .agg(F.round(F.sum("line_sales"), 2).alias("sales")))

category_window = Window.partitionBy("category").orderBy(F.desc("sales"), F.asc("product_id"))
top_products = (product_sales
    .withColumn("category_rank", F.dense_rank().over(category_window))
    .filter(F.col("category_rank") <= 2))

top_products.orderBy("category", "category_rank", "product_id").show(30, truncate=False)
""",
        approach="Join facts to dimensions, calculate line sales, aggregate to product-category grain, then rank only that compact result within category.",
        expected="Each category returns at most two product ranks; Electronics is led by `Laptop Pro`, followed by `Smartphone X`.",
        interpretation="Category managers can compare leaders fairly within their own product groups instead of against the entire catalogue.",
        bank_focus="finding the highest-value transactions per customer after joining accounts",
        bank_tasks="Join transactions to accounts to obtain customer ID.|Keep successful transactions.|Define a customer-partitioned descending amount window.|Add `row_number`.|Add `rank` and `dense_rank` for comparison.|Return each customer's top transaction.|Return top three distinct amounts per customer.|Add transaction ID as a deterministic tie-breaker for row number.|Explain the output grain.|Inspect the physical plan for exchange and sort.",
        challenge="Fraud analysts want each customer's three largest successful debits per calendar month, retaining ties and deterministic evidence rows. Design the grain and ranking rule.",
        errors=[
            ("No partitionBy", "All rows enter one global window.", "Partition by the business group such as customer or category."),
            ("Non-deterministic row_number", "The order columns do not break ties.", "Add a stable unique tie-breaker."),
            ("Ranking detail before aggregation", "Duplicate lines distort product ranking.", "Aggregate to the intended ranking grain first."),
            ("Confusing rank semantics", "Ties and gaps do not match the requirement.", "Choose row_number, rank, or dense_rank explicitly."),
        ],
    ),
    dict(
        day=16, topic="Advanced Window Functions",
        concepts=["lag", "lead", "cumulative sum", "window frame", "sequence analysis"],
        what="Advanced windows access neighboring rows or cumulative frames within an ordered group.",
        why="Change detection, running totals, time gaps, and next-event analysis require context from a sequence.",
        how="`lag` and `lead` read relative rows; aggregate functions with `rowsBetween` calculate over a defined frame.",
        internal="Spark performs the same exchange-and-sort foundation as ranking, then evaluates frame state while scanning each ordered partition.",
        production="Teams calculate balance movements, customer purchase gaps, session behavior, cumulative exposure, and slowly changing record changes.",
        analogy="A runner looks at the athlete immediately ahead and behind while also checking the cumulative distance completed so far.",
        performance="Reuse compatible window specifications and ensure large customer or account groups do not create extreme skew.",
        compare="lag, lead, and cumulative aggregates", comparison_answer="`lag` reads a previous row, `lead` reads a following row, and a framed aggregate summarizes a range such as all rows to the current row.",
        functions=[
            ("lag", "Read previous row value", "F.lag('amount').over(w)", "Change analysis"),
            ("lead", "Read next row value", "F.lead('date').over(w)", "Next-event timing"),
            ("rowsBetween", "Define row frame", "w.rowsBetween(Window.unboundedPreceding, Window.currentRow)", "Running totals"),
            ("sum over window", "Cumulative total", "F.sum('amount').over(frame)", "Running measures"),
        ],
        retail_df="retail_orders", retail_dataset="Retail customer order sequence",
        retail_requirement="compare each completed order with the customer's previous order and calculate cumulative spend.",
        retail_code="""
customer_sequence = Window.partitionBy("customer_id").orderBy("order_date", "order_id")
running_frame = customer_sequence.rowsBetween(Window.unboundedPreceding, Window.currentRow)

order_sequence = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .select("customer_id", "order_id", "order_date", "total_amount")
    .withColumn("previous_amount", F.lag("total_amount").over(customer_sequence))
    .withColumn("next_order_date", F.lead("order_date").over(customer_sequence))
    .withColumn("change_from_previous", F.round(F.col("total_amount") - F.col("previous_amount"), 2))
    .withColumn("cumulative_spend", F.round(F.sum("total_amount").over(running_frame), 2)))

order_sequence.orderBy("customer_id", "order_date", "order_id").show(30, truncate=False)
""",
        approach="Create one deterministic customer sequence, derive a running frame from it, and reuse both for neighbor and cumulative metrics.",
        expected="A customer's first order has null previous amount; customer `C001` progresses from ₹2,499 to cumulative spend **₹67,499** after order `O1013`.",
        interpretation="Marketing can detect spend acceleration and time to next purchase without collapsing individual orders.",
        bank_focus="comparing consecutive transactions and calculating cumulative account activity",
        bank_tasks="Partition transactions by account and order by date plus ID.|Add previous transaction amount.|Add next transaction date.|Calculate change from previous amount.|Calculate days to next transaction.|Create cumulative debit amount.|Create cumulative credit amount.|Keep first-event nulls rather than forcing zero without explanation.|Check tie behavior for same-day events.|Explain how this differs from groupBy.",
        challenge="Detect accounts with three rapidly increasing debits in sequence. Define deterministic event order, comparison logic, and evidence columns.",
        errors=[
            ("Default frame misunderstood", "Ordered aggregate frames may not match row-based intent.", "Declare `rowsBetween` explicitly."),
            ("Tied timestamps", "Sequence is non-deterministic.", "Add a stable event ID to ordering."),
            ("Wrong partition key", "Values leak across customers or accounts.", "State the entity whose history is independent."),
            ("Replacing first lag with zero blindly", "No previous event is not the same as zero.", "Preserve null or add a first-event flag."),
        ],
    ),
    dict(
        day=17, topic="User-Defined Functions (UDFs)",
        concepts=["Python UDF", "return type", "serialization", "built-in alternatives"],
        what="A Python UDF wraps custom Python logic so it can be applied as a Spark column expression.",
        why="UDFs fill gaps when a rule cannot be expressed reasonably with built-in Spark functions.",
        how="Spark sends column values between the JVM execution engine and Python workers, runs the function, and converts results to the declared return type.",
        internal="Regular Python UDFs create a serialization boundary and are less visible to Catalyst than native expressions.",
        production="Teams govern UDF ownership, input/output contracts, null behavior, tests, and performance; built-ins remain the first choice.",
        analogy="A UDF is sending a package to a specialist workshop outside the main factory line, then bringing the result back.",
        performance="Prefer built-ins, SQL expressions, or higher-order functions; benchmark unavoidable UDFs and consider vectorized alternatives when appropriate.",
        compare="built-in expressions and Python UDFs", comparison_answer="Built-ins run inside Spark's optimized engine; Python UDFs cross a language boundary and hide logic from many optimizations.",
        functions=[
            ("udf", "Register Python function as Column function", "F.udf(fn, StringType())", "Unavoidable custom logic"),
            ("@F.udf", "Decorator syntax", "@F.udf('string')", "Reusable UDF declaration"),
            ("pandas_udf", "Vectorized Arrow UDF", "@F.pandas_udf('double')", "Vectorizable custom logic"),
            ("when", "Native conditional alternative", "F.when(condition, value)", "Preferred classification"),
        ],
        retail_df="retail_customers", retail_dataset="Retail customer spending",
        retail_requirement="demonstrate customer segmentation with a tested Python function, then show the preferred built-in equivalent.",
        retail_code="""
from pyspark.sql.types import StringType

def segment_customer(total_spend):
    if total_spend is None:
        return "UNKNOWN"
    if total_spend >= 30000:
        return "PLATINUM"
    if total_spend >= 10000:
        return "GOLD"
    return "STANDARD"

segment_udf = F.udf(segment_customer, StringType())

customer_spend = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .groupBy("customer_id")
    .agg(F.sum("total_amount").alias("total_spend")))

segmented = customer_spend.withColumn("udf_segment", segment_udf("total_spend"))
preferred = segmented.withColumn(
    "builtin_segment",
    F.when(F.col("total_spend") >= 30000, "PLATINUM")
     .when(F.col("total_spend") >= 10000, "GOLD")
     .otherwise("STANDARD"))
preferred.orderBy(F.desc("total_spend")).show(truncate=False)
""",
        approach="Write a pure function with null behavior, declare the return type, apply it once, and compare with an equivalent native expression.",
        expected="Customer `C001` has total spend **₹67,499** and receives **PLATINUM** from both implementations.",
        interpretation="The business rule works, but the built-in version is preferred because Spark can optimize it directly.",
        bank_focus="creating a documented banking risk classification only when built-ins are insufficient",
        bank_tasks="Write a pure risk function with null handling.|Declare its Spark return type.|Apply it to loan amount and interest rate.|Create test cases for every rule boundary.|Compare output with a built-in `when` implementation.|Explain serialization overhead.|Inspect the plan for a Python evaluation node.|Avoid reading external mutable state inside the UDF.|Record unexpected inputs as `UNKNOWN`.|Recommend whether the rule should remain a UDF.",
        challenge="A bank has a complex, versioned risk formula maintained by model governance. Design a safe UDF interface, test strategy, version field, and performance validation.",
        errors=[
            ("No return type", "Spark cannot reliably encode the Python result.", "Declare the exact Spark return type."),
            ("UDF fails on null", "Python logic assumes every input is present.", "Define and test null behavior explicitly."),
            ("Using UDF for simple conditions", "Native optimization is lost unnecessarily.", "Use built-in expressions whenever possible."),
            ("Capturing large objects", "The closure is serialized to workers.", "Keep UDF dependencies small and deterministic."),
        ],
    ),
    dict(
        day=18, topic="RDD Fundamentals",
        concepts=["RDD", "transformation", "action", "pair RDD", "DataFrame versus RDD"],
        what="An RDD is Spark's lower-level distributed collection of objects, divided into partitions and transformed lazily.",
        why="RDD knowledge explains Spark's foundations and helps with genuinely unstructured records or specialized algorithms, though DataFrames are preferred for structured ETL.",
        how="Transformations such as `map` and `filter` create lineage; actions such as `collect` or `count` trigger partition computation.",
        internal="Spark schedules RDD lineage as stages and tasks, recomputing lost partitions from lineage when possible.",
        production="Most data engineering stays with DataFrames; RDDs appear in legacy code, low-level parsing, and custom partition operations.",
        analogy="An RDD is a distributed pile of index cards; you describe how each worker should transform its pile.",
        performance="Avoid Python object overhead for structured data and never collect an unbounded RDD to the driver.",
        compare="RDDs and DataFrames", comparison_answer="RDDs offer low-level object control but little schema optimization; DataFrames are schema-aware, Catalyst-optimized, and usually faster for ETL.",
        functions=[
            ("parallelize", "Create an RDD", "sc.parallelize(data, 2)", "Small demonstrations"),
            ("map", "Transform every element", "rdd.map(function)", "Record parsing"),
            ("filter", "Keep elements", "rdd.filter(predicate)", "Record selection"),
            ("reduceByKey", "Aggregate pair values", "pairs.reduceByKey(lambda a,b: a+b)", "Keyed totals"),
            ("collect", "Return all elements to driver", "rdd.collect()", "Only bounded teaching results"),
        ],
        retail_df="retail_orders", retail_dataset="Raw retail text records",
        retail_requirement="parse raw pipe-delimited retail order text and calculate completed sales by store with an RDD.",
        retail_code="""
raw_order_lines = [
    "O2001|S001|COMPLETE|1200.0",
    "O2002|S002|CANCELLED|800.0",
    "O2003|S001|COMPLETE|2300.0",
    "O2004|S002|COMPLETE|1500.0",
]

raw_rdd = spark.sparkContext.parallelize(raw_order_lines, 2)
store_totals_rdd = (raw_rdd
    .map(lambda line: line.split("|"))
    .filter(lambda parts: parts[2] == "COMPLETE")
    .map(lambda parts: (parts[1], float(parts[3])))
    .reduceByKey(lambda left, right: left + right))

print(sorted(store_totals_rdd.collect()))  # safe only because this result has two rows
""",
        approach="Parallelize a bounded sample, parse fields, filter status, form `(store, amount)` pairs, and reduce locally before collecting two totals.",
        expected="The result is `[('S001', 3500.0), ('S002', 1500.0)]`.",
        interpretation="The exercise exposes low-level distributed mechanics, while a production structured pipeline should normally use DataFrames.",
        bank_focus="processing raw banking transaction records with a small RDD demonstration",
        bank_tasks="Create an RDD from five pipe-delimited transactions.|Split each record into fields.|Filter successful records.|Convert amount text to float safely.|Create account-amount pairs.|Reduce amounts by account.|Count input records.|Identify malformed records in a separate RDD.|Convert valid parsed rows to a DataFrame.|Explain why the DataFrame is preferable after parsing.",
        challenge="A legacy mainframe feed contains mixed record types and malformed lines. Design an RDD parsing boundary that returns typed DataFrames for valid records and rejects with reason codes.",
        errors=[
            ("Collecting raw data", "Every object moves to driver memory.", "Aggregate or write distributed results; collect only bounded outputs."),
            ("Parsing without validation", "Malformed lines cause task failures.", "Check field count and types, and route rejects separately."),
            ("Using groupByKey for sums", "All values move across the network before reduction.", "Use `reduceByKey` or DataFrame aggregation."),
            ("Keeping structured work in RDDs", "Catalyst and compact encodings are lost.", "Convert to a typed DataFrame after low-level parsing."),
        ],
    ),
    dict(
        day=19, topic="Spark Execution and Lazy Evaluation",
        concepts=["lazy evaluation", "logical plan", "DAG", "narrow transformation", "wide transformation", "action"],
        what="Lazy evaluation means Spark records transformations as a plan and computes them only when an action needs a result.",
        why="Spark can optimize the full chain, avoid unused work, and pipeline compatible operations.",
        how="Transformations extend lineage; an action triggers analysis, optimization, physical planning, stage creation, and task execution.",
        internal="Catalyst rewrites DataFrame plans, and exchanges mark shuffle boundaries that split stages in the DAG scheduler.",
        production="Engineers use `explain`, Spark UI, event logs, and metrics to connect source code to actual execution.",
        analogy="You write a complete shopping list before visiting the store, allowing one optimized trip instead of traveling after every item.",
        performance="Inspect physical plans, minimize repeated actions, and persist only reused expensive plans.",
        compare="narrow and wide transformations", comparison_answer="Narrow operations consume a small known set of parent partitions; wide operations redistribute data and introduce shuffle boundaries.",
        functions=[
            ("explain", "Print execution plans", "df.explain('formatted')", "Plan inspection"),
            ("count", "Trigger computation", "df.count()", "Action demonstration"),
            ("take", "Return bounded rows", "df.take(5)", "Small action"),
            ("write", "Materialize output", "df.write.parquet(path)", "Pipeline action"),
        ],
        retail_df="retail_orders", retail_dataset="Retail transformation pipeline",
        retail_requirement="build a lazy completed-sales pipeline, inspect its plan, and identify the action and shuffle boundary.",
        retail_code="""
lazy_pipeline = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .select("store_id", "order_id", "total_amount")
    .groupBy("store_id")
    .agg(F.sum("total_amount").alias("revenue"))
    .filter(F.col("revenue") > 10000))

print("No action has run merely by defining lazy_pipeline.")
lazy_pipeline.explain("formatted")

# show() is the action that now asks Spark to compute the result.
lazy_pipeline.orderBy(F.desc("revenue")).show()
""",
        approach="Define a chain without intermediate actions, inspect the optimized plan, then deliberately trigger computation with one display action.",
        expected="The plan includes pushed filters/projections plus an exchange for `groupBy`; stores S001, S002, and S004 exceed ₹10,000.",
        interpretation="Spark can combine the filter and projection before shuffling only the fields required for store totals.",
        bank_focus="tracing a lazy banking transaction pipeline from transformation to action",
        bank_tasks="Build a filter-select pipeline without an action.|Add a grouped total and predict the exchange.|Call `explain('formatted')`.|Label every operation as transformation or action.|Identify narrow transformations.|Identify the wide transformation.|Trigger exactly one bounded action.|Explain why repeated `count()` calls recompute by default.|Find pushed filters in a Parquet plan.|Draw the optimized DAG in a markdown cell.",
        challenge="A notebook takes 40 minutes because analysts repeatedly call counts after every step. Redesign the validation strategy while retaining trustworthy checkpoints.",
        errors=[
            ("Expecting transformations to run immediately", "Spark is lazy.", "Identify the first action and inspect its full lineage."),
            ("Adding many debugging actions", "Each action can recompute the pipeline.", "Use targeted validations and persist only justified reused intermediates."),
            ("Reading only source code", "The physical plan may differ after optimization.", "Use formatted explain and Spark UI evidence."),
            ("Assuming every transformation shuffles", "Many filters and projections are narrow.", "Look for exchanges in the physical plan."),
        ],
    ),
    dict(
        day=20, topic="Partitioning",
        concepts=["partition", "repartition", "coalesce", "partitioned write", "data skew"],
        what="A partition is a unit of distributed data processed by one task at a time; partitioning controls parallelism and file layout.",
        why="Too few partitions underuse the cluster, too many add overhead, and uneven partitions create stragglers.",
        how="`repartition` reshuffles to rebalance or partition by keys; `coalesce` usually reduces partitions with less movement; partitioned writes create directory layouts.",
        internal="Every stage launches tasks for its partitions. Exchanges create new partitioning, while coalesce can collapse existing dependencies.",
        production="Teams size files, choose low-cardinality partition columns, monitor skew, and separate compute partitioning from storage partitioning.",
        analogy="Partitions are boxes assigned to workers: giant boxes delay one worker, while thousands of tiny boxes waste handling time.",
        performance="Target balanced, reasonably sized partitions and avoid high-cardinality directory partition columns.",
        compare="repartition and coalesce", comparison_answer="`repartition` can increase or decrease and performs a shuffle for balance; `coalesce` normally reduces with less movement but may preserve imbalance.",
        functions=[
            ("repartition", "Redistribute partitions", "df.repartition(8, 'store_id')", "Balance or key distribution"),
            ("coalesce", "Reduce partitions", "df.coalesce(2)", "Fewer output files"),
            ("getNumPartitions", "Inspect partition count", "df.rdd.getNumPartitions()", "Diagnostics"),
            ("partitionBy", "Directory-partition writes", "writer.partitionBy('state')", "Prunable storage layout"),
        ],
        retail_df="retail_orders", retail_dataset="Retail orders by store and date",
        retail_requirement="compare repartition and coalesce, then write completed orders partitioned by store ID.",
        retail_code="""
completed = retail_orders.filter(F.col("order_status") == "COMPLETE")
by_store = completed.repartition(4, "store_id")
compact = by_store.coalesce(2)

print("Original partitions:", completed.rdd.getNumPartitions())
print("After repartition:", by_store.rdd.getNumPartitions())
print("After coalesce:", compact.rdd.getNumPartitions())

partition_path = f"{lab_root}/orders_by_store"
(completed.write.mode("overwrite")
    .partitionBy("store_id")
    .parquet(partition_path))
print("Partitioned output:", partition_path)
""",
        approach="Filter first, explicitly rebalance by store, reduce for demonstration, and separately write a store-partitioned Parquet layout.",
        expected="Repartition reports 4 partitions and coalesce reports 2; the output folder contains store-specific directories.",
        interpretation="Compute parallelism and storage layout are related but distinct choices, each driven by workload access patterns.",
        bank_focus="partitioning transactions by branch or processing date while controlling output files",
        bank_tasks="Inspect transaction partition count.|Repartition transactions to four partitions.|Repartition by account ID.|Compare partition row counts.|Coalesce to two partitions.|Explain when coalesce can remain skewed.|Write by a low-cardinality branch or date field after integration.|Explain why customer ID is a poor directory partition.|Estimate file-count implications.|Inspect the plan for the repartition exchange.",
        challenge="A daily bank table writes 30,000 tiny files and one branch contains 60% of transactions. Propose compute and storage partition strategies with measurable targets.",
        errors=[
            ("One partition", "A global operation or coalesce removed parallelism.", "Increase balanced partitions before heavy downstream work."),
            ("Thousands of tiny files", "Excessive partitions are written independently.", "Compact and tune output partitions to target file sizes."),
            ("High-cardinality partitionBy", "Directory count explodes.", "Choose common filter columns with bounded cardinality."),
            ("Ignoring skew", "One key owns a disproportionate share of rows.", "Measure key frequency and apply a workload-specific skew strategy."),
        ],
    ),
    dict(
        day=21, topic="Performance Optimization",
        concepts=["cache", "persist", "broadcast join", "predicate pushdown", "column pruning"],
        what="Performance optimization reduces time and resources while preserving exactly the same business result.",
        why="Efficient jobs meet SLAs, control cloud cost, and leave cluster capacity for other workloads.",
        how="Engineers reduce data early, choose good formats and partitions, reuse expensive results selectively, and influence join strategies only with evidence.",
        internal="Catalyst prunes columns and pushes filters; the planner chooses joins; cached blocks let later actions skip upstream lineage.",
        production="Optimization begins with metrics and plans, changes one bottleneck at a time, and verifies both correctness and improvement.",
        analogy="Optimization is improving a delivery route after measuring traffic, not simply buying more trucks.",
        performance="Measure before and after; cache only reused results, broadcast only bounded dimensions, and unpersist promptly.",
        compare="cache, persist, and checkpoint", comparison_answer="Cache uses the default persistence level, persist chooses a storage level, and checkpoint truncates lineage by writing reliable materialized data.",
        functions=[
            ("cache", "Persist with default level", "df.cache()", "Reused intermediate"),
            ("persist", "Choose storage level", "df.persist(StorageLevel.MEMORY_AND_DISK)", "Controlled reuse"),
            ("unpersist", "Release cached blocks", "df.unpersist()", "Resource cleanup"),
            ("broadcast", "Hint small-side broadcast", "F.broadcast(dim)", "Avoid large join shuffle"),
            ("explain", "Verify plan choices", "df.explain('formatted')", "Evidence"),
        ],
        retail_df="retail_orders", retail_dataset="Retail customer-order join",
        retail_requirement="optimize a reused completed-order dataset and join it to the small store dimension with a verified broadcast.",
        retail_code="""
from pyspark import StorageLevel

reused_completed = (retail_orders
    .filter(F.col("order_status") == "COMPLETE")
    .select("order_id", "store_id", "customer_id", "order_date", "total_amount")
    .persist(StorageLevel.MEMORY_AND_DISK))

# Materialize once because two downstream consumers reuse it.
print("Completed rows:", reused_completed.count())

optimized_join = reused_completed.join(
    F.broadcast(retail_stores.select("store_id", "store_name", "state")),
    "store_id", "left"
)
optimized_join.explain("formatted")
optimized_join.groupBy("state").agg(F.sum("total_amount").alias("revenue")).show()

reused_completed.unpersist()
""",
        approach="Reduce rows and columns, persist a truly reused intermediate, broadcast the bounded dimension, verify the plan, and release memory.",
        expected="The plan contains `BroadcastHashJoin`; state revenue includes KA ₹100,648.50, MH ₹41,499.50, DL ₹7,601, and ONLINE ₹10,499.",
        interpretation="The large fact remains distributed while each executor receives a small store lookup, avoiding a two-sided join shuffle.",
        bank_focus="optimizing customer-account joins with measurement-driven caching and broadcasting",
        bank_tasks="Filter and project transaction facts before a join.|Broadcast the small branch dimension.|Verify `BroadcastHashJoin` in the plan.|Cache a reused successful-transaction intermediate.|Materialize the cache once.|Use it for two different summaries.|Unpersist after use.|Compare plans with and without broadcast.|Explain predicate pushdown in a Parquet read.|Write a before/after measurement checklist.",
        challenge="A bank job regressed from 20 to 70 minutes. Build an evidence-first investigation covering input growth, plan changes, skew, shuffle, spill, file counts, and cache use.",
        errors=[
            ("Caching everything", "Memory pressure and eviction outweigh recomputation savings.", "Cache only expensive reused results and unpersist."),
            ("Broadcasting a large table", "Executors may run out of memory.", "Use statistics and size evidence before forcing broadcast."),
            ("Optimizing without a baseline", "Improvement cannot be proven.", "Record duration, input size, shuffle, spill, and output metrics."),
            ("Changing logic while tuning", "Faster output may be incorrect.", "Reconcile counts and totals before and after every optimization."),
        ],
    ),
    dict(
        day=22, topic="Spark SQL",
        concepts=["temporary view", "SQL query", "SQL/DataFrame equivalence", "query plan"],
        what="Spark SQL executes SQL queries over DataFrames and tables using the same Catalyst optimizer and execution engine.",
        why="SQL makes analytics accessible and lets teams express joins, filters, aggregates, and windows declaratively.",
        how="A DataFrame becomes queryable through a temporary view; `spark.sql` parses SQL into the same logical-plan system used by DataFrame APIs.",
        internal="The SQL parser creates an unresolved plan, the analyzer resolves fields and functions, Catalyst optimizes it, and Spark executes a physical plan.",
        production="Teams combine SQL models with PySpark orchestration, tests, reusable functions, and governed catalog tables.",
        analogy="DataFrame and SQL APIs are two languages giving instructions to the same kitchen.",
        performance="Compare physical plans rather than assuming one API is faster; avoid opaque SQL strings and select only needed columns.",
        compare="Spark SQL and the DataFrame API", comparison_answer="Both normally reach the same optimizer and performance; the better choice is the clearest maintainable expression for the team and task.",
        functions=[
            ("createOrReplaceTempView", "Register session view", "df.createOrReplaceTempView('orders')", "SQL access"),
            ("spark.sql", "Execute SQL", "spark.sql('SELECT ...')", "Declarative transformations"),
            ("sql", "Use SQL expressions in select", "F.expr('CASE WHEN ... END')", "Mixed API code"),
            ("explain", "Inspect SQL plan", "result.explain('formatted')", "Plan comparison"),
        ],
        retail_df="retail_orders", retail_dataset="Retail sales temporary views",
        retail_requirement="calculate store revenue and average order value with Spark SQL, then compare the DataFrame plan.",
        retail_code="""
retail_orders.createOrReplaceTempView("orders")
retail_stores.createOrReplaceTempView("stores")

sql_store_kpis = spark.sql('''
SELECT
    s.store_id,
    s.store_name,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM orders o
JOIN stores s ON o.store_id = s.store_id
WHERE o.order_status = 'COMPLETE'
GROUP BY s.store_id, s.store_name
ORDER BY revenue DESC
''')

sql_store_kpis.show(truncate=False)
sql_store_kpis.explain("formatted")
""",
        approach="Register session-scoped views, express the same filtered join and aggregation in SQL, and inspect its physical plan.",
        expected="Bengaluru Central leads with **₹100,648.50** revenue; the plan contains join, filter, aggregate, and sort operations.",
        interpretation="SQL users and PySpark developers can collaborate on one optimized execution engine and common business definitions.",
        bank_focus="analyzing banking transactions with temporary views and auditable SQL",
        bank_tasks="Register customers, accounts, transactions, and branches as views.|Count successful transactions in SQL.|Calculate amount by transaction type.|Join transactions to accounts.|Join the result to branches.|Calculate branch/type KPIs.|Use a SQL CASE expression for amount bands.|Reproduce one query with the DataFrame API.|Compare physical plans.|Explain the scope and lifetime of a temporary view.",
        challenge="Write a SQL design for monthly branch transaction KPIs with customer counts, debit/credit totals, and high-value flags, then list reconciliation checks.",
        errors=[
            ("View not found", "It was not registered in this session or the name differs.", "Register the DataFrame and use consistent names."),
            ("Ambiguous SQL column", "Joined tables share a field name.", "Use table aliases and qualified references."),
            ("SQL injection through parameters", "Untrusted text is concatenated into SQL.", "Validate parameters or use safe DataFrame expressions."),
            ("Assuming SQL is automatically faster", "Both APIs use the same optimizer.", "Compare plans and readability, not syntax stereotypes."),
        ],
    ),
    dict(
        day=23, topic="Delta Lake",
        concepts=["Delta table", "ACID", "transaction log", "MERGE", "update", "delete", "time travel"],
        what="Delta Lake is a table format that adds a transaction log, ACID operations, schema controls, and versioned reads to data-lake files.",
        why="Reliable pipelines need atomic commits, concurrent-read safety, upserts, deletes, and reproducible historical versions.",
        how="Data files hold rows while `_delta_log` records table versions and committed actions; readers construct a consistent snapshot.",
        internal="Optimistic concurrency validates a proposed commit against intervening versions before atomically publishing a new log entry.",
        production="Bronze, Silver, and Gold tables use governed paths or catalog names, idempotent merges, retention policy, and access controls.",
        analogy="Parquet files are pages; Delta's transaction log is the official index recording exactly which pages belong to each edition.",
        performance="Use sensible file sizes and partitioning, compact small files, collect statistics, and keep merge predicates selective.",
        compare="Parquet files and Delta tables", comparison_answer="Parquet defines a columnar file format; Delta adds a transaction log and table semantics while storing data in Parquet files.",
        functions=[
            ("format('delta')", "Read/write Delta format", "df.write.format('delta').save(path)", "Delta table creation"),
            ("DeltaTable.forPath", "Open Delta table API", "DeltaTable.forPath(spark, path)", "DML operations"),
            ("merge", "Upsert source rows", "target.alias('t').merge(source.alias('s'), condition)", "Incremental loads"),
            ("update", "Update matched rows", "table.update(condition, values)", "Corrections"),
            ("delete", "Delete matched rows", "table.delete(condition)", "Governed removal"),
            ("versionAsOf", "Read historical version", "reader.option('versionAsOf', 0)", "Time travel"),
        ],
        retail_df="retail_orders", retail_dataset="Retail Delta orders table",
        retail_requirement="create a Delta table, merge an updated order plus a new order, and read the original version.",
        retail_code="""
# Delta requires a Delta-enabled SparkSession. Run the optional setup cell below,
# restart the kernel if packages are installed, then execute this cell.
delta_path = f"{lab_root}/delta/orders"

try:
    from delta.tables import DeltaTable

    retail_orders.write.format("delta").mode("overwrite").save(delta_path)
    updates = spark.createDataFrame([
        ("O1002", "C002", "S002", date(2026, 1, 5), "COMPLETE", 8500.0),
        ("O1016", "C003", "S001", date(2026, 3, 1), "COMPLETE", 1999.0),
    ], retail_orders.schema)

    target = DeltaTable.forPath(spark, delta_path)
    (target.alias("t")
        .merge(updates.alias("s"), "t.order_id = s.order_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute())

    spark.read.format("delta").load(delta_path).filter("order_id IN ('O1002','O1016')").show()
    print("Version 0 rows:", spark.read.format("delta").option("versionAsOf", 0).load(delta_path).count())
except Exception as exc:
    print("Delta demo not active in this kernel.")
    print("Follow the Delta setup note, restart the kernel, and rerun. Details:", str(exc)[:300])
""",
        approach="Write the baseline atomically, merge by stable order ID, inspect changed rows, and use versioned read for reproducibility.",
        expected="With Delta enabled, `O1002` becomes COMPLETE, `O1016` is inserted, the current table has 16 rows, and version 0 has 15 rows.",
        interpretation="The incremental load is idempotent by order ID and historical state remains queryable for audit and recovery.",
        bank_focus="building a banking transaction Delta table with idempotent upsert and audit history",
        bank_tasks="Create a Delta path for transactions.|Write the baseline table.|Create one corrected and one new transaction.|Merge by transaction ID.|Prove a retry does not add a duplicate.|Read version zero.|Describe an approved correction with update.|Describe a governed deletion use case.|Inspect table history if available.|List retention and privacy controls required by the bank.",
        challenge="Design an idempotent transaction CDC merge with insert, correction, and reversal events, including ordering, audit columns, and late-arrival rules.",
        errors=[
            ("Delta data source not found", "The package or session extensions are missing.", "Install a compatible Delta package and restart with a Delta-enabled session."),
            ("Merge matches multiple source rows", "Source keys are duplicated.", "Deterministically deduplicate source events before merge."),
            ("Non-idempotent insert logic", "Retry creates new business rows.", "Match on stable keys and test reruns."),
            ("Unsafe vacuum/retention", "Files needed for history may be removed.", "Follow platform retention and governance policies."),
        ],
    ),
    dict(
        day=24, topic="End-to-End ETL: Bronze, Silver, Gold",
        concepts=["Bronze", "Silver", "Gold", "data quality", "idempotency", "lineage"],
        what="Medallion ETL organizes raw ingestion, cleaned integrated data, and business-ready outputs into Bronze, Silver, and Gold layers.",
        why="Layered responsibilities make pipelines testable, recoverable, auditable, and easier for teams to own.",
        how="Bronze preserves source fidelity and metadata; Silver enforces contracts and integrates entities; Gold publishes stable business grains and KPIs.",
        internal="Each layer materializes a contract, reducing repeated lineage and providing restart points; the storage format controls atomicity and versioning.",
        production="Orchestration supplies run IDs and dates, quality gates block bad promotion, and monitoring records counts, totals, duration, and freshness.",
        analogy="Bronze is the receiving dock, Silver is the inspected warehouse, and Gold is the finished-product showroom.",
        performance="Incrementally process changed partitions, compact files, reuse conformed dimensions, and design Gold tables for actual access patterns.",
        compare="Bronze, Silver, and Gold", comparison_answer="Bronze preserves raw truth, Silver creates clean reusable entities, and Gold serves a defined business question at a stable grain.",
        functions=[
            ("write.mode", "Choose write behavior", "df.write.mode('overwrite')", "Layer materialization"),
            ("withColumn", "Add lineage/quality fields", "df.withColumn('ingest_date', F.current_date())", "Bronze metadata"),
            ("join", "Integrate conformed entities", "facts.join(dim, key)", "Silver models"),
            ("groupBy / agg", "Publish measures", "df.groupBy(dim).agg(...) ", "Gold KPIs"),
            ("partitionBy", "Lay out incremental data", "writer.partitionBy('business_date')", "Prunable storage"),
        ],
        retail_df="retail_orders", retail_dataset="Complete retail project datasets",
        retail_requirement="build reproducible Bronze metadata, validated Silver order lines, and a Gold daily-store-category sales table.",
        retail_code="""
run_id = "classroom-run-2026-03-01"

# Bronze: source fidelity plus ingestion metadata.
bronze_orders = (retail_orders
    .withColumn("source_system", F.lit("retail_pos"))
    .withColumn("ingest_run_id", F.lit(run_id)))

# Silver: valid completed orders integrated with line and product context.
silver_sales = (bronze_orders
    .filter((F.col("order_status") == "COMPLETE") & F.col("order_id").isNotNull())
    .join(retail_order_items, "order_id", "inner")
    .join(retail_products.select("product_id", "product_name", "category"), "product_id", "left")
    .withColumn("net_line_amount",
                F.round(F.col("quantity") * F.col("unit_price") * (1 - F.col("discount")), 2))
    .select("order_id", "order_date", "store_id", "customer_id", "product_id",
            "product_name", "category", "quantity", "net_line_amount", "ingest_run_id"))

# Gold grain: one row per order date, store, and category.
gold_daily_sales = (silver_sales
    .groupBy("order_date", "store_id", "category")
    .agg(
        F.countDistinct("order_id").alias("order_count"),
        F.sum("quantity").alias("units_sold"),
        F.round(F.sum("net_line_amount"), 2).alias("revenue"),
    ))

assert bronze_orders.count() == retail_orders.count()
assert silver_sales.filter(F.col("category").isNull()).count() == 0
gold_daily_sales.orderBy("order_date", "store_id", "category").show(50, truncate=False)
""",
        approach="Give each layer one responsibility, carry run lineage, integrate only validated facts, publish a declared Gold grain, and enforce quality checks before promotion.",
        expected="Bronze retains 15 order rows; Silver has completed line-level sales with no null category; Gold returns daily store-category KPI rows.",
        interpretation="The project now separates reproducible raw history, reusable clean detail, and dashboard-ready business metrics.",
        bank_focus="designing the parallel Banking Transaction Analytics Platform across Bronze, Silver, and Gold",
        bank_tasks="Define Bronze tables and lineage columns for all six banking datasets.|Write schema and required-key checks.|Create accepted and rejected transaction outputs.|Build a Silver customer-account view.|Build a Silver transaction fact with branch and customer keys.|Create transaction amount and high-value flags.|Define a daily branch/type Gold grain.|Calculate count, total, average, and distinct customers.|Add reconciliation from raw to Silver to Gold.|Document incremental keys and rerun behavior.",
        challenge="Design the complete banking pipeline for late events, duplicate transactions, customer privacy, audit retention, quality gates, and daily KPI publication.",
        errors=[
            ("Bronze data is cleaned destructively", "Raw source fidelity is lost.", "Preserve original values and add metadata in Bronze."),
            ("Silver is dashboard-specific", "Reusable entities become coupled to one report.", "Keep conformed detail reusable; put report logic in Gold."),
            ("Gold grain is undocumented", "Consumers double-count measures.", "State keys and one-row-per definition in the contract."),
            ("No rerun design", "Retries duplicate or overwrite incorrect scope.", "Use idempotent keys, partitions, merges, and run audit."),
        ],
    ),
    dict(
        day=25, topic="Capstone Project, Debugging, and Interview Readiness",
        concepts=["KPI contract", "end-to-end project", "debugging", "optimization", "interview storytelling"],
        what="The capstone combines data modeling, transformations, validation, performance reasoning, and communication into one production-style solution.",
        why="Real data engineering work is not a list of APIs; it is delivering trustworthy, maintainable data products and explaining design choices.",
        how="Start from requirements and grain, build layered transformations, validate every boundary, inspect execution, and publish documented KPIs.",
        internal="The final Spark application becomes a DAG of scans, projections, filters, joins, exchanges, aggregates, windows, and writes.",
        production="A release includes code review, tests, job configuration, orchestration, monitoring, ownership, runbook, lineage, and access controls.",
        analogy="The capstone is the final building inspection: structure, utilities, safety checks, and user needs must all work together.",
        performance="Optimize the measured critical path only after correctness; verify plans, skew, shuffle, spill, file sizes, and workload reuse.",
        compare="a notebook demo and a production data product", comparison_answer="A demo proves logic on a sample; a production product adds contracts, tests, idempotency, scale evidence, security, observability, and operational ownership.",
        functions=[
            ("assert", "Fail fast on invariants", "assert bad_rows == 0", "Data-quality gate"),
            ("explain", "Inspect execution plan", "df.explain('formatted')", "Performance review"),
            ("join", "Integrate entities", "facts.join(dim, key)", "Project modeling"),
            ("groupBy / agg", "Build KPIs", "df.groupBy(...).agg(...) ", "Gold outputs"),
            ("Window", "Add rankings/sequences", "function.over(window)", "Advanced analytics"),
        ],
        retail_df="retail_orders", retail_dataset="Retail Sales Analytics Platform capstone",
        retail_requirement="publish the final retail KPI pack: revenue, time trends, store/category performance, top products/customers, AOV, and purchase frequency.",
        retail_code="""
# Reuse the validated Silver sales detail from Day 24.
retail_kpis = {
    "total_revenue": silver_sales.agg(F.round(F.sum("net_line_amount"), 2).alias("total_revenue")),
    "daily_revenue": silver_sales.groupBy("order_date").agg(F.round(F.sum("net_line_amount"), 2).alias("revenue")),
    "monthly_revenue": (silver_sales
        .withColumn("month", F.date_format("order_date", "yyyy-MM"))
        .groupBy("month").agg(F.round(F.sum("net_line_amount"), 2).alias("revenue"))),
    "store_revenue": silver_sales.groupBy("store_id").agg(F.round(F.sum("net_line_amount"), 2).alias("revenue")),
    "category_revenue": silver_sales.groupBy("category").agg(F.round(F.sum("net_line_amount"), 2).alias("revenue")),
    "customer_metrics": (silver_sales.groupBy("customer_id")
        .agg(F.countDistinct("order_id").alias("purchase_frequency"),
             F.round(F.sum("net_line_amount"), 2).alias("customer_revenue"))),
}

product_rank_window = Window.orderBy(F.desc("product_revenue"), F.asc("product_id"))
retail_kpis["top_products"] = (silver_sales.groupBy("product_id", "product_name")
    .agg(F.round(F.sum("net_line_amount"), 2).alias("product_revenue"))
    .withColumn("sales_rank", F.dense_rank().over(product_rank_window)))

completed_order_values = (retail_orders.filter("order_status = 'COMPLETE'")
    .agg(F.round(F.avg("total_amount"), 2).alias("average_order_value")))
retail_kpis["average_order_value"] = completed_order_values

for name, result in retail_kpis.items():
    print(f"\\n=== {name} ===")
    result.orderBy(result.columns[0]).show(20, truncate=False) if len(result.columns) > 1 else result.show()

assert retail_orders.select("order_id").distinct().count() == retail_orders.count()
assert silver_sales.filter(F.col("net_line_amount") < 0).count() == 0
""",
        approach="Reuse validated Silver detail, create one DataFrame per KPI contract, rank products deterministically, and finish with invariants and explain-plan review.",
        expected="The notebook displays all required KPI tables; average completed order value is **₹12,326.77**, with product and customer leaders ranked from validated detail.",
        interpretation="The 25-day project delivers interview-ready evidence: code, business grains, controls, architecture reasoning, and performance awareness.",
        bank_focus="completing the Banking Transaction Analytics Platform and presenting it as an interview project",
        bank_tasks="Build total successful transaction amount.|Compare debit and credit count/amount.|Calculate average transaction amount.|Calculate transactions per customer.|Calculate branch transaction volume.|Rank top customers by activity.|Publish account balance KPIs without duplicating balances.|Calculate loan exposure by type/status.|Identify high-value transactions with a parameter.|Design suspicious-pattern flags and evidence output.",
        challenge="Present a 10-minute banking capstone walkthrough covering requirements, architecture, grain, quality, joins, windows, optimization evidence, security, failure recovery, and three future improvements.",
        errors=[
            ("KPI definitions are implicit", "Different teams calculate different populations or grains.", "Publish formula, filters, grain, owner, and freshness."),
            ("Demo-only code is called production-ready", "Tests, operations, security, and reruns are missing.", "Describe the hardening gap honestly and add a delivery checklist."),
            ("Debugging starts with random code changes", "The first failing boundary is unknown.", "Reproduce, isolate, inspect schema/counts/plan, then change one cause."),
            ("Interview answer lists APIs only", "It does not show engineering judgment.", "Use situation, requirement, design, trade-off, validation, and result."),
        ],
    ),
]


DATA_SETUP = r'''
import os
import sys
from datetime import date
from pathlib import Path
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType, DateType
)

# On Windows, Spark workers must use the same real Python executable as this kernel.
# This also avoids the Microsoft Store `python3.exe` application alias.
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = (SparkSession.builder
         .appName("25-Day PySpark Learning Plan")
         .master("local[2]")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.python.worker.reuse", "true")
         .config("spark.pyspark.python", sys.executable)
         .config("spark.pyspark.driver.python", sys.executable)
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

def make_df(rows, schema):
    """Create a small classroom DataFrame with an explicit schema."""
    return spark.createDataFrame(rows, schema)

# ---------------------------- Retail domain ----------------------------
retail_customers = make_df([
    ("C001", "Aarav Sharma", "Bengaluru", "KA", date(2024, 1, 15)),
    ("C002", "Diya Patel", "Mumbai", "MH", date(2024, 2, 10)),
    ("C003", "Kabir Singh", "Delhi", "DL", date(2024, 3, 12)),
    ("C004", "Meera Nair", "Kochi", "KL", date(2024, 4, 8)),
    ("C005", "Rohan Das", "Kolkata", "WB", date(2024, 5, 19)),
    ("C006", "Ananya Iyer", "Chennai", "TN", date(2024, 6, 22)),
    ("C007", "Vivaan Rao", "Hyderabad", "TS", date(2024, 7, 11)),
    ("C008", "Ishita Gupta", "Pune", "MH", date(2024, 8, 4)),
    ("C009", "Arjun Verma", "Jaipur", "RJ", date(2024, 9, 17)),
    ("C010", "Sara Khan", "Lucknow", "UP", date(2024, 10, 29)),
    ("C011", "Neel Joshi", "Ahmedabad", "GJ", date(2024, 11, 13)),
    ("C012", "Tara Menon", "Bengaluru", "KA", date(2025, 1, 5)),
], "customer_id string, customer_name string, city string, state string, signup_date date")

retail_products = make_df([
    ("P001", "Laptop Pro", "Electronics", 65000.0),
    ("P002", "Smartphone X", "Electronics", 28500.0),
    ("P003", "Wireless Earbuds", "Electronics", 2499.0),
    ("P004", "Office Chair", "Furniture", 8500.0),
    ("P005", "Study Desk", "Furniture", 12000.0),
    ("P006", "Running Shoes", "Fashion", 3999.0),
    ("P007", "Winter Jacket", "Fashion", 5499.0),
    ("P008", "Mixer Grinder", "Home", 4200.0),
    ("P009", "Cookware Set", "Home", 3299.0),
    ("P010", "Yoga Mat", "Sports", 999.0),
    ("P011", "Cricket Bat", "Sports", 2999.0),
    ("P012", "Coffee Pack", "Grocery", 349.0),
], "product_id string, product_name string, category string, price double")

retail_orders = make_df([
    ("O1001", "C001", "S001", date(2026, 1, 3), "COMPLETE", 2499.0),
    ("O1002", "C002", "S002", date(2026, 1, 5), "CANCELLED", 8500.0),
    ("O1003", "C003", "S004", date(2026, 1, 8), "COMPLETE", 3299.0),
    ("O1004", "C004", "S002", date(2026, 1, 14), "COMPLETE", 28500.0),
    ("O1005", "C005", "S003", date(2026, 1, 21), "COMPLETE", 5499.0),
    ("O1006", "C006", "S003", date(2026, 1, 25), "PENDING", 4200.0),
    ("O1007", "C007", "S001", date(2026, 2, 2), "COMPLETE", 12499.0),
    ("O1008", "C008", "S001", date(2026, 2, 6), "COMPLETE", 18500.0),
    ("O1009", "C009", "S003", date(2026, 2, 9), "COMPLETE", 1102.0),
    ("O1010", "C010", "S004", date(2026, 2, 13), "COMPLETE", 4200.0),
    ("O1011", "C011", "S002", date(2026, 2, 18), "COMPLETE", 12999.5),
    ("O1012", "C012", "S001", date(2026, 2, 20), "COMPLETE", 2150.5),
    ("O1013", "C001", "S001", date(2026, 2, 22), "COMPLETE", 65000.0),
    ("O1014", "C003", "S004", date(2026, 2, 24), "COMPLETE", 3000.0),
    ("O1015", "C007", "S003", date(2026, 2, 26), "COMPLETE", 1000.0),
], "order_id string, customer_id string, store_id string, order_date date, order_status string, total_amount double")

retail_order_items = make_df([
    ("O1001", "P003", 1, 2499.0, 0.00),
    ("O1002", "P004", 1, 8500.0, 0.00),
    ("O1003", "P009", 1, 3299.0, 0.00),
    ("O1004", "P002", 1, 28500.0, 0.00),
    ("O1005", "P007", 1, 5499.0, 0.00),
    ("O1006", "P008", 1, 4200.0, 0.00),
    ("O1007", "P005", 1, 12000.0, 0.00),
    ("O1007", "P012", 1, 499.0, 0.00),
    ("O1008", "P004", 2, 8500.0, 0.00),
    ("O1008", "P010", 2, 1000.0, 0.25),
    ("O1009", "P012", 2, 349.0, 0.00),
    ("O1009", "P010", 1, 449.0, 0.10),
    ("O1010", "P008", 1, 4200.0, 0.00),
    ("O1011", "P006", 2, 3999.0, 0.00),
    ("O1011", "P007", 1, 5499.0, 0.00),
    ("O1012", "P011", 1, 2999.0, 0.30),
    ("O1012", "P012", 1, 349.0, 0.85),
    ("O1013", "P001", 1, 65000.0, 0.00),
    ("O1014", "P003", 1, 2499.0, 0.00),
    ("O1014", "P012", 2, 349.0, 0.28),
    ("O1015", "P010", 1, 999.0, 0.00),
], "order_id string, product_id string, quantity int, unit_price double, discount double")

retail_stores = make_df([
    ("S001", "Bengaluru Central", "Bengaluru", "KA"),
    ("S002", "Mumbai High Street", "Mumbai", "MH"),
    ("S003", "Delhi Market", "Delhi", "DL"),
    ("S004", "Online Store", "Online", "ONLINE"),
], "store_id string, store_name string, city string, state string")

retail_payments = make_df([
    ("PAY01", "O1001", "UPI", 2499.0, "SUCCESS"),
    ("PAY02", "O1002", "CARD", 8500.0, "REFUNDED"),
    ("PAY03", "O1003", "UPI", 3299.0, "SUCCESS"),
    ("PAY04", "O1004", "CARD", 28500.0, "SUCCESS"),
    ("PAY05", "O1005", "CASH", 5499.0, "SUCCESS"),
    ("PAY06", "O1006", "UPI", 4200.0, "PENDING"),
    ("PAY07", "O1007", "CARD", 12499.0, "SUCCESS"),
    ("PAY08", "O1008", "CARD", 18500.0, "SUCCESS"),
    ("PAY09", "O1009", "UPI", 1102.0, "SUCCESS"),
    ("PAY10", "O1010", "UPI", 4200.0, "SUCCESS"),
    ("PAY11", "O1011", "CARD", 12999.5, "SUCCESS"),
    ("PAY12", "O1012", "CASH", 2150.5, "SUCCESS"),
], "payment_id string, order_id string, payment_type string, payment_amount double, payment_status string")

retail_inventory = make_df([
    ("P001", "S001", 8, date(2026, 2, 28)), ("P002", "S001", 14, date(2026, 2, 28)),
    ("P003", "S001", 40, date(2026, 2, 28)), ("P004", "S002", 6, date(2026, 2, 28)),
    ("P005", "S002", 5, date(2026, 2, 28)), ("P006", "S003", 22, date(2026, 2, 28)),
    ("P007", "S003", 11, date(2026, 2, 28)), ("P008", "S004", 35, date(2026, 2, 28)),
    ("P009", "S004", 30, date(2026, 2, 28)), ("P010", "S001", 55, date(2026, 2, 28)),
    ("P011", "S003", 17, date(2026, 2, 28)), ("P012", "S004", 120, date(2026, 2, 28)),
], "product_id string, store_id string, stock_quantity int, last_updated date")

# ---------------------------- Banking domain ---------------------------
bank_customers = make_df([
    ("BC001", "Aditya Mehta", "Mumbai", "RETAIL", date(2022, 1, 15)),
    ("BC002", "Priya Rao", "Bengaluru", "RETAIL", date(2022, 4, 10)),
    ("BC003", "Nikhil Shah", "Ahmedabad", "PREMIUM", date(2021, 7, 21)),
    ("BC004", "Fatima Ali", "Hyderabad", "RETAIL", date(2023, 2, 2)),
    ("BC005", "Karan Malhotra", "Delhi", "CORPORATE", date(2020, 11, 18)),
    ("BC006", "Lakshmi Nair", "Kochi", "PREMIUM", date(2021, 9, 9)),
    ("BC007", "Rahul Sen", "Kolkata", "RETAIL", date(2024, 1, 4)),
    ("BC008", "Zoya Khan", "Lucknow", "RETAIL", date(2023, 6, 12)),
    ("BC009", "Manav Joshi", "Pune", "CORPORATE", date(2020, 5, 20)),
    ("BC010", "Ira Kapoor", "Jaipur", "PREMIUM", date(2022, 8, 30)),
], "customer_id string, customer_name string, city string, customer_type string, join_date date")

bank_accounts = make_df([
    ("A001", "BC001", "SAVINGS", 125000.0, "B001"),
    ("A002", "BC002", "SAVINGS", 82000.0, "B002"),
    ("A003", "BC003", "CURRENT", 510000.0, "B003"),
    ("A004", "BC004", "SAVINGS", 45000.0, "B004"),
    ("A005", "BC005", "CURRENT", 1250000.0, "B005"),
    ("A006", "BC006", "SAVINGS", 230000.0, "B006"),
    ("A007", "BC007", "SAVINGS", 18000.0, "B007"),
    ("A008", "BC008", "SAVINGS", 67000.0, "B008"),
    ("A009", "BC009", "CURRENT", 890000.0, "B009"),
    ("A010", "BC010", "SAVINGS", 175000.0, "B010"),
    ("A011", "BC001", "CURRENT", 340000.0, "B001"),
    ("A012", "BC003", "SAVINGS", 92000.0, "B003"),
], "account_id string, customer_id string, account_type string, balance double, branch_id string")

bank_transactions = make_df([
    ("T001", "A001", date(2026, 1, 3), "UPI_DEBIT", 4500.0, "SUCCESS"),
    ("T002", "A002", date(2026, 1, 5), "NEFT_CREDIT", 75000.0, "SUCCESS"),
    ("T003", "A003", date(2026, 1, 8), "RTGS_DEBIT", 225000.0, "SUCCESS"),
    ("T004", "A004", date(2026, 1, 11), "ATM_DEBIT", 10000.0, "SUCCESS"),
    ("T005", "A005", date(2026, 1, 14), "NEFT_CREDIT", 350000.0, "SUCCESS"),
    ("T006", "A006", date(2026, 1, 18), "UPI_DEBIT", 2500.0, "FAILED"),
    ("T007", "A007", date(2026, 1, 22), "IMPS_CREDIT", 18000.0, "SUCCESS"),
    ("T008", "A008", date(2026, 1, 28), "UPI_DEBIT", 6500.0, "SUCCESS"),
    ("T009", "A009", date(2026, 2, 1), "RTGS_DEBIT", 410000.0, "SUCCESS"),
    ("T010", "A010", date(2026, 2, 4), "NEFT_CREDIT", 90000.0, "SUCCESS"),
    ("T011", "A011", date(2026, 2, 7), "NEFT_DEBIT", 85000.0, "SUCCESS"),
    ("T012", "A012", date(2026, 2, 10), "UPI_CREDIT", 12000.0, "SUCCESS"),
    ("T013", "A001", date(2026, 2, 12), "ATM_DEBIT", 15000.0, "SUCCESS"),
    ("T014", "A003", date(2026, 2, 15), "NEFT_CREDIT", 125000.0, "SUCCESS"),
    ("T015", "A005", date(2026, 2, 18), "RTGS_DEBIT", 275000.0, "SUCCESS"),
    ("T016", "A009", date(2026, 2, 21), "NEFT_CREDIT", 210000.0, "SUCCESS"),
], "transaction_id string, account_id string, transaction_date date, transaction_type string, amount double, transaction_status string")

bank_branches = make_df([
    ("B001", "Mumbai Fort", "Mumbai", "MH"), ("B002", "Bengaluru MG Road", "Bengaluru", "KA"),
    ("B003", "Ahmedabad Central", "Ahmedabad", "GJ"), ("B004", "Hyderabad Banjara", "Hyderabad", "TS"),
    ("B005", "Delhi Connaught", "Delhi", "DL"), ("B006", "Kochi Marine", "Kochi", "KL"),
    ("B007", "Kolkata Park", "Kolkata", "WB"), ("B008", "Lucknow Hazratganj", "Lucknow", "UP"),
    ("B009", "Pune Camp", "Pune", "MH"), ("B010", "Jaipur C-Scheme", "Jaipur", "RJ"),
], "branch_id string, branch_name string, city string, state string")

bank_loans = make_df([
    ("L001", "BC001", "HOME", 4200000.0, 8.45, "ACTIVE"),
    ("L002", "BC002", "VEHICLE", 850000.0, 9.10, "ACTIVE"),
    ("L003", "BC003", "BUSINESS", 7500000.0, 10.25, "ACTIVE"),
    ("L004", "BC004", "PERSONAL", 350000.0, 12.50, "CLOSED"),
    ("L005", "BC005", "BUSINESS", 12000000.0, 9.75, "ACTIVE"),
    ("L006", "BC006", "HOME", 3100000.0, 8.30, "ACTIVE"),
    ("L007", "BC008", "PERSONAL", 500000.0, 13.25, "DELINQUENT"),
    ("L008", "BC010", "VEHICLE", 1100000.0, 9.00, "ACTIVE"),
], "loan_id string, customer_id string, loan_type string, loan_amount double, interest_rate double, loan_status string")

bank_credit_cards = make_df([
    ("CC001", "BC001", "GOLD", 200000.0, 45000.0),
    ("CC002", "BC002", "CLASSIC", 100000.0, 12000.0),
    ("CC003", "BC003", "PLATINUM", 500000.0, 175000.0),
    ("CC004", "BC004", "CLASSIC", 75000.0, 8000.0),
    ("CC005", "BC005", "CORPORATE", 1000000.0, 420000.0),
    ("CC006", "BC006", "PLATINUM", 400000.0, 99000.0),
    ("CC007", "BC008", "GOLD", 180000.0, 135000.0),
    ("CC008", "BC010", "GOLD", 225000.0, 51000.0),
], "card_id string, customer_id string, card_type string, credit_limit double, outstanding_amount double")

lab_root = str(Path.cwd() / "pyspark_course_data")
print(f"Spark {spark.version} is ready.")
print("Retail and banking classroom DataFrames are loaded; Day 1 performs the first actions.")
'''


def build_notebook() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "course": {
            "title": "25-Day PySpark Learning Plan",
            "audience": "Data Engineer / Azure Data Engineer / PySpark Developer",
            "teaching_ratio": "30% theory / 70% practical",
        },
    }

    cells = [
        md("""
        # 25-Day PySpark Learning Plan

        **Beginner → advanced | Data Engineer • Azure Data Engineer • PySpark Developer**

        This is a complete classroom notebook built around two continuous projects:

        - **Instructor project:** Retail Sales Analytics Platform
        - **Student project:** Banking Transaction Analytics Platform

        Every day follows: **Concept → Notes → Syntax → Retail Example → Explanation → Banking Assignment → Expected Result → Interview Questions**.

        > Teaching balance: approximately 30% theory and 70% hands-on practice. Complete the notebook in order because later days intentionally reuse earlier concepts.
        """),
        md("""
        ## How to use this notebook

        1. Study one numbered day per session (about 2–3 hours).
        2. Run the **Course Lab Setup** once at the start of a fresh kernel.
        3. Predict every schema and result before running its code cell.
        4. Complete the ten retail practice questions, then the banking assignment without looking for a full solution.
        5. Keep a separate answer notebook or Git repository for your work.
        6. End each session by speaking the interview answers aloud in your own words.

        **Local prerequisites:** Java 8/11/17 (compatible with your PySpark release), Python, Jupyter, and PySpark. In managed Azure Databricks or Microsoft Fabric, use the provided Spark runtime instead of creating a local cluster.
        """),
        md("""
        ## Environment notes

        - The notebook sets Spark to `local[2]` for a laptop-friendly classroom session. Remove the local master setting when a managed platform supplies the cluster.
        - On native Windows, in-memory transformations work with a normal PySpark install, but local CSV/JSON/Parquet **writes** can require a compatible Hadoop Windows setup (`HADOOP_HOME` and `winutils.exe`). A managed Spark service, WSL/Linux environment, or an organization-approved Hadoop installation avoids that local filesystem limitation.
        - If a Spark session already exists, `getOrCreate()` reuses it. Restart the kernel after changing Spark packages or Delta extensions.
        - Day 23 requires a `delta-spark` version compatible with the active Spark runtime. Databricks runtimes usually provide Delta already.
        """),
        code("""
        # Optional local installation — uncomment only if your environment needs it.
        # %pip install pyspark
        # Day 23 only (choose a delta-spark version compatible with your PySpark runtime):
        # %pip install delta-spark
        """),
        md("""
        ## Curriculum map

        | Phase | Days | Outcome |
        |---|---:|---|
        | Foundations | 1–4 | Understand Spark, architecture, DataFrames, and data sources |
        | Core transformations | 5–9 | Select, filter, transform, clean strings, and work with dates |
        | Analytics | 10–16 | Aggregate, group, join, combine, handle nulls, and use windows |
        | Execution and engineering | 17–22 | Use UDFs/RDDs carefully, reason about DAGs, partition, optimize, and write SQL |
        | Lakehouse and projects | 23–25 | Use Delta concepts, build Bronze/Silver/Gold ETL, and finish both capstones |
        """),
        md("""
        ## Course Lab Setup

        The cell below creates realistic, small in-memory datasets. Its purpose is repeatability: all learners see the same results without downloading files. Production systems would read governed storage paths and secrets from environment-specific configuration.

        The retail tables contain roughly 10–20 records where appropriate; the banking tables are independent assignment data. Monetary values use `double` for classroom simplicity—production financial systems normally use a suitable fixed-precision `DecimalType`.
        """),
        code(DATA_SETUP),
        md("""
        ## Project progression

        ```text
        Retail raw data                    Banking raw data
              │                                  │
              ▼                                  ▼
           Bronze                             Bronze
              │                                  │
        Quality + cleaning                 Quality + cleaning
              │                                  │
              ▼                                  ▼
           Silver                             Silver
              │                                  │
        Joins + business rules            Customer + account integration
              │                                  │
        Aggregates + windows              Transactions + windows
              │                                  │
              ▼                                  ▼
            Gold                               Gold
              │                                  │
        Retail KPI pack                  Banking KPI assignment
        ```
        """),
    ]

    for spec in SPECS:
        day = spec["day"]
        cells.extend([
            md(f"""
            ---

            # Day {day} — {spec['topic']}

            **Project milestone:** {spec['retail_requirement'][0].upper() + spec['retail_requirement'][1:]}
            """),
            md("## 1. Learning Objectives\n\nBy the end of this session, you should be able to:\n\n" + "\n".join(f"- {x}" for x in objectives(spec))),
            md(f"""
            ## 2. Detailed Notes

            ### What is it?

            {spec['what']}

            ### Why do we need it?

            {spec['why']}

            ### How does it work?

            {spec['how']}

            ### What happens inside Spark?

            {spec['internal']}

            ### What happens in production?

            {spec['production']}

            ### Simple analogy

            {spec['analogy']}

            ### Performance and design note

            {spec['performance']}
            """),
            md("## 3. Important PySpark Functions\n\n" + functions_table(spec["functions"])),
            md(f"""
            ## 4. Retail Dataset — {spec['retail_dataset']}

            Primary DataFrame for today: `{spec['retail_df']}`.

            Run the inspection cell before the tutorial. `printSchema()` shows names, data types, and nullability; `show()` displays records but does not guarantee business order unless `orderBy` is used.
            """),
            code(f"{spec['retail_df']}.printSchema()\n{spec['retail_df']}.show(20, truncate=False)"),
            md(f"""
            ## 5. Retail Hands-On Tutorial

            **Business requirement**

            {spec['retail_requirement'][0].upper() + spec['retail_requirement'][1:]}

            **Plan before coding**

            {spec['approach']}
            """),
            code(spec["retail_code"]),
            md(f"""
            ### Code explanation

            - The first operation establishes the correct source and business population.
            - Column expressions remain distributed; Spark builds a plan instead of looping through rows in Python.
            - Names and output grain are made explicit so downstream users know what one row represents.
            - The final display is intentionally small; production pipelines normally validate and write the distributed result.

            ### Expected output

            {spec['expected']}

            ### Business interpretation

            {spec['interpretation']}
            """),
            md("## 6. Retail Practice Problems\n\n" + numbered(practice_questions(spec))),
            md(f"""
            ## 7. Banking Assignment

            **Dataset/schema**

            Use the notebook tables most relevant to this session: `bank_customers`, `bank_accounts`, `bank_transactions`, `bank_branches`, `bank_loans`, and `bank_credit_cards`. Inspect the exact schema before coding and use stable IDs as keys.

            **Business scenario**

            Your banking team needs a reliable result for **{spec['bank_focus']}**. Use today's concepts plus only previously taught concepts.

            **Assignment questions**

            {numbered(bank_questions(spec))}

            **Expected result requirements**

            - State the output grain (one row per what) before the code.
            - Return business-friendly column names and deterministic presentation order where needed.
            - Include record-count, key, null, and financial-total checks appropriate to the result.
            - Do not use `collect()` for the full dataset or use a concept scheduled for a later day.
            - Explain the business meaning in 3–5 sentences; screenshots alone are not a submission.

            > A complete solution is intentionally not included. Build it in your answer notebook, compare it with the stated requirements, and ask for review only after recording your own reasoning.
            """),
            md(f"""
            ## 8. Banking Challenge

            {spec['challenge']}

            **Deliverables:** a stated grain, transformation plan, PySpark implementation, expected evidence columns, two quality checks, and one scale/security consideration.
            """),
            md("## 9. Common Errors\n\n" + errors_table(spec["errors"])),
            md("## 10. Interview Questions and Short Spoken Answers\n\n" + interview_section(spec)),
            md(f"""
            ## 11. Day Summary

            - **Concepts learned:** {', '.join(spec['concepts'])}.
            - **Important functions:** {', '.join('`' + x[0] + '`' for x in spec['functions'])}.
            - **Retail problem solved:** {spec['retail_requirement']}
            - **Banking work:** you designed and validated {spec['bank_focus']} without receiving a copy-paste solution.
            - **Interview takeaway:** {spec['comparison_answer']}

            **Exit ticket:** Explain today's output grain, point to the first shuffle or action if one exists, and name one production validation you would add.
            """),
        ])

        if day == 23:
            cells.insert(-11, md("""
            ### Optional Delta-enabled local session

            Delta packages and configuration vary by Spark version. In Databricks, Delta is normally available already. Locally, install a compatible `delta-spark`, stop the existing session, restart the kernel, and create the session with `configure_spark_with_delta_pip` plus the Delta SQL extension and catalog configuration. The tutorial cell catches a missing setup so the rest of the course remains runnable.
            """))

    cells.extend([
        md("""
        ---

        # Final Project Acceptance Checklist

        ## Retail Sales Analytics Platform

        - [ ] Raw customers, products, orders, order items, stores, payments, and inventory are represented.
        - [ ] Bronze retains source values and ingestion lineage.
        - [ ] Silver has enforced keys/types, quality exceptions, and reusable integrated detail.
        - [ ] Gold publishes total/daily/monthly revenue, revenue by store/category, top products/customers, AOV, purchase frequency, product ranking, and store performance.
        - [ ] Counts and totals reconcile between layers.
        - [ ] The physical plan and partition/file strategy have been reviewed.
        - [ ] The pipeline is idempotent and has a rerun/recovery design.

        ## Banking Transaction Analytics Platform

        - [ ] Raw customers, accounts, transactions, branches, loans, and credit cards are represented.
        - [ ] Bronze, rejected-data, Silver, and Gold contracts are documented.
        - [ ] Customer-account integration and transaction fact grains are correct.
        - [ ] Gold includes total transaction amount, debit vs credit, average transaction amount, transactions/customer, branch volume, top customers, balances, loan exposure, high-value activity, and suspicious-pattern evidence.
        - [ ] Financial measures are not duplicated by joins.
        - [ ] Privacy, access, retention, and audit requirements are addressed.
        - [ ] A 10-minute interview walkthrough and a one-page architecture diagram are ready.
        """),
        md("""
        # 25-Day Outcome

        After completing both projects, you can independently build PySpark DataFrame transformations; read/write CSV, JSON, and Parquet; filter, join, aggregate, and use windows; write Spark SQL; reason about the DAG, tasks, partitions, shuffles, cache, and broadcast joins; explain Delta Lake and medallion architecture; debug common failures; and communicate design trade-offs confidently in interviews.

        **Next practice cycle:** rerun the banking capstone from a blank notebook, add automated tests for five business rules, and explain every physical-plan exchange you see.
        """),
    ])

    nb["cells"] = cells
    return nb


if __name__ == "__main__":
    notebook = build_notebook()
    nbf.validate(notebook)
    nbf.write(notebook, OUTPUT)
    print(f"Wrote {OUTPUT}")
    print(f"Cells: {len(notebook.cells)}")
