import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import evSOLve.JEvolution.chromosomes.IntChromosome;
import evSOLve.JEvolution.chromosomes.PermChromosome;


public class MyPhenotype extends SortPhenotype {


    private int _k = 2;


    private static ArrayList<Pattern> _data;
    private int _nrFeaturesToUse;

    /**
     * Constructs the basic phenotype.
     *
     * @throws IOException
     */
    public MyPhenotype(ArrayList<Pattern> patterns, double featuresToUsePercentage) throws IOException {
        _data = patterns;
        _nrFeaturesToUse = (int) Math.floor((double) this.getAttributeCount() * featuresToUsePercentage);

    }
    public MyPhenotype(ArrayList<Pattern> patterns) throws IOException {
        _data = patterns;

    }
    public MyPhenotype(ArrayList<Pattern> patterns, int nrFeaturesToUse) throws IOException {
        _data = patterns;
        _nrFeaturesToUse = nrFeaturesToUse;

    }


    public int getAttributeCount() {
        return _data.get(0).getAttributeCount();
    }

    public int getUsedFeatures() {
        return _nrFeaturesToUse;
    }
    public void setUsedFeatures(int nrFeaturesToUse){_nrFeaturesToUse=nrFeaturesToUse;}


    public void doOntogeny(List genotype) {
        IntChromosome chrom = (IntChromosome) genotype.get(0);
        ArrayList<Integer> perm = (ArrayList<Integer>) chrom.getBases();
        nCorrect = 0;
        nBases = _data.size();

        for (int i = 0; i < nBases; i++) {
            if (KNNClassifier.leaveOneOutEvaluate(_data, i, perm, this.getUsedFeatures(), _k)) {
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
