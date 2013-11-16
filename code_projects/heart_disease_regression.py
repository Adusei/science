#Predict the presence of heart disease in the patient. 

import numpy as np
import pandas as pd
import urllib2 as ul

from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix

INPUT_FILE = '/Users/john/code/science/data/heart-disease-stats.csv'
TRAIN_PCT = .7

def preprocess_data(input_file):
		data = pd.read_csv(input_file, delimiter=',').dropna()
		data = data[['age', 'cp','chol', 'trestbps','heartdisease::category|0|1']]
		data = data.rename(columns={'heartdisease::category|0|1': 'label', 'cp': 'chest_pain','trestbps':'blood_pressure','col':'cholestoral'})
		return data

def run_model(data):
    # shuffle dataset
    data = data.reindex(np.random.permutation(data.index))

    split_pt = int(TRAIN_PCT * len(data))

    print '=' * 50
    print ' ' * 20  + '.... the data set has ' +  str(len(data)) + ' total records and the splt pt is ' + str(split_pt) + '....'
    print '=' * 50

    train_x = data[:split_pt].drop('label', 1)
    train_y = data[:split_pt].label 
    	#QUESTION -> How are these linked? by index via their order in the data set?

    test_x = data[split_pt:].drop('label', 1)
    test_y = data[split_pt:].label

    model = LR()                        # model is an "instance" of the class LR
    model.fit(train_x, train_y)         # perform model fit ("in place")

    # get model outputs
    inputs = map(str, train_x.columns.format())
    coeffs = model.coef_[0]
    accuracy = model.score(test_x, test_y)

    predicted_y = model.predict(test_x)
    cm = confusion_matrix(test_y, predicted_y)

    print 'inputs = {0}'.format(inputs)
    print 'coeffs = {0}'.format(coeffs)
    print 'accuracy = {0}'.format(accuracy)     # mean 0/1 loss
    print 'confusion matrix:\n', cm, '\n'


if __name__ == '__main__':
    data = preprocess_data(INPUT_FILE)
    print data
    run_model(data)
    
#Training Set:
#https://github.com/dzorlu/GADS/blob/master/data/logit-train.csv


#More information can be found here:
#http://archive.ics.uci.edu/ml/datasets/Heart+Disease

#9 cp: chest pain type 
	#-- Value 1: typical angina 
	#-- Value 2: atypical angina 
	#-- Value 3: non-anginal pain 
	#-- Value 4: asymptomatic 

#10 trestbps: resting blood pressure (in mm Hg on admission to the hospital) 
#12 chol: serum cholestoral in mg/dl 

#16 fbs: (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false) 

#19 restecg: resting electrocardiographic results 
	#-- Value 0: normal 
	#-- Value 1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV) 
	#-- Value 2: showing probable or definite left ventricular hypertrophy by Estes' criteria 

#38 exang: exercise induced angina (1 = yes; 0 = no) 
#40 oldpeak = ST depression induced by exercise relative to rest 
#41 slope: the slope of the peak exercise ST segment 
	#-- Value 1: upsloping 
	#-- Value 2: flat 
	#-- Value 3: downsloping 
#44 ca: number of major vessels (0-3) colored by flourosopy 
#51 thal: 3 = normal; 6 = fixed defect; 7 = reversable defect

#58 num: diagnosis of heart disease (angiographic disease status) 
#-- Value 0: < 50% diameter narrowing 
#-- Value 1: > 50% diameter narrowing 

##Questions 
#1 - Train your logistic regression model with the training set applying 10-fold cross-validation. 
  #(a) Report the average AUC as well as misclassification rate (percent of times you guessed the label wrong).  
#2 - Train your model applying 5-fold cross-validation, but this time to select the features. 
  #Hint: This construct might help: features.iloc[:,index]
  #(a) Report the average AUC. Note that the code is very similar to first question, only this time we select the features, rather than the records. 
  #(b) If you want to reduce the number of features, which two features would you remove from the model first (hint: RFECV ). 
