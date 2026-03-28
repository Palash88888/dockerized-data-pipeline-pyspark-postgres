DROP TABLE IF EXISTS employees_clean;

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