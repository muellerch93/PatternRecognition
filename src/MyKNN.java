import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import javax.print.attribute.HashAttributeSet;


public class MyKNN 
{	
	private static HashMap sortByValues(HashMap map) { 
	       List list = new LinkedList(map.entrySet());
	       // Defined Custom Comparator here
	       Collections.sort(list, new Comparator() {
	            public int compare(Object o1, Object o2) {
	               return ((Comparable) ((Map.Entry) (o1)).getValue())
	                  .compareTo(((Map.Entry) (o2)).getValue());
	            }
	       });

	       // Here I am copying the sorted list in HashMap
	       // using LinkedHashMap to preserve the insertion order
	       HashMap sortedHashMap = new LinkedHashMap();
	       for (Iterator it = list.iterator(); it.hasNext();) {
	              Map.Entry entry = (Map.Entry) it.next();
	              sortedHashMap.put(entry.getKey(), entry.getValue());
	       } 
	       return sortedHashMap;
	  }

	public static boolean leaveOneOutEvaluate(ArrayList<DataInstance> traindata, int testIdx, ArrayList<Integer> permutations, int subselectCount, int K)
	{
		
        HashMap<DataInstance,Double> unsorted = new HashMap<DataInstance,Double>();
        
		DataInstance testSample = traindata.get(testIdx);
		
		for(int i=0; i<traindata.size(); i++)
		{
			if(i != testIdx)
			{
				unsorted.put(traindata.get(i), traindata.get(i).distanceTo(testSample, permutations, subselectCount));
			}
		}
		
		
		HashMap<DataInstance, Double> sorted = sortByValues(unsorted);
		
		
		
		HashMap<Integer, Integer> votes = new HashMap<Integer,Integer>();
		
		
		for(DataInstance di:sorted.keySet())
		{
			if(votes.get(di.getTarget()) == null)
			{
				votes.put(di.getTarget(), 1);
			}
			else
			{
				votes.put(di.getTarget(), votes.get(di.getTarget())+1);
			}
			
			break;
		}
		
		int maxClass = -1;
		int maxCnt = 0;
		
		int k=0; 
		for(Integer c:votes.keySet())
		{
			if(votes.get(c) > maxCnt)
			{
				maxClass = c;
				maxCnt = votes.get(c);
			}
			k++;
			
			if(k >= K)
			{
				break;
			}
		}
		
		
		return maxClass == testSample.getTarget();
	
				
		
	}
	
	
	
	public MyKNN()
	{
		
	}
	
	

}
