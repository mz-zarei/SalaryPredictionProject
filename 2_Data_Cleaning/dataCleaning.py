# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mohammad Zarei
# Created Date: 4 Aug 2022
# ---------------------------------------------------------------------------
"""Clean the raw collected data"""

# imports
import pandas as pd

df = pd.read_csv("/Users/mz/Documents/GitHub_Projects/SalaryPredProject/1_Data_Collection/glassdoor_jobs.csv")


# change column names
df.columns = ['title', 'salary', 'description', 'rating', 
                'company', 'location', 'size', 'founded',
                'ownership', 'industry', 'sector', 'revenue']

# Filter rows with no salary (salary=-1)
df = df[df.salary != '-1']

# Parse salary estimate column
df.salary = df.salary.apply(lambda x: x.split('(')[0])
df.salary = df.salary.apply(lambda x: x.replace('$','').replace('K',''))

df['hourly'] = df.salary.apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['estimate_by_employer'] = df.salary.apply(lambda x: 1 if 'employer' in x.lower() else 0)
df.salary = df.salary.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = df.salary.apply(lambda x: int(x.split('-')[0]))
df['min_salary'] = df.apply(lambda x: x.min_salary*2 if x.hourly==1 else x.min_salary, axis=1)  # convert hourly to yearly

df['max_salary'] = df.salary.apply(lambda x: int(x.split('-')[1] if '-' in x else int(x)))
df['min_salary'] = df.apply(lambda x: x.min_salary*2 if x.hourly==1 else x.min_salary, axis=1)  # convert hourly to yearly

df['avg_salary'] = (df.min_salary + df.max_salary)/2

# Parse company name text
df.company = df.apply(lambda x: x.company if x['rating'] < 0 else x.company.split('\n')[0], axis=1)

# Parse location text
df['state'] = df.apply(lambda x: x.location[-2:].upper(), axis=1)
# df.state.value_counts()

# Find the age of companies
df['age'] = df.founded.apply(lambda x: 2022 - int(x))

# Extract impotant data from job description
df['aws'] = df.description.apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['sql'] = df.description.apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['sas'] = df.description.apply(lambda x: 1 if 'sas' in x.lower() else 0)
df['python'] = df.description.apply(lambda x: 1 if 'python' in x.lower() else 0)

df.to_csv('./glassdoor_jobs_cleaned.csv', index=False)