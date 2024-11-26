#Spark Job to Clean Data and Generate Insights
# Load the data from the CSV.
# Clean and transform the data (similar to what we did using Pandas).
# Generate additional data points, such as:
# Debt-to-Income Ratio: A new column derived from Monthly Debt and Annual Income.
# Categorizing customers based on their Credit Score.
# Analyzing loan distribution by purpose and home ownership status.
# Let's proceed with the Spark job implementation.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lower, mean, round
from pyspark.sql.types import IntegerType

# Initialize a SparkSession
spark = SparkSession.builder.appName("LoanDataETL").getOrCreate()

# Load the CSV file into a Spark DataFrame (Extract)
file_path = "path/to/credit_train.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Step 1: Data Cleaning (Transform)

# Normalize text columns to lowercase
df = df.withColumn("Term", lower(col("Term"))) \
       .withColumn("Home Ownership", lower(col("Home Ownership"))) \
       .withColumn("Purpose", lower(col("Purpose")))

# Handle anomalies in the 'Home Ownership' column
df = df.withColumn("Home Ownership", when(col("Home Ownership") == "havemortgage", "home mortgage")
                                        .otherwise(col("Home Ownership")))

# Impute missing values for critical numeric columns
df = df.fillna({'Credit Score': df.agg({'Credit Score': 'median'}).collect()[0][0],
                'Annual Income': df.agg({'Annual Income': 'median'}).collect()[0][0],
                'Bankruptcies': 0,
                'Tax Liens': 0})

# Drop columns with excessive missing values
df = df.drop("Months since last delinquent")

# Step 2: Generating Additional Insights

# Calculate Debt-to-Income Ratio
df = df.withColumn("Debt-to-Income Ratio", round((col("Monthly Debt") * 12) / col("Annual Income"), 2))

# Categorize customers based on Credit Score
df = df.withColumn("Credit Category", when(col("Credit Score") >= 750, "Excellent")
                                      .when((col("Credit Score") >= 700) & (col("Credit Score") < 750), "Good")
                                      .when((col("Credit Score") >= 650) & (col("Credit Score") < 700), "Fair")
                                      .when((col("Credit Score") >= 600) & (col("Credit Score") < 650), "Poor")
                                      .otherwise("Very Poor"))

# Step 3: Save the cleaned and enriched data to Parquet format (Load)
output_path = "path/to/cleaned_credit_data"
df.write.mode("overwrite").parquet(output_path)

# Stop the Spark session
spark.stop()
