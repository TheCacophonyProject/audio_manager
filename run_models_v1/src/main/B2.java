package main;


import java.sql.Connection;  
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.instance.imagefilter.EdgeHistogramFilter;
import weka.classifiers.functions.Logistic;
//import weka.classifiers.functions.MultilayerPerceptron;
import weka.classifiers.functions.SMO;
import weka.classifiers.functions.supportVector.RBFKernel;
import weka.classifiers.trees.LMT;
import weka.classifiers.meta.CostSensitiveClassifier;

public class B2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String modelRunName = "2020_02_07_1";
		String modelName = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/" + modelRunName + "/weka_model/model.model";
		
		try {
		Connection conn = null;
//		String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
		String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Temp/audio_analysis_db2.db";
        // create a connection to the database  
        
			conn = DriverManager.getConnection(url);
		 
        System.out.println("Connection to SQLite has been established.");  
        Statement stmt  = conn.createStatement();
        // String sql = "UPDATE onsets SET version = 999 WHERE ID = 3939";
//        String sql = "SELECT ID, recording_id, start_time_seconds, duration_seconds from onsets WHERE MPEG7_Edge_Histogram0 IS NULL";
        String sql = "SELECT " +
                "MPEG7_Edge_Histogram0, " +
                "MPEG7_Edge_Histogram1, " +
                "MPEG7_Edge_Histogram2, " +
                "MPEG7_Edge_Histogram3, " +
                "MPEG7_Edge_Histogram4, " +
                "MPEG7_Edge_Histogram5, " +
                "MPEG7_Edge_Histogram6, " +
                "MPEG7_Edge_Histogram7, " +
                "MPEG7_Edge_Histogram8, " +
                "MPEG7_Edge_Histogram9, " +
                
                "MPEG7_Edge_Histogram10,  " +
                "MPEG7_Edge_Histogram11, " +
                "MPEG7_Edge_Histogram12, " +
                "MPEG7_Edge_Histogram13, " +
                "MPEG7_Edge_Histogram14, " +
                "MPEG7_Edge_Histogram15, " +
                "MPEG7_Edge_Histogram16, " +
                "MPEG7_Edge_Histogram17, " +
                "MPEG7_Edge_Histogram18, " +
                "MPEG7_Edge_Histogram19, " +
                
                "MPEG7_Edge_Histogram20, " +
                "MPEG7_Edge_Histogram21, " +
                "MPEG7_Edge_Histogram22, " +
                "MPEG7_Edge_Histogram23, " +
                "MPEG7_Edge_Histogram24, " +
                "MPEG7_Edge_Histogram25, " +
                "MPEG7_Edge_Histogram26, " +
                "MPEG7_Edge_Histogram27, " +
                "MPEG7_Edge_Histogram28, " +
                "MPEG7_Edge_Histogram29, " +
                
                "MPEG7_Edge_Histogram30, " +
                "MPEG7_Edge_Histogram31, " +
                "MPEG7_Edge_Histogram32, " +
                "MPEG7_Edge_Histogram33, " +
                "MPEG7_Edge_Histogram34, " +
                "MPEG7_Edge_Histogram35, " +
                "MPEG7_Edge_Histogram36, " +
                "MPEG7_Edge_Histogram37, " +
                "MPEG7_Edge_Histogram38, " +
                "MPEG7_Edge_Histogram39, " +
                
                "MPEG7_Edge_Histogram40,  " +
                "MPEG7_Edge_Histogram41, " +
                "MPEG7_Edge_Histogram42, " +
                "MPEG7_Edge_Histogram43, " +
                "MPEG7_Edge_Histogram44, " +
                "MPEG7_Edge_Histogram45, " +
                "MPEG7_Edge_Histogram46, " +
                "MPEG7_Edge_Histogram47, " +
                "MPEG7_Edge_Histogram48, " +
                "MPEG7_Edge_Histogram49, " +
                
                "MPEG7_Edge_Histogram50,  " +
                "MPEG7_Edge_Histogram51, " +
                "MPEG7_Edge_Histogram52, " +
                "MPEG7_Edge_Histogram53, " +
                "MPEG7_Edge_Histogram54, " +
                "MPEG7_Edge_Histogram55, " +
                "MPEG7_Edge_Histogram56, " +
                "MPEG7_Edge_Histogram57, " +
                "MPEG7_Edge_Histogram58, " +
                "MPEG7_Edge_Histogram59, " +
                
                "MPEG7_Edge_Histogram60, " +
                "MPEG7_Edge_Histogram61, " +
                "MPEG7_Edge_Histogram62, " +
                "MPEG7_Edge_Histogram63, " +
                "MPEG7_Edge_Histogram64, " +
                "MPEG7_Edge_Histogram65, " +
                "MPEG7_Edge_Histogram66, " +
                "MPEG7_Edge_Histogram67, " +
                "MPEG7_Edge_Histogram68, " +
                "MPEG7_Edge_Histogram69, " +
                
                "MPEG7_Edge_Histogram70, " +
                "MPEG7_Edge_Histogram71, " +
                "MPEG7_Edge_Histogram72, " +
                "MPEG7_Edge_Histogram73, " +
                "MPEG7_Edge_Histogram74, " +
                "MPEG7_Edge_Histogram75, " +
                "MPEG7_Edge_Histogram76, " +
                "MPEG7_Edge_Histogram77, " +
                "MPEG7_Edge_Histogram78, " +
                "MPEG7_Edge_Histogram79,  " +       
                        
 				"recording_id,  " +
 				"start_time_seconds,  " +
 				"duration_seconds,  " + 				
                "device_super_name,  " +
                "device_name,  " +
                "recordingDateTime,  " +
                "actual_confirmed   " +  
            
                "FROM onsets " +
                
                "ORDER BY recording_id DESC";
        
//        ResultSet rs    = stmt.executeQuery(sql);  
        
//        DataSource source = new DataSource("/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2020_02_07_1/weka_model/input.arff");																						
//		Instances dataset = source.getDataSet();
//		
//		System.out.println(dataset);
        
        // - nominal
        ArrayList<Attribute> attributes = new ArrayList<Attribute>();  
               
        for (int i = 0; i < 80; i++)	{     
        	attributes.add(new Attribute("MPEG7_Edge_Histogram" + i));
        }
		
		ArrayList<String> deviceSuperNameLabels = new ArrayList<String>();
		deviceSuperNameLabels.add("Hammond_Park");
		deviceSuperNameLabels.add("grants_shed");
		deviceSuperNameLabels.add("Living_Springs");
		deviceSuperNameLabels.add("Kerikeri_Peninsula_Pest_Control");
		deviceSuperNameLabels.add("Motuihe");
		deviceSuperNameLabels.add("Predator_Free_Miramar");
		deviceSuperNameLabels.add("Te_Motu_Kairangi-Miramar_Ecological_Restoration");
		deviceSuperNameLabels.add("Elorosa");
		deviceSuperNameLabels.add("Lochmara");
		deviceSuperNameLabels.add("Fale_monitor");
		deviceSuperNameLabels.add("karaka_bay");
		deviceSuperNameLabels.add("Somerfield");
		deviceSuperNameLabels.add("boyle_field_project");
		deviceSuperNameLabels.add("chow");
		deviceSuperNameLabels.add("livingsprings");
		deviceSuperNameLabels.add("Te_Motu_Kairangi-Predator_Free_Miramar");
		
		attributes.add(new Attribute("deviceSuperName", deviceSuperNameLabels));
				
		ArrayList<String> classLabels = new ArrayList<String>();
		classLabels.add("morepork_more-pork");
		classLabels.add("unknown");
		classLabels.add("siren");
		classLabels.add("dog");
		classLabels.add("duck");
		classLabels.add("dove");
		classLabels.add("human");
		classLabels.add("bird");
		classLabels.add("car");
		classLabels.add("rumble");
		classLabels.add("white_noise");
		classLabels.add("cow");
		classLabels.add("buzzy_insect");
		classLabels.add("plane");
		classLabels.add("hammering");
		classLabels.add("frog");
		classLabels.add("morepork_more-pork_part");
		classLabels.add("chainsaw");
		classLabels.add("crackle");
		classLabels.add("car_horn");
		classLabels.add("water");
		classLabels.add("fire_work");
		classLabels.add("maybe_morepork_more-pork");
		classLabels.add("music");
		
		attributes.add(new Attribute("class", classLabels));
		
		ResultSet rs    = stmt.executeQuery(sql);  
		
      
		
		// 2. create Instances object
		Instances data = new Instances(modelRunName, attributes, 0);
		data.setClassIndex(data.numAttributes() - 1);
		
		CostSensitiveClassifier myModel = (CostSensitiveClassifier) weka.core.SerializationHelper.read(modelName);

	    
	    
	 // loop through the result set  
	      while (rs.next()) {  
	          System.out.println(rs.getInt(1) +  "\t" +   
	                             rs.getInt(2) + "\t" +  
	                             rs.getString(80));  
	          
	          
	          // 3. fill with data
	  	    // first instance
	  		 double[] vals = new double[data.numAttributes()];
	  	    // - numeric
	  		 
//	  		 for (int i = 0; i < 80; i++) {
//	  			 vals[i] = 1; 
//	  		 }
	  		 
	  		for (int i = 0; i < 80; i++) {
	  			 vals[i] = rs.getInt(i+1); 
	  		 }
	  			 
	  		 
	  	   
	  	    // - nominal
	  	    vals[80] = deviceSuperNameLabels.indexOf("grants_shed");
	  	    vals[81] = classLabels.indexOf("music");
	  	    
	  	  Instance instanceToTest = new DenseInstance(1.0, vals);
		    instanceToTest.setDataset(data);
//		    data.add(new DenseInstance(1.0, vals));
		    
		    System.out.println(data);
		    System.out.println(instanceToTest);
		    
		    
//    		int result = (int) myModel.classifyInstance(newInst);
    		int result = (int) myModel.classifyInstance(instanceToTest);
//    		double probablilty = myModel.distributionForInstance(newInst)[result];
    		
    		double probablilty = myModel.distributionForInstance(instanceToTest)[result];
    		
    		System.out.println(result + "," + probablilty);
	          
	      }
	    
		
		
		
//		
//            System.out.println(rs.getInt("MPEG7_Edge_Histogram0") + "\t" + 
//                               rs.getInt("MPEG7_Edge_Histogram1") + "\t" + 
//                               rs.getString("device_super_name") + "\t" + 
//                               rs.getString("actual_confirmed"));
//            
//            Instance newInstance  = new DenseInstance(0);
//            newInstance.setDataset(dataset);
//            
//            newInstance.setValue(MPEG7_Edge_Histogram0, 4);
//          
//                        
//    		newInstance.setValue(0, rs.getInt("MPEG7_Edge_Histogram0"));
//    		newInstance.setValue(MPEG7_Edge_Histogram1, rs.getInt("MPEG7_Edge_Histogram1"));
//    		newInstance.setValue(MPEG7_Edge_Histogram2, rs.getInt("MPEG7_Edge_Histogram2"));
//    		newInstance.setValue(MPEG7_Edge_Histogram3, rs.getInt("MPEG7_Edge_Histogram3"));
//    		newInstance.setValue(MPEG7_Edge_Histogram4, rs.getInt("MPEG7_Edge_Histogram4"));
//    		newInstance.setValue(MPEG7_Edge_Histogram5, rs.getInt("MPEG7_Edge_Histogram5"));
//    		newInstance.setValue(MPEG7_Edge_Histogram6, rs.getInt("MPEG7_Edge_Histogram6"));
//    		newInstance.setValue(MPEG7_Edge_Histogram7, rs.getInt("MPEG7_Edge_Histogram7"));
//    		newInstance.setValue(MPEG7_Edge_Histogram8, rs.getInt("MPEG7_Edge_Histogram8"));
//    		newInstance.setValue(MPEG7_Edge_Histogram9, rs.getInt("MPEG7_Edge_Histogram9"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram10, rs.getInt("MPEG7_Edge_Histogram10"));
//    		newInstance.setValue(MPEG7_Edge_Histogram11, rs.getInt("MPEG7_Edge_Histogram11"));
//    		newInstance.setValue(MPEG7_Edge_Histogram12, rs.getInt("MPEG7_Edge_Histogram12"));
//    		newInstance.setValue(MPEG7_Edge_Histogram13, rs.getInt("MPEG7_Edge_Histogram13"));
//    		newInstance.setValue(MPEG7_Edge_Histogram14, rs.getInt("MPEG7_Edge_Histogram14"));
//    		newInstance.setValue(MPEG7_Edge_Histogram15, rs.getInt("MPEG7_Edge_Histogram15"));
//    		newInstance.setValue(MPEG7_Edge_Histogram16, rs.getInt("MPEG7_Edge_Histogram16"));
//    		newInstance.setValue(MPEG7_Edge_Histogram17, rs.getInt("MPEG7_Edge_Histogram17"));
//    		newInstance.setValue(MPEG7_Edge_Histogram18, rs.getInt("MPEG7_Edge_Histogram18"));
//    		newInstance.setValue(MPEG7_Edge_Histogram19, rs.getInt("MPEG7_Edge_Histogram19"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram20, rs.getInt("MPEG7_Edge_Histogram20"));
//    		newInstance.setValue(MPEG7_Edge_Histogram21, rs.getInt("MPEG7_Edge_Histogram21"));
//    		newInstance.setValue(MPEG7_Edge_Histogram22, rs.getInt("MPEG7_Edge_Histogram22"));
//    		newInstance.setValue(MPEG7_Edge_Histogram23, rs.getInt("MPEG7_Edge_Histogram23"));
//    		newInstance.setValue(MPEG7_Edge_Histogram24, rs.getInt("MPEG7_Edge_Histogram24"));
//    		newInstance.setValue(MPEG7_Edge_Histogram25, rs.getInt("MPEG7_Edge_Histogram25"));
//    		newInstance.setValue(MPEG7_Edge_Histogram26, rs.getInt("MPEG7_Edge_Histogram26"));
//    		newInstance.setValue(MPEG7_Edge_Histogram27, rs.getInt("MPEG7_Edge_Histogram27"));
//    		newInstance.setValue(MPEG7_Edge_Histogram28, rs.getInt("MPEG7_Edge_Histogram28"));
//    		newInstance.setValue(MPEG7_Edge_Histogram29, rs.getInt("MPEG7_Edge_Histogram29"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram30, rs.getInt("MPEG7_Edge_Histogram30"));
//    		newInstance.setValue(MPEG7_Edge_Histogram31, rs.getInt("MPEG7_Edge_Histogram31"));
//    		newInstance.setValue(MPEG7_Edge_Histogram32, rs.getInt("MPEG7_Edge_Histogram32"));
//    		newInstance.setValue(MPEG7_Edge_Histogram33, rs.getInt("MPEG7_Edge_Histogram33"));
//    		newInstance.setValue(MPEG7_Edge_Histogram34, rs.getInt("MPEG7_Edge_Histogram34"));
//    		newInstance.setValue(MPEG7_Edge_Histogram35, rs.getInt("MPEG7_Edge_Histogram35"));
//    		newInstance.setValue(MPEG7_Edge_Histogram36, rs.getInt("MPEG7_Edge_Histogram36"));
//    		newInstance.setValue(MPEG7_Edge_Histogram37, rs.getInt("MPEG7_Edge_Histogram37"));
//    		newInstance.setValue(MPEG7_Edge_Histogram38, rs.getInt("MPEG7_Edge_Histogram38"));
//    		newInstance.setValue(MPEG7_Edge_Histogram39, rs.getInt("MPEG7_Edge_Histogram39"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram40, rs.getInt("MPEG7_Edge_Histogram40"));
//    		newInstance.setValue(MPEG7_Edge_Histogram41, rs.getInt("MPEG7_Edge_Histogram41"));
//    		newInstance.setValue(MPEG7_Edge_Histogram42, rs.getInt("MPEG7_Edge_Histogram42"));
//    		newInstance.setValue(MPEG7_Edge_Histogram43, rs.getInt("MPEG7_Edge_Histogram43"));
//    		newInstance.setValue(MPEG7_Edge_Histogram44, rs.getInt("MPEG7_Edge_Histogram44"));
//    		newInstance.setValue(MPEG7_Edge_Histogram45, rs.getInt("MPEG7_Edge_Histogram45"));
//    		newInstance.setValue(MPEG7_Edge_Histogram46, rs.getInt("MPEG7_Edge_Histogram46"));
//    		newInstance.setValue(MPEG7_Edge_Histogram47, rs.getInt("MPEG7_Edge_Histogram47"));
//    		newInstance.setValue(MPEG7_Edge_Histogram48, rs.getInt("MPEG7_Edge_Histogram48"));
//    		newInstance.setValue(MPEG7_Edge_Histogram49, rs.getInt("MPEG7_Edge_Histogram49"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram50, rs.getInt("MPEG7_Edge_Histogram50"));
//    		newInstance.setValue(MPEG7_Edge_Histogram51, rs.getInt("MPEG7_Edge_Histogram51"));
//    		newInstance.setValue(MPEG7_Edge_Histogram52, rs.getInt("MPEG7_Edge_Histogram52"));
//    		newInstance.setValue(MPEG7_Edge_Histogram53, rs.getInt("MPEG7_Edge_Histogram53"));
//    		newInstance.setValue(MPEG7_Edge_Histogram54, rs.getInt("MPEG7_Edge_Histogram54"));
//    		newInstance.setValue(MPEG7_Edge_Histogram55, rs.getInt("MPEG7_Edge_Histogram55"));
//    		newInstance.setValue(MPEG7_Edge_Histogram56, rs.getInt("MPEG7_Edge_Histogram56"));
//    		newInstance.setValue(MPEG7_Edge_Histogram57, rs.getInt("MPEG7_Edge_Histogram57"));
//    		newInstance.setValue(MPEG7_Edge_Histogram58, rs.getInt("MPEG7_Edge_Histogram58"));
//    		newInstance.setValue(MPEG7_Edge_Histogram59, rs.getInt("MPEG7_Edge_Histogram59"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram60, rs.getInt("MPEG7_Edge_Histogram60"));
//    		newInstance.setValue(MPEG7_Edge_Histogram61, rs.getInt("MPEG7_Edge_Histogram61"));
//    		newInstance.setValue(MPEG7_Edge_Histogram62, rs.getInt("MPEG7_Edge_Histogram62"));
//    		newInstance.setValue(MPEG7_Edge_Histogram63, rs.getInt("MPEG7_Edge_Histogram63"));
//    		newInstance.setValue(MPEG7_Edge_Histogram64, rs.getInt("MPEG7_Edge_Histogram64"));
//    		newInstance.setValue(MPEG7_Edge_Histogram65, rs.getInt("MPEG7_Edge_Histogram65"));
//    		newInstance.setValue(MPEG7_Edge_Histogram66, rs.getInt("MPEG7_Edge_Histogram66"));
//    		newInstance.setValue(MPEG7_Edge_Histogram67, rs.getInt("MPEG7_Edge_Histogram67"));
//    		newInstance.setValue(MPEG7_Edge_Histogram68, rs.getInt("MPEG7_Edge_Histogram68"));
//    		newInstance.setValue(MPEG7_Edge_Histogram69, rs.getInt("MPEG7_Edge_Histogram69"));
//    		
//    		newInstance.setValue(MPEG7_Edge_Histogram70, rs.getInt("MPEG7_Edge_Histogram70"));
//    		newInstance.setValue(MPEG7_Edge_Histogram71, rs.getInt("MPEG7_Edge_Histogram71"));
//    		newInstance.setValue(MPEG7_Edge_Histogram72, rs.getInt("MPEG7_Edge_Histogram72"));
//    		newInstance.setValue(MPEG7_Edge_Histogram73, rs.getInt("MPEG7_Edge_Histogram73"));
//    		newInstance.setValue(MPEG7_Edge_Histogram74, rs.getInt("MPEG7_Edge_Histogram74"));
//    		newInstance.setValue(MPEG7_Edge_Histogram75, rs.getInt("MPEG7_Edge_Histogram75"));
//    		newInstance.setValue(MPEG7_Edge_Histogram76, rs.getInt("MPEG7_Edge_Histogram76"));
//    		newInstance.setValue(MPEG7_Edge_Histogram77, rs.getInt("MPEG7_Edge_Histogram77"));
//    		newInstance.setValue(MPEG7_Edge_Histogram78, rs.getInt("MPEG7_Edge_Histogram78"));
//    		newInstance.setValue(MPEG7_Edge_Histogram79, rs.getInt("MPEG7_Edge_Histogram79"));
//    		
//    		newInstance.setValue(device_super_name, rs.getInt("device_super_name"));
//    		newInstance.setValue(unknown, "?");
//    		
//    		
//    		dataset.add(newInstance);
//    		
//    		dataset.setClassIndex(dataset.numAttributes() - 1);
	    
//	    Instances testset = data.stringFreeStructure();
//	    Instance instance = new DenseInstance(2);

//    		Instance newInst = testDataset.instance(0);
    		// Load the model

//	    	Instance newInst = data.instance(0);
	    	
    		
                               
          
        
//        conn.close();
//        System.out.println("Finished");
                
        
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 

	}

}
