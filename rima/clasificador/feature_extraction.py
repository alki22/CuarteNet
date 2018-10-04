import pickle

from silabas import silabas as separar

_VOCALES = {'a', 'e', 'i', 'o', 'u'}

_ABIERTAS = {'a', 'e', 'o', 'á', 'é', 'ó'}

_CERRADAS = {'i', 'u', 'í', 'ú'}

_DIPTONGOS = {'ai', 'au', 'ei', 'eu', 'ia', 'ie', 'io',
              'iu', 'oi', 'ou', 'ua', 'ue', 'ui', 'uo'}

_NSOVOCAL = {'a', 'e', 'i', 'o', 'u', 'n', 's'}

_ACENTUADAS = {'á', 'é', 'í', 'ó', 'ú'}


def tieneDiptongo(palabra: str) -> bool:
    return any([d for d in _DIPTONGOS if d in palabra])


def esAguda(silabas: list) -> bool:
    """ Devuelve si la palabra es aguda,
        considera sólo el caso en que no es esdrújula o sobreesdrújula """
    if len(silabas) == 1:
        return True

    tieneAcentoAgudo = any([a for a in _ACENTUADAS if a in silabas[-1]])
    tieneAcentoGrave = any([a for a in _ACENTUADAS if a in silabas[-2]])

    terminaNSVocal = silabas[-1][-1] in _NSOVOCAL

    return ((terminaNSVocal and tieneAcentoAgudo) or
            (not tieneAcentoGrave and not tieneAcentoAgudo))


def silabaTonica(silabas: list) -> int:
    """ Dada una lista de sílabas de una palabra
        devuelve el índice de la sílaba tónica """
    for i in range(len(silabas)):
        if any([a for a in _ACENTUADAS if a in silabas[i]]):
            return i

        if i >= len(silabas) - 1:
            if esAguda(silabas):
                return len(silabas) - 1
            else:
                return len(silabas) - 2


def vocalTonica(silabas: list, tonica: int) -> str:
    if len(silabas) == 0:
        return ""

    silabaTonica = silabas[tonica]
    vocalAbierta = [a for a in _ABIERTAS if a in silabaTonica]
    vocalCerrada = [c for c in _CERRADAS if c in silabaTonica]

    if any(vocalAbierta):
        return vocalAbierta[0]

    elif any(vocalCerrada):
        return vocalCerrada[0]

    else:
        return vocalTonica(silabas, tonica - 1)


def sigTonica(silabas: list, tonica: int) -> str:
    if len(silabas) == 0:
        return ""

    vocTonica = vocalTonica(silabas, tonica)
    posicion = silabas[tonica].index(vocTonica)

    if 0 <= posicion < len(silabas[tonica]) - 1:
        return silabas[tonica][posicion + 1]
    else:
        if tonica < len(silabas) - 1:
            return silabas[tonica + 1][0]
        else:
            return ""


def antTonica(silabas: list, tonica: int) -> str:
    if len(silabas) == 0:
        return ""

    vocTonica = vocalTonica(silabas, tonica)
    posicion = silabas[tonica].index(vocTonica)

    if 0 < posicion <= len(silabas[tonica]) - 1:
        return silabas[tonica][posicion - 1]
    else:
        if tonica > 0:
            return silabas[tonica - 1][-1]
        else:
            return ""


def vocalesPostonicas(silabas: list, tonica: int) -> str:
    if len(silabas) == 0:
        return ""

    indexTonica = silabas[tonica].index(vocalTonica(silabas, tonica))
    postonicas = "".join(silabas[tonica:][indexTonica:])

    return "".join([v for v in _VOCALES if v in postonicas])


def features(palabra: str) -> list:
    silabas = separar(palabra)
    tonica = silabaTonica(silabas)

    features = [vocalTonica(silabas, tonica), sigTonica(silabas, tonica),
                antTonica(silabas, tonica), vocalesPostonicas(silabas, tonica),
                tieneDiptongo(palabra)]

    return features


def diccDeFeatures(primeraPalabra: str, segundaPalabra: str) -> dict:
    """ Devuelve el diccionario de features correspondiente al par
        de terminaciones de estrofa """
    featuresPrimera = features(primeraPalabra)
    featuresSegunda = features(segundaPalabra)

    featuresPar = {
                        # Features de la primera palabra de la 3-upla
                        'termPrimera': primeraPalabra,
                        'vocalTonicaPrimera': featuresPrimera[0],
                        'sigTonicaPrimera': featuresPrimera[1],
                        'antTonicaPrimera': featuresPrimera[2],
                        'postonicasPrimera': featuresPrimera[3],
                        'diptongoPrimera': featuresPrimera[4],

                        # Features de la segunda palabra de la 3-upla
                        'termSegunda': segundaPalabra,
                        'vocalTonicaSegunda': featuresSegunda[0],
                        'sigTonicaSegunda': featuresSegunda[1],
                        'antTonicaSegunda': featuresSegunda[2],
                        'postonicasSegunda': featuresSegunda[3],
                        'diptongoSegunda': featuresSegunda[4],
                  }
    return featuresPar

def dataDeEntrenamiento(path: str) -> (list, list):
    """ Devuelve una lista de diccionarios de features de cada par del corpus
        y un vector [cant_elementos] con la etiqueta 1 si riman y 0 si no """
    with open(path, 'rb') as archivo:
        dataset = pickle.load(archivo)

    corpus = []
    etiquetas = []

    for tripla in dataset:
        corpus.append(diccDeFeatures(tripla[0], tripla[1]))
        etiquetas.append(tripla[2])

    return corpus, etiquetas
