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

public class Main4 {

	static String modelName = "model.model";
	static String imageDirectory = "./images";
	static String imageToProcess = "input.jpg";

	public static void main(String[] args) throws Exception {
		// see https://weka.8497.n7.nabble.com/warnings-td42935.html for suppressing warning when running from command line
		// ie use https://weka.8497.n7.nabble.com/warnings-td42935.html

//		imageDirectory = "./images";

		DataSource source = new DataSource("input.arff");																						
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
		// https://www.youtube.com/watch?v=wSB5oByt7ko
		testDataset.setClassIndex(testDataset.numAttributes() - 1);

		Instance newInst = testDataset.instance(0);
		// Load the model
		LMT myModel = (LMT) weka.core.SerializationHelper.read(modelName);

		int result = (int) myModel.classifyInstance(newInst);
		System.out.println(result);
	}

}


