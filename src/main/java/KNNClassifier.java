import java.util.*;

public class KNNClassifier
{


	public KNNClassifier()
	{

	}

	private static <K, V extends Comparable<? super V>> HashMap<K, V> sortByValue(HashMap<K, V> map) {

		List<HashMap.Entry<K, V>> list = new LinkedList<HashMap.Entry<K, V>>(map.entrySet());
		Collections.sort( list, new Comparator<Map.Entry<K, V>>() {
			public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
				return (o1.getValue()).compareTo( o2.getValue() );
			}
		});

		HashMap<K, V> result = new LinkedHashMap<K, V>();
		for (Map.Entry<K, V> entry : list) {
			result.put(entry.getKey(), entry.getValue());
		}
		return result;
	}

	public static boolean leaveOneOutEvaluate( int testPatternId, ArrayList<Integer> individual,ArrayList<Pattern> patterns, double distanceFeaturePercentage,
											   int K, boolean allowDuplicates) {

        HashMap<Pattern,Double> unsorted = new HashMap<Pattern,Double>();
		Pattern testPattern = patterns.get(testPatternId);
		ArrayList<Integer> newIndividual = new ArrayList<Integer>();

		if(!allowDuplicates) {
			//remove duplicates in permutation
			for (Integer cFeature : individual)
				if (!newIndividual.contains(cFeature))
					newIndividual.add(cFeature);
		}else
			newIndividual = individual;

		//we got rid of duplicates, now we can determine the number of features we want to use for distance calculation
		int nrFeaturesToUse = (int) Math.floor((double) newIndividual.size() * distanceFeaturePercentage);

		//add patterns and their distance to the testPattern into a hashmap,
		for(int i=0; i<patterns.size(); i++) {
			if (i != testPatternId) {
				//unsorted.put(patterns.get(i), patterns.get(i).distanceTo(testPattern, newIndividual, subselectCount));
				unsorted.put(patterns.get(i), patterns.get(i).distanceTo(testPattern, newIndividual, nrFeaturesToUse));
			}
		}


		HashMap<Pattern, Double> sorted = sortByValue(unsorted);
		HashMap<Integer, Integer> votes = new HashMap<Integer,Integer>();


		int j=0;
		for(Pattern pattern:sorted.keySet()) {
			if(votes.get(pattern.getTarget()) == null)
				votes.put(pattern.getTarget(), 1);
			else
				votes.put(pattern.getTarget(), votes.get(pattern.getTarget())+1);
			j++;
			if(j==K)
				break;
		}


		int maxClass = -1;
		int maxCnt = 0;
		
		j=0;
		for(Integer c:votes.keySet()) {
			if(votes.get(c) > maxCnt) {
				maxClass = c;
				maxCnt = votes.get(c);
			}
			j++;
			if(j == K)
				break;

		}
		
		
		return maxClass == testPattern.getTarget();
	
				
		
	}
	
	
	

	
	

}
