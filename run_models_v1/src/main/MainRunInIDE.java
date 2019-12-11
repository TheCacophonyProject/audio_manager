package main;


import java.io.File;

import java.util.List;

import org.apache.commons.io.FileUtils;

import weka.core.Instance;
import weka.core.Instances;

import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;
import weka.classifiers.trees.LMT;

public class MainRunInIDE {
	// https://www.youtube.com/watch?v=6o19TPn181g
	// https://www.youtube.com/watch?v=fh4ouoKs8H0&list=PLea0WJq13cnBVfsPVNyRAus2NK-KhCuzJ&index=14
	// https://www.youtube.com/watch?v=wSB5oByt7ko


//	static String modelName = "model.model";
//	static String imageDirectory = "./images";
//	static String imageToProcess = "input.jpg";
	
	static String modelName = "/home/tim/Work/Cacophony/Audio_Analysis/Weka/folder_for_running_model_from_eclipse/weka_model/model.model";
	static String imageDirectory = "/home/tim/Work/Cacophony/Audio_Analysis/Weka/folder_for_running_model_from_eclipse/weka_model/images";
//	static String imageToProcess = "/home/tim/Work/Cacophony/Audio_Analysis/Weka/folder_for_running_model_from_eclipse/weka_model/morepork_more-pork$381004$19.6.jpg";	
	
	public static void main(String[] args) throws Exception {
		// see https://weka.8497.n7.nabble.com/warnings-td42935.html for suppressing warning when running from command line
		
		DataSource source = new DataSource("/home/tim/Work/Cacophony/Audio_Analysis/Weka/folder_for_running_model_from_eclipse/weka_model/input.arff");																						
		Instances data = source.getDataSet();

		final EdgeHistogramFilter filter = new EdgeHistogramFilter();

		filter.setImageDirectory(imageDirectory);
		filter.setInputFormat(data);
		Instances dataWithAttributes = Filter.useFilter(data, filter);

		// Now remove filename attribute
		String[] opts = new String[] { "-R", "1" };
		Remove remove = new Remove();
		remove.setOptions(opts);
		remove.setInputFormat(dataWithAttributes);
		Instances testDataset = Filter.useFilter(dataWithAttributes, remove);

		// Run through model
		
		testDataset.setClassIndex(testDataset.numAttributes() - 1);

		Instance newInst = testDataset.instance(0);
		
		
		// Load the model
		LMT myModel = (LMT) weka.core.SerializationHelper.read(modelName);
		
		double[] classProbabilities = myModel.distributionForInstance(newInst);
		for (double classProbability : classProbabilities){
			System.out.println(classProbability);
		}
		
		int result = (int) myModel.classifyInstance(newInst);
		double probablilty = myModel.distributionForInstance(newInst)[result];
		
		
		
		System.out.println(result + "," + probablilty);
	}

}


