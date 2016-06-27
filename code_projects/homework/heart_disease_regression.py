import numpy as np
import pandas as pd
import urllib2 as ul
import pylab as pl
import pprint as pp
import json as js

from sklearn import cross_validation as cv
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import roc_curve, auc, confusion_matrix
from sklearn.grid_search import GridSearchCV as gs

INPUT_FILE = '/Users/john/data/gads//heart-disease-stats.csv'
PLOT_OUTPUT_FILE = '/Users/john/data/gads/heart-disease-plot.png'
NUM_FOLDS = 10
# initialize results sets
all_fprs, all_tprs, all_aucs = (np.zeros(NUM_FOLDS), np.zeros(NUM_FOLDS),np.zeros(NUM_FOLDS))
RESULTS = []

def preprocess_data(input_file):
		data = pd.read_csv(input_file, delimiter=',').dropna()
		#data = data[['age', 'cp','chol', 'trestbps','heartdisease::category|0|1']]
		#data = data.rename(columns={'heartdisease::category|0|1': 'label', 'cp': 'chest_pain','trestbps':'blood_pressure','col':'cholestoral'})
		data = data.rename(columns={'heartdisease::category|0|1': 'label'})
		return data

def kfolds(features, labels,num_folds):
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True)
    return kf

def run_model(train_features, train_labels,test_features, test_labels,iteration=None,excluded_feature=None):
		model_results = {}
		model = LR()
		model.fit(train_features, train_labels)

		# get model outputs
		inputs = map(str, train_features.columns.format())
		coeffs = model.coef_[0]
		accuracy = model.score(test_features, test_labels)

		predicted_labels = model.predict(test_features)
		cm = confusion_matrix(test_labels, predicted_labels)

		# print 'inputs = {0}'.format(inputs)
		# print 'coeffs = {0}'.format(coeffs)
		# print 'accuracy = {0}'.format(accuracy)
		# print 'confusion matrix:\n', cm, '\n'

		pred_labels = model.predict(test_features)

		## Still a little confised about thie
		fpr, tpr, thresholds = roc_curve(test_labels, pred_labels, pos_label=1)
		roc_auc = auc(fpr, tpr)

		# print 'fpr:' + str(fpr)

		all_fprs[iteration] = fpr[1]
		all_tprs[iteration] = fpr[1]
		all_aucs = roc_auc

		# print str(roc_auc) + '<-- roc auc'
		# print str(all_aucs) + '<-- all auc'

		## all_fpr is an array of length initiated with
		## the amount of folds in the execution
		## fpr looks something like this: [ 0.    0.25  1.  ]
		## all fprs are appended to in order of the iteration


		#all_aucs[iteration] = roc_auc
		# print 'all fprs:' + str(all_fprs)

		RESULTS.append(model_results)

		#pl.clf()
		#pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
		#pl.plot([0, 1], [0, 1], 'k--')
		#pl.xlim([0.0, 1.0])
		#pl.ylim([0.0, 1.0])
		#pl.xlabel('False Positive Rate')
		#pl.ylabel('True Positive Rate')
		#pl.title('Receiver operating characteristic example')
		#pl.legend(loc="lower right")
		#pl.show(1)

		return fpr, tpr, excluded_feature

def plot_results(all_fprs,all_tprs,all_aucs): #THIS DOESNT WORK... PLEASE HELP!
	  # plot ROC curve

		pl.clf()
		pl.plot(all_fprs, all_tprs, label='ROC curve (area = %0.2f)' % all_aucs[0])
		pl.plot([0, 1], [0, 1], 'k--')
		pl.xlim([0.0, 1.0])
		pl.ylim([0.0, 1.0])
		pl.xlabel('False Positive Rate')
		pl.ylabel('True Positive Rate')
		pl.title('Receiver operating characteristic example')
		pl.legend(loc="lower right")
		pl.show(1)
		pl.savefig(PLOT_OUTPUT_FILE, bbox_inches=0)

def roc_it(data,excluded_feature=None):
    # create cv iterator (note: train pct is set implicitly by number of folds)

		print '==\n' * 3
		print data[:3]
		print '==\n' * 3
		features = data.drop('label', 1)
		print features[:3]

		labels = data.label

		num_recs = len(data)
		kf = kfolds(features, labels, NUM_FOLDS)

		for i, (train_index, test_index) in enumerate(kf):

			loop_ind = '\n'+ '=' * 20 + 'Loop Number: ' + str(i) + '=' * 20

			print loop_ind * 3 + '\n'

			train_features = features.loc[train_index].dropna()
			train_labels = labels.loc[train_index].dropna()

			test_features = features.loc[test_index].dropna()
			test_labels = labels.loc[test_index].dropna()

			run_model(train_features, train_labels,test_features, test_labels, i, excluded_feature)


def leave_one_out(data):
		features = data.drop('label', 1)
		#features = features.iloc[:,index]
		labels = data.label
		for i,(excluded_feature) in enumerate(features):
			loop_ind = '\n'+ '=' * 20 + 'Excluding Feature: ' + excluded_feature + '=' * 20
			# print loop_ind
			loop_features = data.drop(excluded_feature, 1)

			roc_it(data,excluded_feature)

			# print i, loop_featureps

if __name__ == '__main__':
		data = preprocess_data(INPUT_FILE)
		roc_it(data)
		all_aucs = [.8]
		# plot_results(all_fprs, all_tprs, all_aucs)

		#leave_one_out(data)
		#results_json = js.dumps(RESULTS)
		#pp.pprint(RESULTS)

#############################
####### HW Questions ########
#############################

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
