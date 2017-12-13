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


def doEvolve(data,isIntegerEncoding,allowDuplicates,distanceFeaturePercentage):
	if isIntegerEncoding == "true":
		encoding = "Integer"
	else:
		encoding = "Binary"

	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",isIntegerEncoding,str(distanceFeaturePercentage), allowDuplicates] 
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	bestFitness = split[len(split)-3].split()[2]
	return bestFitness

def run(data, isIntegerEncoding, allowDuplicates):
	bestFitnessValues = []
    
	if (isIntegerEncoding == "true"):
		encoding = "Integer"
		bestFitnessValues.append(doEvolve(data,isIntegerEncoding,allowDuplicates,1))
		for i in range(2,11):
			bestFitnessValues.append(bestFitnessValues[i-2])
	else:
		encoding = "Binary"
		for i in range(1,11):
			distanceFeaturePercentage = i/10.0
			bestFitnessValues.append(doEvolve(data,isIntegerEncoding,allowDuplicates,distanceFeaturePercentage))
			print "%s" % bestFitnessValues[i-1]
	target_path = "results/%s/%s_%s_total_%s" % (data,data,encoding,allowDuplicates)
	target_file = open("%s.dat" % target_path,'w')
	for i in range(1,11):
		target_file.write("%s    %s\n" % (i*10,bestFitnessValues[i-1]))
	target_file.close()
	return target_path

data = ["ionosphere_mapped","semeion_mapped"]

#evolution with integer encoding
#file1 = run(data[1],"true","true")
#file2 = run(data[1],"true","false")
#evolution with binary encoding, duplicates do not occur in this approach 
#file3 = run(data[1],"false","false")

i = 0 
file1 = "results/%s/%s_Integer_total_true" % (data[i],data[i])
file2 = "results/%s/%s_Integer_total_false" % (data[i],data[i])
file3 = "results/%s/%s_Binary_total_false" % (data[i],data[i])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (file1,file2,file3,data[i],"all"), "results/plot_all.plt"])

