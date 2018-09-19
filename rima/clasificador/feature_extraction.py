from silabas import silabas as separar

_DIPTONGOS = {'ai', 'au', 'ei', 'eu', 'ia', 'ie', 'io', 'iu', 'oi', 'ou', 'ua',
		 	  'ue', 'ui', 'uo'}

_NSOVOCAL = {'a', 'e', 'i', 'o', 'u', 'n', 's'}

_ACENTUADAS = {'á', 'é', 'í', 'ó', 'ú'}

def tieneDiptongo(palabra):
	return any([d for d in _DIPTONGOS if d in palabra])

def esAguda(silabas):
	return ((silabas[-1][-1] in _NSOVOCAL and any(a for a in _ACENTUADAS if a in silabas[-1])) or 
		(not any(a for a in _ACENTUADAS if a in silabas[-2]) and not silabas[-1][-1] in _NSOVOCAL))

def acentuacion(palabra):
	silabas = separar(palabra)

	for i in range(len(silabas)):
		if any(a for a in _ACENTUADAS if a in silabas[i]):
			return palabra, silabas, i, silabas[i]

		if i >= len(silabas) - 1:
			if esAguda(silabas):
				return palabra, silabas, len(silabas) - 1, silabas[-1]
			else:
				return palabra, silabas, len(silabas) - 2, silabas[-2]