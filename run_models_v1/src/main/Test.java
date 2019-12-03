package main;

import org.json.JSONObject;

import weka.classifiers.trees.LMT;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;

public class Test {
	static String modelName = "model_iteration_2.model";
	static String baseDirectory = null;
	static String iterationDirectory = "data_for_second_iteration/";
	static String inputDirectory = "input_to_model/";
	static String outputDirectory = "output_from_model/";

	static String imageDirectory = null;

	static String stagingDirectory = null;
	static String classifiedAsmoreporkDirectory = null;
	static String classifiedAsUnknownDirectory = null;

	static String stagingFileName = "what_is_this.jpg";
	
	public static void main(String[] args) throws Exception {
		whatIsThis();
	}
	
	private static int whatIsThis() throws Exception {
		
		String home = System.getProperty("user.home");	
		
		baseDirectory = home + "/Work/Cacophony/Audio Analysis/training_images/" + iterationDirectory;
		stagingDirectory = baseDirectory + outputDirectory + "staging/";
		
		// DataSource source = new DataSource("./data/what_is_this.arff");
		DataSource source = new DataSource(baseDirectory + outputDirectory + "what_is_this.arff"); // this file will
																									// need to be
																									// created and
																									// modified to suit
																									// model classes
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
		LMT myModel = (LMT) weka.core.SerializationHelper.read(baseDirectory + outputDirectory + modelName);

		int result = (int) myModel.classifyInstance(newInst);
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
