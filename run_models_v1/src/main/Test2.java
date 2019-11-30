package main;


import weka.classifiers.trees.LMT;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;

//import weka.classifiers.trees.LMT;
//import weka.core.Instance;
//import weka.core.Instances;
//import weka.core.converters.ConverterUtils.DataSource;

//import weka.filters.unsupervised.attribute.Remove;
//import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;

public class Test2 {

	public static void main(String[] args) {
		try {
		
		String home = System.getProperty("user.home");	
		
		
		String pathToModel = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_11_28_1/Model_created_from_previous_run/model.model";
		
		
			
			DataSource source = new DataSource("/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_11_28_1/what_is_this3.arff");
//			DataSource source = new DataSource("what_is_this.arff");
			
			Instances data = source.getDataSet();
			final EdgeHistogramFilter filter = new EdgeHistogramFilter();
			filter.setImageDirectory("/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_11_28_1/staging/");
			
			filter.setInputFormat(data);
			Instances dataWithAttributes = Filter.useFilter(data, filter);

			// Now remove filename attribute
			String[] opts = new String[] { "-R", "1" };
			Remove remove = new Remove();
			remove.setOptions(opts);
			remove.setInputFormat(dataWithAttributes);
			Instances testDataset = Filter.useFilter(dataWithAttributes, remove);
			
			testDataset.setClassIndex(testDataset.numAttributes() - 1);

			Instance newInst = testDataset.instance(0);
			
			LMT myModel = (LMT) weka.core.SerializationHelper.read(pathToModel);
			
			int result = (int) myModel.classifyInstance(newInst);
			System.out.println("result is: " + result);
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
