#Predict the presence of heart disease in the patient. 

import numpy as np
import pandas as pd
import urllib2 as ul
import pylab as pl
import time

from sklearn import cross_validation as cv
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import roc_curve, auc, confusion_matrix

INPUT_FILE = '/Users/john/code/science/data/heart-disease-stats.csv'
PLOT_OUTPUT_FILE = '/Users/john/code/science/data/heart-disease-plot.png'
TRAIN_PCT = .7
NUM_FOLDS = 10

def preprocess_data(input_file):
		data = pd.read_csv(input_file, delimiter=',').dropna()
		data = data[['age', 'cp','chol', 'trestbps','heartdisease::category|0|1']]
		data = data.rename(columns={'heartdisease::category|0|1': 'label', 'cp': 'chest_pain','trestbps':'blood_pressure','col':'cholestoral'})
		#data = data.rename(columns={'heartdisease::category|0|1': 'label'})
		return data

def kfolds(features, labels):
    kf = cv.KFold(n=len(features), n_folds=NUM_FOLDS, shuffle=True)

def run_model(data):
    data = data.reindex(np.random.permutation(data.index))     # shuffle dataset

    split_pt = int(TRAIN_PCT * len(data))

    train_x = data[:split_pt].drop('label', 1)
    train_y = data[:split_pt].label 
    	# QUESTION -> How are these linked? by index via 
    	#					 -> their order in the data set?

    test_x = data[split_pt:].drop('label', 1)
    test_y = data[split_pt:].label

    model = LR()
    	# QUESTION -> Where can i see the source code for this?
    	#					 -> What does the model aim to do... is it 
    	#					 -> finding Alpha and Beta in the logit fn
    	# 				 -> then applying the results to the test?

    model.fit(train_x, train_y)

    # get model outputs
    inputs = map(str, train_x.columns.format())
    coeffs = model.coef_[0]
    accuracy = model.score(test_x, test_y)

    predicted_y = model.predict(test_x)
    cm = confusion_matrix(test_y, predicted_y)

    print 'inputs = {0}'.format(inputs)
    print 'coeffs = {0}'.format(coeffs)
    print 'accuracy = {0}'.format(accuracy)
    print 'confusion matrix:\n', cm, '\n'


def roc_it(data):
    # create cv iterator (note: train pct is set implicitly by number of folds)
		features = data.drop('label', 1)
		labels = data.label 

		num_recs = len(data)
		print num_recs
		kf = cv.KFold(n=num_recs, n_folds=NUM_FOLDS, shuffle=True)

    # initialize results sets
		all_fprs, all_tprs, all_aucs = (np.zeros(NUM_FOLDS), np.zeros(NUM_FOLDS),
			np.zeros(NUM_FOLDS))

		for i, (train_index, test_index) in enumerate(kf):
				print str(i) +'\n'#,train_index, test_index
        # initialize & train model
				model = LR()

        # debug!
				train_features = features.loc[train_index].dropna()
				train_labels = labels.loc[train_index].dropna()

				test_features = features.loc[test_index].dropna()
				test_labels = labels.loc[test_index].dropna()

				model.fit(train_features, train_labels)

        # predict labels for test features
				pred_labels = model.predict(test_features)

        # calculate ROC/AUC
				fpr, tpr, thresholds = roc_curve(test_labels, pred_labels, pos_label=1)
				roc_auc = auc(fpr, tpr)

				print '\nfpr = {0}'.format(fpr)
				print 'tpr = {0}'.format(tpr)
				print 'auc = {0}'.format(roc_auc)

				all_fprs[i] = fpr[1]
				all_tprs[i] = tpr[1]
				all_aucs[i] = roc_auc

		print '\nall_fprs = {0}'.format(all_fprs)
		print 'all_tprs = {0}'.format(all_tprs)
		print 'all_aucs = {0}'.format(all_aucs)

	  # plot ROC curve
		pl.clf()
		pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
		pl.plot([0, 1], [0, 1], 'k--')
		pl.xlim([0.0, 1.0])
		pl.ylim([0.0, 1.0])
		pl.xlabel('False Positive Rate')
		pl.ylabel('True Positive Rate')
		pl.legend(loc="lower right")
		pl.savefig(PLOT_OUTPUT_FILE, bbox_inches=0)
		#time.sleep(10)

if __name__ == '__main__':
		data = preprocess_data(INPUT_FILE)
		roc_it(data)
    #run_model(data)



#Training Set:
#https://github.com/dzorlu/GADS/blob/master/data/logit-train.csv

##Questions 
#1 - Train your logistic regression model with the training set applying 10-fold cross-validation. 
  #(a) Report the average AUC as well as misclassification rate (percent of times you guessed the label wrong).  
#2 - Train your model applying 5-fold cross-validation, but this time to select the features. 
  #Hint: This construct might help: features.iloc[:,index]
  #(a) Report the average AUC. Note that the code is very similar to first question, only this time we select the features, rather than the records. 
  #(b) If you want to reduce the number of features, which two features would you remove from the model first (hint: RFECV ). 


########################
#### DATA DICTIONRY ####
########################

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
