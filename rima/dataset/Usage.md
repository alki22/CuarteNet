# Dataset rima consonante

El mismo esta constituido por tuplas de la forma (a, b, 1) o (a, b, 0) donde el 1 o 0 indica si a y b riman o no.

Para leerlo desde python se puede utilizar el siguiente codigo:

```python
with open('dataset.pk', 'rb') as fp:
        dataset = pickle.load(fp)
```