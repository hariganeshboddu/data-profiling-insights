## Data Profiling Insights

Based on the initial analysis of the provided dataset, here are the key findings:

### Dataset Overview:
- **Total Records:** 100,514
- **Total Columns:** 19
- The dataset includes information on loans, customers, credit scores, income, and various financial attributes.

### Key Columns:
- **Loan ID:** Unique identifier for each loan
- **Customer ID:** Unique identifier for each customer
- **Loan Status:** Categorical data indicating loan status (e.g., Fully Paid, Charged Off)
- **Current Loan Amount:** Numeric, represents the loan amount
- **Term:** Loan term (e.g., Short Term, Long Term)
- **Credit Score, Annual Income, and Years in Current Job** provide insights into customer profiles.

### Missing Data:
- Columns like Credit Score, Annual Income, Months since last delinquent, Bankruptcies, and Tax Liens have missing values:
  - **Credit Score and Annual Income:** ~20% missing values.
  - **Months since last delinquent:** ~53% missing values.
- These missing values need to be handled during ETL processing.

### Data Types:
- **Numeric:** Current Loan Amount, Credit Score, Annual Income, etc.
- **Categorical:** Loan Status, Term, Home Ownership, Purpose, Years in Current Job.
- **Identifiers:** Loan ID, Customer ID.

---

## Recommendations for ETL and Storage

### Data Storage Design:
- **Database Choice:** Use a cloud-based data warehouse like Snowflake or Amazon Redshift for scalability, performance, and integration with BI tools.
- **Schema Design:** A star schema with a central fact table (`loan_facts`) and dimension tables (`dim_customer`, `dim_loan`, etc.) to optimize analytical queries.
- **Partitioning and Indexing:** Partition the fact table by Loan Status or Loan Term to speed up queries. Index columns like Customer ID and Loan ID to enhance lookups.

### Proposed Physical Data Model:

#### Fact Table (`loan_facts`):
- Loan ID, Customer ID, Current Loan Amount, Credit Score, Annual Income, Loan Status, Term, etc.

#### Dimension Tables:
1. **`dim_customer:`** Customer ID, Years in Current Job, Home Ownership, etc.
2. **`dim_loan:`** Loan ID, Purpose, Term, Loan Status.
3. **`dim_time:`** Date, Month, Year (for time-based analysis).

---

## ETL Pipeline Design:
1. **Extract:** Load the data from CSV files or the 3rd party API into a staging area.
2. **Transform:**
   - Handle missing values: Impute or drop based on column relevance.
   - Data type conversions: Ensure correct types (e.g., convert Years in Current Job to numeric).
   - Cleanse data: Remove duplicates, normalize categorical values, and validate ranges.
3. **Load:** Store transformed data into a data warehouse.

### Tools:
- **Apache Airflow:** For orchestrating the ETL pipeline.
- **DBT (Data Build Tool):** For transforming data within the warehouse.
- **Spark:** For scalable data processing, especially for large volumes.
- **AWS S3:** For staging raw data files before loading into the warehouse.

---

## Additional Data Profiling Insights:

### Missing Values:
- Columns with significant missing values:
  - Months since last delinquent: ~53% missing.
  - Credit Score and Annual Income: ~20% missing.
  - Bankruptcies and Tax Liens: less than 1% missing.
- We can consider imputing missing values for critical columns like Credit Score and dropping less critical ones like Months since last delinquent.

### Categorical Data Distribution:
- **Loan Status:**
  - Fully Paid: 77,361 loans (~77%).
  - Charged Off: 22,639 loans (~23%).
- **Term:**
  - Short Term: 72,208 loans (~72%).
  - Long Term: 27,792 loans (~28%).
- **Home Ownership:**
  - Majority of customers have Home Mortgage (48,410) or Rent (42,194).
  - Own Home has 9,182 customers.
  - The category "HaveMortgage" appears to be an anomaly and may require normalization.
- **Purpose of Loan:**
  - Predominantly for Debt Consolidation (78,552 loans).
  - Other common purposes include Home Improvements, Business Loan, and Buy a Car.

---

## Schema Design:

### Fact Table (`loan_facts`)

| Column Name              | Data Type | Description                                |
|--------------------------|-----------|--------------------------------------------|
| Loan ID                 | STRING    | Unique identifier for each loan            |
| Customer ID             | STRING    | Unique identifier for each customer        |
| Current Loan Amount     | DOUBLE    | Current amount of the loan                 |
| Term                    | STRING    | Loan term (e.g., short term, long term)    |
| Loan Status             | STRING    | Status of the loan (e.g., Fully Paid, Charged Off) |
| Credit Score            | INTEGER   | Customer's credit score                    |
| Annual Income           | DOUBLE    | Customer's annual income                   |
| Debt-to-Income Ratio    | DOUBLE    | Ratio of monthly debt to annual income     |
| Credit Category         | STRING    | Categorized credit score                   |
| Purpose                 | STRING    | Purpose of the loan (e.g., debt consolidation) |
| Home Ownership          | STRING    | Type of home ownership (e.g., rent, own home) |
| Monthly Debt            | DOUBLE    | Customer's monthly debt                    |
| Years of Credit History | DOUBLE    | Years of credit history                    |
| Number of Open Accounts | INTEGER   | Total number of open accounts              |
| Number of Credit Problems | INTEGER | Number of credit issues                    |
| Current Credit Balance  | DOUBLE    | Current credit balance                     |
| Maximum Open Credit     | DOUBLE    | Maximum open credit available              |
| Bankruptcies            | INTEGER   | Number of bankruptcies                     |
| Tax Liens               | INTEGER   | Number of tax liens                        |

### Dimension Tables:

1. **`dim_customer`:**
   - Attributes: Customer ID, Years in Current Job, Home Ownership, Credit Category, etc.

2. **`dim_loan`:**
   - Attributes: Loan ID, Term, Purpose, Loan Status, etc.

3. **`dim_time`:**
   - Attributes: Date, Month, Year, etc., for time-based analysis.

---

## Partitioning and Indexing Strategy:
- **Partitioning:** Fact table by Loan Status and Term to improve query performance.
- **Indexing:** Use indexes on frequently queried columns like Customer ID, Loan ID, and Credit Category.

