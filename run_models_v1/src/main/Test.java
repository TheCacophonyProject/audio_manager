package main;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import org.json.JSONObject;


import weka.*;
import weka.classifiers.trees.LMT;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.Instance;
import weka.core.Instances;

public class Test {
	// https://www.youtube.com/watch?v=6o19TPn181g
	// https://www.youtube.com/watch?v=fh4ouoKs8H0&list=PLea0WJq13cnBVfsPVNyRAus2NK-KhCuzJ&index=14

	public static void main(String[] args) throws Exception {
		System.out.println("Starting");
		String modelLocation = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_09_17_1/weka_models/morepork_base.model";
		
		String arrFilesToEvaluateFolder = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_09_17_1/arff_files";
		String arrfFileToEvaluate = "206580_21.0_1.5.mfcc.arff";		
	    
	    String fileToEvaluate = arrFilesToEvaluateFolder + "/" + arrfFileToEvaluate;

		LMT morepork_unknown_base = (LMT) weka.core.SerializationHelper.read(modelLocation);

		
		JSONObject result= evaluateArff(morepork_unknown_base, fileToEvaluate);
		System.out.println(result);	
	}
		
	public static JSONObject evaluateArff(LMT morepork_unknown_base, String arrFileToEvaluate) throws Exception {		

	    DataSource unknownSource = new DataSource(arrFileToEvaluate);
		Instances testDataset = unknownSource.getDataSet();
		testDataset.setClassIndex(testDataset.numAttributes()-1);		

		double actualClass = testDataset.instance(0).classValue();
		String actual = testDataset.classAttribute().value((int) actualClass);
		
		Instance newInst = testDataset.instance(0);
		
		double predLMT = morepork_unknown_base.classifyInstance(newInst);
				
		String predString = testDataset.classAttribute().value((int) predLMT);
				
		JSONObject result = new JSONObject();
		result.put("actual", actual);
		result.put("predicted", predString);
		
		
		return result;

	}

}
