# Employee Data Pipeline 🚀

## 📌 Overview
This project demonstrates a complete data pipeline that generates raw employee data, cleans and transforms it using PySpark, and loads it into a PostgreSQL database.

---

## 🛠️ Tech Stack
- Python (Data Generation)
- PySpark (Data Processing)
- PostgreSQL (Database)
- Docker (Containerization)

---

## 📂 Project Structure
employee-data-pipeline/
│
├── data/
│   └── employees_raw.csv
│
├── docker/
│   └── docker-compose.yml
│
├── scripts/
│   ├── generate_data.py
│   └── spark_job.py
│
├── sql/
│   └── create_table.sql
│
└── README.md

---

## ⚙️ Setup Instructions

### 1. Start Services
cd docker  
docker compose up -d  

---

### 2. Generate Raw Data
cd scripts  
python generate_data.py  

---

### 3. Copy Files to Spark Container
docker cp ../data/employees_raw.csv spark_app:/employees_raw.csv  
docker cp ../scripts/spark_job.py spark_app:/spark_job.py  

---

### 4. Create Database Table
docker exec -it postgres_db psql -U user -d employees_db  

Then run:
CREATE TABLE employees_clean (
 employee_id INTEGER PRIMARY KEY,
 first_name VARCHAR(50),
 last_name VARCHAR(50),
 full_name VARCHAR(100),
 email VARCHAR(100),
 email_domain VARCHAR(50),
 hire_date DATE,
 job_title VARCHAR(100),
 department VARCHAR(50),
 salary DECIMAL(10,2),
 salary_band VARCHAR(20),
 manager_id INTEGER,
 address TEXT,
 city VARCHAR(50),
 state VARCHAR(2),
 zip_code VARCHAR(10),
 birth_date DATE,
 age INTEGER,
 tenure_years DECIMAL(3,1),
 status VARCHAR(20)
);

---

### 5. Run Spark Job
docker exec -it spark_app spark-submit --packages org.postgresql:postgresql:42.7.3 /spark_job.py  

---

### 6. Verify Data
docker exec -it postgres_db psql -U user -d employees_db  

SELECT COUNT(*) FROM employees_clean;  
SELECT * FROM employees_clean LIMIT 10;  
SELECT * FROM employees_clean
WHERE salary IS NULL OR name IS NULL;
SELECT * FROM employees_clean
WHERE salary IS NULL OR name IS NULL;
ALTER TABLE employees_clean
ADD COLUMN annual_salary NUMERIC;
UPDATE employees_clean
SET annual_salary = salary * 12;
---

## 🔄 Data Pipeline Flow
1. Generate raw employee data  
2. Clean and transform using PySpark  
3. Load into PostgreSQL  

---

## ✨ Features
- Handles invalid emails and inconsistent formats  
- Removes duplicates  
- Standardizes text fields  
- Creates derived columns (full_name, age, tenure, salary_band)  
- Fully containerized setup  

---

## 🎯 Outcome
A complete ETL pipeline (Extract, Transform, Load) built using modern tools and best practices.
