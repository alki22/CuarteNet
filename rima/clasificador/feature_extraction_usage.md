![logo](https://i.ytimg.com/vi/aWgHy7DUH90/hqdefault.jpg)

# Instrucciones para extraer features

```python
import feature_extraction

# Si se tienen dos palabras:

"""Devuelve el diccionario de features correspondiente al par 
   de terminaciones de estrofa"""
features = diccDeFeatures(palabra1, palabra2)

# Si se tiene un dataset en formato pickle:

""" Devuelve una lista de diccionarios con las features de cada par del corpus
    y un vector y [cant_elementos] con la etiqueta 1 si riman y 0 si no"""
features, etiquetas = dataDeEntrenamiento(pathDelArchivo)
```