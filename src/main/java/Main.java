

import java.io.IOException;
import java.util.ArrayList;

import evSOLve.JEvolution.Individual;
import evSOLve.JEvolution.JEvolution;
import evSOLve.JEvolution.JEvolutionException;
import evSOLve.JEvolution.JEvolutionReporter;
import evSOLve.JEvolution.chromosomes.IntChromosome;
import evSOLve.JEvolution.chromosomes.PermChromosome;


public class Main{

    public static void main(String[] args) throws IOException {

        // The three data sets to use:

        // IONOSPHERE (TWO CLASS PROBLEM, good/bad signal)
        // https://archive.ics.uci.edu/ml/datasets/Ionosphere
        // number of features: 34
         String inputFile = "data/ionosphere_mapped.data";

        // SEMEION HANDWRITTEN DIGITS (10 CLASS PROBLEM, 0...9)
        // https://archive.ics.uci.edu/ml/datasets/Semeion+Handwritten+Digit
        // number of features: 256 (!!!)
        // String inputFile = "data/semeion_mapped.data";

        // RED WINE QUALITY (6 CLASS PROBLEM, since only scores between 3 and 8 available in the data set)
        // https://archive.ics.uci.edu/ml/datasets/Wine+Quality
        // number of features: 11


        // OPTIONAL WINE DATASET (INITIAL ONE):
        // https://archive.ics.uci.edu/ml/datasets/Wine
        // number of features: 13
        // String inputFile = "data/wine.data";



        JEvolution EA = JEvolution.getInstance();																					//+ call it an EA
// 		EA.setMaximization(false);																											//o minimization problem
        JEvolutionReporter EAReporter = (JEvolutionReporter)EA.getReporter();			//- get the reporter
        			                        //+ create a chromosome

        // Load datafrom file
        ArrayList<Pattern> patterns=MyFileIO.readPatternsFromFile(inputFile);


        //init phenotype with problem specific patterns
        MyPhenotype phenotype = new MyPhenotype(patterns, 3);

        IntChromosome chrom = new IntChromosome(phenotype.getAttributeCount());
        //PermChromosome chrom = new PermChromosome();
        try {
            chrom.setLength(phenotype.getAttributeCount());
            //chrom.setCrossoverPoints(knnPheno.getUsedFeatures());

            //- only set to justify try statement..;-)
            chrom.setMutationRate(0.1);
//			chromX.setSoupType(Chromosome.LAPLACE);
//			chromX.setCrossoverPoints(2);
// 			Utilities.setRandomSeed(88);

            EA.addChromosome(chrom);																//+ tell EA about your chromosome
            EA.setPhenotype(phenotype);											                    //+ tell EA about your Phenotype class
//			EA.setSelection(new TournamentSelection(3));
// 			EA.setPopulationSize(25, 50);
            EA.setFitnessThreshold(1.0);																//o better fitness not possible
           // EA.setMaximalGenerations(20);														//o

            EAReporter.setReportLevel(JEvolutionReporter.BRIEF);
// 			EAReporter.useFitnessRepository(true);

        } catch (JEvolutionException e) {
            System.out.println(e.toString());
            System.out.println("Continuing with default values.");
        }
        System.out.println("Starting evolution...");

        EA.doEvolve(100);



        Individual best = EAReporter.getBestIndividual();
        best.toFile("bestResult.xml");
        //Individual bestFromFile = new Individual("bestResult.xml");

        //System.out.println(best.getGenotype().equals(bestFromFile.getGenotype()));

    }

}