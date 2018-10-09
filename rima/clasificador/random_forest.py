from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from feature_extraction import *
from sklearn.metrics import classification_report

import pickle
import os.path

archivoModelo = 'modelo.pk'
archivoVectorizador = 'vectorizador.pk'

if not (os.path.isfile(archivoModelo) and os.path.isfile(archivoVectorizador)):

	clf = RandomForestClassifier(n_estimators=100)

	features, etiquetas = dataDeEntrenamiento('../dataset/dataset.pk')
	testIndex = int(len(features)*0.8)

	vectorizador = DictVectorizer()

	X = vectorizador.fit_transform(features[:testIndex])
	y = etiquetas[:testIndex]

	clf.fit(X, y)

	pickle.dump(clf, open(archivoModelo, 'wb'))
	pickle.dump(vectorizador, open(archivoVectorizador, 'wb'))

features, etiquetas = dataDeEntrenamiento('../dataset/dataset.pk')
testIndex = int(len(features)*0.8)

clf = pickle.load(open(archivoModelo, 'rb'))
vectorizador = pickle.load(open(archivoVectorizador, 'rb'))

test_corpus = features[testIndex:]

testX = vectorizador.transform(test_corpus)

resultados = clf.predict(testX)
valor = etiquetas[testIndex:]

precision = 0

for i in range(len(valor)):
	if resultados[i] == valor[i]:
		precision += 1

precision = precision/len(resultados)

print(precision)

print(classification_report(resultados, valor))
