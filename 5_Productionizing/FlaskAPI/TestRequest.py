# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29
@author: Mohammad Zarei
"""

import requests 
from TestInput import test_input

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}
data = {"input": test_input}

r = requests.get(URL,headers=headers, json=data) 

print(r.json())

