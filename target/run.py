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

def calcLength(individual):
	splitIndividual = individual.split("|")
	splitIndividual.pop()
	newIndividual = []
	for i in range(0,len(splitIndividual),1):
		if splitIndividual[i] not in newIndividual:
			newIndividual.append(splitIndividual[i])

	return len(newIndividual)


def doEvolve(data,encoding,allowDuplicates,distanceFeaturePercentage):

	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",encoding,str(distanceFeaturePercentage), allowDuplicates]
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	print result
	bestFitness = split[len(split)-3].split()[2]

	avgIndividualLengths = []
	for i in range(1,len(split)-8,8):
		avgIndividualLengths.append(split[i].split()[1])

	featureOccurrencies = []
	for i in range(2,len(split)-8,8):
		featureOccurrencies.append(split[i].split(" ",1)[1])

	avgFitnessValues = []
	for i in range(5,len(split)-7,8):
		avgFitnessValues.append(split[i].split()[1])

	bestIndividualLengths = []
	for i in range(7,len(split)-7,8):
		bestIndividualLengths.append(calcLength(split[i].split()[1]))
	return bestFitness,avgFitnessValues,avgIndividualLengths,bestIndividualLengths,featureOccurrencies

def run(data, encoding, allowDuplicates):
	bestFitnessValues = []
	averagesFitness = []
	averagesLength = []
	bestsLength = []
	maxFitnessIndex = 0
	bestDistanceFeaturePercentage = 0.0;
	if (encoding == "integer"):
		bestFitness, avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(data,encoding,allowDuplicates,1)
		bestFitnessValues.append(bestFitness)
		averagesFitness.append(avgFitnessValues)
		averagesLength.append(avgIndividualLengths)
		bestsLength.append(bestIndividualLengths)
		for i in range(2,11):
			bestFitnessValues.append(bestFitnessValues[i-2])
			averagesFitness.append(averagesFitness[i-2])
			averagesLength.append(averagesLength[i-2])
			bestsLength.append(bestsLength[i-2])
	else:
		if(data == "semeion_mapped"):
			bottom = 5
			for i in range(1,bottom):
				bestFitnessValues.append(0)
				averagesFitness.append(0)
				averagesLength.append(0)
				bestsLength.append(0)
		else:
			bottom = 1
		for i in range(bottom,11):
			distanceFeaturePercentage = i/10.0
			bestFitness,avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(data,encoding,allowDuplicates,distanceFeaturePercentage)
			bestFitnessValues.append(bestFitness)
			averagesFitness.append(avgFitnessValues)
			averagesLength.append(avgIndividualLengths)
			bestsLength.append(bestIndividualLengths)
			if (bestFitnessValues[maxFitnessIndex] < bestFitnessValues[i-1]):
				maxFitnessIndex = i-1
				bestDistanceFeaturePercentage = i/10.0
			print "%s" % bestFitnessValues[i-1]

	l =  bestDistanceFeaturePercentage * float(averagesLength[maxFitnessIndex][0])
	print l
	cut_path = "results/%s/%s_%s_cut_%s" % (data,data,encoding,allowDuplicates)
	cut_file = open("%s.dat" % cut_path,'w')
	for i in range(1,11):
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
		if encoding == "permutation":
			avg_length_file.write("%s	%s\n" % (i,l))
		else:
			avg_length_file.write("%s	%s\n" % (i,averagesLength[maxFitnessIndex][i]))
	avg_length_file.close()

	best_length_path = "results/%s/%s_%s_best_length_%s" % (data,data,encoding,allowDuplicates)
	best_length_file = open("%s.dat" % best_length_path,'w')
	for i in range(0,len(bestsLength[maxFitnessIndex])):
		if encoding == "permutation":
			best_length_file.write("%s	%s\n" % (i,l))
		else:
			best_length_file.write("%s	%s\n" % (i,bestsLength[maxFitnessIndex][i]))
	best_length_file.close()

	feature_occurrency_path = "results/%s/%s_%s_feature_occurrency_%s" % (data,data,encoding,allowDuplicates)
	feature_occurrency_file = open("%s.dat" % feature_occurrency_path,'w')
	if encoding == "integer":
		for i in range(0,len(featureOccurrencies),10):
			split =  featureOccurrencies[i].split(",")
			feature_occurrency_file.write("%s" % i)
			for j in range(0,len(split)):
				if j == 0:
					feature_occurrency_file.write(" %s " % split[j][1:])
				elif j==len(split)-1:
					feature_occurrency_file.write(" %s " % split[j][:-1])
				else:
					feature_occurrency_file.write(" %s " % split[j])
			feature_occurrency_file.write("\n")
	feature_occurrency_file.close();
	return cut_path,avg_fitness_path,avg_length_path,best_length_path,feature_occurrency_path

# add robots data
data = ["ionosphere_mapped","semeion_mapped","sensor_readings_mapped","a"]

i = 2
#evolution with integer encoding
cut1, avg_fitness1, avg_length1, best_length1, feature_occurrency1 = run(data[i], "integer", "true")
cut2, avg_fitness2, avg_length2, best_length2, feature_occurrency2 = run(data[i], "integer", "false")
#evolution with permution encoding, duplicates do not occur in this approach
cut3, avg_fitness3, avg_length3, best_length3, feature_occurrency3 = run(data[i], "permutation", "false")


#file1 = "results/%s/%s_Integer_total_true" % (data[i],data[i])
#file2 = "results/%s/%s_Integer_total_false" % (data[i],data[i])
#file3 = "results/%s/%s_Permutation_total_false" % (data[i],data[i])
print "plotting: %s %s %s" % (cut1,cut2,cut3)
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (avg_fitness1,avg_fitness2,avg_fitness3,data[i],"avg_fitness_generations"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (avg_length1,avg_length2,avg_length3,data[i],"avg_length_generations"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (best_length1,best_length2,best_length3,data[i],"best_length_generations"), "results/plot_all.plt"])
call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (cut1,cut2,cut3,data[i],"cut"), "results/plot_all.plt"])

call(["gnuplot","-e","file1='%s.dat';outputFile='results/%s/%s.eps'" % (feature_occurrency1,data[i],"hist"), "results/plot_hist.plt"])

#call(["gnuplot","-e","filename='%s.dat';outputFile='results/%s/%s.eps'" % (file3,data[1],"permutation"), "results/plot.plt"])
