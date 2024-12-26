# +
import pandas as pd
import sys
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# used chat gbt 4 to help write q5, 

# +
# steps to load data from mendota_ice.csv

#freeze_df = freeze_df[["year", "days"]]
#freeze_df = freeze_df.dropna()
#freeze_df = freeze_df.rename(columns = {"Winter":"year", "Days of Ice Cover":"days"})
#freeze_df['days'] = freeze_df['days'].astype(int)
#freeze_df = freeze_df.drop(0)
#freeze_df["year"] = freeze_df["year"].str[:4]
#freeze_df['year'] = freeze_df['year'].astype(int)
#freeze_df = freeze_df.sort_values(by = "year")

#freeze_df.to_csv("hw5.csv", index = False)
# -

# loeading data
def q1(filename):
    freeze_df = pd.read_csv(filename)

    return freeze_df


#plotting days v year
def q2(df):
    plt.plot(df["year"], df["days"])
    plt.xlabel("year")
    plt.ylabel("days")
    plt.savefig("data_plot.jpg")


#normilize x values
def q3(df):
    print("Q3")
    return_array = np.empty((len(df), 2))
    max_x = max(df["year"])
    min_x = min(df["year"])
    for i in range(len(df)):
        xi_norm = (df["year"].iloc[i] - min_x) /(max_x - min_x)
        i_array = np.array([xi_norm, 1])
        return_array[i] = i_array
    
    print(return_array)
    return return_array


# get weights w and b
def q4(X, df):
    print("Q4")
    XT_X = np.linalg.inv(np.dot(X.T  ,X))
    XT_X_XT = np.dot(XT_X, X.T)
    Y = df["days"]
    w_b = np.dot(XT_X_XT, Y)
    print(w_b)
    return w_b


# +
# computes gradinet

def compute_gradients(x, y, w, b):
    n = len(y)
    prediction = w * x + b
    diff = prediction-y
    
    gradient_w = (1/(n)) * np.sum(diff * x)
    gradient_b = (1/(n)) * np.sum(diff)
    #print(gradient_w, gradient_b)
    return gradient_w, gradient_b


# -

# computes cost
def compute_cost(x, y, w, b):
    n = len(y)
    prediction = w * x + b
    diff = prediction-y
    
    cost = (1/(2*n)) * np.sum(diff **2)
    #print(cost)
    return cost


# +
# functions to find weights through gradient descent

def q5(df, alpha, iterations):
    print("Q5a")
    
    x = np.array(df["year"])
    y = np.array(df["days"])
    weights = np.zeros(2)
    x = (x - min(x)) / (max(x) - min(x))
    history = np.zeros(iterations)
    for i in range(iterations):
        grad_w, grad_b = compute_gradients(x, y, weights[0], weights[1])
        cost = compute_cost(x, y, weights[0], weights[1])
        if i % 10 == 0:
            print(weights)
        
        weights[0] = weights[0] - alpha * grad_w
        weights[1] = weights[1] - alpha * grad_b
        
        history[i] = cost

    print("Q5b: 0.3" )
    print("Q5c: 450" )
    print("Q5d")
    
    plt.plot(history)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.savefig("loss_plot.jpg")


# -

# function to find t hat
def q6(X, x, weights):
    norm_x = (x - min(X)) / (max(X) - min(X))
    y_hat = weights[0] * norm_x + weights[1]
    print("Q6: " + str(y_hat))


# determine what sign w is and interpret
def q7(weights):
    w = weights[0]
    if w > 0:
        print("Q7a: >")
        print("Q7b: as the year increases the number of frozen days increases")
        
    elif w < 0:
        print("Q7a: <")
        print("Q7b: as the year increases the number of frozen days decreases")
        
    else:
        print("Q7a: =")
        print("Q7b: as the year increases the number of frozen days does not change")


# find when there will be zero frozen days and interpret
def q8(X, weights):
    w = weights[0]
    b = weights[1]
    x_max = max(X)
    x_min = min(X)
    left = (-1 * b * (x_max - x_min) / w) + x_min
    print("Q8a: " + str(left))
    print("Q8b: The year is 2463 which is more than 400 years from now. That is a lot of time so it is hard to know what will happen that far in the future")


# +
#file = "hw5.csv"
#df = q1(file)
#X = q3(df)
#w_b = q4(X, df)
#q5(df, 0.3, 450)
#q8(df["year"], w_b)
# -

freeze_df = q1(sys.argv[1])
q2(freeze_df)
X = q3(freeze_df)
w_b = q4(X, freeze_df)
q5(freeze_df, float(sys.argv[2]), int(sys.argv[3]))
q6(freeze_df["year"], 2023, w_b)
q7(w_b)
q8(freeze_df["year"], w_b)


