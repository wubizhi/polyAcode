#!/usr/bin/env python

import sys

import numpy as np
from sklearn import linear_model, metrics

C_LST = [0.001,0.01,0.1,1.0,2.0]
TOL = 0.00001
D = 658
K = 10

FEATURE_NAME = {0:'All',
                1:'Conservation level',
                2:'Nucleosome positioning',
                3:'Secondary structure',
                4:'Transcript structure',
                5:'Short 3mer motif',
                6:'PAS signal & variants',
                7:'Known regulators',
                8:'Potential unknown motifs'}

FEATURE_IDX= {0:range(0, 658),
              1:range(0, 8),
              2:range(8, 12),
              3:range(12, 20),
              4:range(20, 32),
              5:range(32, 288),
              6:range(288, 336),
              7:range(336, 376),
              8:range(376, 658)}

def get_subfeature(X, idx_str):
    n, __ = X.shape
    idx_lst = map(int, idx_str.split(','))
    X_sub = np.array([[] for i in range(0, n)])
    
    if 0 in idx_lst:
        X_sub = X[:, FEATURE_IDX[0]]
    else:
        for i in range(1, 9):
            if i in idx_lst:
                X_sub = np.hstack((X_sub, X[:, FEATURE_IDX[i]]))
    
    return X_sub


def main():
    intrain = sys.argv[1]
    intest = sys.argv[2]
    feature_idx = sys.argv[3]
    K = int(sys.argv[4])
    N = int(sys.argv[5])

    data_train = np.load(intrain)
    data_test = np.load(intest)
    X_train = data_train[:, 0:-1]
    Y_train = data_train[:, -1]
    X_test = data_test[:, 0:-1]
    Y_test = data_test[:, -1]
    
    X_train_sub = get_subfeature(X_train, feature_idx)
    X_test_sub = get_subfeature(X_test, feature_idx)
    
    model = linear_model.LogisticRegressionCV(cv=K, Cs=C_LST, penalty='l2', dual=False, tol=TOL, n_jobs=N, verbose=1)
    model.fit(X_train_sub, Y_train)
    
    Y_test_proba = model.predict_proba(X_test_sub)[:, 1]
    accuracy = model.score(X_test_sub, Y_test)
    auc = metrics.roc_auc_score(Y_test, Y_test_proba)
    fpr, tpr, thresholds = metrics.roc_curve(Y_test, Y_test_proba)
 
    print '****************************************************************************************'
    print 'accuracy : %.1f%%\tAUC : %.3f' % (accuracy*100, auc)

    
if __name__ == '__main__':
    main()

