import csv
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_employee_data(num_records=1000):
    fake = Faker('en_US')
    employees = []
    
    # 1. Base set of 1000 records
    for i in range(1, num_records + 1):
        employee_id = 1000 + i
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Mix of valid and invalid email formats
        if random.random() < 0.15: # 15% invalid emails
            email = random.choice([
                f"{first_name.lower()}.{last_name.lower()}@company", # missing domain
                f"{first_name.lower()}@{fake.word()}.com",
                f"{first_name.lower()}.{last_name.lower()}@@company.com", # double @
                "", # empty email
                f"{first_name.lower()}@.com" # invalid domain
            ])
        else:
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
            if random.random() < 0.1: # 10% uppercase emails
                email = email.upper()

        # Some future hire dates (data errors)
        if random.random() < 0.05: # 5% future hire dates
            hire_date = (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        else:
            hire_date = fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')

        job_title = random.choice(['Software Engineer', 'Data Analyst', 'Project Manager', 'HR Specialist', 'Sales Representative'])
        department = random.choice(['IT', 'Analytics', 'HR', 'Sales', 'Marketing'])
        
        # Mixed case in categorical fields
        if random.random() < 0.2:
            department = department.upper() if random.random() < 0.5 else department.lower()
            job_title = job_title.upper() if random.random() < 0.5 else job_title.lower()

        # Salary values with currency symbols and commas
        base_salary = round(random.uniform(40000, 150000), 2)
        if random.random() < 0.3: # 30% formatted salary
            salary = f"${base_salary:,.2f}"
        else:
            salary = str(base_salary)

        # Some null/empty values in non-critical fields (manager_id)
        manager_id = random.choice([2001, 2002, 2003, None])
        
        address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.postcode()
        birth_date = fake.date_of_birth(minimum_age=22, maximum_age=65).strftime('%Y-%m-%d')
        status = random.choice(['Active', 'Inactive', 'On Leave'])

        employees.append([
            employee_id, first_name, last_name, email, hire_date,
            job_title, department, salary, manager_id, address, city,
            state, zip_code, birth_date, status
        ])

    # 2. Add some duplicates (around 20 records)
    for _ in range(20):
        employees.append(random.choice(employees))

    return employees

def write_to_csv(data, filename='employees_raw.csv'):
    headers = [
        'employee_id', 'first_name', 'last_name', 'email', 'hire_date',
        'job_title', 'department', 'salary', 'manager_id', 'address', 'city',
        'state', 'zip_code', 'birth_date', 'status'
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

if __name__ == "__main__":
    employee_data = generate_employee_data(1000)
    write_to_csv(employee_data, '../data/employees_raw.csv')
    print(f"Generated employees_raw.csv with {len(employee_data)} records (including duplicates and quality issues).")
