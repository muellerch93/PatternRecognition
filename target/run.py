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
		encoding = "Permutation"

	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",isIntegerEncoding,str(distanceFeaturePercentage), allowDuplicates] 
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	bestFitness = split[len(split)-3].split()[2]
	avgFitnessValues = []
	for i in range(3,len(split)-7,6):
		avgFitnessValues.append(split[i].split()[1])
	return bestFitness,avgFitnessValues


def run(data, isIntegerEncoding, allowDuplicates):
	bestFitnessValues = []
	averages = []
	if (isIntegerEncoding == "true"):
		encoding = "Integer"
		bestFitness, avgFitnessValues = doEvolve(data,isIntegerEncoding,allowDuplicates,1)
		bestFitnessValues.append(bestFitness)
		averages.append(avgFitnessValues)
		for i in range(2,11):
			bestFitnessValues.append(bestFitnessValues[i-2])
			averages.append(averages[i-2])
	else:
		encoding = "Permutation"
		if(data == "semeion_mapped"):
			bottom = 5
			for i in range(1,bottom):
				bestFitnessValues.append(0)
		else: 
			bottom = 1
		for i in range(bottom,11):
			distanceFeaturePercentage = i/10.0
			bestFitness,avgFitnessValues = doEvolve(data,isIntegerEncoding,allowDuplicates,distanceFeaturePercentage)
			bestFitnessValues.append(bestFitness)
			averages.append(avgFitnessValues)
			print "%s" % bestFitnessValues[i-1]
	
	target_path = "results/%s/%s_%s_total_%s" % (data,data,encoding,allowDuplicates)
	target_file = open("%s.dat" % target_path,'w')
	maxFitnessIndex = 0
	for i in range(1,11):
		if (bestFitnessValues[maxFitnessIndex] < bestFitnessValues[i-1]):
			maxFitnessIndex = i-1
		target_file.write("%s    %s\n" % (i*10,bestFitnessValues[i-1]))
	target_file.close()
	
	# write avg of generations for run (cutting point) that led to the overal best individual (only relevant for permutation encoding)
	print "avg. at %s : %s" % (maxFitnessIndex,averages[maxFitnessIndex])
	avg_path = "results/%s/%s_%s_avg_%s" % (data,data,encoding,allowDuplicates)
	avg_file = open("%s.dat" % avg_path,'w')
	for i in range(0,len(averages[maxFitnessIndex])):
		avg_file.write("%s    %s\n" % (i,averages[maxFitnessIndex][i]))
	print averages[maxFitnessIndex]
	avg_file.close()

	return target_path,avg_path

data = ["ionosphere_mapped","semeion_mapped"]

i = 0 
#evolution with integer encoding
file1,avg1 = run(data[i],"true","true")
file2,avg2 = run(data[i],"true","false")
#evolution with permution encoding, duplicates do not occur in this approach 
file3,avg3 = run(data[i],"false","false")


#file1 = "results/%s/%s_Integer_total_true" % (data[i],data[i])
#file2 = "results/%s/%s_Integer_total_false" % (data[i],data[i])
#file3 = "results/%s/%s_Permutation_total_false" % (data[i],data[i])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (file1,file2,file3,data[i],"cut"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (avg1,avg2,avg3,data[i],"generations"), "results/plot_all.plt"])
#call(["gnuplot","-e","filename='%s.dat';outputFile='results/%s/%s.eps'" % (file3,data[1],"permutation"), "results/plot.plt"])
