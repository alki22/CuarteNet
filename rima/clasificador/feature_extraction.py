from silabas import silabas as separar

_VOCALES = {'a', 'e', 'i', 'o', 'u'}

_ABIERTAS = {'a', 'e', 'o', 'á', 'é', 'ó'}

_CERRADAS = {'i', 'u', 'í', 'ú'}

_DIPTONGOS = {'ai', 'au', 'ei', 'eu', 'ia', 'ie', 'io', 'iu', 'oi', 'ou', 'ua',
		 	  'ue', 'ui', 'uo'}

_NSOVOCAL = {'a', 'e', 'i', 'o', 'u', 'n', 's'}

_ACENTUADAS = {'á', 'é', 'í', 'ó', 'ú'}

def tieneDiptongo(palabra):
	return any([d for d in _DIPTONGOS if d in palabra])

def esAguda(silabas):
	return ((silabas[-1][-1] in _NSOVOCAL and any([a for a in _ACENTUADAS if a in silabas[-1]])) or 
		(not any([a for a in _ACENTUADAS if a in silabas[-2]]) and not silabas[-1][-1] in _NSOVOCAL))

def vocalTonica(silabas, i):
	silabaTonica = silabas[i]
	vocalAbierta = [a for a in _ABIERTAS if a in silabaTonica]
	vocalCerrada = [c for c in _CERRADAS if c in silabaTonica]
	
	if any(vocalAbierta):
		return vocalAbierta[0]
	else:
		return vocalCerrada[0]

def sigTonica(silabas, i):
	tonica = vocalTonica(silabas, i)
	posicion = silabas[i].index(tonica)
	
	if 0 <= posicion < len(silabas[i]) - 1:
		return silabas[i][posicion + 1]
	else:
		if i < len(silabas) - 1:
			return silabas[i + 1][0]
		else:
			return ""

def antTonica(silabas, i):
	tonica = vocalTonica(silabas, i)
	posicion = silabas[i].index(tonica)
	
	if 0 < posicion <= len(silabas[i]) - 1:
		return silabas[i][posicion - 1]
	else:
		if i > 0:
			return silabas[i - 1][-1]
		else:
			return ""

def vocalesPostonicas(silabas, i):
	indexTonica = silabas[i].index(vocalTonica(silabas, i))
	postonicas = "".join(silabas[i:][indexTonica:])
	
	return "".join([v for v in _VOCALES if v in postonicas])

def silabaTonica(silabas):

	for i in range(len(silabas)):
		if any([a for a in _ACENTUADAS if a in silabas[i]]):
			return i

		if i >= len(silabas) - 1:
			if esAguda(silabas):
				return len(silabas) - 1
			else:
				return len(silabas) - 2

def features(palabra):
	silabas = separar(palabra)
	tonica = silabaTonica(silabas)
	
	return (vocalTonica(silabas, tonica), sigTonica(silabas, tonica), 
			antTonica(silabas, tonica), vocalesPostonicas(silabas, tonica), 
			tieneDiptongo(palabra))