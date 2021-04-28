#y-axis : 'share_price' - '5'
#x-axis : 'share_price'
import statistics
import pandas as pd
import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
#read in .csv
X = pd.read_csv("ipo_data_cleaned.csv")

#create testing and training objects
y = (X['5'] - X['share_price']) / X['share_price']
#y = maybe other single categories
X = X.drop('5', 'columns')
X = X.drop('class', 'columns')

#create lists for results
coefficients = []
mean_squared_errors = []
r2s = []
for i in range(500):

    #X = X.add()
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = None)

    #create linear regression object
    reg = LinearRegression()

    #fit using datasets
    reg.fit(X_train, y_train)

    #make predictions
    y_pred = reg.predict(X_test)

    #Append to lists
    coefficients.append(reg.coef_)
    mean_squared_errors.append(mean_squared_error(y_test, y_pred))
    r2s.append(r2_score(y_pred, y_test))

print('coefficients: \n', coefficients, '\n')
print('r2s: \n', r2s, '\n')
print('\nAvgR2:', statistics.mean(r2s))
