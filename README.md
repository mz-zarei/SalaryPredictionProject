# Data science job salary estimation model development (end-to-end project)
## Project phases:

1. Data collection (Done)
    - Over 1000 job info are scraped from Glassdoor using selenium library
    - With each job, we got the following: Job title, Salary Estimate, Job Description, Rating, Pros from reviews, Cons from reviews, Company, Location, Company Size, Company Founded Date, Type of Ownership, Industry, Sector, Revenue

2. Data cleaning
    - Parsing salary estimate texts, company name, location, states
    - Extracting new features: age, seniority level, job category, requirementes (AWS, Python, SQL, SAS)

3. Exploratory Data Analysis (EDA)
    - Distributions and value counts of features investigated
    - Linear correlation between features are analysed
    - Pivot tables are developed to get insights

![alt text](https://github.com/mz-zarei/SalaryPredictionProject/3_EDA/bar.png "Salary by Sector")
![alt text](https://github.com/mz-zarei/SalaryPredictionProject/3_EDA/pvTable.png "Salary by Position")
![alt text](https://github.com/mz-zarei/SalaryPredictionProject/3_EDA/WC.png "Word cloud of job descriptions")

4. Model training
5. Productionizing ML model

## Resources
- https://www.youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t
- https://mersakarya.medium.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905


