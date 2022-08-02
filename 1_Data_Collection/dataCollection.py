#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mohammad Zarei
# Created Date: 2 Aug 2022
# ---------------------------------------------------------------------------
"""Get data from Glassdoor using GlassdoorScraper module"""
import GlassdoorScraper as gs
import pandas as pd

path = "/Users/mz/Documents/GitHub_Projects/SalaryPredProject/chromedriver"
res_df = gs.get_jobs(keyword='data scientist', num_jobs=1000, verbose=False, path=path,slp_time=15)
res_df.to_csv('glassdoor_jobs.csv', index = False)
