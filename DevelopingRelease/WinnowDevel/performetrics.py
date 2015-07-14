"""
Performance measures for testing applications in Winnow
"""

import numpy as np
from scipy import stats


def rmse(betaColumn, betaTrueFalse):
	"""
	Returns the root mean squared error given the known truth and effects

		Example:

			>>> betaCol = np.array([1, 2, 3, 4, 5, 6])
			>>> betaTF = np.array([1, 0, 1, 1, 0, 0])
			>>> rmse(betaCol, betaTF)
			13.0

	:param betaColum: collected positions
	:param betaTrueFalse: known truth of the collected positions
	:return: the root mean squared error
	"""
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.mean(np.square(np.subtract(betaColumn, betaTrueFalse)))

def mae(betaColumn, betaTrueFalse):
	"""
	Returns the mean absolute error of the data set

		Example:

			>>> betaCol = np.array([1, 2, 3, 4, 5, 6])
			>>> betaTF = np.array([1, 0, 1, 1, 0, 0])
			>>> mae(betaCol, betaTF)
			3.0

	:param betaColumn: collected positions
	:param betaTrueFalse: known truth of the collected positions
	:return: the mean absolute error
	"""
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.mean(np.absolute(np.subtract(betaColumn, betaTrueFalse)))

def r(betaColumn, betaTrueFalse):
	"""
	Returns the correlation coefficient between the known-truth effects and the detected true/false effects

		Example:

			>>> x = [1, 2, 3, 4, 5]
			>>> y = [5, 9, 10, 12, 13]
			>>> r(x, y)
			0.96457885687693812

	:param betaColumn: collected known-truth effects
	:param betaTrueFalse: detected true/false effects
	:return: the correlation coefficient
	"""

	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return stats.stats.pearsonr(betaColumn, betaTrueFalse)[0]

def r2(betaColumn, betaTrueFalse):
	"""
	Produces the coefficient of determination (AKA the correlation coefficient squared); gives the percentage of
	variation accounted for by the relationship between the given variables

		Example:

			>>> x = [3, 4, 5, 6, 7]
			>>> y = [9, 10, 13, 12, 18]
			>>> r2(x, y)
			0.81300813008130068

	:param betaColumn: data set
	:param betaTrueFalse: data set
	:return: the coefficient of determination
	"""
	betaColumn = np.array(betaColumn)
	betaTrueFalse = np.array(betaTrueFalse)
	return np.square(stats.stats.pearsonr(betaColumn, betaTrueFalse)[0])

def auc(snpTrueFalse, scoreColumn):
	"""
	Returns the area under the receiver-operator curve for binary classification (i.e. true/false on whether a SNP
	was part of the known-truth list or not)

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> auc(snpTF,score)
			0.56944444444444442

	:param snpTrueFalse: true/false data set
	:param scoreColumn: score data set
	:return: the area under the receiver-operator curve
	"""
	scoreColumn = np.array(scoreColumn)
	snpTrueFalse = np.array(snpTrueFalse)
	x1 = scoreColumn[snpTrueFalse == True]
	n1 = x1.size
	x2 = scoreColumn[snpTrueFalse == False]
	n2 = x2.size
	r = stats.rankdata(np.hstack((x1,x2)))
	auc = (np.sum(r[0:n1]) - n1 * (n1+1)/2) / (n1 * n2)
	return 1 - auc

def tp(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the total number of SNPs correctly identified as significant from the analysis

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> tp(snpTF, threshold, score)
			4

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the total number of SNPs correctly identified as significant
	"""
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	truePositives = 0
	for each in testColumn:
		if each is True and snpTrueFalse[count] is True:
			truePositives += 1
		count += 1
	return truePositives

def fp(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the number of SNPs incorrectly identified as significant

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> fp(snpTF, threshold, score)
			3

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the total number of SNPs incorrectly identified as significant
	"""
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	falsePositives = 0
	for each in testColumn:
		if each is True and snpTrueFalse[count] is False:
			falsePositives += 1
		count += 1
	return falsePositives

def tn(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the number of SNPs correctly identified as not significant

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> tn(snpTF, threshold, score)
			3

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the total number of SNPs correctly identified as not significant
	"""
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	trueNegatives = 0
	for each in testColumn:
		if each is False and snpTrueFalse[count] is False:
			trueNegatives += 1
		count += 1
	return trueNegatives

def fn(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the number of SNPs incorrectly identified as not significant

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> fn(snpTF, threshold, score)
			2

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the total number of SNPs incorrectly identified as not significant
	"""
	testColumn = list()
	for each in scoreColumn:
		if float(each) < threshold:
			testColumn.append(True)
		else:
			testColumn.append(False)
	count = 0
	falseNegatives = 0
	for each in testColumn:
		if each is False and snpTrueFalse[count] is True:
			falseNegatives += 1
		count += 1
	return falseNegatives

def tpr(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the proportion of true positives identified from the entire data set

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> tpr(snpTF, threshold, score)
			0.6666666666666666

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the proportion of true positives
	"""
	truePositives = tp(snpTrueFalse, threshold, scoreColumn)
	count = 0.0
	for each in snpTrueFalse:
		if each is True:
			count += 1.0
	return float(truePositives/count)

def fpr(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the proportion of false positives identified from the data set

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> fpr(snpTF, threshold, score)
			0.5

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the proportion of false positives
	"""
	falsePositives = fp(snpTrueFalse, threshold, scoreColumn)
	count = 0.0
	for each in snpTrueFalse:
		if each is False:
			count += 1.0
	return float(falsePositives/count)

def error(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the error value of the analysis (NOT standard error!) defined as the total false identifications,
	positive or negative, by the total number identified

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> error(snpTF,threshold,score)
			0.4166666666666667

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the error value
	"""
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	trueNegatives = float(tn(snpTrueFalse, threshold, scoreColumn))
	falseNegatives = float(fn(snpTrueFalse, threshold, scoreColumn))
	return (falseNegatives + falsePositives) / (truePositives + trueNegatives + falsePositives + falseNegatives)

def sens(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the sensitivity value of the analysis; defined as the number of correctly identified positives
	divided by the total number of known-truth positives

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> sens(snpTF, threshold, score)
			0.6666666666666666

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the sensitivity value
	"""
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falseNegatives = float(fn(snpTrueFalse, threshold, scoreColumn))
	return truePositives / (truePositives + falseNegatives)

def spec(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the specificity value; defined as the number of correctly identified negatives divided by the total
	number of known-truth negatives

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> spec(snpTF, threshold, score)
			0.5

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the specificity value
	"""
	trueNegatives = float(tn(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	return trueNegatives / (trueNegatives + falsePositives)

def precision(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the precision; defined as the number of correctly identified positives divided by the total identified
	positives

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold=0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> precision(snpTF, threshold, score)
			0.5714285714285714

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the precision value
	"""
	truePositives = float(tp(snpTrueFalse, threshold, scoreColumn))
	falsePositives = float(fp(snpTrueFalse, threshold, scoreColumn))
	return truePositives / (truePositives + falsePositives)

def youden(snpTrueFalse, threshold, scoreColumn):
	"""
	Returns the Youden statistic for the data

		Example:

			>>> snpTF=[True,False,True,True,True,False,False,True,False,False,True,False]
			>>> threshold = 0.05
			>>> score=[0.003,0.65,0.004,0.006,0.078,0.003,0.0001,0.513,0.421,0.0081,0.043,0.98]
			>>> youden(snpTF,threshold,score)
			0.16666666666666652

	:param snpTrueFalse: true/false data set
	:param threshold: significant threshold
	:param scoreColumn: score data set
	:return: the float representation of the Youden statistic
	"""
	sensitivity = float(sens(snpTrueFalse, threshold, scoreColumn))
	specificity = float(spec(snpTrueFalse, threshold, scoreColumn))
	return sensitivity + specificity - 1.0

if __name__ == "__main__":
    import doctest
    doctest.testmod()