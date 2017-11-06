/*
 * JEvolution Version 0.9.8 at 1/25/13 5:04 PM
 */

/*
 * Copyright (c) 2013.
 */

import java.util.List;

import evSOLve.JEvolution.Phenotype;
import evSOLve.JEvolution.chromosomes.PermChromosome;

import evSOLve.JEvolution.misc.Xml;

import org.jdom2.Element;

/** A Phenotype for the test of permutation encoding. The goal is to find the
* permutation of elements in ascending order. By default permutation
* elements start with 0. The correct chromosome with 10 elements 
* would then be 0|1|2|3|4|5|6|7|8|9
*
* 0.1
* @author Helmut A. Mayer
* @ since December 10, 1999
*
*/
public class SortPhenotype implements Phenotype {
	
	protected double fitness;
	protected int nBases;								// the number of elements
	protected int nCorrect;								// the phenotypic expression
		
/** Constructs the basic phenotype. */
	public SortPhenotype() {
	}
	
	
    /** Constructs the phenotype from XML.
     *
     * @param element			a JDOM element
     *
     */		
	public SortPhenotype(Element element) {
	
		nBases = Xml.getProperty(element, "Items", 0);
		nCorrect = Xml.getProperty(element, "Correct", 0);
	}


/** A proper clone. Here the phenotype is simply an integer, so super.clone() handles
* everything just fine.
*
* @returns Object							The clone.
*
*/

	public Object clone() {
		try {
			SortPhenotype clone = (SortPhenotype)super.clone();
			return clone;
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
			if (index.intValue() == i)
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
	
		
/** Saves the phenotype to XML.
*
* @param element			a JDOM element
*
*/
    public void toXml(Element element) {
    
		Xml.addChildTo(element, "Items", String.valueOf(nBases));	
		Xml.addChildTo(element, "Correct", String.valueOf(nCorrect));	
	}
//
}