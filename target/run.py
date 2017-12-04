from subprocess import *

def jarWrapper(*args):
	arguments = list(args)
	print list(args)
	process = Popen(['java', '-jar']+arguments, stdout=PIPE, stderr=PIPE)
	result = ""
	while process.poll() is None:
		line = process.stdout.readline()
		if line != '' and line.endswith('\n'):
			result += line
	return result


def doFastEvolve(data,isIntegerEncoding,allowDuplicates):
	bestFitness = ""
	encoding = "Binary"
	if isIntegerEncoding=="true":
		encoding = "Integer"
	if data == "ionosphere_mapped":
		distanceFeaturePercentage = 0.25
	elif data == "semeion_mapped":
		distanceFeaturePercentage = 0.95

	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",isIntegerEncoding,str(distanceFeaturePercentage), allowDuplicates] # Any number of args to be passed to the jar file
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	bestFitness = split[len(split)-3].split()[2]
	print "%s" % bestFitness

def doEvolve(data, isIntegerEncoding, allowDuplicates):
    bestFitness = []
    encoding = "Binary"
    if isIntegerEncoding=="true":
    	encoding = "Integer"
    for i in range(1,11):
	    distanceFeaturePercentage = str(i/10.0)
	    args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",isIntegerEncoding,distanceFeaturePercentage, allowDuplicates] # Any number of args to be passed to the jar file
	    result = jarWrapper(*args)
	    target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,i*10,allowDuplicates)
	    target_file = open(target_path,'w')
	    target_file.write(result)
	    target_file.close()
	    split = result.splitlines()
	    bestFitness.append(split[len(split)-3].split()[2])
	    print "%s" % bestFitness[i-1]

    target_path = "results/%s/%s_%s_total_%s.dat" % (data,data,encoding,allowDuplicates)
    target_file = open(target_path,'w')
    for i in range(1,11):
        target_file.write("%s    %s\n" % (i,bestFitness[i-1]))
    target_file.close()

    call(["gnuplot","-e","filename='%s';outputFile='results/%s/%s_%s_total_%s.eps'" % (target_path,data,data,encoding,allowDuplicates), "results/plot.plt"])


data = ["ionosphere_mapped","semeion_mapped"]

#evolution with integer encoding
doFastEvolve(data[1],"true","true")
doFastEvolve(data[1],"true","false")

#evolution with binary encoding, duplicates do not occur in this approach 
doFastEvolve(data[1],"false","false")
