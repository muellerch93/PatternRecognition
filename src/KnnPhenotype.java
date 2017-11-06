import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;



import evSOLve.JEvolution.chromosomes.PermChromosome;


public class KnnPhenotype extends SortPhenotype {

    protected double fitness;
    protected int nBases;                                // the number of elements
    protected int nCorrect;                                // the phenotypic expression
    protected int _k = 1;


    static ArrayList<DataInstance> _data;

    private int _nrFeaturesToUse;

    /**
     * Constructs the basic phenotype.
     *
     * @throws IOException
     */
    public KnnPhenotype(String pathToFile, double featuresToUsePercentage) throws IOException {

        String[] fnameParts = pathToFile.split("/");

        if (fnameParts[fnameParts.length - 1].equals("wine.data") || fnameParts[fnameParts.length - 1].equals("ionosphere_mapped.data") || fnameParts[fnameParts.length - 1].equals("semeion_mapped.data") || fnameParts[fnameParts.length - 1].equals("redwinequality_mapped.data")) {
            System.out.println("Load data from " + pathToFile);

            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(pathToFile)));

            String line;

            _data = new ArrayList<DataInstance>();

            while ((line = br.readLine()) != null) {
                _data.add(new DataInstance(line));
            }

            br.close();

        } else {
            throw new IOException("Unknown data file, no parsing rule for this");
        }


        _nrFeaturesToUse = (int) Math.floor((double) this.getAttributeCount() * featuresToUsePercentage);

    }

    public KnnPhenotype(String pathToFile, int nrFeaturesToUse) throws IOException {

        String[] fnameParts = pathToFile.split("/");

        if (fnameParts[fnameParts.length - 1].equals("wine.data") || fnameParts[fnameParts.length - 1].equals("ionosphere_mapped.data") || fnameParts[fnameParts.length - 1].equals("semeion_mapped.data") || fnameParts[fnameParts.length - 1].equals("redwinequality_mapped.data")) {
            System.out.println("Load data from " + pathToFile);

            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(pathToFile)));

            String line;

            _data = new ArrayList<DataInstance>();

            while ((line = br.readLine()) != null) {
                _data.add(new DataInstance(line));
            }

            br.close();
            System.out.println("Finished loading data from "+ pathToFile);

        } else {
            throw new IOException("Unknown data file, no parsing rule for this");
        }


        _nrFeaturesToUse = nrFeaturesToUse;

    }


    public int getAttributeCount() {
        return _data.get(0).getAttributeCount();
    }

    public int getUsedFeatures() {
        return _nrFeaturesToUse;
    }



    public void doOntogeny(List genotype) {
        PermChromosome chrom = (PermChromosome) genotype.get(0);
        ArrayList<Integer> perm = (ArrayList<Integer>) chrom.getBases();
        nCorrect = 0;
        nBases = _data.size();


        for (int i = 0; i < nBases; i++) {
            if (MyKNN.leaveOneOutEvaluate(_data, i, perm, this.getUsedFeatures(), _k)) {
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
