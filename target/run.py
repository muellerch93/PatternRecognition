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
	print result
	return result


def doEvolve(data,isIntegerEncoding,allowDuplicates,distanceFeaturePercentage):
	if isIntegerEncoding == "true":
		encoding = "integer"
	else:
		encoding = "permutation"

	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",isIntegerEncoding,str(distanceFeaturePercentage), allowDuplicates]
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	bestFitness = split[len(split)-3].split()[2]
	avgFitnessValues = []
	for i in range(4,len(split)-7,7):
		avgFitnessValues.append(split[i].split()[1])
	avgIndividualLength = []
	for i in range(1,len(split)-8,7):
		avgIndividualLength.append(split[i].split()[1])
	return bestFitness,avgFitnessValues,avgIndividualLength


def run(data, isIntegerEncoding, allowDuplicates):
	bestFitnessValues = []
	averagesFitness = []
	averagesLength = []
	if (isIntegerEncoding == "true"):
		encoding = "integer"
		bestFitness, avgFitnessValues, avgIndividualLengths = doEvolve(data,isIntegerEncoding,allowDuplicates,1)
		bestFitnessValues.append(bestFitness)
		averagesFitness.append(avgFitnessValues)
		averagesLength.append(avgIndividualLengths)
		for i in range(2,11):
			bestFitnessValues.append(bestFitnessValues[i-2])
			averagesFitness.append(averagesFitness[i-2])
			averagesLength.append(averagesLength[i-2])
	else:
		encoding = "permutation"
		if(data == "semeion_mapped"):
			bottom = 5
			for i in range(1,bottom):
				bestFitnessValues.append(0)
				averagesFitness.append(0)
				averagesLength.append(0)
		else:
			bottom = 1
		for i in range(bottom,11):
			distanceFeaturePercentage = i/10.0
			bestFitness,avgFitnessValues, avgIndividualLengths = doEvolve(data,isIntegerEncoding,allowDuplicates,distanceFeaturePercentage)
			bestFitnessValues.append(bestFitness)
			averagesFitness.append(avgFitnessValues)
			averagesLength.append(avgIndividualLengths)
			print "%s" % bestFitnessValues[i-1]


	cut_path = "results/%s/%s_%s_cut_%s" % (data,data,encoding,allowDuplicates)
	cut_file = open("%s.dat" % cut_path,'w')
	maxFitnessIndex = 0
	for i in range(1,11):
		if (bestFitnessValues[maxFitnessIndex] < bestFitnessValues[i-1]):
			maxFitnessIndex = i-1
		cut_file.write("%s    %s\n" % (i*10,bestFitnessValues[i-1]))
	cut_file.close()

	# write avg of generations for run (cutting point) that led to the overal best individual (only relevant for permutation encoding)
	#print "avg. at %s : %s" % (maxFitnessIndex,averages[maxFitnessIndex])
	avg_fitness_path = "results/%s/%s_%s_avg_fitness_%s" % (data,data,encoding,allowDuplicates)
	avg_fitness_file = open("%s.dat" % avg_fitness_path,'w')
	for i in range(0,len(averagesFitness[maxFitnessIndex])):
		avg_fitness_file.write("%s    %s\n" % (i,averagesFitness[maxFitnessIndex][i]))
	#print averages[maxFitnessIndex]
	avg_fitness_file.close()

	avg_length_path = "results/%s/%s_%s_avg_length_%s" % (data,data,encoding,allowDuplicates)
	avg_length_file = open("%s.dat" % avg_length_path,'w')
	for i in range(0,len(averagesLength[maxFitnessIndex])):
		avg_length_file.write("%s	%s\n" % (i,averagesLength[maxFitnessIndex][i]))
	avg_length_file.close()

	return cut_path,avg_fitness_path,avg_length_path

data = ["ionosphere_mapped","semeion_mapped"]

i = 0
#evolution with integer encoding
cut1, avg_fitness1, avg_length1 = run(data[i], "true", "true")
cut2, avg_fitness2, avg_length2 = run(data[i], "true", "false")
#evolution with permution encoding, duplicates do not occur in this approach
cut3, avg_fitness3, avg_length3 = run(data[i], "false", "false")


#file1 = "results/%s/%s_Integer_total_true" % (data[i],data[i])
#file2 = "results/%s/%s_Integer_total_false" % (data[i],data[i])
#file3 = "results/%s/%s_Permutation_total_false" % (data[i],data[i])
print "plotting: %s %s %s" % (cut1,cut2,cut3)
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (avg_fitness1,avg_fitness2,avg_fitness3,data[i],"avg_fitness_generations"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (avg_length1,avg_length2,avg_length3,data[i],"avg_length_generations"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (cut1,cut2,cut3,data[i],"cut"), "results/plot_all.plt"])

#call(["gnuplot","-e","filename='%s.dat';outputFile='results/%s/%s.eps'" % (file3,data[1],"permutation"), "results/plot.plt"])
