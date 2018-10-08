import feature_extraction
from sklearn.svm import SVC
from random import sample
from sklearn.feature_extraction import DictVectorizer

clf = SVC(gamma='auto')
X, y = feature_extraction.dataDeEntrenamiento('../dataset/dataset.pk')
v = DictVectorizer(sparse=False)
X = v.fit_transform(X)
length = len(X)
total = set([i for i in range(0, length)])
rand_ints = sample(range(0, length), int(length*0.8))
tune_idx = list(total - set(rand_ints))
x_train = [X[i] for i in rand_ints]
y_train = [y[i] for i in rand_ints]
x_tune = [X[i] for i in tune_idx]
y_tune = [y[i] for i in tune_idx]


clf.fit(x_train, y_train)

print(clf.score(x_tune, y_tune))
