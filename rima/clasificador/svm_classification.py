import feature_extraction
from sklearn.svm import SVC
from random import sample
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

X, y = feature_extraction.dataDeEntrenamiento('../dataset/dataset.pk')
v = DictVectorizer(sparse=True)
X = v.fit_transform(X)
length = X.shape[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

print('===== Training =====')
clf = SVC(kernel='rbf')
clf.fit(X_train, y_train)

print('Accuracy:', clf.score(X_test, y_test))
y_pred = clf.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
