#model of altitudinal forest vegtetation belts in Switzerland
#author: Andreas Paul Zischg
#literature describing the implemented model
#Huber, B., Gubelmann, P., Zischg, A., Augustin, S., and Frehner, M.: Modellierung der Vegetationshöhenstufen und der Areale von Buche und Tanne für die Schweiz, Schweizerische Zeitschrift für Forstwesen, 170, 326–337, doi:10.3188/szf.2019.0326, 2019.
#Huber, B., Zischg, A., Burnand, J., Frehner, M., and Carraro, G.: Mit welchen Klimaparametern kann man Grenzen plausibel erklären, die in NaiS (Nachhaltigkeit und Erfolgskontrolle im Schutzwald) verwendet werden um Ökogramme auszuwählen?: Schlussbericht des Projektes im Forschungsprogramm "Wald und Klimawandel" des Bundesamtes für Umwelt BAFU, Bern und der Eidg. Forschungsanstalt WSL, Birmensdorf, 2015.
#Gubelmann, P., Huber, B., Frehner, M., Zischg, A., Burnand, J., and Carraro, G.: Quantifizierung und Verschie-bung der Höhenstufengrenzen sowie des Tannen- und Buchenareals in der Schweiz mit zwei Klimazukünften: Schlussbericht des Projektes «Adaptierte Ökogramme» im Forschungsprogramm «Wald und Klimawandel», ETH Zurich, Zurich, 2019.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns; sns.set()
import sys
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.pipeline import make_pipeline
from sklearn import svm
from sklearn.impute import SimpleImputer
#imp=SimpleImputer(missing_values=np.nan, strategy='most_frequent')
#from pandas.tools.plotting import scatter_matrix

# Defines how many percent of the data is used to train and test the models. Here we use 20% of the data for testing
test_ratio=0.2

#read sample data
myworkspace="D:/CCW20/GIS/samples"
samples_n_df=pd.read_csv(myworkspace+"/"+"samples_n.csv", delimiter=";")
#samples_n_negative_df=pd.read_csv(myworkspace+"/"+"samples_n_negative.csv", delimiter=";")

#attributes
#t = temperature
t_attributeslist8110=["TYYMIN8110","TYYMEAN8110","TYYMAX8110","TOCTMIN8110","TOCTMEAN8110","TOCTMAX8110","TJULMIN8110","TJULMEAN8110","TJULMAX8110","TJANMIN8110","TJANMEAN8110","TJANMAX8110","TAPRMIN8110","TAPRMEAN8110","TAPRMAX8110","TABSMIN","TABSMAX"]
t_attributeslist6190=["TYYMIN6190","TYYMEAN6190","TYYMAX6190","TOCTMIN6190","TOCTMEAN6190","TOCTMAX6190","TJULMIN6190","TJULMEAN6190","TJULMAX6190","TJANMIN6190","TJANMEAN6190","TJANMAX6190","TAPRMIN6190","TAPRMEAN6190","TAPRMAX6190","TABSMIN","TABSMAX"]
#kont = thermal continentality
kont_attributeslist=["KONTYY1800","KONTYY1400","KONTYY1000","KONTYY","KONTOCT2000","KONTOCT1800","KONTOCT1400","KONTOCT1000","KONTOCT","KONTJUL2000","KONTJUL1800","KONTJUL1400","KONTJUL1000","KONTJUL","KONTJAN2000","KONTJAN1800","KONTJAN1400","KONTJAN1000","KONTJAN","KONTJAHR2000","KONTAPR2000","KONTAPR1800","KONTAPR1400","KONTAPR1000","KONTAPR","KONTABS2000","KONTABS1000","KONTABS"]
#foehn = foehn wind
foehnh_attributeslist=["FOEHNHYY","FOEHNHOCT","FOEHNHJUL","FOEHNHJAN","FOEHNHAPR"]
#ns = precipitation = rnorm
ns_attributeslist=["NSYY","NSSEP","NSOCT","NSNOV","NSMAY","NSMAR","NSJUN","NSJUL","NSJAN","NSFEB","NSDEC","NSAUG","NSAPR","NS_JJA","NS_AMJJAS","NS_AMJJA"]
#rad = global radiation
rad_attributeslist=["GLOBRADYYW","GLOBRADJULW","GLOBRADJANW","GLOBRADAPRW", "GLOBRADOCTW"]
#lf = relative air moisture
lf_attributeslist=["MLFYY","MLFOCT","MLFJUL","MLFJAN","MLFAPR","LFOCT","LFJUL","LFJAN","LFAPR","LFYY"]

#*************************************************************
#functions
#*************************************************************
def split_train_test(data, test_ratio):
    shuffled_indices=np.random.permutation(len(data))
    test_set_size = int(len(data)*test_ratio)
    test_indices=shuffled_indices[:test_set_size]
    train_indices=shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]
def gridasciitonumpyarrayfloat(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=float)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
def gridasciitonumpyarrayint(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=int)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr

# *************************************************************
#end functions
# *************************************************************




#original linear models







#*************************************************************
#extract altitudinal vegetation level 4
#and clean data
samples_n_4_df=samples_n_df[samples_n_df.HSMAX==4]
#samples_n_4_df=samples_n_4_df.drop(['OBJECTID'], axis=1)
samples_n_4_df=samples_n_4_df.assign(CLASS=1)
imp.fit(samples_n_4_df)
samples_n_4_dfclean=pd.DataFrame(imp.transform(samples_n_4_df), columns=samples_n_4_df.columns)
#samples_n_negative_4_df=samples_n_negative_df[samples_n_negative_df.HSMAX==4]
#samples_n_negative_4_df=samples_n_negative_4_df.drop(['OBJECTID'], axis=1)
#samples_n_negative_4_df=samples_n_negative_4_df.assign(CLASS=0)
#imp.fit(samples_n_negative_4_df)
#samples_n_negative_4_dfclean=pd.DataFrame(imp.transform(samples_n_negative_4_df), columns=samples_n_negative_4_df.columns)
trainset_n_4, testset_n_4=split_train_test(samples_n_4_dfclean, test_ratio)
#trainset_n_negative_4, testset_n_negative_4=split_train_test(samples_n_negative_4_dfclean, test_ratio)
#merge positive and negative samples
#train_hs4=pd.concat([trainset_n_4,trainset_n_negative_4], ignore_index=True, sort=False)
#test_hs4=pd.concat([testset_n_4,testset_n_negative_4], ignore_index=True, sort=False)

#transform and scale the data
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion
num_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("std_scaler", StandardScaler()),])
full_pipeline=FeatureUnion(transformer_list=[("num_pipeline", num_pipeline)])
trainset_n_4_prepared=full_pipeline.fit_transform(trainset_n_4)
trainset_n_4_prepared_df=pd.DataFrame(trainset_n_4_prepared, columns=testset_n_4.columns)
testset_n_4_prepared=full_pipeline.fit_transform(testset_n_4)
testset_n_4_prepared_df=pd.DataFrame(testset_n_4_prepared, columns=testset_n_4.columns)
#***********************************************
#test the linear regressor
X=trainset_n_4_prepared_df[["NS_AMJJA","KONTAPR1400","ETAETP","FOEHNHYY","GLOBRADYYW"]].to_numpy()
y=trainset_n_4.TYYMEAN8110.values
labels=trainset_n_4.CLASS.values.astype(int)
Xtest=testset_n_4_prepared_df[["NS_AMJJA","KONTAPR1400","ETAETP","FOEHNHYY","GLOBRADYYW"]].to_numpy()
ytest=testset_n_4.TYYMEAN8110.values
labelstest=testset_n_4.CLASS.values.astype(int)
from sklearn.linear_model import LinearRegression
lin_reg= LinearRegression()
lin_reg.fit(X,y)
#test on training set
from sklearn.metrics import mean_squared_error
hs4_predictions=lin_reg.predict(X)
lin_mse=mean_squared_error(y,hs4_predictions)
lin_rmse=np.sqrt(lin_mse)
lin_rmse
np.std(y)
#**********************************************
#test Decision Tree Regressor
from sklearn.tree import DecisionTreeRegressor
tree_reg=DecisionTreeRegressor()
tree_reg.fit(X,y)
hs4_predictions=tree_reg.predict(X)
tree_mse=mean_squared_error(y,hs4_predictions)
tree_rmse=np.sqrt(tree_mse)
tree_rmse
#cross validation
from sklearn.model_selection import cross_val_score
scores=cross_val_score(tree_reg, X, y, scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores=np.sqrt(-scores)
scores
scores.mean()
#**********************************************
#test Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
forest_reg=RandomForestRegressor()
forest_reg.fit(X, y)
hs4_predictions=forest_reg.predict(X)
forest_mse=mean_squared_error(y,hs4_predictions)
forest_rmse=np.sqrt(forest_mse)
forest_rmse
#evaluate on test set
hs4_predictionstest=forest_reg.predict(Xtest)
forest_mse=mean_squared_error(ytest,hs4_predictionstest)
forest_rmse=np.sqrt(forest_mse)
forest_rmse
#store the model
from sklearn.externals import joblib
joblib.dump(forest_reg, myworkspace+"/"+"randomforestmodel_hs4_n.pkl")
#**********************************************
#test SVM
from sklearn.svm import LinearSVC
svm_clf=Pipeline((("scaler", StandardScaler()), ("linear_svc", LinearSVC(C=1, loss="hinge")),))
X=train_hs4[["NS_AMJJA","KONTAPR1400","ETAETP","FOEHNHYY","GLOBRADYYW"]].to_numpy()
labels=train_hs4.CLASS.values.astype(int)
svm_clf.fit(X,labels)
Xtest=test_hs4[["NS_AMJJA","KONTAPR1400","ETAETP","FOEHNHYY","GLOBRADYYW"]].to_numpy()
labelstest=test_hs4.CLASS.values.astype(int)
svmprediction=svm_clf.predict(Xtest)
svmpredictionsdf=pd.DataFrame({'obs':labelstest, 'pred':svmprediction})
hit=svmprediction*labelstest
hitrate=sum(hit)/float(len(hit))
#kernel trick
from sklearn.svm import SVC
poly_kernel_svm_clf=Pipeline((("scaler", StandardScaler()), ("svm_clf", SVC(kernel="poly", degree = 3, coef0=1, C=100)),))
poly_kernel_svm_clf.fit(X,labels)
kernel_prediction=poly_kernel_svm_clf.predict(Xtest)
hit=kernel_prediction*labelstest
hitrate=sum(hit)/float(len(hit))
hitrate
#GAussian kernel
from sklearn.svm import SVC
rbf_kernel_svm_clf=Pipeline((("scaler", StandardScaler()), ("svm_clf", SVC(kernel="rbf", gamma=5, C=100)),))
rbf_kernel_svm_clf.fit(X,labels)
rbfkernel_prediction=rbf_kernel_svm_clf.predict(Xtest)
hit=rbfkernel_prediction*labelstest
hitrate=sum(hit)/float(len(hit))
hitrate

#**************************************************************************************************************
#beech area model
#**************************************************************************************************************
