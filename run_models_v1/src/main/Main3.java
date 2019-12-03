package main;


import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.io.FileUtils;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;
//import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;
//import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;
import weka.classifiers.trees.LMT;

public class Main3 {

	static String modelName = "model.model";
	static String stagingDirectory = null;
	

	static String stagingFileName = "input.jpg";

	

	public static void main(String[] args) throws Exception {
		// see https://weka.8497.n7.nabble.com/warnings-td42935.html for suppressing warning when running from command line
		// ie use https://weka.8497.n7.nabble.com/warnings-td42935.html
		
	
//		 stagingDirectory = "staging";
//		 stagingDirectory = "/staging";
		 stagingDirectory = "./staging";
		
//		 stagingDirectory = "staging/";
//		 stagingDirectory = "/staging/";
//		 stagingDirectory = "./staging/";

		 
//		File testStatingExists = new File(stagingDirectory);
//		whatIsThis();
		 
		 String dirName = stagingDirectory;
	        
	        List<File> files = (List<File>) FileUtils.listFiles(new File(dirName), null, true);
	        
	        files.forEach(System.out::println);
	        
	        whatIsThis();
	}


	

	private static int whatIsThis() throws Exception {
		// DataSource source = new DataSource("./data/what_is_this.arff");
//		DataSource source = new DataSource(baseDirectory + outputDirectory + "what_is_this.arff"); // this file will
																									// need to be
																									// created and
																									// modified to suit
		
		
		DataSource source = new DataSource("input.arff");																							// model classes
																									// expected
		Instances data = source.getDataSet();

		final EdgeHistogramFilter filter = new EdgeHistogramFilter();
//		filter.setImageDirectory("./data/images");
//		filter.setImageDirectory(imageDirectory);
		filter.setImageDirectory(stagingDirectory);
		filter.setInputFormat(data);
		Instances dataWithAttributes = Filter.useFilter(data, filter);

		// Now remove filename attribute
		String[] opts = new String[] { "-R", "1" };
		Remove remove = new Remove();
		remove.setOptions(opts);
		remove.setInputFormat(dataWithAttributes);
		Instances testDataset = Filter.useFilter(dataWithAttributes, remove);

		// Run through model
		// https://www.youtube.com/watch?v=wSB5oByt7ko
		testDataset.setClassIndex(testDataset.numAttributes() - 1);

		Instance newInst = testDataset.instance(0);

//		double actualValue = newInst.classValue();

		// Load the model
//		LMT myModel = (LMT) weka.core.SerializationHelper.read("./data/models/EdgeHistogram_LMT.model");
//		LMT myModel = (LMT) weka.core.SerializationHelper.read(baseDirectory + outputDirectory + modelName);
		LMT myModel = (LMT) weka.core.SerializationHelper.read(modelName);

		int result = (int) myModel.classifyInstance(newInst);
		System.out.println(result);
		return result;
//		System.out.println("result is : " + result);

//		if (result == 1.0) {
//			return false;
//		}else {
//			return true;
//		}

//		System.out.println("actualValue is " + actualValue);
//		System.out.println("result is " + result);

//		ArffSaver saver = new ArffSaver();
//		saver.setInstances(dataWithAttributesNoFilename);
//		saver.setFile(new File("./data/base1.arff"));
//		saver.writeBatch();
	}

}


