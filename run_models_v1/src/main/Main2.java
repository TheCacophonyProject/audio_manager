package main;

import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;

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

public class Main2 {

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

	static ArrayList<String> imageDirectories = new ArrayList<String>();
	static ArrayList<String> deviceDirectorys = new ArrayList<String>();

	public static void main(String[] args) throws Exception {

		String home = System.getProperty("user.home");
		baseDirectory = home + "/Work/Cacophony/Audio Analysis/training_images/" + iterationDirectory;

		deviceDirectorys.add("fpF7B9AFNn6hvfVgdrJB/");
		deviceDirectorys.add("grants_shed/");

		imageDirectories.add("maybe_morepork/");
		imageDirectories.add("morepork/");
		imageDirectories.add("morepork_but_noisy/");
		imageDirectories.add("not_morepork/");
		imageDirectories.add("quiet_morepork/");
		imageDirectories.add("unknown/");

//		imageDirectory = baseDirectory + "data_for_first_iteration/fpF7B9AFNn6hvfVgdrJB/input_to_model/morepork/";
		stagingDirectory = baseDirectory + outputDirectory + "staging/";
		File testStatingExists = new File(stagingDirectory);
		if (!testStatingExists.exists()) {
			testStatingExists.mkdirs();
		}

//		classifiedAsmoreporkDirectory = baseDirectory + "data_for_first_iteration/fpF7B9AFNn6hvfVgdrJB/output_from_model/morepork";
//		classifiedAsUnknownDirectory = baseDirectory + "data_for_first_iteration/fpF7B9AFNn6hvfVgdrJB/output_from_model/unknown";

		// Create output directories
		for (String deviceDirectory : deviceDirectorys) {
			for (String imageDirectory : imageDirectories) {
				// Create the output directories
				File directoryName = new File(
						baseDirectory + outputDirectory + deviceDirectory + imageDirectory);
				if (!directoryName.exists()) {
					directoryName.mkdirs();
				}
			}
		}

		for (String deviceDirectory : deviceDirectorys) {
			for (String imageDirectory : imageDirectories) {
				processImageInputDirectory(deviceDirectory, imageDirectory);
			}
		}
	}

	private static void processImageInputDirectory(String deviceDirectory, String imageDirectory) throws Exception {
		String fullPathToImageInputDirectory = baseDirectory + inputDirectory + deviceDirectory + imageDirectory;
		String fullPathToImageOutputDirectoryMinusClassifcation = baseDirectory + outputDirectory + deviceDirectory;
		File dir = new File(fullPathToImageInputDirectory);
		File[] directoryListing = dir.listFiles();
		if (directoryListing != null) {
			for (File file : directoryListing) {
				if (file.isFile()) {
					String fileBeingProcessedName = file.getName();
					System.out.println("fileBeingProcessedName is " + fileBeingProcessedName);

//		    	  Files.move(Paths.get(file.getAbsolutePath()), Paths.get(stagingDirectory + File.separator + stagingFileName), StandardCopyOption.REPLACE_EXISTING);
					Files.copy(Paths.get(file.getAbsolutePath()), Paths.get(stagingDirectory + stagingFileName),
							StandardCopyOption.REPLACE_EXISTING);
//		    	   if (isThisAClassicMoreporkCall()){
//		    		   Files.move(Paths.get(stagingDirectory + File.separator + stagingFileName), Paths.get(classifiedAsmoreporkDirectory + File.separator + fileBeingProcessedName), StandardCopyOption.REPLACE_EXISTING);
//		    	   }else {
//		    		   Files.move(Paths.get(stagingDirectory + File.separator + stagingFileName), Paths.get(classifiedAsUnknownDirectory + File.separator + fileBeingProcessedName), StandardCopyOption.REPLACE_EXISTING);
//		    	   }
					int result = whatIsThis();

					switch (result) {
					case 0:
//		  			return "morepork";
						Files.move(Paths.get(stagingDirectory + stagingFileName),
								Paths.get(fullPathToImageOutputDirectoryMinusClassifcation + "morepork/"
										+ fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					case 1:
//		  			return "maybe_morepork";
						Files.move(Paths.get(stagingDirectory + stagingFileName),
								Paths.get(fullPathToImageOutputDirectoryMinusClassifcation + "maybe_morepork/"
										+ fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					case 2:
//		  			return "morepork_but_noisy";
						Files.move(Paths.get(stagingDirectory + stagingFileName),
								Paths.get(fullPathToImageOutputDirectoryMinusClassifcation + "morepork_but_noisy/"
										+ fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					case 3:
//		  			return "quiet_morepork";
						Files.move(Paths.get(stagingDirectory + stagingFileName),
								Paths.get(fullPathToImageOutputDirectoryMinusClassifcation + "quiet_morepork/"
										+ fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					case 4:
//		  			return "not_morepork";	
						Files.move(Paths.get(stagingDirectory + stagingFileName),
								Paths.get(fullPathToImageOutputDirectoryMinusClassifcation + "not_morepork/"
										+ fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					case 5:
//		  			return "unknown";
						Files.move(Paths.get(stagingDirectory + stagingFileName), Paths.get(
								fullPathToImageOutputDirectoryMinusClassifcation + "unknown/" + fileBeingProcessedName),
								StandardCopyOption.REPLACE_EXISTING);
						break;
					}

				}

			}
		}
		// assessPic();
	}

	private static int whatIsThis() throws Exception {
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

