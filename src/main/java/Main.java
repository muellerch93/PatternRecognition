

import java.util.ArrayList;

import evSOLve.JEvolution.JEvolution;
import evSOLve.JEvolution.chromosomes.Chromosome;
import evSOLve.JEvolution.chromosomes.IntChromosome;
import evSOLve.JEvolution.chromosomes.PermChromosome;


public class Main {

    public static void main(String[] args) throws Exception {

        // The three data sets to use:

        // IONOSPHERE (TWO CLASS PROBLEM, good/bad signal)
        // https://archive.ics.uci.edu/ml/datasets/Ionosphere
        // number of features: 34
        //String inputFile = "data/ionosphere_mapped.data";

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


        //+ call it an EA
// 		EA.setMaximization(false);																											//o minimization problem
        // JEvolutionReporter EAReporter = (JEvolutionReporter)EA.getReporter();			                            //- get the reporter
        //+ create a chromosome
        ArrayList<Pattern> patterns;
        boolean isIntegerEncoding;
        double distanceFeaturePercentage;
        boolean isEuclideanDistance;

        if(args.length == 4){
            String inputFilePath= args[0];
            patterns = MyFileIO.readPatternsFromFile(inputFilePath);
            isIntegerEncoding = Boolean.parseBoolean(args[1]);
            distanceFeaturePercentage = Double.parseDouble(args[2]);
            isEuclideanDistance = Boolean.parseBoolean(args[3]);

        }else{
            patterns = MyFileIO.readPatternsFromFile("data/ionosphere_mapped.data");
            isIntegerEncoding = true;
            distanceFeaturePercentage = 0.3;
            isEuclideanDistance = true;

        }


        doEvolution(patterns,isIntegerEncoding,distanceFeaturePercentage,isEuclideanDistance);
        //doEvolution(patterns, true,0.3, true);

        // Individual best = EAReporter.getBestIndividual();
        // best.toFile("bestResult.xml");
        //Individual bestFromFile = new Individual("bestResult.xml");

        //System.out.println(best.getGenotype().equals(bestFromFile.getGenotype()));

    }

    public static void doEvolution(ArrayList<Pattern> patterns, boolean isIntegerEncoding, double distanceFeaturePercentage,
                                   boolean isEuclideanDistance) throws Exception {
        JEvolution EA = JEvolution.getInstance();
        //PermChromosome chrom = new PermChromosome();
        //init phenotype with problem specific patterns

        MyPhenotype phenotype = new MyPhenotype(patterns, distanceFeaturePercentage, isEuclideanDistance);
        Chromosome chrom;
        if (isIntegerEncoding)
            chrom=new IntChromosome(phenotype.getAttributeCount());
        else
            chrom=new PermChromosome(phenotype.getAttributeCount());
        chrom.setLength(phenotype.getAttributeCount());
        //chrom.setCrossoverPoints(knnPheno.getUsedFeatures());

        //- only set to justify try statement..;-)
        chrom.setMutationRate(0.1);
//			chromX.setSoupType(Chromosome.LAPLACE);
//			chromX.setCrossoverPoints(2);
// 			Utilities.setRandomSeed(88);

        EA.addChromosome(chrom);                                                                //+ tell EA about your chromosome
        EA.setPhenotype(phenotype);                                                                //+ tell EA about your Phenotype class
//			EA.setSelection(new TournamentSelection(3));
// 			EA.setPopulationSize(25, 50);
        EA.setFitnessThreshold(1.0);                                                                //o better fitness not possible
        EA.setMaximalGenerations(50);                                                        //o

        // EAReporter.setReportLevel(JEvolutionReporter.BRIEF);
// 			EAReporter.useFitnessRepository(true);


        System.out.println("Starting evolution...");

        EA.doEvolve();

    }

}