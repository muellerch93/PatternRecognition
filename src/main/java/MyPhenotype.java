import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;


import evSOLve.JEvolution.chromosomes.IntChromosome;
import evSOLve.JEvolution.chromosomes.PermChromosome;


public class MyPhenotype extends SortPhenotype {


    private int k = 1;


    private ArrayList<Pattern> data;
    private double distanceFeaturePercentage;
    private boolean isEuclideanDistance;
    private static Random rand;
    private static int individualCount = 1;
    private static double sum;
    private static double maxFitness;
    private static int featureOccurrenceCount[];
    /**
     * Constructs the basic phenotype.
     *
     * @throws IOException
     */

    /**
     * public MyPhenotype(ArrayList<Pattern> patterns) throws IOException {
     * this.data = patterns;
     * <p>
     * }
     **/

    public MyPhenotype(ArrayList<Pattern> patterns, double distanceFeaturePercentage, boolean isEuclideanDistance) throws IOException {
        rand = new Random();
        this.data = patterns;
        featureOccurrenceCount = new int[patterns.get(0)._features.length];
        this.distanceFeaturePercentage = distanceFeaturePercentage;
        this.isEuclideanDistance = isEuclideanDistance;
    }


    public int getAttributeCount() {
        return data.get(0).getAttributeCount();
    }


    public void setUsedFeaturesPercentage(double distanceFeaturePercentage) {
        this.distanceFeaturePercentage = distanceFeaturePercentage;
    }


    public void doOntogeny(List genotype) {
        IntChromosome chrom = (IntChromosome) genotype.get(0);
        ArrayList<Integer> individual = (ArrayList<Integer>) chrom.getBases();

        ArrayList<Integer> newIndividual = new ArrayList<Integer>();

        //remove duplicates in permutation
        for (Integer cFeature : individual) {
            if (!newIndividual.contains(cFeature))
                newIndividual.add(cFeature);
            featureOccurrenceCount[cFeature]++;
        }
        if(!isEuclideanDistance)
            individual = newIndividual;

        sum += newIndividual.size();

        individualCount++;

        if (individualCount > Main.populationSize) {
            System.out.println("length: "+sum/Main.populationSize);
            System.out.println("feature_occurency: "+ Arrays.toString(featureOccurrenceCount));
            featureOccurrenceCount = new int[featureOccurrenceCount.length];
            individualCount = 1;
            sum = 0;
        }


        nCorrect = 0;
        nBases = data.size();
        //this function is called for each individual once

       // System.out.println(individual);
        //System.out.println(nBases);
        for (int i = 0; i < nBases; i++) {
            if (KNNClassifier.leaveOneOutEvaluate(i, individual, data, distanceFeaturePercentage, k)) {
                nCorrect++;
            }
        }



    }


    /**
     * Here the fitness is simply the percentage of correct elements.
     */


    public void calcFitness() {
        fitness = (double) nCorrect / (double) nBases;
    }


    /**
     * Access to the fitness of the Phenotype.
     */

    public double getFitness() {
        return fitness;
    }


    /**
     * A String representation of the Phenotype.
     */

    public String toString() {
        return (nCorrect + " elements out of " + nBases + " correct.");
    }


//
}
