package main;

import java.util.ArrayList;

import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;
import weka.core.Instances;

public class Test3 {

	public static void main(String[] args) {
		
		// file:///home/tim/Downloads/WekaManual-3-9-3.pdf	
		
		Attribute MPEG7_Edge_Histogram0 = new Attribute("MPEG7_Edge_Histogram0");
		Attribute MPEG7_Edge_Histogram1 = new Attribute("MPEG7_Edge_Histogram1");
		
		ArrayList<String> labels = new ArrayList<String>();
		labels.add("dog");
		labels.add("white_noise");
		
		Attribute cls = new Attribute("class", labels);
		
		ArrayList<Attribute> attributes = new ArrayList<Attribute>();
		attributes.add(MPEG7_Edge_Histogram0);
		attributes.add(MPEG7_Edge_Histogram1);
		
		attributes.add(cls);
		
		Instances dataset = new Instances("Test-dataset", attributes, 0);
		
		double[] values = new double[dataset.numAttributes()];
		System.out.println("dataset.numAttributes() " + dataset.numAttributes());
		values[0] = 111;
		values[1] = 222;
		
		Instance instance = new DenseInstance(1.0, values);
		dataset.add(instance);
		
		// 4. output data
	    System.out.println(dataset);

	}

}
