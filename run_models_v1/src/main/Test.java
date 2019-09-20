package main;
import java.io.File;
import java.io.FileInputStream;
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

public class Test {
	// https://www.youtube.com/watch?v=6o19TPn181g
	// https://www.youtube.com/watch?v=fh4ouoKs8H0&list=PLea0WJq13cnBVfsPVNyRAus2NK-KhCuzJ&index=14

	public static void main(String[] args) throws Exception {
		System.out.println("Starting2");
		
		// Get list of arff files in the sub dir called arffs when running this code from a jar
		
			File curDir = new File(".");
//	        File arffDir = new File("./arffFiles/");
//	   ArrayList<File> arffFiles =  getAllArffFiles(curDir);
	   
	   Set<String> arffFiles = listFilesUsingJavaIO(".");
	   Iterator<String> itr = arffFiles.iterator();
	   while(itr.hasNext()){
		   System.out.println(itr.next());
		 }
	   
	   
	  
	    
	    
		
		
//		String modelLocation = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_09_17_1/weka_models/morepork_base.model";		
//		String arrFilesToEvaluateFolder = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_09_17_1/arff_files";
//		String arrfFileToEvaluate = "206580_21.0_1.5.mfcc.arff";	
		
		String modelLocation = "morepork_base.model";		
////		String arrFilesToEvaluateFolder = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2019_09_17_1/arff_files";
//		String arrfFileToEvaluate = "206580_21.0_1.5.mfcc.arff";	
		
//		modelLocation = args[0];
//		System.out.println("modelLocation is " + modelLocation);
		
//		arrFilesToEvaluateFolder = args[1];
//		System.out.println("arrFilesToEvaluateFolder is " + arrFilesToEvaluateFolder);
//		
//		arrfFileToEvaluate = args[1];
//		System.out.println("arrfFileToEvaluate is " + arrfFileToEvaluate);		
		
			
	    
//	    String fileToEvaluate = arrFilesToEvaluateFolder + "/" + arrfFileToEvaluate;
//	    String fileToEvaluate = arrfFileToEvaluate;

//		LMT morepork_unknown_base = (LMT) weka.core.SerializationHelper.read(modelLocation);
		 
//		for (File fileToEvaluate : arffFiles) {
//			System.out.println(fileToEvaluate.getName());
////			JSONObject result= evaluateArff(morepork_unknown_base, fileToEvaluate.getName());
////			System.out.println(result);
//		   }
		

		
			
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
	
	public static Set<String> listFilesUsingJavaIO(String dir) {
	    return Stream.of(new File(dir).listFiles())
	      .filter(file -> !file.isDirectory())
	      .map(File::getName)
	      .collect(Collectors.toSet());
	}
	
	private static ArrayList<File> getAllArffFiles(File curDir) {	
		ArrayList<File> arffFilesToReturn = new ArrayList<File>();
		System.out.println("Getting files");
//		System.out.println("arffDir is " + arffDir);
        File[] filesList = curDir.listFiles();
        for(File f : filesList){            
            if(f.isFile()){
            	String parts[] = f.getName().split(".");
            	System.out.println(parts);
//            	String ext = parts[parts.length-1];
//            	if (ext.contentEquals("arff")) {
//            		arffFilesToReturn.add(f);
//            	}
                
            }
        }
        return arffFilesToReturn;
        

    }

}
