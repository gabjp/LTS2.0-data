import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, classification_report
from astropy.stats import sigma_clip, mad_std
from astropy.table import Table

_morph = ['FWHM_n', 'A', 'B', 'KRON_RADIUS']
_feat = ['u_iso',
             'J0378_iso',
             'J0395_iso',
             'J0410_iso',
             'J0430_iso',
             'g_iso',
             'J0515_iso',
             'r_iso',
             'J0660_iso',
             'i_iso',
             'J0861_iso',
             'z_iso']

data = pd.read_csv("data/clf/clf.csv")

train = data[(data.split=="train")]
val = data[data.split=="val"]
test = data[data.split=="test"]
train_val = data[~(data.split=="test")]


print("Avaliando: Treinado em train avaliado em val")
clf_total_dr4 = RandomForestClassifier(random_state=2, n_estimators=100, bootstrap=False)
clf_total_dr4.fit(train[_morph+_feat], y=train["target"])
y_pred_test = clf_total_dr4.predict(val[_morph+_feat])
print(classification_report(val["target"], y_pred_test, digits=6))

print("Avaliando: Treinado em train avaliado em test")
clf_total_dr4 = RandomForestClassifier(random_state=2, n_estimators=100, bootstrap=False)
clf_total_dr4.fit(train[_morph+_feat], y=train["target"])
y_pred_test = clf_total_dr4.predict(test[_morph+_feat])
print(classification_report(test["target"], y_pred_test, digits=6))

print("Avaliando: Treinado em train+val avaliado em test")
clf_total_dr4 = RandomForestClassifier(random_state=2, n_estimators=100, bootstrap=False)
clf_total_dr4.fit(train_val[_morph+_feat], y=train_val["target"])
y_pred_test = clf_total_dr4.predict(test[_morph+_feat])
print(classification_report(test["target"], y_pred_test, digits=6))