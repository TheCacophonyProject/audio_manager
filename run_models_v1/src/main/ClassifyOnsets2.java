package main;


import java.sql.Connection;  
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

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

public class ClassifyOnsets2 {

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
        
        ResultSet rs    = stmt.executeQuery(sql);  
        
        DataSource source = new DataSource("/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/2020_02_07_1/weka_model/input.arff");																						
		Instances dataset = source.getDataSet();
		
		
		
		Attribute MPEG7_Edge_Histogram0 = new Attribute("MPEG7_Edge_Histogram0");
		Attribute MPEG7_Edge_Histogram1 = new Attribute("MPEG7_Edge_Histogram1");
		Attribute MPEG7_Edge_Histogram2 = new Attribute("MPEG7_Edge_Histogram2");
		Attribute MPEG7_Edge_Histogram3 = new Attribute("MPEG7_Edge_Histogram3");
		Attribute MPEG7_Edge_Histogram4 = new Attribute("MPEG7_Edge_Histogram4");
		Attribute MPEG7_Edge_Histogram5 = new Attribute("MPEG7_Edge_Histogram5");
		Attribute MPEG7_Edge_Histogram6 = new Attribute("MPEG7_Edge_Histogram6");
		Attribute MPEG7_Edge_Histogram7 = new Attribute("MPEG7_Edge_Histogram7");
		Attribute MPEG7_Edge_Histogram8 = new Attribute("MPEG7_Edge_Histogram8");
		Attribute MPEG7_Edge_Histogram9 = new Attribute("MPEG7_Edge_Histogram9");
		
		Attribute MPEG7_Edge_Histogram10 = new Attribute("MPEG7_Edge_Histogram10");
		Attribute MPEG7_Edge_Histogram11 = new Attribute("MPEG7_Edge_Histogram11");
		Attribute MPEG7_Edge_Histogram12 = new Attribute("MPEG7_Edge_Histogram12");
		Attribute MPEG7_Edge_Histogram13 = new Attribute("MPEG7_Edge_Histogram13");
		Attribute MPEG7_Edge_Histogram14 = new Attribute("MPEG7_Edge_Histogram14");
		Attribute MPEG7_Edge_Histogram15 = new Attribute("MPEG7_Edge_Histogram15");
		Attribute MPEG7_Edge_Histogram16 = new Attribute("MPEG7_Edge_Histogram16");
		Attribute MPEG7_Edge_Histogram17 = new Attribute("MPEG7_Edge_Histogram17");
		Attribute MPEG7_Edge_Histogram18 = new Attribute("MPEG7_Edge_Histogram18");
		Attribute MPEG7_Edge_Histogram19 = new Attribute("MPEG7_Edge_Histogram19");		
		
		Attribute MPEG7_Edge_Histogram20 = new Attribute("MPEG7_Edge_Histogram20");
		Attribute MPEG7_Edge_Histogram21 = new Attribute("MPEG7_Edge_Histogram21");
		Attribute MPEG7_Edge_Histogram22 = new Attribute("MPEG7_Edge_Histogram22");
		Attribute MPEG7_Edge_Histogram23 = new Attribute("MPEG7_Edge_Histogram23");
		Attribute MPEG7_Edge_Histogram24 = new Attribute("MPEG7_Edge_Histogram24");
		Attribute MPEG7_Edge_Histogram25 = new Attribute("MPEG7_Edge_Histogram25");
		Attribute MPEG7_Edge_Histogram26 = new Attribute("MPEG7_Edge_Histogram26");
		Attribute MPEG7_Edge_Histogram27 = new Attribute("MPEG7_Edge_Histogram27");
		Attribute MPEG7_Edge_Histogram28 = new Attribute("MPEG7_Edge_Histogram28");
		Attribute MPEG7_Edge_Histogram29 = new Attribute("MPEG7_Edge_Histogram29");
		
		Attribute MPEG7_Edge_Histogram30 = new Attribute("MPEG7_Edge_Histogram30");
		Attribute MPEG7_Edge_Histogram31 = new Attribute("MPEG7_Edge_Histogram31");
		Attribute MPEG7_Edge_Histogram32 = new Attribute("MPEG7_Edge_Histogram32");
		Attribute MPEG7_Edge_Histogram33 = new Attribute("MPEG7_Edge_Histogram33");
		Attribute MPEG7_Edge_Histogram34 = new Attribute("MPEG7_Edge_Histogram34");
		Attribute MPEG7_Edge_Histogram35 = new Attribute("MPEG7_Edge_Histogram35");
		Attribute MPEG7_Edge_Histogram36 = new Attribute("MPEG7_Edge_Histogram36");
		Attribute MPEG7_Edge_Histogram37 = new Attribute("MPEG7_Edge_Histogram37");
		Attribute MPEG7_Edge_Histogram38 = new Attribute("MPEG7_Edge_Histogram38");
		Attribute MPEG7_Edge_Histogram39 = new Attribute("MPEG7_Edge_Histogram39");
		
		Attribute MPEG7_Edge_Histogram40 = new Attribute("MPEG7_Edge_Histogram40");
		Attribute MPEG7_Edge_Histogram41 = new Attribute("MPEG7_Edge_Histogram41");
		Attribute MPEG7_Edge_Histogram42 = new Attribute("MPEG7_Edge_Histogram42");
		Attribute MPEG7_Edge_Histogram43 = new Attribute("MPEG7_Edge_Histogram43");
		Attribute MPEG7_Edge_Histogram44 = new Attribute("MPEG7_Edge_Histogram44");
		Attribute MPEG7_Edge_Histogram45 = new Attribute("MPEG7_Edge_Histogram45");
		Attribute MPEG7_Edge_Histogram46 = new Attribute("MPEG7_Edge_Histogram46");
		Attribute MPEG7_Edge_Histogram47 = new Attribute("MPEG7_Edge_Histogram47");
		Attribute MPEG7_Edge_Histogram48 = new Attribute("MPEG7_Edge_Histogram48");
		Attribute MPEG7_Edge_Histogram49 = new Attribute("MPEG7_Edge_Histogram49");
		
		Attribute MPEG7_Edge_Histogram50 = new Attribute("MPEG7_Edge_Histogram50");
		Attribute MPEG7_Edge_Histogram51 = new Attribute("MPEG7_Edge_Histogram51");
		Attribute MPEG7_Edge_Histogram52 = new Attribute("MPEG7_Edge_Histogram52");
		Attribute MPEG7_Edge_Histogram53 = new Attribute("MPEG7_Edge_Histogram53");
		Attribute MPEG7_Edge_Histogram54 = new Attribute("MPEG7_Edge_Histogram54");
		Attribute MPEG7_Edge_Histogram55 = new Attribute("MPEG7_Edge_Histogram55");
		Attribute MPEG7_Edge_Histogram56 = new Attribute("MPEG7_Edge_Histogram56");
		Attribute MPEG7_Edge_Histogram57 = new Attribute("MPEG7_Edge_Histogram57");
		Attribute MPEG7_Edge_Histogram58 = new Attribute("MPEG7_Edge_Histogram58");
		Attribute MPEG7_Edge_Histogram59 = new Attribute("MPEG7_Edge_Histogram59");
		
		Attribute MPEG7_Edge_Histogram60 = new Attribute("MPEG7_Edge_Histogram60");
		Attribute MPEG7_Edge_Histogram61 = new Attribute("MPEG7_Edge_Histogram61");
		Attribute MPEG7_Edge_Histogram62 = new Attribute("MPEG7_Edge_Histogram62");
		Attribute MPEG7_Edge_Histogram63 = new Attribute("MPEG7_Edge_Histogram63");
		Attribute MPEG7_Edge_Histogram64 = new Attribute("MPEG7_Edge_Histogram64");
		Attribute MPEG7_Edge_Histogram65 = new Attribute("MPEG7_Edge_Histogram65");
		Attribute MPEG7_Edge_Histogram66 = new Attribute("MPEG7_Edge_Histogram66");
		Attribute MPEG7_Edge_Histogram67 = new Attribute("MPEG7_Edge_Histogram67");
		Attribute MPEG7_Edge_Histogram68 = new Attribute("MPEG7_Edge_Histogram68");
		Attribute MPEG7_Edge_Histogram69 = new Attribute("MPEG7_Edge_Histogram69");
		
		Attribute MPEG7_Edge_Histogram70 = new Attribute("MPEG7_Edge_Histogram70");
		Attribute MPEG7_Edge_Histogram71 = new Attribute("MPEG7_Edge_Histogram71");
		Attribute MPEG7_Edge_Histogram72 = new Attribute("MPEG7_Edge_Histogram72");
		Attribute MPEG7_Edge_Histogram73 = new Attribute("MPEG7_Edge_Histogram73");
		Attribute MPEG7_Edge_Histogram74 = new Attribute("MPEG7_Edge_Histogram74");
		Attribute MPEG7_Edge_Histogram75 = new Attribute("MPEG7_Edge_Histogram75");
		Attribute MPEG7_Edge_Histogram76 = new Attribute("MPEG7_Edge_Histogram76");
		Attribute MPEG7_Edge_Histogram77 = new Attribute("MPEG7_Edge_Histogram77");
		Attribute MPEG7_Edge_Histogram78 = new Attribute("MPEG7_Edge_Histogram78");
		Attribute MPEG7_Edge_Histogram79 = new Attribute("MPEG7_Edge_Histogram79");
		
		Attribute device_super_name = new Attribute("device_super_name");
		Attribute unknown = new Attribute("unknown");
		
		if (dataset.classIndex() == -1)
			dataset.setClassIndex(dataset.numAttributes() - 1);
		
//		 for(int i = 0 ; i < dataset.numAttributes() ; i++)
//		 {
//
//		     newInstance.setValue(i , 2);
//		     //i is the index of attribute
//		     //value is the value that you want to set
//		 }
//		 //add the new instance to the main dataset at the last position
//		 dataset.add(newInstance);
		int count = 0;
        while (rs.next()) {  
        	count++;
        	if (count > 10){
        		break;
        	}
            System.out.println(rs.getInt("MPEG7_Edge_Histogram0") + "\t" + 
                               rs.getInt("MPEG7_Edge_Histogram1") + "\t" + 
                               rs.getString("device_super_name") + "\t" + 
                               rs.getString("actual_confirmed"));
            
            Instance newInstance  = new DenseInstance(0);
            newInstance.setDataset(dataset);
            
            newInstance.setValue(MPEG7_Edge_Histogram0, 4);
          
                        
    		newInstance.setValue(MPEG7_Edge_Histogram0, rs.getInt("MPEG7_Edge_Histogram0"));
    		newInstance.setValue(MPEG7_Edge_Histogram1, rs.getInt("MPEG7_Edge_Histogram1"));
    		newInstance.setValue(MPEG7_Edge_Histogram2, rs.getInt("MPEG7_Edge_Histogram2"));
    		newInstance.setValue(MPEG7_Edge_Histogram3, rs.getInt("MPEG7_Edge_Histogram3"));
    		newInstance.setValue(MPEG7_Edge_Histogram4, rs.getInt("MPEG7_Edge_Histogram4"));
    		newInstance.setValue(MPEG7_Edge_Histogram5, rs.getInt("MPEG7_Edge_Histogram5"));
    		newInstance.setValue(MPEG7_Edge_Histogram6, rs.getInt("MPEG7_Edge_Histogram6"));
    		newInstance.setValue(MPEG7_Edge_Histogram7, rs.getInt("MPEG7_Edge_Histogram7"));
    		newInstance.setValue(MPEG7_Edge_Histogram8, rs.getInt("MPEG7_Edge_Histogram8"));
    		newInstance.setValue(MPEG7_Edge_Histogram9, rs.getInt("MPEG7_Edge_Histogram9"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram10, rs.getInt("MPEG7_Edge_Histogram10"));
    		newInstance.setValue(MPEG7_Edge_Histogram11, rs.getInt("MPEG7_Edge_Histogram11"));
    		newInstance.setValue(MPEG7_Edge_Histogram12, rs.getInt("MPEG7_Edge_Histogram12"));
    		newInstance.setValue(MPEG7_Edge_Histogram13, rs.getInt("MPEG7_Edge_Histogram13"));
    		newInstance.setValue(MPEG7_Edge_Histogram14, rs.getInt("MPEG7_Edge_Histogram14"));
    		newInstance.setValue(MPEG7_Edge_Histogram15, rs.getInt("MPEG7_Edge_Histogram15"));
    		newInstance.setValue(MPEG7_Edge_Histogram16, rs.getInt("MPEG7_Edge_Histogram16"));
    		newInstance.setValue(MPEG7_Edge_Histogram17, rs.getInt("MPEG7_Edge_Histogram17"));
    		newInstance.setValue(MPEG7_Edge_Histogram18, rs.getInt("MPEG7_Edge_Histogram18"));
    		newInstance.setValue(MPEG7_Edge_Histogram19, rs.getInt("MPEG7_Edge_Histogram19"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram20, rs.getInt("MPEG7_Edge_Histogram20"));
    		newInstance.setValue(MPEG7_Edge_Histogram21, rs.getInt("MPEG7_Edge_Histogram21"));
    		newInstance.setValue(MPEG7_Edge_Histogram22, rs.getInt("MPEG7_Edge_Histogram22"));
    		newInstance.setValue(MPEG7_Edge_Histogram23, rs.getInt("MPEG7_Edge_Histogram23"));
    		newInstance.setValue(MPEG7_Edge_Histogram24, rs.getInt("MPEG7_Edge_Histogram24"));
    		newInstance.setValue(MPEG7_Edge_Histogram25, rs.getInt("MPEG7_Edge_Histogram25"));
    		newInstance.setValue(MPEG7_Edge_Histogram26, rs.getInt("MPEG7_Edge_Histogram26"));
    		newInstance.setValue(MPEG7_Edge_Histogram27, rs.getInt("MPEG7_Edge_Histogram27"));
    		newInstance.setValue(MPEG7_Edge_Histogram28, rs.getInt("MPEG7_Edge_Histogram28"));
    		newInstance.setValue(MPEG7_Edge_Histogram29, rs.getInt("MPEG7_Edge_Histogram29"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram30, rs.getInt("MPEG7_Edge_Histogram30"));
    		newInstance.setValue(MPEG7_Edge_Histogram31, rs.getInt("MPEG7_Edge_Histogram31"));
    		newInstance.setValue(MPEG7_Edge_Histogram32, rs.getInt("MPEG7_Edge_Histogram32"));
    		newInstance.setValue(MPEG7_Edge_Histogram33, rs.getInt("MPEG7_Edge_Histogram33"));
    		newInstance.setValue(MPEG7_Edge_Histogram34, rs.getInt("MPEG7_Edge_Histogram34"));
    		newInstance.setValue(MPEG7_Edge_Histogram35, rs.getInt("MPEG7_Edge_Histogram35"));
    		newInstance.setValue(MPEG7_Edge_Histogram36, rs.getInt("MPEG7_Edge_Histogram36"));
    		newInstance.setValue(MPEG7_Edge_Histogram37, rs.getInt("MPEG7_Edge_Histogram37"));
    		newInstance.setValue(MPEG7_Edge_Histogram38, rs.getInt("MPEG7_Edge_Histogram38"));
    		newInstance.setValue(MPEG7_Edge_Histogram39, rs.getInt("MPEG7_Edge_Histogram39"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram40, rs.getInt("MPEG7_Edge_Histogram40"));
    		newInstance.setValue(MPEG7_Edge_Histogram41, rs.getInt("MPEG7_Edge_Histogram41"));
    		newInstance.setValue(MPEG7_Edge_Histogram42, rs.getInt("MPEG7_Edge_Histogram42"));
    		newInstance.setValue(MPEG7_Edge_Histogram43, rs.getInt("MPEG7_Edge_Histogram43"));
    		newInstance.setValue(MPEG7_Edge_Histogram44, rs.getInt("MPEG7_Edge_Histogram44"));
    		newInstance.setValue(MPEG7_Edge_Histogram45, rs.getInt("MPEG7_Edge_Histogram45"));
    		newInstance.setValue(MPEG7_Edge_Histogram46, rs.getInt("MPEG7_Edge_Histogram46"));
    		newInstance.setValue(MPEG7_Edge_Histogram47, rs.getInt("MPEG7_Edge_Histogram47"));
    		newInstance.setValue(MPEG7_Edge_Histogram48, rs.getInt("MPEG7_Edge_Histogram48"));
    		newInstance.setValue(MPEG7_Edge_Histogram49, rs.getInt("MPEG7_Edge_Histogram49"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram50, rs.getInt("MPEG7_Edge_Histogram50"));
    		newInstance.setValue(MPEG7_Edge_Histogram51, rs.getInt("MPEG7_Edge_Histogram51"));
    		newInstance.setValue(MPEG7_Edge_Histogram52, rs.getInt("MPEG7_Edge_Histogram52"));
    		newInstance.setValue(MPEG7_Edge_Histogram53, rs.getInt("MPEG7_Edge_Histogram53"));
    		newInstance.setValue(MPEG7_Edge_Histogram54, rs.getInt("MPEG7_Edge_Histogram54"));
    		newInstance.setValue(MPEG7_Edge_Histogram55, rs.getInt("MPEG7_Edge_Histogram55"));
    		newInstance.setValue(MPEG7_Edge_Histogram56, rs.getInt("MPEG7_Edge_Histogram56"));
    		newInstance.setValue(MPEG7_Edge_Histogram57, rs.getInt("MPEG7_Edge_Histogram57"));
    		newInstance.setValue(MPEG7_Edge_Histogram58, rs.getInt("MPEG7_Edge_Histogram58"));
    		newInstance.setValue(MPEG7_Edge_Histogram59, rs.getInt("MPEG7_Edge_Histogram59"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram60, rs.getInt("MPEG7_Edge_Histogram60"));
    		newInstance.setValue(MPEG7_Edge_Histogram61, rs.getInt("MPEG7_Edge_Histogram61"));
    		newInstance.setValue(MPEG7_Edge_Histogram62, rs.getInt("MPEG7_Edge_Histogram62"));
    		newInstance.setValue(MPEG7_Edge_Histogram63, rs.getInt("MPEG7_Edge_Histogram63"));
    		newInstance.setValue(MPEG7_Edge_Histogram64, rs.getInt("MPEG7_Edge_Histogram64"));
    		newInstance.setValue(MPEG7_Edge_Histogram65, rs.getInt("MPEG7_Edge_Histogram65"));
    		newInstance.setValue(MPEG7_Edge_Histogram66, rs.getInt("MPEG7_Edge_Histogram66"));
    		newInstance.setValue(MPEG7_Edge_Histogram67, rs.getInt("MPEG7_Edge_Histogram67"));
    		newInstance.setValue(MPEG7_Edge_Histogram68, rs.getInt("MPEG7_Edge_Histogram68"));
    		newInstance.setValue(MPEG7_Edge_Histogram69, rs.getInt("MPEG7_Edge_Histogram69"));
    		
    		newInstance.setValue(MPEG7_Edge_Histogram70, rs.getInt("MPEG7_Edge_Histogram70"));
    		newInstance.setValue(MPEG7_Edge_Histogram71, rs.getInt("MPEG7_Edge_Histogram71"));
    		newInstance.setValue(MPEG7_Edge_Histogram72, rs.getInt("MPEG7_Edge_Histogram72"));
    		newInstance.setValue(MPEG7_Edge_Histogram73, rs.getInt("MPEG7_Edge_Histogram73"));
    		newInstance.setValue(MPEG7_Edge_Histogram74, rs.getInt("MPEG7_Edge_Histogram74"));
    		newInstance.setValue(MPEG7_Edge_Histogram75, rs.getInt("MPEG7_Edge_Histogram75"));
    		newInstance.setValue(MPEG7_Edge_Histogram76, rs.getInt("MPEG7_Edge_Histogram76"));
    		newInstance.setValue(MPEG7_Edge_Histogram77, rs.getInt("MPEG7_Edge_Histogram77"));
    		newInstance.setValue(MPEG7_Edge_Histogram78, rs.getInt("MPEG7_Edge_Histogram78"));
    		newInstance.setValue(MPEG7_Edge_Histogram79, rs.getInt("MPEG7_Edge_Histogram79"));
    		
    		newInstance.setValue(device_super_name, rs.getInt("device_super_name"));
    		newInstance.setValue(unknown, "?");
    		
    		
    		dataset.add(newInstance);
    		
    		dataset.setClassIndex(dataset.numAttributes() - 1);

//    		Instance newInst = testDataset.instance(0);
    		// Load the model

    		
    		CostSensitiveClassifier myModel = (CostSensitiveClassifier) weka.core.SerializationHelper.read(modelName);

    		int result = (int) myModel.classifyInstance(newInstance);
    		double probablilty = myModel.distributionForInstance(newInstance)[result];
    		
    		System.out.println(result + "," + probablilty);
                               
        }  
        
        conn.close();
        System.out.println("Finished");
                
        
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 

	}

}
