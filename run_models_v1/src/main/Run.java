package main;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.json.JSONObject;

//import org.apache.commons.io.Fr


import weka.*;
import weka.classifiers.trees.LMT;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.Instance;
import weka.core.Instances;

public class Run {
	// https://www.youtube.com/watch?v=6o19TPn181g
	// https://www.youtube.com/watch?v=fh4ouoKs8H0&list=PLea0WJq13cnBVfsPVNyRAus2NK-KhCuzJ&index=14

	public static void main(String[] args) throws Exception {
			
		String modelLocation = "model.model";	
		String arffFileToEvaluate = "input.arff";
		LMT lmtModel = (LMT) weka.core.SerializationHelper.read(modelLocation);
		
		DataSource unknownSource = new DataSource(arffFileToEvaluate);
		Instances testDataset = unknownSource.getDataSet();
		testDataset.setClassIndex(testDataset.numAttributes()-1);		

		double actualClass = testDataset.instance(0).classValue();
		String actual = testDataset.classAttribute().value((int) actualClass);
		
		Instance newInst = testDataset.instance(0);
		
		double predLMT = lmtModel.classifyInstance(newInst);
				
		String predString = testDataset.classAttribute().value((int) predLMT);
				
		JSONObject result = new JSONObject();
		result.put("actual", actual);
		result.put("predicted", predString);	
		
		System.out.println(result);
				
//		FileWriter file = new FileWriter("output.json");
//		file.write(result.toString());
//		file.close();
//		System.out.println("Saved in output.json");
	
	}

}
