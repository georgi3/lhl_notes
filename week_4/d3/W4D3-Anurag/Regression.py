# Import the packages
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor


# change the directory
os.chdir("E:\\Training\\Mindmap_Genpact\\Training_Material\\Inferential_Statistics\\Python_Hands_On")

# Read the data
mtcar = pd.read_csv("mtcars.csv",index_col=0)
car = pd.read_csv("mtcars.csv",index_col=0)
car.dtypes

# Duplicate the hp column
car["hp_copy"] = car.hp

# Creating frequency table of unique values of hp_copy column
remove = car.hp_copy.value_counts()

# identifying which value to remove
ValueToBeRemoved = remove.index[remove[0:]==2].values

# Replacing values to be removed with NA(condition is freq == 2)
car.hp_copy[car['hp_copy'].isin(ValueToBeRemoved)] = None

# checking whether values are replaced with NA
car.hp_copy

# To count number of NA in column
sum(pd.isna(car.hp_copy))

#New Data frame for Regression
car_try_regression = car

# drop "hp" column
car_try_regression=car_try_regression.drop(axis=1,columns="hp")

# rename "hp_copy" with "hp"
car_try_regression = car_try_regression.rename(columns={"hp_copy":"hp"})

# for column specific % of missing value
pd.isna(car_try_regression).mean()

# for % of missing value from entire data
pd.isna(car_try_regression).mean().mean()

# for % of missing values in each row
pd.isna(car_try_regression).mean(axis=1)

# encoding "vs" column to v-shaped and straight - engine types
car_try_regression.vs[car_try_regression.vs==0] = 'V-Shaped'
car_try_regression.vs[car_try_regression.vs==1] = 'Straight'

car_try_regression.am[car_try_regression.am==0] = 'Automatic'
car_try_regression.am[car_try_regression.am==1] = 'Manual'


####Lower Triangular Correlation Matrix to identify highest correlation with HP to be used for replacement of NA Values####
res = mtcar.corr()
res = np.tril(res)

####Plotting Cyl and HP####
import matplotlib
matplotlib.style.use('ggplot')
car_try_regression[['cyl','hp']].plot.scatter(x="cyl",y="hp")
plt.show()

####Replacing with Median as per Cyl Category - 4,6,8####
car_try_regression.hp[car_try_regression.cyl==4]
med4 = np.median(car_try_regression.hp[car_try_regression.cyl==4].dropna())
car_try_regression.hp[(car_try_regression.cyl==4) & (pd.isna(car_try_regression.hp))] = med4

car_try_regression.hp[car_try_regression.cyl==6]
med6 = np.median(car_try_regression.hp[car_try_regression.cyl==6].dropna())
car_try_regression.hp[(car_try_regression.cyl==6) & (pd.isna(car_try_regression.hp))] = med6

car_try_regression.hp[car_try_regression.cyl==8]
med8 = np.median(car_try_regression.hp[car_try_regression.cyl==8].dropna())
car_try_regression.hp[(car_try_regression.cyl==8) & (pd.isna(car_try_regression.hp))] = med8

#Define DV
#qsec = DV

#Define Hypothesis
# H0 = qsec is predicted by mpg, cyl, disp, hp, drat, wt, vs, am, gear and carb
# H1 = qsec has no relation with mpg, cyl, disp, hp, drat, wt, vs, am, gear and carb

#################################################################################
################################# Modeling ######################################
#################################################################################

###### Defining Data Types ######
car_try_regression.vs = car_try_regression.vs.astype('category')
car_try_regression.am = car_try_regression.am.astype('category')
car_try_regression.cyl = car_try_regression.cyl.astype('category')
car_try_regression.dtypes

###### Train Test Split ######
train = car_try_regression.sample(frac=0.7)
test = car_try_regression.loc[~car_try_regression.index.isin(train.index)]

###### Regression Modeling ######
multinomModel = smf.ols('qsec ~ C(cyl)+disp+wt+C(am)+carb+hp+vs',data=train).fit()
multinomModel.summary()

multinomModel = smf.ols('qsec ~ disp+wt+C(vs)+C(am)+hp',data=train).fit()
multinomModel.summary()

#### Test on Testing Data ####
predict_values = multinomModel.predict(test.drop(axis=1, columns='qsec'))

actualVsPredcit = pd.DataFrame({'actual':test.qsec,'predicted':predict_values})

correlation_accuracy = actualVsPredcit.corr()

(correlation_accuracy.iloc[0,0]+correlation_accuracy.iloc[1,1])/(correlation_accuracy.iloc[0,0]+correlation_accuracy.iloc[0,1]+correlation_accuracy.iloc[1,0]+correlation_accuracy.iloc[1,1])
