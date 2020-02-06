package main;

import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;

public class GetEdgeHistogramFeatures {
	
	static String modelName = "model.model";
	static String imageDirectory = "./images";

	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		DataSource source = new DataSource("input.arff");																						
		Instances data = source.getDataSet();

		final EdgeHistogramFilter filter = new EdgeHistogramFilter();

		filter.setImageDirectory(imageDirectory);
		filter.setInputFormat(data);
		Instances dataWithAttributes = Filter.useFilter(data, filter);
//		System.out.println(dataWithAttributes);
		System.out.println(dataWithAttributes.get(0));

	}

}
