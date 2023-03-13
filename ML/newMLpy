
from pandas import read_csv
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
pd.options.display.max_rows = 9999
pd.options.display.max_columns = 9999
# load data and arrange into Pandas dataframe
df = read_csv("data.csv")
feature_names = ['OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TOV', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'PACE', 'POSS', 'PIE', 'FGM', 'FG_PCT', 'FG3M', 'FG3_PCT', 'FTM', 'FT_PCT', 'BLK', 'AVG_PTS', 'CONTEST_SHOT', 'CHARGES', 'SCREEN_AST', 'LOOSE_BALL', 'BOX_OUT', 'DAYS', 'INJ', 'GP', 'PTS', 'H/A']+['OPP_OFF_RATING', 'OPP_DEF_RATING', 'OPP_NET_RATING', 'OPP_AST_PCT', 'OPP_AST_TOV', 'OPP_AST_RATIO', 'OPP_OREB_PCT', 'OPP_DREB_PCT', 'OPP_REB_PCT', 'OPP_TM_TOV_PCT', 'OPP_EFG_PCT', 'OPP_TS_PCT', 'OPP_PACE', 'OPP_POSS', 'OPP_PIE', 'OPP_FGM', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3_PCT', 'OPP_FTM', 'OPP_FT_PCT', 'OPP_BLK', 'OPP_AVG_PTS', 'OPP_CONTEST_SHOT', 'OPP_CHARGES', 'OPP_SCREEN_AST', 'OPP_LOOSE_BALL', 'OPP_BOX_OUT', 'OPP_DAYS', 'OPP_INJ', 'OPP_GP', 'OPP_PTS', 'OPP_H/A']
#print(df.describe())
#Split into features and target (Price)
newdf = df.drop('PTS', axis = 1)
X = df.drop(['PTS'], axis = 1)
y = df['PTS'] + df['OPP_PTS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 20)


#Scale data, otherwise model will fail.
#Standardize features by removing the mean and scaling to unit variance
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


# define the model
#Experiment with deeper and wider networks
#TRY ADDING CONVOLUTIONAL LAYERS
model = Sequential()
#TRY DIFFERENT ACTIVATIONS
model.add(Dense(128, input_dim= 64, activation='relu'))
model.add(Dense(64, activation='relu'))
#Output layer
#TRY NO LINEAR ACTIVATION
model.add(Dense(1, activation='linear'))
#TRY A DIFFERENT OPTIMZER THAN ADAM
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])
model.summary()
#print(model.summary())
'''
history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs = 50)

from matplotlib import pyplot as plt
#plot the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

############################################
#Predict on test data
predictions = model.predict(X_test_scaled[:5])
print("Predicted values are: ", predictions)
print("Real values are: ", y_test[:5])
##############################################

#Comparison with other models..
#Neural network - from the current code
mse_neural, mae_neural = model.evaluate(X_test_scaled, y_test)
print('Mean squared error from neural net: ', mse_neural)
print('Mean absolute error from neural net: ', mae_neural)
'''
######################################################################
#Linear regression
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
'''
### Linear regression
lr_model = linear_model.LinearRegression()
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)
mse_lr = mean_squared_error(y_test, y_pred_lr)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
print('Mean squared error from linear regression: ', mse_lr)
print('Mean absolute error from linear regression: ', mae_lr)
'''
############################################################
### Decision tree
tree = DecisionTreeRegressor()
tree.fit(X_train_scaled, y_train)
y_pred_tree = tree.predict(X_test_scaled)
mse_dt = mean_squared_error(y_test, y_pred_tree)
mae_dt = mean_absolute_error(y_test, y_pred_tree)
print('Mean squared error using decision tree: ', mse_dt)
print('Mean absolute error using decision tree: ', mae_dt)

##############################################
#Random forest.
#Increase number of tress and see the effect
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators = 130, random_state=30)
model.fit(X_train_scaled, y_train)

y_pred_RF = model.predict(X_test_scaled)

mse_RF = mean_squared_error(y_test, y_pred_RF)
mae_RF = mean_absolute_error(y_test, y_pred_RF)
print('Mean squared error using Random Forest: ', mse_RF)
print('Mean absolute error Using Random Forest: ', mae_RF)

#Feature ranking...
import pandas as pd
feature_list = list(X.columns)
feature_imp = pd.Series(model.feature_importances_, index=feature_list).sort_values(ascending=False)
print(feature_imp)

#Mean squared error from neural net:  147.79714965820312
#Mean absolute error from neural net:  9.549633979797363
