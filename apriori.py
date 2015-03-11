#encoding:utf-8
import sys , collections , itertools

def patternSupport(pattern,datas):
	count = 0
	for data in datas :
		if pattern.issubset(data):
			count += 1
	return count

def calThreshold(level):
	return level - 1

def generateCandis(patterns,level):
	candis = []
	for pattern1 in patterns :
		for pattern2 in patterns :
			if pattern1 != pattern2 :
				candi = pattern1.union(pattern2)
				if len(candi) == level and candi not in candis:
					candis.append(candi)
	return candis

def generateRules(pattern,support,min_conf,datas):
	length = len(pattern)
	subsets = [] 
	rules = []
	for i in range(1,length) :
		subsets += [ set(s) for s in itertools.combinations(pattern,i) ]
	for i,subset in enumerate(subsets) :
		subset_support = patternSupport(subset,datas)
		if float(support) / subset_support >= min_conf :
			rules.append( (subset,pattern-subset) )
	return rules

if __name__ == "__main__" :
	
	filename = sys.argv[1]
	min_sup = float(sys.argv[2])
	min_conf = float(sys.argv[3])

	try :
		f = open(filename)
		datas , sup_count = [] , []
		# sup_count is built for first level freq items
		for line in f.readlines() :
			tmp = set(line.split())
			datas.append(tmp)
			sup_count += tmp 
		f.close()

		min_sup = min_sup*len(datas)
		sup_count = collections.Counter(sup_count)
		freqs = [ set(item) for item in sup_count if sup_count[item] >= min_sup ]
		current_freqs = freqs

		result_freqs = []
		next_level = 2 

		while len(current_freqs) > calThreshold(next_level) :
			candis = generateCandis(current_freqs,next_level)
			current_freqs = [ candi for candi in candis if patternSupport(candi,datas) >= min_sup ]
			result_freqs += current_freqs
			next_level   += 1
	
		print "result_freqs",result_freqs
		rules = []
		for pattern in result_freqs :
			support = patternSupport(pattern,datas)
			rules += generateRules(pattern,support,min_conf,datas)

		for rule in rules :
			print("{} -> {}".format(",".join(list(rule[0])),",".join(list(rule[1]))))

	except IOError :
		print("File dosen't exist !")
