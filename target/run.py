from subprocess import *

def jarWrapper(*args):
	arguments = list(args)
	process = Popen(['java', '-jar']+arguments, stdout=PIPE, stderr=PIPE)
	result = ""
	while process.poll() is None:
		line = process.stdout.readline()
		if line != '' and line.endswith('\n'):
			result += line
	return result

def doEvolve(allowDuplicates):
    bestFitness = []
    for i in range(1,11):
	    distanceFeaturePercentage = i/10.0
	    args = ['PatternRecognition-1.0-SNAPSHOT.jar',"%s" % distanceFeaturePercentage, allowDuplicates] # Any number of args to be passed to the jar file
	    result = jarWrapper(*args)
	    target_path = "results/Ionisphere_Int_%s_%s.txt" % (i*10,allowDuplicates)
	    target_file = open(target_path,'w')
	    target_file.write(result)
	    target_file.close()
	    split = result.splitlines()
	    bestFitness.append(split[len(split)-3].split()[2])
	    print "%s" % bestFitness[i-1]

    target_path = "results/Ionisphere_Int_%s_%s.dat" % ("total",allowDuplicates)
    target_file = open(target_path,'w')
    for i in range(1,11):
        target_file.write("%s    %s\n" % (i,bestFitness[i-1]))
    target_file.close()

    call(["gnuplot","-e","filename='results/Ionisphere_Int_total_%s.dat';outputFile='results/Ionisphere_Int_total_%s.eps'" % (allowDuplicates,allowDuplicates), "results/plot.plt"])

doEvolve("true")
doEvolve("false")
