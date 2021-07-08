import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

import statsmodels.api as sm
from statsmodels.tsa.api import Holt



def evaluate(df, yhat_df, target):
    rmse = sqrt(mean_squared_error(df[target], yhat_df[target]))
    return rmse


def plot_and_eval(train, test,yhat_df, target):
    plt.figure(figsize = (15,6))
    plt.plot(train[target], label='Train')
    plt.plot(test[target], label='Test')
    plt.plot(yhat_df[target])
    plt.title(target)
    rmse = evaluate(test, yhat_df, target)
    print(target, '--rmse:{:.5f}'.format(rmse))
    plt.show()
    return rmse


def final_plot(train, test, future, target):
    plt.figure(figsize = (15,6))
    plt.plot(train[target], label='Train')
    plt.plot(test[target], label='Test')
    plt.plot(future[target])
    plt.title(target)
    plt.show()
