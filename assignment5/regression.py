from sklearn.base import BaseEstimator, ClassifierMixin
from scipy.special import softmax
from sklearn.preprocessing import OneHotEncoder
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from scipy.special import softmax
from sklearn.metrics import plot_confusion_matrix


class MyLogisticReg(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.params = {}
        self.n_features = None
        self.n_class = None
        self.encoder = OneHotEncoder(sparse=False)
        self.verbose = 0

    def init_params(self, X, y):
        """Randomly initializing parameters"""
        self.n_features = X.shape[1]  # number of features
        # the matrix for slope coefficients
        self.params['coef'] = np.random.randn(self.n_features, self.n_class)
        # the y-intercept
        self.params['intercept'] = np.random.randn(1, self.n_class)
        if self.verbose:
            print("[INFO] Initialized parameters.")
            print(f"Shape of coefficient matrix: {self.params['coef'].shape}")
            print(f"Shape of intercept matrix: {self.params['intercept'].shape}")

    def get_logits(self, X, y=None):
        # logits = log(odds) = X@W + b
        if 'coef' not in self.params and y is None:
            # initialize the parameters if haven't
            # self.init_params(X)
            raise Exception("This LogisticRegression instance is not fitted yet." +
                             "Call 'fit' with appropriate arguments before using this estimator.")
        elif 'coef' not in self.params and y is not None:
            print("[INFO] The model is not fitted yet. Using random parameters.")
            self.init_params(X, y)
        return X @ self.params['coef'] + self.params['intercept']
    
    def predict_proba(self, X, y=None):
        """
        If binary classification, use sigmoid function.
        If multi-class classification, use softmax function.
        """
        if y is not None:
            # predict using randomly initialized parameters
            logits = self.get_logits(X, y)
        else:
            logits = self.get_logits(X)
            
        if self.n_class == 1:
            # binary classification uses sigmoid function
            return 1 / (1 + np.exp(-logits))
        
        # https://machinelearningmastery.com/softmax-activation-function-with-python/
        # https://stackoverflow.com/questions/43290138/softmax-function-of-a-numpy-array-by-row
        # or just scipy.special.softmax
        # minus by the max values in every row to prevent exponentials from reaching infinity
        mx = np.max(logits, axis=-1, keepdims=True)
        numerator = np.exp(logits - mx)
        denominator = np.sum(numerator, axis=-1, keepdims=True)
        return numerator / denominator

    def fit(self, X, y, learning_rate=0.05, iterations=1000, verbose=0):
        self.verbose = verbose
        
        if isinstance(X, pd.DataFrame):
            # convert Dataframe to numpy for faster computations 
            X = X.values
        if isinstance(y, pd.DataFrame):
            y = y.values
        
        # get the number of classes in the target labels
        n_classes = len(np.unique(y.flatten()))
        # set to 1 instead of 2 for binary classification, 
        #  because of how matrix multiplication works for binary classifcation
        self.n_class = n_classes if n_classes > 2 else 1
        if self.n_class > 2:
            # one-hot encode the target labels for multi-class classification
            y = self.encoder.fit_transform(y)
        
        # initialize parameters
        self.init_params(X, y)
        m = X.shape[0]  # number of samples
        
        if self.verbose:
            print("[INFO] Training ...")
        for i in range(1, iterations + 1):
            # using method for binary classification
            if self.n_class == 1:
                # make predictions by computing probability
                y_proba = self.predict_proba(X)
                # calculate the binary cross-entropy loss
                loss = - (1 / m) * np.sum(y * np.log(y_proba) \
                            + (1 - y) * np.log(1 - y_proba))
                
                # calculate gradients via derivatives
                #  with respect to loss function (refer above)
                dW = (1 / m) * (X.T @ (y_proba - y))
                db = (1 / m) * np.sum(y_proba - y)
                
            # using method for multi-class classification
            else:
                # make predictions by computing probability
                y_proba = self.predict_proba(X, y)
                # calculate the categorical cross-entropy loss.
                # Here the `y` stands for "target" (the true class labels),
                #  and the `y_proba` stands for output 
                #  (the computed probability via softmax;
                #  not the predicted class label).
                loss = - (1 / m) * np.sum(y * np.log(y_proba))

                # calculate gradients via derivatives 
                #  with respect to loss function (refer above)
                dW = (1 / m) * (X.T @ (y_proba - y))
                db = (1 / m) * np.sum((y_proba - y), axis=0, keepdims=True)
                # print(dW.shape, db.shape)
                # break

            # use gradient descent to update parameters
            # parameter = parameter - (learning_rate * derivative_of_parameter)
            self.params['coef'] -= (learning_rate * dW)
            self.params['intercept'] -= (learning_rate * db)
            
            if self.verbose and (i == 1 or i % 100 == 0):
                print(f"\nIteration {i}/{iterations}")
                print("--" * 12)
                print(f"Loss: {loss}")
                print(f"Coefficient:\n{self.params['coef']}")
                print(f"Intercept:\n{self.params['intercept']}")

    def predict(self, X, threshold=0.5):
        y_proba = self.predict_proba(X)
        if self.n_class == 1:
            y_pred = np.where(y_proba > threshold, 1, 0)
        else:
            # get the index of the max probability as the predicted class
            y_pred = np.argmax(y_proba, axis=1)
        return y_pred
    
    def predict_score(self, X, y):
        from sklearn.metrics import accuracy_score
        y_pred = self.predict(X)
        # if self.n_class > 1:
        #     # one-hot encode it first before
        #     y = self.encoder.transform(y)
        #     y = np.argmax(y, axis=1)
        return accuracy_score(y.reshape(-1), y_pred.reshape(-1))
# from scipy.special import softmax
# def softmax(x):
#     # https://stackoverflow.com/questions/43290138/softmax-function-of-a-numpy-array-by-row
#     # minus by the max values in every row to prevent exponentials from reaching infinity
#     mx = np.max(x, axis=-1, keepdims=True)
#     print(f"{mx = }")
#     print(f"{x - mx = }")
#     numerator = np.exp(x - mx)
#     denominator = np.sum(numerator, axis=-1, keepdims=True)
#     print(f"{denominator = }")
#     return numerator / denominator

# MULTI-CLASS CLASSIFICATION

X2, y2 = load_iris(return_X_y=True)
y2 = y2.reshape(-1, 1)
print(f"{X2.shape}\n{y2.shape}")
my_log_reg = MyLogisticReg()
# set verbose=1 to see the training progress
my_log_reg.fit(X2, y2, learning_rate=0.05, iterations=1500, verbose=0)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.3, random_state=42)
log_reg = LogisticRegression(penalty='none', solver='sag', multi_class='multinomial', random_state=42)
log_reg.fit(X2, y2)
print("Result in accuracy:")
print(f"My implementation\t: {my_log_reg.predict_score(X2, y2)}")
print(f"Sklearn implementation\t: {log_reg.score(X2, y2)}")

plot_confusion_matrix(my_log_reg, X2, y2, cmap='Blues', display_labels=['Healthy', 'Heart Disease'])
plt.grid(None)