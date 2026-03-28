from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, initcap, regexp_replace, split, current_date, year, when

# 1. Start Spark
spark = SparkSession.builder \
    .appName("EmployeePipeline") \
    .getOrCreate()

# 2. Load CSV
df = spark.read.csv("/employees_raw.csv", header=True, inferSchema=True)

# 3. Remove duplicates
df = df.dropDuplicates(["employee_id"])

# 4. Clean names
df = df.withColumn("first_name", initcap(col("first_name"))) \
       .withColumn("last_name", initcap(col("last_name")))

# 5. Clean email
df = df.withColumn("email", lower(col("email")))
df = df.filter(col("email").rlike("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$"))

# 6. Standardize department
df = df.withColumn("department", initcap(col("department")))

# 7. Clean salary + band
df = df.withColumn("salary", regexp_replace(col("salary"), "[$,]", "").cast("double"))

df = df.withColumn(
    "salary_band",
    when(col("salary") < 60000, "Low")
    .when(col("salary") < 100000, "Medium")
    .otherwise("High")
)

# 8. Add full_name + email_domain
df = df.withColumn("full_name", col("first_name") + " " + col("last_name")) \
       .withColumn("email_domain", split(col("email"), "@")[1])

# 9. Age & tenure
df = df.withColumn("age", year(current_date()) - year(col("birth_date"))) \
       .withColumn("tenure_years", year(current_date()) - year(col("hire_date")))

# 10. Save cleaned data (optional)
df.write.mode("overwrite").csv("/home/jovyan/employees_clean", header=True)

# 11. Load into PostgreSQL
df.write \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://postgres:5432/employees_db") \
  .option("dbtable", "employees_clean") \
  .option("user", "user") \
  .option("password", "password") \
  .option("driver", "org.postgresql.Driver") \
  .mode("overwrite") \
  .save()

spark.stop()