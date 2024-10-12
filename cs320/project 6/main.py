from sklearn.linear_model import LinearRegression, LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler


xcol = [ "past_purchase_amt", "age", "duration"] 
ycol = ["clicked"]
        
class UserPredictor:
    def __init__(self):
        self.model =  Pipeline([
        ("pf", PolynomialFeatures(degree=2, include_bias=True)),
        ("std", StandardScaler()),
        ("lr", LogisticRegression(fit_intercept=True)),
        ])
        
    def fit(self, users, logs, click):
        df = logs[logs["url"] == "/tv.html"]
        result = df.groupby('id').agg({'date': 'first', 'duration': 'sum'}).reset_index()
        full_df = pd.merge(users, click )
        merged_df = full_df.merge(result, on='id', how='left')
        merged_df['duration'] = merged_df['duration'].fillna(0)        
        
        train, test = train_test_split(merged_df, random_state = 250, test_size = 0.01)


        self.model.fit(train[xcol], train[ycol])
        self.model.score(test[xcol], test[ycol])
        
    def predict(self, users, logs):
        df = logs[logs["url"] == "/tv.html"]
        result = df.groupby('id').agg({'date': 'first', 'duration': 'sum'}).reset_index()
        merged_df = users.merge(result, on='id', how='left')
        merged_df['duration'] = merged_df['duration'].fillna(0)

        y_pred = self.model.predict(merged_df[xcol])
        return y_pred
        
