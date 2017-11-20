import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import evSOLve.JEvolution.chromosomes.IntChromosome;
import evSOLve.JEvolution.chromosomes.PermChromosome;


public class MyPhenotype extends SortPhenotype {


    private int k = 1;


    private ArrayList<Pattern> data;
    private double distanceFeaturePercentage;
    private boolean distanceAllowDuplicates;

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

    public MyPhenotype(ArrayList<Pattern> patterns, double distanceFeaturePercentage, boolean distanceAllowDuplicates) throws IOException {
        this.data = patterns;
        this.distanceFeaturePercentage = distanceFeaturePercentage;
        this.distanceAllowDuplicates = distanceAllowDuplicates;
    }


    public int getAttributeCount() {
        return data.get(0).getAttributeCount();
    }


    public void setUsedFeaturesPercentage(double distanceFeaturePercentage) {
        this.distanceFeaturePercentage = distanceFeaturePercentage;
    }


    public void doOntogeny(List genotype) {
        IntChromosome chrom = (IntChromosome) genotype.get(0);
        ArrayList<Integer> perm = (ArrayList<Integer>) chrom.getBases();

        nCorrect = 0;
        nBases = data.size();

        for (int i = 0; i < nBases; i++) {
            if (KNNClassifier.leaveOneOutEvaluate(i, perm, data, distanceFeaturePercentage, k, distanceAllowDuplicates)) {
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
