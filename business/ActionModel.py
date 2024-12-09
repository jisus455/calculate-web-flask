from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np

class ActionModel:
    model, grid_model = None, None
    X_train, x_test = None, None
    y_train, y_test = None, None

    def __init__(self, route, testsize):
        new = {"rain": 0, "no rain": 1}

        # Cargamos el dataset con numpy
        dataset = pd.read_csv(route)

        # Sanitizamos el dataset
        x = dataset.drop(labels='Rain', axis=1)
        data = np.array(x).reshape(2500,5)

        y = dataset['Rain'].apply(func=lambda x: new[x])
        target = np.array(y)

        # Separamos los datos de entrenamiento y validacion
        self.X_train, self.x_test, self.y_train, self.y_test = train_test_split(data, target, 
            test_size=float(testsize), random_state=15)

    def fitModel(self):
        # Entrenamos el modelo
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.model.fit(self.X_train, self.y_train)
    
    def getScore(self):
        # Calculamos el accuracy score
        y_predict = self.model.predict(self.x_test)
        score = accuracy_score(self.y_test, y_predict)
        return score
    
    def bestParam(self):
        # Probamos distintos parametros con el modelo
        parameters = {
            'n_neighbors': np.arange(1,22, dtype='int8'),
            'weights': ['uniform', 'distance'], 
            'algorithm': ['ball_tree', 'kd_tree', 'brute']
        }
        self.grid_model = GridSearchCV(self.model, param_grid=parameters, scoring='accuracy', cv=5)
        self.grid_model.fit(self.X_train, self.y_train)
        return self.grid_model.best_params_, self.grid_model.best_score_