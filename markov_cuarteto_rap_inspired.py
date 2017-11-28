import random, re

# freqDict is a dict of dict containing frequencies
def addToDict(fileName, freqDict):
	f = open(fileName, 'r')
	words = re.sub("\n", " ", f.read()).lower().split(' ')
	words = [x for x in words if x != '$$']
	# count frequencies curr -> succ
	for curr, succ in zip(words[1:], words[:-1]):
		# check if curr is already in the dict of dicts
		if curr not in freqDict:
			freqDict[curr] = {succ: 1}
		else:
			# check if the dict associated with curr already has succ
			if succ not in freqDict[curr]:
				freqDict[curr][succ] = 1;
			else:
				freqDict[curr][succ] += 1;

	# compute percentages
	probDict = {}
	for curr, currDict in freqDict.items():
		probDict[curr] = {}
		currTotal = sum(currDict.values())
		for succ in currDict:
			probDict[curr][succ] = currDict[succ] / currTotal
	print(probDict)
	return probDict

def markov_next(curr, probDict):
	if curr not in probDict:
		return random.choice(list(probDict.keys()))
	else:
		succProbs = probDict[curr]
		randProb = random.random()
		currProb = 0.0
		for succ in succProbs:
			currProb += succProbs[succ]
			if randProb <= currProb:
				return succ
		return random.choice(list(probDict.keys()))

def makeRap(curr, probDict, T = random.randint(50, 100)):
	rap = [curr]
	for t in range(T):
		rap.append(markov_next(rap[-1], probDict))
	song = ''
	i = 0
	done = False
	while not done:
		verse_length = random.randint(4, 9)
		song += " ".join(rap[i:i + verse_length]) + '\n'
		i += verse_length
		if i >= len(rap):
			done = True
	return song

if __name__ == '__main__':
	rapFreqDict = {}
	rapProbDict = addToDict('data/cuarteto+latinos.txt', rapFreqDict)
	# rapProbDict = addToDict('lyrics2.txt', rapFreqDict)

	startWord = input("What do you want to start your cuarteto with?\n > ")
	print("Alright, here's your cuarteto:")
	for i in range(10):
		print(makeRap(startWord, rapProbDict))
		print('----------------------')
