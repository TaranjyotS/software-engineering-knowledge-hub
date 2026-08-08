# Data Engineering, ETL, Big Data & Analytics

> **Purpose:** Transaction datasets, Pandas, ETL pipelines, data quality, batch/streaming, lineage, lakehouse, S3, Delta Lake, PySpark, and analytics architecture.
> **Use this file for:** data engineering, backend data pipeline, and analytics engineering interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

This is a new topic file created because the attached repository files did not have a dedicated Markdown page for this subject. It is merged from the organized topic-wise interview-prep pack and follows the same repository style as the existing notes.

---

## Consolidated Interview Questions & Technical Notes

The section below is merged from the previously organized topic-wise interview-prep pack so the repository keeps the detailed technical Q&A in one place.

> Transaction datasets, Pandas, ETL pipelines, data quality, batch/streaming/micro-batch, data lineage, lakehouse, Delta Lake, PySpark, analytics, and reporting architecture.

### Topic Sections

1. Big Data, PySpark & Data Engineering — `Interview_Prep_Topics_and_Questions.md`
2. Document Parsing, OCR & PDF Processing — `Interview_Prep_Topics_and_Questions.md`
3. Data Visualization — `Interview_Prep_Topics_and_Questions.md`
4. Transaction Dataset Schema — `transaction_etl_sql_data_engineering_interview_handbook.md`
5. Python / Pandas Data Handling — `transaction_etl_sql_data_engineering_interview_handbook.md`
6. Data Quality — `transaction_etl_sql_data_engineering_interview_handbook.md`
7. Data Engineering / ETL Pipelines — `transaction_etl_sql_data_engineering_interview_handbook.md`
8. Batch, Streaming & Micro-Batch Processing — `transaction_etl_sql_data_engineering_interview_handbook.md`
9. Architecture Design Considerations — `transaction_etl_sql_data_engineering_interview_handbook.md`
10. Data Lineage — `transaction_etl_sql_data_engineering_interview_handbook.md`
11. Storage Model Design — `transaction_etl_sql_data_engineering_interview_handbook.md`
12. Amazon S3 Performance Optimization — `transaction_etl_sql_data_engineering_interview_handbook.md`
13. Delta Lake & Lakehouse Architecture — `transaction_etl_sql_data_engineering_interview_handbook.md`
14. Incremental Loads — `transaction_etl_sql_data_engineering_interview_handbook.md`
15. Common Interview Follow-Ups — `transaction_etl_sql_data_engineering_interview_handbook.md`
16. Data Engineering & Large Datasets — `ML_AI_Systems_Interview_Prep_Handbook.md`

---

### 10. Big Data, PySpark & Data Engineering
#### 10.1 Big data frameworks

**Interview answer:**

> Big data frameworks enable distributed processing and storage of very large datasets across clusters. They provide scalability, fault tolerance, and parallel computation.

Common tools:

- Apache Spark
- Hadoop/HDFS
- Kafka
- Flink
- Hive

---

#### 10.2 Apache Spark / PySpark

**Interview answer:**

> PySpark is the Python API for Apache Spark. It allows us to process large datasets in a distributed way across multiple machines. Spark splits data into partitions and processes them in parallel across executors coordinated by a driver program.

##### Architecture

```text
Driver Program
   ↓
Cluster Manager
   ↓
Executors
   ↓
Tasks on Partitions
```

---

#### 10.3 Transformations vs Actions
##### Transformations are lazy

```python
df.filter(...)
df.select(...)
df.groupBy(...)
```

##### Actions trigger execution

```python
df.show()
df.count()
df.collect()
df.write.parquet(...)
```

---

#### 10.4 Narrow vs Wide Transformations

| Narrow                    | Wide                                     |
| ------------------------- | ---------------------------------------- |
| No shuffle                | Requires shuffle                         |
| `select`, `filter`, `map` | `groupBy`, `join`, `distinct`, `orderBy` |
| Cheaper                   | More expensive                           |

**Answer:**

> Narrow transformations do not require data movement across partitions. Wide transformations require shuffle, which is expensive because data moves across executors.

---

#### 10.5 Repartition vs Coalesce

| Method          | Meaning                                        |
| --------------- | ---------------------------------------------- |
| `repartition()` | Increase/decrease partitions with shuffle      |
| `coalesce()`    | Usually reduce partitions without full shuffle |

---

#### 10.6 Broadcast Join

Use when one table is small enough to fit in executor memory.

```python
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_df), "user_id", "left")
```

**Answer:**

> Broadcast joins avoid shuffling the large table by sending the small table to every executor.

---

#### 10.7 Skew Handling

If one key has too many rows, one partition becomes a bottleneck.

Solutions:

- Enable AQE
- Broadcast small table
- Salt hot keys
- Repartition by join key
- Pre-aggregate before join

##### Skew detection SQL

```sql
SELECT join_key, COUNT(*) AS cnt
FROM table_name
GROUP BY join_key
ORDER BY cnt DESC;
```

---

#### 10.8 PySpark Rolling GMV Example

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.functions import broadcast

## Daily GMV per product
daily_gmv = (
    transactions
    .groupBy("product_id", "txn_date")
    .agg(F.sum("amount").alias("daily_gmv"))
)

## 7-day rolling GMV
w = (
    Window
    .partitionBy("product_id")
    .orderBy(F.col("txn_date").cast("timestamp"))
    .rowsBetween(-6, 0)
)

rolling_gmv = daily_gmv.withColumn(
    "rolling_7d_gmv",
    F.sum("daily_gmv").over(w)
)

## Join users using broadcast if users is small
joined = transactions.join(
    broadcast(users),
    "user_id",
    "inner"
)

country_gmv = (
    joined
    .groupBy("country", "txn_date")
    .agg(F.sum("amount").alias("gmv"))
)
```

---

#### 10.9 Spark bottleneck troubleshooting

**Answer:**

> I would inspect the physical plan, use the Spark UI to identify slow stages, check shuffle read/write, skewed partitions, task duration, and executor memory. Then I would test targeted optimizations such as broadcast joins, partition tuning, AQE, caching reused DataFrames, and salting skewed keys.

---

### 12. Document Parsing, OCR & PDF Processing
#### 12.1 Document Parsing

**Interview answer:**

> Document parsing is the process of extracting structured and meaningful information from unstructured or semi-structured documents such as PDFs, Word files, scanned images, emails, and spreadsheets. In AI systems, parsing is usually the first step before cleaning, chunking, embedding, and indexing for RAG.

##### Pipeline

```text
Documents
   ↓
Text Extraction / OCR
   ↓
Cleaning
   ↓
Chunking
   ↓
Metadata Extraction
   ↓
Embeddings
   ↓
Vector Database
   ↓
RAG / AI Agent
```

---

#### 12.2 When to use OCR

Use OCR when content is not machine-readable:

- Scanned PDFs
- Images
- Receipts
- Invoices
- Handwritten forms
- Screenshots

Do **not** use OCR when the PDF already has selectable text. Direct extraction is faster and more accurate.

---

#### 12.3 How OCR works
##### OCR pipeline

```text
Scanned Image/PDF
   ↓
Image Preprocessing
   ↓
Text Detection
   ↓
Character Recognition
   ↓
Post-processing
   ↓
Structured Text
```

##### Steps

1. Convert image to grayscale
2. Remove noise
3. Correct rotation/deskew
4. Detect text regions
5. Recognize characters/words
6. Clean and structure extracted text

Tools:

- Tesseract
- AWS Textract
- Azure AI Document Intelligence
- Google Document AI

---

#### 12.4 PyPDF2 / pypdf

**Interview answer:**

> PyPDF2, now commonly maintained as pypdf, is a Python library for reading and manipulating PDFs. It can extract text from text-based PDFs, merge and split PDFs, rotate pages, and read metadata. It does not perform OCR, so scanned PDFs require OCR tools.

##### Example

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

for page in reader.pages:
    text = page.extract_text()
    print(text)
```

##### Limitations

- Poor for scanned PDFs
- Limited for complex layouts
- Not ideal for tables
- No OCR support

---

### 14. Data Visualization
#### 14.1 What is Data Visualization?

**Interview answer:**

> Data visualization is the process of representing data graphically so that trends, patterns, correlations, anomalies, and performance issues can be understood quickly.

---

#### 14.2 Common visualization types

| Chart Type   | Use Case                       |
| ------------ | ------------------------------ |
| Bar chart    | Compare categories             |
| Line chart   | Show trends over time          |
| Pie chart    | Show proportions               |
| Scatter plot | Show relationships/correlation |
| Box plot     | Show distributions/outliers    |
| Heatmap      | Show intensity or correlations |

---

#### 14.3 Visualization for AI Systems

Useful dashboard metrics:

- API latency
- Token usage
- Cost per user/team
- Hallucination rate
- Retrieval precision
- Tool failure rate
- User feedback
- Error rates
- Model performance over time

Tools:

- Matplotlib
- Plotly
- Power BI
- Tableau
- Grafana
- CloudWatch dashboards

---

### 1. Transaction Dataset Schema

The interview scenario used a transaction dataset with columns similar to the following:

| Column Name        |           Type | Description                                                               |
| ------------------ | -------------: | ------------------------------------------------------------------------- |
| `transaction_id`   |         string | Unique transaction identifier                                             |
| `customer_id`      |         string | Customer identifier                                                       |
| `product_id`       |         string | Product identifier                                                        |
| `category`         |         string | Product category                                                          |
| `amount`           |          float | Transaction amount                                                        |
| `quantity`         |            int | Number of items purchased                                                 |
| `discount`         |          float | Discount applied on transaction                                           |
| `payment_method`   |         string | Payment mode such as card, UPI, cash, wallet                              |
| `transaction_date` | date/timestamp | Date/time of transaction                                                  |
| `region`           |         string | Customer or transaction region                                            |
| `status`           |         string | Transaction status, for example `SUCCESS`, `FAILED`, `PENDING`, or `PAID` |

#### Sample Records

| transaction_id | customer_id | product_id | category    | amount | quantity | discount | payment_method | transaction_date | region | status  |
| -------------- | ----------- | ---------- | ----------- | -----: | -------: | -------: | -------------- | ---------------- | ------ | ------- |
| T001           | C01         | P101       | Electronics |   1000 |        1 |      100 | Card           | 2026-06-01       | Mumbai | SUCCESS |
| T002           | C02         | P102       | Fashion     |   2000 |        2 |      150 | UPI            | 2026-06-01       | Delhi  | SUCCESS |
| T003           | C01         | P103       | Grocery     |    500 |        1 |       50 | Cash           | 2026-06-02       | Mumbai | FAILED  |
| T004           | C03         | P104       | Electronics |   1500 |        1 |      200 | Card           | 2026-06-02       | Pune   | SUCCESS |

#### First-Level Analysis Covered

For this dataset, the discussion covered:

- Loading data into a DataFrame or SQL table
- Validating schema
- Handling missing or invalid values
- Calculating revenue
- Grouping data by region/category/customer
- Adding derived columns such as `final_amount`
- Designing data quality checks
- Designing cloud ETL pipelines
- Writing SQL for analytical questions

---

### 2. Python / Pandas Data Handling
#### 2.1 Add a New Column
##### Interview Question

> **“How do you add a new column?”**

A sensible derived column for this dataset is `final_amount`.

```python
import pandas as pd

df["final_amount"] = df["amount"] - df["discount"]
```

##### Example

| transaction_id | amount | discount | final_amount |
| -------------- | -----: | -------: | -----------: |
| T001           |   1000 |      100 |          900 |
| T002           |   2000 |      150 |         1850 |
| T003           |    500 |       50 |          450 |

##### Interview Answer

> “I would create a derived column using vectorized Pandas operations. For example, `final_amount = amount - discount`. This is efficient because Pandas applies the operation across the full column instead of looping row by row.”

---

#### 2.2 Add Date-Based Columns

If asked to create features from the transaction date:

```python
df["transaction_date"] = pd.to_datetime(df["transaction_date"])
df["purchase_year"] = df["transaction_date"].dt.year
df["purchase_month"] = df["transaction_date"].dt.month
df["purchase_day"] = df["transaction_date"].dt.day
```

Useful derived columns:

| New Column       | Purpose                      |
| ---------------- | ---------------------------- |
| `final_amount`   | Actual amount after discount |
| `purchase_year`  | Year-level reporting         |
| `purchase_month` | Monthly reporting            |
| `purchase_day`   | Daily reporting              |
| `is_successful`  | Flag successful transactions |

Example:

```python
df["is_successful"] = df["status"].eq("SUCCESS")
```

---

#### 2.3 Handling Missing Values
##### Interview Question

> **“How do you handle missing values in this dataset?”**

The correct approach depends on the **business meaning** of the column.

```python
missing_summary = df.isnull().sum()
print(missing_summary)
```

#### Column-Level Missing Value Strategy

| Column             | Handling Strategy                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| `transaction_id`   | Critical. Drop/reject/quarantine because it should be unique and mandatory.                       |
| `customer_id`      | Important. Retrieve from source if possible; otherwise mark as `Unknown` only if business allows. |
| `product_id`       | Important. Retrieve from product master; otherwise reject/quarantine.                             |
| `category`         | Derive from product master; otherwise fill as `Unknown`.                                          |
| `amount`           | Critical. Do not blindly impute. Investigate or quarantine.                                       |
| `quantity`         | Important. Infer from order detail if possible; otherwise use median only if acceptable.          |
| `discount`         | Usually optional. Fill with `0` if missing means no discount was applied.                         |
| `payment_method`   | Fill as `Unknown` if missing.                                                                     |
| `transaction_date` | Critical. Retrieve from source or reject/quarantine.                                              |
| `region`           | Derive from customer profile if available; otherwise fill as `Unknown`.                           |
| `status`           | Investigate. Sometimes missing can become `PENDING`, but only if business confirms.               |

##### Pandas Example

```python
## Fill optional columns
df["discount"] = df["discount"].fillna(0)
df["payment_method"] = df["payment_method"].fillna("Unknown")
df["region"] = df["region"].fillna("Unknown")

## Drop or quarantine records missing critical fields
df_clean = df.dropna(subset=[
    "transaction_id",
    "amount",
    "transaction_date"
])
```

##### Interview Answer

> “I classify columns into critical and non-critical fields. For critical fields such as transaction ID, amount, and transaction date, I would investigate the source or quarantine/drop the records if they are very few. For non-critical fields like discount or payment method, I would apply business-driven imputation.”

---

#### 2.4 Handling the Discount Column
##### Interview Question

> **“How do you handle missing values in the discount column?”**

##### Strong Answer

> “For the discount column, I would first understand the business meaning. Since discount is optional, a missing discount often means no discount was applied. If the business confirms that assumption, I would replace missing values with zero. I would not use mean or median because discount has a business meaning, and average discount could distort revenue calculations.”

##### Code

```python
df["discount"] = df["discount"].fillna(0)
df["final_amount"] = df["amount"] - df["discount"]
```

##### Why Not Mean/Median?

Avoid this for discount unless business explicitly asks for statistical imputation:

```python
df["discount"] = df["discount"].fillna(df["discount"].mean())
```

Why? Because it may incorrectly reduce revenue by applying an artificial discount.

##### Better Rule

```text
Missing discount = 0 only if business confirms missing means “no discount applied”.
```

---

#### 2.5 Basic Data Validation in Pandas

```python
## Duplicate transaction IDs
duplicate_transactions = df[df["transaction_id"].duplicated()]

## Invalid amount
invalid_amounts = df[df["amount"] <= 0]

## Invalid quantity
invalid_quantities = df[df["quantity"] <= 0]

## Invalid discount
invalid_discounts = df[df["discount"] < 0]

## Discount greater than amount
discount_exceeds_amount = df[df["discount"] > df["amount"]]

## Invalid status
allowed_statuses = ["SUCCESS", "FAILED", "PENDING", "PAID"]
invalid_statuses = df[~df["status"].isin(allowed_statuses)]

## Invalid dates
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
invalid_dates = df[df["transaction_date"].isnull()]
```

---

### 4. Data Quality
#### 4.1 Data Quality Dimensions
##### Interview Question

> **“How do you find data quality in this case?”**

A strong answer uses these dimensions:

| Dimension            | Meaning                            | Example                                               |
| -------------------- | ---------------------------------- | ----------------------------------------------------- |
| Completeness         | Required fields are populated      | `transaction_id`, `amount`, `date` should not be null |
| Uniqueness           | No duplicate business keys         | `transaction_id` should be unique                     |
| Validity             | Values follow allowed format/range | `amount > 0`, `quantity > 0`                          |
| Consistency          | Related fields do not contradict   | `discount <= amount`                                  |
| Accuracy             | Data matches trusted source        | Revenue matches finance system                        |
| Timeliness/Freshness | Data arrives on time               | Daily file arrives before SLA                         |
| Integrity            | References exist in master data    | `customer_id` exists in customer table                |

---

#### 4.2 Column-Level Data Quality Rules

| Column             | Data Quality Rule                                                     |
| ------------------ | --------------------------------------------------------------------- |
| `transaction_id`   | Not null, unique                                                      |
| `customer_id`      | Not null, exists in customer master                                   |
| `product_id`       | Not null, exists in product master                                    |
| `amount`           | Not null, greater than 0                                              |
| `quantity`         | Greater than 0                                                        |
| `discount`         | Greater than or equal to 0 and less than or equal to amount           |
| `payment_method`   | Must be from allowed values                                           |
| `transaction_date` | Valid date, not in future                                             |
| `region`           | Valid known region or `Unknown`                                       |
| `status`           | Must be allowed status such as `SUCCESS`, `FAILED`, `PENDING`, `PAID` |

##### SQL Data Quality Checks

```sql
-- Missing transaction IDs
SELECT COUNT(*) AS missing_transaction_ids
FROM transactions
WHERE transaction_id IS NULL;

-- Duplicate transactions
SELECT transaction_id, COUNT(*) AS duplicate_count
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Invalid amount
SELECT *
FROM transactions
WHERE amount <= 0;

-- Discount greater than amount
SELECT *
FROM transactions
WHERE discount > amount;

-- Future transaction dates
SELECT *
FROM transactions
WHERE transaction_date > CURRENT_DATE;
```

##### Pandas Data Quality Checks

```python
quality_report = {
    "missing_transaction_id": df["transaction_id"].isnull().sum(),
    "duplicate_transaction_id": df["transaction_id"].duplicated().sum(),
    "invalid_amount": (df["amount"] <= 0).sum(),
    "invalid_quantity": (df["quantity"] <= 0).sum(),
    "invalid_discount": (df["discount"] < 0).sum(),
    "discount_gt_amount": (df["discount"] > df["amount"]).sum(),
}
print(quality_report)
```

---

#### 4.3 Automating Data Quality Checks

Useful tools/patterns:

- Great Expectations
- AWS Deequ
- Custom Pandas validation scripts
- PySpark validation jobs
- Databricks expectations / Delta Live Tables expectations

##### Interview Answer

> “In production, I would automate data quality checks and generate a report with completeness, duplicate rate, validation failures, and freshness status. If critical thresholds are breached, I would fail the pipeline or route bad records to quarantine and alert the team.”

---

### 5. Data Engineering / ETL Pipelines
#### 5.1 Simple Five-Step Data Quality Pipeline
##### Interview Question

> **“Can you design a simple five-line pipeline for this system?”**

```text
Source Systems
      ↓
Data Ingestion
      ↓
Data Quality Checks
      ↓
Cleaning / Quarantine
      ↓
Quality Report + Monitoring
      ↓
Data Warehouse / Analytics / ML
```

##### Five Steps

1. **Ingest the Data**
   Load transaction data from CSV, database, API, Kafka, or S3.

2. **Validate the Data**
   Check missing values, duplicates, invalid amount, invalid status, and discount > amount.

3. **Clean or Quarantine Invalid Records**
   Fill discount with zero if valid, standardize dates, remove duplicates, and quarantine critical bad records.

4. **Generate Data Quality Report**
   Report completeness percentage, duplicate count, failed validation count, and overall data quality score.

5. **Store and Monitor**
   Load clean data into warehouse/lakehouse and monitor for quality/freshness failures.

##### Interview Answer

> “I would build a five-step pipeline: ingest the data, validate quality rules, clean or quarantine records, generate a quality report, and load the trusted data into downstream systems with monitoring and alerts.”

---

#### 5.2 Cloud-Based ETL Pipeline
##### Interview Question

> **“How would you design the architecture to ingest data, store it in cloud, clean it, and make it available to reports?”**

```text
Source Systems
   ↓
Ingestion Layer
   ↓
Raw Cloud Storage
   ↓
Validation / Data Quality Checks
   ↓
Cleaning & Transformation
   ↓
Curated Data Warehouse / Lakehouse
   ↓
Reports / Dashboards / ML / Downstream Systems
```

##### Detailed Answer

> “I would ingest transaction data from APIs, databases, files, or Kafka. I would first land the raw data into cloud object storage such as S3, Azure Data Lake, or GCS. The raw layer is kept unchanged for audit and reprocessing.”
> “Then I would run data quality checks such as missing transaction IDs, invalid amounts, invalid discounts, invalid dates, duplicate transactions, and invalid status values.”
> “After validation, I would clean and transform the data. For example, missing discounts can be filled with zero if that matches the business rule, and `final_amount = amount - discount` can be calculated.”
> “The clean data would be stored in a curated layer or data warehouse like Snowflake, Redshift, BigQuery, or Synapse. Reports and dashboards can then use this trusted data.”

---

#### 5.3 Event-Driven Batch ETL From S3
##### Interview Question

> **“A batch file is dumped into S3. The moment S3 receives the data, the pipeline should trigger. How do you design this ETL pipeline?”**

```text
Source System
   ↓
S3 Raw Bucket
   ↓
S3 Event Notification
   ↓
Lambda / Step Functions
   ↓
Glue / Spark ETL Job
   ↓
Data Quality Checks
   ↓
S3 Curated Layer / Data Warehouse
   ↓
Reports / Dashboards / Downstream Systems
```

##### AWS-Oriented Design

| Stage         | AWS Service Example                      | Purpose                      |
| ------------- | ---------------------------------------- | ---------------------------- |
| Ingestion     | S3                                       | Store raw batch files        |
| Trigger       | S3 Event Notification                    | Detect new file arrival      |
| Orchestration | Lambda / Step Functions / Airflow        | Start and manage pipeline    |
| Processing    | AWS Glue / Spark / EMR                   | Extract, transform, validate |
| Storage       | S3 Curated / Redshift / Snowflake        | Store trusted data           |
| Reporting     | Athena / QuickSight / Power BI / Tableau | Consume transformed data     |
| Monitoring    | CloudWatch / SNS                         | Logs, metrics, alerts        |

##### Interview Answer

> “I would design it as an event-driven batch ETL pipeline. When the file lands in S3, an S3 event triggers Lambda or Step Functions, which starts a Glue or Spark job. The job reads the raw data, validates schema and business rules, cleans and transforms the records, writes bad records to quarantine, and stores clean data in Parquet format in a curated layer or warehouse. Reports then consume the curated data. I would also add logging, retry logic, monitoring, alerts, and metadata tracking.”

---

#### 5.4 Handling Bad Records / Quarantine Pattern

Do not silently delete bad records.

```text
Raw Data
   ↓
Validation
   ├── Valid Records → Curated Layer
   └── Invalid Records → Quarantine/Error Layer
```

##### Examples of Bad Records

- Missing `transaction_id`
- Invalid `amount <= 0`
- `discount > amount`
- Invalid status
- Invalid date
- Corrupt file format

##### Example S3 Layout

```text
s3://data-lake/transactions/raw/
s3://data-lake/transactions/staging/
s3://data-lake/transactions/curated/
s3://data-lake/transactions/quarantine/
```

##### Interview Answer

> “For bad records, I would move them to a quarantine or error location with the failure reason. This makes the pipeline auditable and prevents bad data from entering downstream reports.”

---

### 6. Batch, Streaming & Micro-Batch Processing
#### 6.1 Batch Processing

Batch processing means collecting data over a period and processing it together.

##### Examples

- Daily sales reports
- End-of-day reconciliation
- Monthly payroll processing
- Historical data processing

##### Tools

- Apache Spark
- AWS Glue
- Hadoop MapReduce
- Airflow
- Databricks Jobs

##### Architecture

```text
Source Systems
      ↓
S3 / Data Lake
      ↓
Airflow / Scheduler
      ↓
Spark / Glue Job
      ↓
Warehouse / Lakehouse
      ↓
BI Dashboards
```

##### Pros

- Simple architecture
- Cost-effective
- Good for large historical datasets

##### Cons

- Higher latency
- Not suitable for immediate action

---

#### 6.2 Streaming Processing

Streaming processes data continuously as soon as it arrives.

##### Examples

- Fraud detection
- Real-time transaction alerts
- Real-time dashboards
- IoT event processing

##### Tools

- Apache Kafka
- Apache Flink
- Spark Structured Streaming
- AWS Kinesis
- Kafka Streams

##### Architecture

```text
Applications / APIs
        ↓
Kafka / Kinesis
        ↓
Flink / Spark Streaming
        ↓
Real-time Validations
        ↓
Data Lake / Warehouse / Alerts
```

##### Pros

- Low latency
- Immediate insights
- Useful for real-time decisions

##### Cons

- More complex
- Higher operational overhead

---

#### 6.3 Micro-Batch Processing

Micro-batch is a hybrid model where data is processed in small time windows, such as every 30 seconds or every 1 minute.

##### Tools

- Spark Structured Streaming
- Databricks
- Some cloud-native streaming ETL frameworks

##### Example

```text
Collect events for 1 minute
      ↓
Process mini-batch
      ↓
Write output
      ↓
Repeat
```

##### Pros

- Easier than true streaming
- Near-real-time
- Good compromise between batch and streaming

##### Cons

- Has small delay
- Not suitable for strict millisecond-level latency

---

#### 6.4 When to Use Which

| Requirement                     | Recommended Approach |
| ------------------------------- | -------------------- |
| Daily finance report            | Batch                |
| Real-time fraud detection       | Streaming            |
| Near-real-time dashboard        | Micro-batch          |
| Historical analysis             | Batch                |
| Immediate customer notification | Streaming            |
| Hourly business metrics         | Batch or micro-batch |

##### Interview Answer

> “The choice depends on business latency requirements. If reports are needed daily, batch is enough. If immediate action is required, such as fraud detection, streaming is better. For near-real-time dashboards, micro-batch can be a practical compromise.”

---

#### 6.5 Lambda vs Kappa Architecture
##### Lambda Architecture

```text
Data Source
   ├── Batch Layer
   ├── Speed Layer
   └── Serving Layer
```

- Uses both batch and streaming paths.
- Good when both historical and real-time processing are needed.
- More complex because two pipelines may need to be maintained.

##### Kappa Architecture

```text
Data Source
      ↓
Streaming Pipeline
      ↓
Serving Layer
```

- Uses streaming pipeline for both real-time and reprocessing.
- Simpler architecture.
- Requires strong streaming infrastructure.

---

### 7. Architecture Design Considerations
##### Interview Question

> **“What do you keep in mind while designing this data architecture?”**

Key factors:

| Factor              | What to Think About                                |
| ------------------- | -------------------------------------------------- |
| Data Volume         | How much data is processed daily/hourly?           |
| Data Velocity       | How fast is data arriving?                         |
| Latency Requirement | Daily, hourly, near-real-time, or real-time?       |
| Data Quality        | What rules define trusted data?                    |
| Scalability         | Can the system handle growth?                      |
| Reliability         | What happens if a job fails?                       |
| Fault Tolerance     | Retries, checkpointing, dead-letter queues         |
| Security            | IAM, encryption, masking, PII controls             |
| Compliance          | Auditability, retention, governance                |
| Cost                | Avoid overengineering and optimize storage/compute |
| Observability       | Logs, metrics, lineage, alerts                     |
| Downstream Usage    | Reporting, ML, APIs, dashboards                    |

##### Interview Answer

> “While designing the architecture, I consider data volume, velocity, latency requirements, data quality, scalability, reliability, security, compliance, observability, and cost. I choose batch, streaming, or micro-batch based on business requirements, and I avoid overengineering. For example, I would not introduce Kafka if daily batch processing is sufficient.”

---

### 8. Data Lineage
##### Interview Question

> **“What is data lineage?”**

##### Definition

> **Data lineage tracks the complete journey of data from source to destination, including where it came from, what transformations were applied, and where it was consumed.**

##### Example

```text
Transactions Database
        ↓
S3 Raw Layer
        ↓
Spark / Glue Transformations
        ↓
Curated Warehouse Table
        ↓
Power BI / Tableau Dashboard
```

Lineage answers:

| Question                                | Example                                            |
| --------------------------------------- | -------------------------------------------------- |
| Where did data originate?               | Transaction database                               |
| What transformations happened?          | Deduplication, discount fill, date standardization |
| Where was it stored?                    | S3 curated layer or Snowflake table                |
| Who consumed it?                        | Finance dashboard, ML model                        |
| What breaks if a source column changes? | Impact analysis                                    |

##### Why Data Lineage Matters

1. **Impact Analysis**
   If `amount` column changes, which dashboards or models break?

2. **Root Cause Analysis**
   If revenue looks wrong, trace back through transformations.

3. **Audit and Compliance**
   Prove where customer/transaction data came from and how it was processed.

4. **Data Trust**
   Users trust reports more when they understand the data journey.

##### Tools

- Apache Atlas
- OpenLineage
- Marquez
- Microsoft Purview
- Collibra
- Informatica
- AWS Glue Data Catalog
- Databricks Unity Catalog

##### Interview Answer

> “Data lineage provides end-to-end visibility into the origin, movement, transformation, and consumption of data. It helps with impact analysis, debugging, compliance, and data governance.”

---

### 9. Storage Model Design
#### 9.1 Raw, Staging, Curated, Serving Layers
##### Interview Question

> **“How would you design the storage model?”**

```text
Source Data
   ↓
Raw Layer
   ↓
Staging Layer
   ↓
Curated Layer
   ↓
Serving / Analytics Layer
```

##### Layer Explanation

| Layer   | Purpose                                     |
| ------- | ------------------------------------------- |
| Raw     | Store original data unchanged               |
| Staging | Validate, clean, standardize                |
| Curated | Store trusted business-ready data           |
| Serving | Optimized for reports, dashboards, APIs, ML |

##### Example Cloud Storage Layout

```text
s3://company-data-lake/transactions/raw/year=2026/month=06/day=01/
s3://company-data-lake/transactions/staging/year=2026/month=06/day=01/
s3://company-data-lake/transactions/curated/year=2026/month=06/day=01/
s3://company-data-lake/transactions/quarantine/year=2026/month=06/day=01/
```

---

#### 9.2 Star Schema for Transactions
##### Fact Table

```text
fact_transactions
- transaction_id
- customer_id
- product_id
- date_id
- region_id
- amount
- discount
- final_amount
- quantity
- status
```

##### Dimension Tables

```text
dim_customer
- customer_id
- customer_name
- customer_segment
```

```text
dim_product
- product_id
- category
- product_name
```

```text
dim_region
- region_id
- region_name
```

```text
dim_date
- date_id
- day
- month
- quarter
- year
```

##### Why Star Schema?

- Fact table stores measurable events.
- Dimension tables store descriptive attributes.
- Easier reporting.
- Faster aggregations.
- Cleaner business model.

##### Example Query

```sql
SELECT
    r.region_name,
    d.month,
    SUM(f.final_amount) AS revenue
FROM fact_transactions f
JOIN dim_region r ON f.region_id = r.region_id
JOIN dim_date d ON f.date_id = d.date_id
WHERE f.status = 'SUCCESS'
GROUP BY r.region_name, d.month;
```

---

#### 9.3 Why Use These Layers?
##### Interview Question

> **“Why are you using these particular layers or this type of storage model?”**

##### Answer

| Component     | Why It Is Used                                         |
| ------------- | ------------------------------------------------------ |
| Raw Layer     | Auditability, reprocessing, original data preservation |
| Staging Layer | Data quality, cleaning, standardization                |
| Curated Layer | Trusted business-ready data                            |
| Serving Layer | Fast reporting and downstream consumption              |
| Star Schema   | Better analytics performance and simpler reporting     |
| S3/Data Lake  | Scalable, low-cost storage                             |
| Warehouse     | Fast SQL analytics and high concurrency                |

##### Strong Interview Answer

> “I use this layered architecture because each layer has a specific purpose. The raw layer preserves original data for audit and reprocessing. The staging layer is used for validations and transformations. The curated layer provides trusted analytics-ready data. The serving layer is optimized for dashboards and downstream systems. This separation improves reliability, maintainability, data quality, and performance.”

---

### 10. Amazon S3 Performance Optimization
##### Interview Question

> **“How do you improve S3 performance?”**

##### Key Techniques

| Optimization           | Benefit                         |
| ---------------------- | ------------------------------- |
| Prefix parallelization | Higher request throughput       |
| Multipart upload       | Faster large file uploads       |
| Parallel reads/writes  | Better throughput               |
| Parquet/ORC format     | Faster analytics queries        |
| Partitioning           | Reduces scan size               |
| Compression            | Lower storage and transfer cost |
| Avoid small files      | Better Spark/Athena performance |
| Transfer Acceleration  | Faster global uploads           |
| Right storage class    | Cost optimization               |

#### 10.1 Partitioning

Good layout:

```text
s3://transactions/year=2026/month=06/day=01/
s3://transactions/year=2026/month=06/day=02/
```

This helps query engines scan only relevant partitions.

Bad layout:

```text
s3://transactions/all_transactions.csv
```

---

#### 10.2 Use Columnar File Formats

Prefer:

- Parquet
- ORC

Avoid for large analytics workloads:

- CSV
- JSON

##### Why Parquet?

- Columnar storage
- Compression
- Predicate pushdown
- Faster scans
- Lower query cost

---

#### 10.3 Avoid Small Files Problem

Bad:

```text
100,000 files × 1 KB
```

Better:

```text
100 files × 256 MB or 1 GB
```

Small files create overhead for Spark and query engines.

---

#### 10.4 Multipart Upload

Use multipart upload for large files.

Benefits:

- Faster uploads
- Retry failed parts only
- Better network utilization

---

#### 10.5 Interview Answer

> “To optimize S3 performance, I would use proper partitioning, Parquet/ORC formats, compression, multipart upload for large files, parallel reads and writes, and avoid the small-files problem. For analytics, I would partition by columns such as date or region so Athena or Spark scans only the required data.”

---

### 11. Delta Lake & Lakehouse Architecture
#### 11.1 What is Delta Lake?
##### Interview Question

> **“What is Delta Lake?”**

##### Definition

> **Delta Lake is an open-source storage layer built on top of a data lake that adds warehouse-like capabilities such as ACID transactions, schema enforcement, schema evolution, time travel, and efficient merge/upsert operations.**

##### Traditional Data Lake Problem

```text
S3
├── transactions1.parquet
├── transactions2.parquet
├── transactions3.parquet
```

Problems:

- No ACID transactions
- Concurrent writes may corrupt data
- Updates/deletes are difficult
- No schema enforcement
- Hard to track versions

##### Delta Lake Structure

```text
S3
├── transactions/
│   ├── part-0001.parquet
│   ├── part-0002.parquet
│   └── _delta_log/
│       ├── 000000.json
│       ├── 000001.json
│       └── ...
```

The `_delta_log` tracks transaction metadata.

---

#### 11.2 Key Delta Lake Features

| Feature            | Why It Matters                         |
| ------------------ | -------------------------------------- |
| ACID Transactions  | Reliable concurrent reads/writes       |
| Schema Enforcement | Prevents bad schema from being written |
| Schema Evolution   | Allows controlled schema changes       |
| Time Travel        | Query previous versions                |
| MERGE/UPSERT       | Supports incremental loads and CDC     |
| Auditability       | Track data versions                    |

##### Time Travel Example

```python
previous_df = (
    spark.read.format("delta")
    .option("versionAsOf", 5)
    .load("/data/transactions")
)
```

##### MERGE / UPSERT Example

```sql
MERGE INTO target_transactions t
USING source_updates s
ON t.transaction_id = s.transaction_id
WHEN MATCHED THEN
    UPDATE SET *
WHEN NOT MATCHED THEN
    INSERT *;
```

---

#### 11.3 What is Lakehouse Architecture?
##### Definition

> **A Lakehouse combines the low-cost scalability of a data lake with the reliability, governance, and performance features of a data warehouse.**

```text
Sources
   ↓
Data Lake Storage
   ↓
Delta Lake / Lakehouse Tables
   ↓
SQL / BI / ML / AI Workloads
```

---

#### 11.4 Bronze, Silver, Gold Layers

| Layer  | Purpose                    | Example                   |
| ------ | -------------------------- | ------------------------- |
| Bronze | Raw data                   | `transactions_raw`        |
| Silver | Cleaned and validated data | `transactions_clean`      |
| Gold   | Business-ready aggregates  | `daily_revenue_by_region` |

##### Lakehouse Flow

```text
Kafka / API / Files
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
Dashboards / ML / Reports
```

##### Interview Answer

> “Delta Lake brings reliability to data lakes by adding ACID transactions, schema enforcement, time travel, and merge capabilities. Lakehouse architecture uses these capabilities to combine data lake flexibility with warehouse reliability. Typically, data flows through Bronze, Silver, and Gold layers to support BI, analytics, and machine learning from a single governed platform.”

---

### 12. Incremental Loads
#### 12.1 What Are Incremental Loads?
##### Interview Question

> **“What are incremental loads?”**

##### Definition

> **Incremental loading means processing only new or changed records since the last successful load instead of reprocessing the entire dataset every time.**

##### Example

If there are 100 million transactions:

| Approach         |        Records Processed |
| ---------------- | -----------------------: |
| Full Load        |          All 100 million |
| Incremental Load | Only new/changed records |

##### Benefits

- Faster processing
- Lower cost
- Less network usage
- Better scalability
- Suitable for daily/hourly pipelines

---

#### 12.2 Incremental Load Strategies
##### 1. Timestamp-Based Loading

Use `updated_at`, `created_at`, or `last_modified_at`.

```sql
SELECT *
FROM transactions
WHERE updated_at > :last_successful_load;
```

Pros:

- Simple
- Easy to implement

Cons:

- Depends on reliable timestamps
- Can miss late-arriving records if not handled carefully

---

##### 2. High Watermark

Track the highest processed ID or timestamp.

```sql
SELECT *
FROM transactions
WHERE transaction_id > :last_processed_transaction_id;
```

Works best when:

- IDs are sequential
- No backdated updates are expected

---

##### 3. Change Data Capture / CDC

CDC captures:

- Inserts
- Updates
- Deletes

Tools:

- Debezium
- AWS DMS
- Oracle GoldenGate
- Kafka Connect

Example CDC record:

```text
operation = UPDATE
transaction_id = T001
old_amount = 1000
new_amount = 900
```

---

##### 4. MERGE / UPSERT

Used in Delta Lake, Snowflake, BigQuery, Redshift, and many warehouses.

```sql
MERGE INTO target t
USING source s
ON t.transaction_id = s.transaction_id
WHEN MATCHED THEN
    UPDATE SET
        amount = s.amount,
        discount = s.discount,
        status = s.status
WHEN NOT MATCHED THEN
    INSERT (
        transaction_id,
        customer_id,
        amount,
        discount,
        status
    )
    VALUES (
        s.transaction_id,
        s.customer_id,
        s.amount,
        s.discount,
        s.status
    );
```

---

#### 12.3 Managing Incremental Loads
##### Interview Question

> **“How do you manage incremental loads?”**

##### Recommended Answer

> “I manage incremental loads using a metadata-driven watermark approach. I maintain a control table that stores the last successful load timestamp. During each run, I extract records newer than that timestamp, validate and transform them, merge them into the target, and update the watermark only after successful completion.”

#### Control Table Example

| pipeline_name   | last_successful_load | status  |
| --------------- | -------------------- | ------- |
| transaction_etl | 2026-06-10 01:00:00  | SUCCESS |

##### Extract Incremental Records

```sql
SELECT *
FROM transactions
WHERE updated_at > (
    SELECT last_successful_load
    FROM control_table
    WHERE pipeline_name = 'transaction_etl'
);
```

##### Update Watermark After Success

```sql
UPDATE control_table
SET
    last_successful_load = CURRENT_TIMESTAMP,
    status = 'SUCCESS'
WHERE pipeline_name = 'transaction_etl';
```

---

#### 12.4 Failure Handling and Idempotency
##### Important Interview Point

> **Only update the watermark after the full pipeline succeeds.**

If the job fails midway:

- Do not update watermark.
- Reprocess same batch on next run.
- Use `MERGE` to avoid duplicates.
- Keep processing idempotent.

##### Late-Arriving Data

Use overlap window:

```sql
SELECT *
FROM transactions
WHERE updated_at >= DATEADD(hour, -1, :last_successful_load);
```

Then use `MERGE` to prevent duplicates.

##### Interview Answer

> “For failure handling, I update the control table only after the pipeline completes successfully. If the job fails, the watermark remains unchanged, so the same data can be reprocessed. To avoid duplicates, I use idempotent writes such as MERGE operations. For late-arriving records, I use an overlap window and deduplicate during merge.”

---

### 14. Common Interview Follow-Ups
#### Q1. Why fill missing discount with zero?

> “Because discount is optional. If business confirms that missing means no discount was applied, zero is the correct business-driven imputation. Mean or median could distort revenue.”

---

#### Q2. What if amount is missing?

> “Amount is critical for revenue calculations. I would not blindly impute it. I would retrieve it from the source system or quarantine/drop the record depending on the business rule.”

---

#### Q3. Why use raw, staging, and curated layers?

> “Raw supports audit and replay. Staging supports validation and cleaning. Curated provides trusted, business-ready data for reports and ML.”

---

#### Q4. Why not query directly from S3 raw data?

> “Raw data may contain duplicates, missing values, invalid records, and inconsistent formats. Curated data improves trust, consistency, and performance.”

---

#### Q5. Batch or streaming for transaction data?

> “For daily reporting, batch is enough. For fraud detection or instant alerts, streaming is better. For near-real-time dashboards, micro-batch can be a practical compromise.”

---

#### Q6. How do you handle duplicate transaction IDs?

```sql
SELECT transaction_id, COUNT(*)
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;
```

Then choose a rule:

- Keep latest by `updated_at`
- Keep successful transaction
- Quarantine duplicates
- Resolve from source system

---

#### Q7. How do you ensure reports are correct?

> “I would use curated data, apply consistent business definitions, validate against source totals, track lineage, monitor data quality, and reconcile key metrics like daily revenue with finance systems.”

---

#### Q8. What is the difference between `WHERE` and `HAVING`?

| Clause   | Used For                         |
| -------- | -------------------------------- |
| `WHERE`  | Filters rows before grouping     |
| `HAVING` | Filters groups after aggregation |

Example:

```sql
SELECT customer_id, COUNT(*)
FROM transactions
WHERE status = 'PAID'
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

---

#### Q9. What is the difference between `ROW_NUMBER`, `RANK`, and `DENSE_RANK`?

| Function       | Behavior                           |
| -------------- | ---------------------------------- |
| `ROW_NUMBER()` | Unique sequence even if values tie |
| `RANK()`       | Same rank for ties, leaves gaps    |
| `DENSE_RANK()` | Same rank for ties, no gaps        |

---

#### Q10. What is the difference between full load and incremental load?

| Full Load             | Incremental Load                   |
| --------------------- | ---------------------------------- |
| Processes all records | Processes only new/changed records |
| Simpler               | More complex                       |
| Slower for large data | Faster                             |
| Higher cost           | Lower cost                         |
| Good for initial load | Good for regular pipelines         |

---

#### Q11. How do you answer a simple interviewer greeting?

If the interviewer starts with:

> “How are you doing today?”

A simple professional response:

> “I’m doing well, thank you. I appreciate the opportunity to speak with you today. How are you doing?”

---

### Data Engineering & Large Datasets

---

#### Handling Large Datasets
##### Interview Question

**How do you work with large datasets?**

##### Answer

For large datasets, avoid loading everything into memory. Use distributed processing, partitioning, efficient file formats, and incremental processing.

##### Techniques

- PySpark
- Dask
- Partitioning
- Parquet files
- Batch processing
- Streaming pipelines
- Data sampling
- Feature selection
- Indexing
- Data versioning

---

#### PySpark
##### Interview Question

**What is PySpark used for?**

##### Answer

PySpark is the Python API for Apache Spark. It is used for distributed data processing across large datasets.

##### PySpark Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("InterviewExample").getOrCreate()

df = spark.read.parquet("s3://bucket/events/")

filtered = df.filter(col("event_type") == "purchase")

result = filtered.groupBy("user_id").count()

result.show()
```

---

#### ETL Pipeline
##### Interview Question

**How would you design a simple ETL pipeline?**

##### Answer

```text
Source data
→ ingestion
→ validation
→ transformation
→ storage
→ downstream reporting/ML system
→ monitoring
```

##### Example Architecture

| Stage         | Example Tool              |
| ------------- | ------------------------- |
| Ingestion     | S3, API, Kafka            |
| Processing    | Python, Spark             |
| Storage       | S3, PostgreSQL, Data Lake |
| Orchestration | Airflow                   |
| Monitoring    | CloudWatch, Prometheus    |
| Reporting     | Dashboard, BI tool        |

---

#### Incremental Loads
##### Interview Question

**How do you manage incremental loads?**

##### Answer

Incremental loading processes only new or changed data instead of reprocessing everything.

##### Strategies

- Timestamp-based loading
- Change Data Capture
- Watermarking
- Partition-based ingestion
- Idempotent writes
- Upserts/merge operations

##### Example

```python
def get_new_records(df, last_processed_timestamp):
    return df[df["updated_at"] > last_processed_timestamp]
```

---
