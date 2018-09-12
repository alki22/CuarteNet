import xmltodict
from itertools import permutations
import pickle
import sys
import string
from tqdm import tqdm

def process_sonnet(filename):
    
    '''
    in: soneto en formato .xml
    Se procesa cada soneto utilizando los cuartetos de cada uno.
    ret: rimas con la forma [(palabraA1, palabraA2, 1)] donde palabraA1 y palabraA2 riman.
    ret: not_rimas con la forma [(palabraA, palabraB, 0)] donde palabraA y palabraB no riman.
    '''

    with open(filename) as fd:
        son = xmltodict.parse(fd.read())
        son = son['TEI']['text']['body']['lg']
        son = son[:2]

    rimasA = []
    rimasB = []
    table = str.maketrans({key: None for key in string.punctuation})

    for estrofa in son:
        estrofa = estrofa['l']

        for i, verso in enumerate(estrofa):
            try:
                verso = verso['#text'].split()
            except KeyError:
                import ipdb; ipdb.set_trace()
            palabra = verso[-1].translate(table)

            if 0 < i < 3:
                rimasB.append(palabra)
            else:
                rimasA.append(palabra)

    rimas = []
    rimas.extend(list(permutations(rimasA, 2)))
    rimas.extend(list(permutations(rimasB, 2)))

    not_rimas = set(permutations(rimasA + rimasB, 2))
    not_rimas = not_rimas - set(rimas)
    not_rimas = list(not_rimas)


    for i in range(len(rimas)):
        rimas[i] = rimas[i] + (1,)

    for i in range(len(not_rimas)):
        not_rimas[i] = not_rimas[i] + (0,)

    return rimas, not_rimas


def main(argv):
    output_directory = '.'
    
    '''
    Code to process a file with a bunch of sonnets

    filenames = []
    with open('files1', 'r') as myfile:
        for line in myfile:
            filenames.append(line.replace('\n', ''))
    '''
    dataset = []

    for fn in tqdm(filenames):
        try:
            rimas, not_rimas = process_sonnet(fn)
        except UnicodeDecodeError:
            import ipdb; ipdb.set_trace()

        dataset.extend(rimas)
        dataset.extend(not_rimas)

    with open('dataset.pk', 'wb') as fp:
        pickle.dump(dataset, fp)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))