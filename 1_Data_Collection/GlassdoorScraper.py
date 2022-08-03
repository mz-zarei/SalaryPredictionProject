
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mohammad Zarei
# Created Date: 2 Aug 2022
# version ='1.0'
# ---------------------------------------------------------------------------
"""A Selenium-based web scraper for Glassdoor job descriptions"""
# ---------------------------------------------------------------------------
# Imports

# use selenium verion 3.14
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    
    # url = "https://www.glassdoor.ca/Job/canada-data-scientist-jobs-SRCH_IL.0,6_IN3_KO7,21.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=Canada&context=Jobs&dropdown=0"
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        
        try:
            driver.find_element_by_xpath('.//*[@id="JAModal"]/div/div[2]/span').click() #clicking to the X.
            print('x out worked')
        except NoSuchElementException:
            pass

        
        time.sleep(0.5)
        
        #Going through each job in this page
        job_buttons  = driver.find_elements_by_xpath('.//*[@class="react-job-listing css-nhtksm eigr9kq0"]')
        job_buttons += driver.find_elements_by_xpath('.//*[@class="react-job-listing job-search-key-nhtksm eigr9kq0"]')
        job_buttons += driver.find_elements_by_xpath('.//*[@class="react-job-listing css-bkasv9 eigr9kq0"]')
                                                                                                                                
        print("number of job buttons in this page: ",len(job_buttons))
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try:
                job_button.click() 
                time.sleep(1)
            except:
                continue
            

            try:
                driver.find_element_by_xpath('.//*[@id="JAModal"]/div/div[2]/span').click() #clicking to the X.
                print(' x out worked')
            except NoSuchElementException:
                pass

            
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//*[@id="JDCol"]/div/article/div/div[1]/div/div/div/div/div[1]/div[1]').text
                    location = driver.find_element_by_xpath('.//*[@id="JDCol"]/div/article/div/div[1]/div/div/div/div/div[1]/div[3]').text
                    job_title = driver.find_element_by_xpath('.//*[@id="JDCol"]/div/article/div/div[1]/div/div/div/div/div[1]/div[2]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('.//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text
            except NoSuchElementException:
                salary_estimate = -1 
            
            try:
                rating = driver.find_element_by_xpath('.//*[@id="employerStats"]/div[1]/div[1]').text
            except NoSuchElementException:
                rating = -1 
            
            try:
                pros = driver.find_element_by_xpath('.//*[@id="Reviews"]/div/div/div[1]').text
                cons = driver.find_element_by_xpath('.//*[@id="Reviews"]/div/div/div[2]').text
            except NoSuchElementException:
                pros = -1 
                cons = -1

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            try:
                size = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element_by_xpath('.//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
            except NoSuchElementException:
                revenue = -1


            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Pros": pros,
            "Cons":cons,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            # add job to jobs
            
            
        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
            print("Went to next page")
        except NoSuchElementException:
            print("Couldn't got to next page. Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
