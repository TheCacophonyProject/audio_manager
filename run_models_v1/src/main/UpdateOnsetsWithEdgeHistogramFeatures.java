package main;

import java.sql.Connection;  
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;  
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

public class UpdateOnsetsWithEdgeHistogramFeatures {
	
static String modelName = "model.model";
static String imageDirectory = "./images";

	public static void main(String[] args) {
		
		 Connection conn = null;  
	        try {  
	           
	        	String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
	            // create a connection to the database  
	            conn = DriverManager.getConnection(url);  
	            System.out.println("Connection to SQLite has been established.");  
	            Statement stmt  = conn.createStatement();
	            // String sql = "UPDATE onsets SET version = 999 WHERE ID = 3939";
//	            String sql = "SELECT ID, recording_id, start_time_seconds, duration_seconds from onsets WHERE MPEG7_Edge_Histogram0 IS NULL";
	            String sql = "SELECT ID, recording_id, start_time_seconds, duration_seconds, MPEG7_Edge_Histogram0 from onsets where MPEG7_Edge_Histogram0 IS NULL"; 
	            ResultSet rs    = stmt.executeQuery(sql);  
	            while (rs.next()) {  
	                System.out.println(rs.getInt("ID") +  "\t" +   
	                                   rs.getInt("recording_id") + "\t" + 
	                                   rs.getInt("start_time_seconds") + "\t" + 
	                                   rs.getInt("duration_seconds"));
	                                   
	            }  
	            
	            conn.close();
	            System.out.println("Finished");

	            
	              
	        } catch (SQLException e) {  
	            System.out.println(e.getMessage());  
	        } 

	}

}
