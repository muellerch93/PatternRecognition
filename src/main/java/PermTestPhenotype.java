/*
 * JEvolution Version 0.9.8 at 1/25/13 5:04 PM
 */

import java.util.List;

import evSOLve.JEvolution.Phenotype;
import evSOLve.JEvolution.chromosomes.PermChromosome;

import org.jdom2.Element;

public class PermTestPhenotype implements Phenotype {
	
	
	protected double fitness;
	protected int nBases;								// the number of elements
	protected int nCorrect;								// the phenotypic expression
	
		
	public PermTestPhenotype() {
	}		
		

/** A proper clone. Here the phenotype is simply an integer, so super.clone() handles
* everything just fine.
*
* @return Object							The clone.
*
*/

	public Object clone() {
		try {
			PermTestPhenotype clone = (PermTestPhenotype)super.clone();
			return(clone);
		} catch (CloneNotSupportedException e) {
			throw new InternalError(e.toString());			//should not happen
		}
	}
	
	
/** The genotype-phenotype mapper just counts the number of correct
* permutation elements.
*/
	
	public void doOntogeny(List genotype) {
	
		PermChromosome chrom = (PermChromosome)genotype.get(0);
		List perm = (List)chrom.getBases();
		nBases = chrom.getLength();
		Integer index;

		nCorrect = 0;		
		for (int i = 0; i < nBases; i++) {
			index = (Integer)perm.get(i);
			if (index == i)
				++nCorrect;
		}
	}
	
	
/** Here the fitness is simply the percentage of correct elements. */


	public void calcFitness() {
		fitness = (double)nCorrect / (double)nBases;
	}
			
				
/** Access to the fitness of the Phenotype. */

	public double getFitness() {
		return fitness;
	}
		
		
/** A String representation of the Phenotype. */

	public String toString() {
		return(nCorrect + " elements out of " + nBases + " correct.");
	}
	    
    /** Saves the phenotype to XML. */
    public void toXml(Element element) {
	}
//
}