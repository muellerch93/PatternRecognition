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
	#if data == "ionosphere_mapped":
	#	distanceFeaturePercentage = 0.25
	#elif data == "semeion_mapped":
	#	distanceFeaturePercentage = 0.95
	distanceFeaturePercentage = 1
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

    target_path = "results/%s/%s_%s_total_%s" % (data,data,encoding,allowDuplicates)
    target_file = open("%s.dat" % target_path,'w')
    for i in range(1,11):
        target_file.write("%s    %s\n" % (i*10,bestFitness[i-1]))
    target_file.close()

    call(["gnuplot","-e","filename='%s.dat';outputFile='%s.eps'" % (target_path,target_path), "results/plot.plt"])
    return target_path

data = ["ionosphere_mapped","semeion_mapped"]

#evolution with integer encoding
file1 = doEvolve(data[0],"true","true")
file2 = doEvolve(data[0],"true","false")
#evolution with binary encoding, duplicates do not occur in this approach 
file3 = doEvolve(data[0],"false","false")
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (file1,file2,file3,data[0],"all"), "results/plot_all.plt"])

