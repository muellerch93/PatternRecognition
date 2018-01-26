from subprocess import *
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def jarWrapper(*args):
	arguments = list(args)
	print list(args)
	process = Popen(['java', '-jar']+arguments, stdout=PIPE, stderr=PIPE)
	result = ""
	while process.poll() is None:
		line = process.stdout.readline()
		if line != '' and line.endswith('\n'):
			result += line
	#print result
	return result

def calcLength(individual):
	splitIndividual = individual.split("|")
	splitIndividual.pop()
	newIndividual = []
	for i in range(0,len(splitIndividual),1):
		if splitIndividual[i] not in newIndividual:
			newIndividual.append(splitIndividual[i])

	return len(newIndividual)

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def doEvolve(dataset_index,encoding,allowDuplicates,distanceFeaturePercentage):
	data = datasets[dataset_index]
	args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % "data/"+data+".data",encoding,str(distanceFeaturePercentage), allowDuplicates]
	result = jarWrapper(*args)
	target_path = "results/%s/%s_%s_%s_%s.txt" % (data,data,encoding,str(distanceFeaturePercentage*100),allowDuplicates)
	target_file = open(target_path,'w')
	target_file.write(result)
	target_file.close()
	split = result.splitlines()
	bestIndividual = split[len(split)-1]
	#print bestIndividual
	bestIndividualSplit = bestIndividual.split("|")
	bestIndividualFeatureCount = [0] * dataset_feature_counts[dataset_index]
	for i in range(0,len(bestIndividualSplit)-1):
		bestIndividualFeatureCount[(int) (bestIndividualSplit[i])] = bestIndividualFeatureCount[(int) (bestIndividualSplit[i])] + 1
	bestIndividualFeatureCount = remove_values_from_list(bestIndividualFeatureCount, 0)
	#print bestIndividualFeatureCount
	bestFitness = split[len(split)-4].split()[2]

	avgIndividualLengths = []
	for i in range(1,len(split)-10,8):
		avgIndividualLengths.append(split[i].split()[1])


	featureOccurrencies = []
	for i in range(2,len(split)-10,8):
		featureOccurrencies.append(split[i].split(" ",1)[1])

	avgFitnessValues = []
	for i in range(5,len(split)-10,8):
		avgFitnessValues.append(split[i].split()[1])

	bestIndividualLengths = []
	for i in range(7,len(split)-10,8):
		bestIndividualLengths.append(calcLength(split[i].split()[1]))
	return bestFitness,bestIndividualFeatureCount,avgFitnessValues,avgIndividualLengths,bestIndividualLengths,featureOccurrencies

def write_result_to_files(
	dataset,encoding,allowDuplicates,bestFitness, avgFitnessValues,
	avgIndividualLengths,bestIndividualLengths,featureOccurrencies):
	desiredLength = 0
	best_fitness_path = "results/%s/%s_%s_%s_%s" % (dataset,dataset,"best_fitness",encoding,allowDuplicates)
	best_fitness_file = open("%s.dat" % best_fitness_path,'w')
	best_fitness_file.write("%s	%s\n" % (0,bestFitness))
	best_fitness_file.close()

	avg_fitness_path = write_fitness_to_file(dataset,"avg_fitness",encoding,allowDuplicates,avgFitnessValues)

	avg_length_path = write_length_to_file(dataset,"avg_length",encoding,allowDuplicates,avgIndividualLengths,desiredLength)
	best_length_path = write_length_to_file(dataset,"best_length",encoding,allowDuplicates,bestIndividualLengths,desiredLength)

	feature_occurrency_path = "results/%s/%s_%s_feature_occurrency_%s" % (dataset,dataset,encoding,allowDuplicates)
	feature_occurrency_file = open("%s.dat" % feature_occurrency_path,'w')
	if encoding == "integer":
		for i in range(0,len(featureOccurrencies),20):
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
	return best_fitness_path,avg_fitness_path,avg_length_path,best_length_path,feature_occurrency_path

def generate_plots(dataset_index,paths,best_individual_features_path,avg_fitness_paths,avg_length_paths,best_length_paths,feature_occurrency_paths,isFast):
	dataset = datasets[dataset_index]
	dataset_feature_count = dataset_feature_counts[dataset_index]
	call(["gnuplot","-e","labelx='generation';labely='fitness';file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'"
		% (avg_fitness_paths[0],avg_fitness_paths[1],avg_fitness_paths[2],dataset,"avg_fitness_generations"), "results/plot_all.plt"])
	call(["gnuplot","-e","labelx='generations';labely='feature countt';file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'"
		% (avg_length_paths[0],avg_length_paths[1],avg_length_paths[2],dataset,"avg_length_generations"), "results/plot_all.plt"])
	call(["gnuplot","-e","labelx='generations';labely='feature count';file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'"
		% (best_length_paths[0],best_length_paths[1],best_length_paths[2],dataset,"best_length_generations"), "results/plot_all.plt"])


	if (isFast):
		call(["gnuplot","-e","labelx='generation';labely='fitness';file1='%s.dat';outputFile='results/%s/%s.eps'"
			% (paths[0],dataset,"best_fitness"), "results/plot_hist_single.plt"])
		call(["gnuplot","-e","featureCount=%s;labelx='encoding';labely='';file1='%s.dat';outputFile='results/%s/%s.eps'"
			% (dataset_feature_count+1,best_individual_features_path[0],dataset,"best_individual"), "results/plot_hist.plt"])
	else:
		call(["gnuplot","-e","labelx='cutting point';labely='fitness';file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'"
			% (paths[0],paths[1],paths[2],dataset,"cut"), "results/plot_all.plt"])

	call(["gnuplot","-e","featureCount=%s;labelx='generation';labely='feature occurrence';file1='%s.dat';outputFile='results/%s/%s.eps'"
		% (dataset_feature_count+1,feature_occurrency_paths[0],dataset,"feature_frequency_integer_x"), "results/plot_hist.plt"])
	call(["gnuplot","-e","featureCount=%s;labelx='generation';labely='feature occurrence';file1='%s.dat';outputFile='results/%s/%s.eps'"
		% (dataset_feature_count+1,feature_occurrency_paths[1],dataset,"feature_frequency_integer"), "results/plot_hist.plt"])
	#call(["gnuplot","-e","file1='%s.dat';file2='%s.dat';file3='%s.dat';outputFile='results/%s/%s.eps'" % (cut1,cut2,cut3,dataset,"cut"), "results/plot_all.plt"])
	#


def run_fast(dataset_index):
	dataset = datasets[dataset_index]

	best_fitness_paths = ["", "", ""]
	avg_fitness_paths = ["", "", ""]
	avg_length_paths = ["", "", ""]
	best_length_paths = ["", "", ""]
	feature_occurrency_paths = ["", "", ""]
	best_fitness_values = [0, 0, 0]
	bestIndividualFeatureCounts =["","",""]

	best_fitness_values[0],bestIndividualFeatureCounts[0], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,"integer","true", 1)
	best_fitness_paths[0],avg_fitness_paths[0],avg_length_paths[0],best_length_paths[0],feature_occurrency_paths[0] = write_result_to_files(
		dataset,"integer","true",best_fitness_values[0], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies)

	best_fitness_values[1],bestIndividualFeatureCounts[1], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,"integer","false", 1)
	best_fitness_paths[1],avg_fitness_paths[1],avg_length_paths[1],best_length_paths[1],feature_occurrency_paths[1] = write_result_to_files(
		dataset,"integer","false",best_fitness_values[1], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies)

	#for permutation choose best length depending on dataset
	if (dataset =="ionosphere_mapped"):
		best_fitness_values[2],bestIndividualFeatureCounts[2], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,"permutation","false",0.25)
	elif (dataset == "semeion_mapped"):
		best_fitness_values[2],bestIndividualFeatureCounts[2], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,"permutation","false",0.9)
	elif (dataset == "sensor_readings_mapped"):
		best_fitness_values[2],bestIndividualFeatureCounts[2], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,"permutation","false",0.25)
	best_fitness_paths[2],avg_fitness_paths[2],avg_length_paths[2],best_length_paths[2],feature_occurrency_paths[2] = write_result_to_files(
		dataset,"permutation","false", best_fitness_values[2], avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies)

	#merge best_fitness into one file
	best_fitness_total_path = "results/%s/%s_best_fitness_total" % (dataset,dataset)
	best_fitness_total_file = open("%s.dat" % (best_fitness_total_path), "w")
	best_fitness_total_file.write("IntegerX %s\n" % (best_fitness_values[0]))
	best_fitness_total_file.write("Integer %s\n" % (best_fitness_values[1]))
	best_fitness_total_file.write("Permutation %s\n" % (best_fitness_values[2]))
	best_fitness_total_file.close()

	best_individual_features_path = "results/%s/%s_best_individual_features" % (dataset,dataset)
	best_individual_features_file = open("%s.dat" % (best_individual_features_path), "w")
	best_individual_features_file.write('"IntegerX (%s unique features)"' % len(bestIndividualFeatureCounts[0]))
	for i in range(0,len(bestIndividualFeatureCounts[0]),1):
		best_individual_features_file.write(" %s " % bestIndividualFeatureCounts[0][i])
	best_individual_features_file.write("\n")
	best_individual_features_file.write('"Integer (%s unique features)"' % len(bestIndividualFeatureCounts[1]))
	for i in range(0,len(bestIndividualFeatureCounts[1]),1):
		best_individual_features_file.write(" %s " % bestIndividualFeatureCounts[1][i])
	best_individual_features_file.write("\n")
	best_individual_features_file.close()

	generate_plots(
		dataset_index,[best_fitness_total_path],[best_individual_features_path],
		avg_fitness_paths, avg_length_paths, best_length_paths,feature_occurrency_paths,True)

def run(dataset_index, encoding, allowDuplicates):
	dataset = datasets[dataset_index]
	bestFitnessValues = []
	averagesFitness = []
	averagesLength = []
	bestsLength = []
	maxFitnessIndex = 0
	bestLength = 0.0;
	if (encoding == "integer"):
		bestFitness,bestIndividualFeatureCount, avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,encoding,allowDuplicates,1)
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
		for i in range(1 , 11):
			length = i/10.0 #length = 0.2 + i/100.0
			bestFitness,bestIndividualFeatureCount, avgFitnessValues, avgIndividualLengths,bestIndividualLengths,featureOccurrencies = doEvolve(dataset_index,encoding,allowDuplicates,length)
			bestFitnessValues.append(bestFitness)
			averagesFitness.append(avgFitnessValues)
			averagesLength.append(avgIndividualLengths)
			bestsLength.append(bestIndividualLengths)
			if (bestFitnessValues[maxFitnessIndex] < bestFitnessValues[i-1]):
				maxFitnessIndex = i-1
				bestLength = i/10.0
			print "%s" % bestFitnessValues[i-1]

	#the length of the permutation individuals that yield the best fitness
	desiredLength =  bestLength * float(averagesLength[maxFitnessIndex][0])

	cut_path = write_fitness_to_file(dataset,"cut",encoding,allowDuplicates,bestFitnessValues)
	# write avg of generations for run (cutting point) that led to the overal best individual (only relevant for permutation encoding)
	#print "avg. at %s : %s" % (maxFitnessIndex,averages[maxFitnessIndex])
	avg_fitness_path = write_fitness_to_file(dataset,"avg_fitness",encoding,allowDuplicates,averagesFitness[maxFitnessIndex])

	avg_length_path = write_length_to_file(dataset,"avg_length",encoding,allowDuplicates,averagesLength[maxFitnessIndex],desiredLength)
	best_length_path = write_length_to_file(dataset,"best_length",encoding,allowDuplicates,bestsLength[maxFitnessIndex],desiredLength)

	feature_occurrency_path = "results/%s/%s_%s_feature_occurrency_%s" % (dataset,dataset,encoding,allowDuplicates)
	feature_occurrency_file = open("%s.dat" % feature_occurrency_path,'w')
	if encoding == "integer":
		for i in range(0,len(featureOccurrencies),30):
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

def write_fitness_to_file(dataset,name,encoding,allowDuplicates,fitnessValues):
	fitness_path = "results/%s/%s_%s_%s_%s" % (dataset,dataset,name,encoding,allowDuplicates)
	fitness_file = open("%s.dat" % fitness_path,'w')
	for i in range(0,len(fitnessValues)):
		if name == "cut":
			fitness_file.write("%s	%s\n" % ((i+1)*10,fitnessValues[i]))
		else:
			fitness_file.write("%s	%s\n" % (i,fitnessValues[i]))
	#print averages[maxFitnessIndex]
	fitness_file.close()
	return fitness_path

def write_length_to_file(dataset,name,encoding,allowDuplicates,lengths,desiredLength):
	length_path = "results/%s/%s_%s_%s_%s" % (dataset,dataset,name,encoding,allowDuplicates)
	length_file = open("%s.dat" % length_path,'w')
	for i in range(0,len(lengths)):
		if encoding == "permutation":
			length_file.write("%s	%s\n" % (i,desiredLength))
		else:
			length_file.write("%s	%s\n" % (i,lengths[i]))
	length_file.close()
	return length_path


def full(dataset_index):
	dataset = datasets[dataset_index]
	best_cut_paths = ["","",""]
	avg_fitness_paths = ["","",""]
	avg_length_paths = ["","",""]
	best_length_paths = ["","",""]
	feature_occurrency_paths = ["","",""]

	#evolution with integer encoding
	best_cut_paths[0], avg_fitness_paths[0], avg_length_paths[0], best_length_paths[0], feature_occurrency_paths[0] = run(dataset_index, "integer", "true")
	best_cut_paths[1], avg_fitness_paths[1], avg_length_paths[1], best_length_paths[1], feature_occurrency_paths[1] = run(dataset_index, "integer", "false")
	#evolution with permution encoding, duplicates do not occur in this approach
	best_cut_paths[2], avg_fitness_paths[2], avg_length_paths[2], best_length_paths[2], feature_occurrency_paths[2] = run(dataset_index, "permutation", "false")
	generate_plots(dataset_index,best_cut_paths,[""],avg_fitness_paths,avg_length_paths,best_length_paths,feature_occurrency_paths,False)


datasets = ["ionosphere_mapped","semeion_mapped","sensor_readings_mapped"]
dataset_feature_counts = [ 34, 256, 24]
#run_fast(1)
full(2)
#for i in range(2,len(datasets)):
	#full(datasets[i])
	#run_fast(datasets[i])
