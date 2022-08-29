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

<img src="https://github.com/mz-zarei/SalaryPredictionProject/blob/EDA/3_EDA/bar.png" alt="Salary by Sector" width="600"/>
<img src="https://github.com/mz-zarei/SalaryPredictionProject/blob/EDA/3_EDA/pvTable.png" alt="Salary by Position" width="600"/>
<img src="https://github.com/mz-zarei/SalaryPredictionProject/blob/EDA/3_EDA/WC.png" alt="Word cloud of job descriptions" width="500"/>


4. Model training
    - Categorical variable are converted to dummy variables
    - Linear relationship between features and target are analysed
    - Four models are trained, fine-tunned, and evaluated on test set
        - Random forest and XGboost model performed the best (MAE of about 8)
5. Productionizing ML model
    - A Falsk API endpoint is hosted on a local webserver 
    - The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary

## Resources
- Project Youtube: https://www.youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t
- Glassdor web scraper: https://mersakarya.medium.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
- Flask Productionization: https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Code ReUse
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
