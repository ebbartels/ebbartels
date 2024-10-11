# +
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
# -

cars = pd.read_csv("car.data")
cars

X = cars[["buying", "maint", "doors", "persons", "lug_boot", "safety"]]
cars_knn
y = cars["class"]

# +
preprocessor = ColumnTransformer(
    transformers = [
        ("onehot", OneHotEncoder(), ["buying", "maint", "doors", "persons", "lug_boot", "safety"])
    ]
)

pipeline = Pipeline (
    steps = [
        ("preprocessor", preprocessor),
        ("KNN", KNeighborsClassifier(n_neighbors = 15))
    ]
)
# -

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


pipeline.fit(X_train, y_train)

# +
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
# -

accuracy


