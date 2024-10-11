#!/usr/bin/env python
# coding: utf-8
# %%
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import os
import pandas as pd


# %%
math_path = os.path.join("student_data", "student-mat.csv")
portuguese_path = os.path.join("student_data", "student-por.csv")
math_csv = pd.read_csv(math_path,sep=";")
portuguese_csv = pd.read_csv(portuguese_path,sep = ";")

# %%
math_csv.head()

# %%
portuguese_csv.head()

# %%
# using school, age, ssex, traveltime, studytime, freetime, absences, failures
# predicting G1, G2, G3

# %%
math_csv = math_csv[["age", "traveltime","studytime", "absences", "failures", "G1", "G2", "G3"]]
portuguese_csv = portuguese_csv[["age", "traveltime","studytime", "absences", "failures", "G1", "G2", "G3"]]

# %%
math_csv.head()

# %%
portuguese_csv.head()

# %%
math_train, math_test = train_test_split(math_csv, test_size = 0.1)
portuguese_train, portuguese_test = train_test_split(portuguese_csv, test_size = 0.1)

# %%
math_reg = LinearRegression()
port_reg = LinearRegression()
X = ["age", "traveltime", "studytime","absences", "failures", "G1", "G2"]
y = ["G3"]

# %%
math_reg.fit(math_train[X], math_train[y])
math_reg.score(math_test[X], math_test[y])

# %%
port_reg.fit(portuguese_train[X], portuguese_train[y])
port_reg.score(portuguese_test[X], portuguese_test[y])

# %%
lin_model = LinearRegression()

math_cvs = cross_val_score(lin_model, math_train[X], math_train[y], cv =5)
print(math_cvs.mean(), math_csv.std())

# %%
lin_model = LinearRegression()

por_cvs = cross_val_score(lin_model, portuguese_train[X], portuguese_train[y], cv =5)
print(por_cvs.mean(), por_cvs.std())

# %%
