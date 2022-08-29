# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mohammad Zarei
# Created Date: 17 Aug 2022
# ---------------------------------------------------------------------------
""" Train/test ML models """
# imports
#%%
from time import process_time_ns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor


import statsmodels.api as sm


data = pd.read_csv('/Users/mz/Documents/GitHub_Projects/SalaryPredProject/3_EDA/job_eda_data.csv')

# Feature selection
features = ['avg_salary',
            'rating', 'size', 'ownership', 
            'industry', 'sector', 'revenue', 
            'hourly', 'estimate_by_employer', 
            'state', 'age', 'aws', 'sql', 
            'sas', 'python', 'job_cat',
            'job_level', 'description_len']
data_model = data[features]

# Handle categorical variables using dummy variable
data_model_dummied = pd.get_dummies(data_model)


# Split train test data
X_data = data_model_dummied.drop('avg_salary', axis=1)
y_data = data_model_dummied.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)

# Fit linear regression model to check feature importance (linearly)
X_train_sm = sm.add_constant(X_train)
SM_model = sm.OLS(y_train, X_train_sm).fit()
SM_model.summary()

# Fit linear regression model as base line model

LR_model = LinearRegression().fit(X_train, y_train)
LR_model_score = np.mean(cross_val_score(LR_model, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

# Add more regularization to the LR model (L1 and L2)

LS_model = Lasso(alpha=0.11).fit(X_train, y_train)
LS_model_score= np.mean(cross_val_score(LS_model, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

## search for best alpha
scores, alphas, l1_ratios = [], [], []
for alpha in np.linspace(0.01, 1, num=20):
    LS_model = Lasso(alpha=alpha).fit(X_train, y_train)
    LS_model_score = np.mean(cross_val_score(LS_model, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))
    scores.append(LS_model_score)
    alphas.append(alpha)

df_error = pd.DataFrame(list(zip(alphas, scores)), columns=['alpha', 'score'])
# print(df_error[df_error.score == max(df_error.score)])

#%%
# plt.plot(alphas, scores)
# plt.show()
#%%
# Fit a random forest model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV

RF_model = RandomForestRegressor()
RF_model_score= np.mean(cross_val_score(RF_model, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

## Grid search for tuning the model hyperparameters
    # Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 10, stop = 500, num = 10)]
    # Metric used for criterion
criterion = ['mse', 'mae']
    # Number of features to consider at every split
max_features = ['auto', 'sqrt', 'log2']
    # Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
    # Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
bootstrap = [True, False]
    # Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


## Random search of parameters, using 3 fold cross validation, 
## search across 100 different combinations, and use all available cores
RF_randomGS = RandomizedSearchCV(estimator = RF_model, 
                                param_distributions=random_grid, 
                                n_iter = 100, cv = 3, verbose=2, 
                                random_state=42, n_jobs = -1, 
                                scoring='neg_mean_absolute_error')
## Fit and evaluate the random search model
RF_randomGS.fit(X_train, y_train)
RF_model_best = RF_randomGS.best_estimator_
RF_model_best_score = np.mean(cross_val_score(RF_model_best, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

# Fit XGBoost model
from xgboost import XGBRegressor

XG_model = XGBRegressor()

params = { 'max_depth': [3, 5, 6, 10, 15, 20],
           'learning_rate': [0.01, 0.1, 0.2, 0.3],
           'subsample': np.arange(0.5, 1.0, 0.1),
           'colsample_bytree': np.arange(0.4, 1.0, 0.1),
           'colsample_bylevel': np.arange(0.4, 1.0, 0.1),
           'n_estimators': [50, 100, 500, 1000]}
XG_randomGS = RandomizedSearchCV(estimator=XG_model,
                         param_distributions=params,
                         n_iter = 100, cv = 3, verbose=2, 
                         random_state=42, n_jobs = -1, 
                         scoring='neg_mean_absolute_error')
XG_randomGS.fit(X_train, y_train)

XG_model_best = XG_randomGS.best_estimator_
XG_model_best_score = np.mean(cross_val_score(XG_model_best, X_train, y_train, cv=3, scoring='neg_mean_absolute_error'))

# Evaluate models on test data
from sklearn.metrics import mean_absolute_error

LR_model_test_mae = mean_absolute_error(y_test, LR_model.predict(X_test))

LS_model = Lasso(alpha=0.11).fit(X_train, y_train)
LS_model_test_mae = mean_absolute_error(y_test, LS_model.predict(X_test))

RF_model_best_test_mae = mean_absolute_error(y_test, RF_model_best.predict(X_test))
XG_model_best_test_mae = mean_absolute_error(y_test, XG_model_best.predict(X_test))

print(f"MAE on Test data \n \
        Linear regression: {LR_model_test_mae}      \n \
        LASSO regression:  {LS_model_test_mae}      \n \
        Random Forest:     {RF_model_best_test_mae} \n \
        XGBoost model:     {XG_model_best_test_mae}")

# Picking the best model
import pickle
pickl = {'model': RF_model_best}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

# Load and test the Pickled model
file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

input = X_test.iloc[1,:].values.reshape(1,-1)
print(model.predict(input))