package main;

import java.io.FileWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class CalculateProbabilityCutOff {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String modelRunName = "2020_02_08_1"; // Change this to same as parameters.modelRunName in python code
		//String device_super_name = "";
		
		Connection conn1 = null;
		String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
		// create a connection to the database

		try {
			conn1 = DriverManager.getConnection(url);
			String sql1 = "select distinct device_super_name from recordings";
			
			PreparedStatement pstmt1 = conn1.prepareStatement(sql1);
			ResultSet rs    = pstmt1.executeQuery(); 
			
			while (rs.next()) {	
				
				String device_super_name = rs.getString("device_super_name");
				createDataForIndivualDeviceSuperName(modelRunName, device_super_name);
			}
			
			conn1.close();
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
	}
	
	public static void createDataForIndivualDeviceSuperName(String modelRunName, String device_super_name){
ArrayList<ModelRunResult> modelRunResults = new ArrayList<ModelRunResult>();
		
		String resultCSVFilePath = "/home/tim/Work/Cacophony/Audio_Analysis/Spreadsheets/JavaAnalysis_" + modelRunName + "_" + device_super_name + ".csv";
		
		int runningTotalTruePositives = 0;
    	int runningTotalTrueNegatives = 0;
    	int runningTotalFalsePositives = 0;
    	int runningTotalFalseNegatives = 0;
    	
    	int runningTotalPositives = 0;
    	int runningTotalNegatives = 0;
    	
    	double truePositiveRate = 0; // it will use this when there is a divide by zero
    	
    	int numberOfResults = 0;
    	
    	
		
		try {
			Connection conn = null;


			String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
			// create a connection to the database

			conn = DriverManager.getConnection(url);

			System.out.println("Connection to SQLite has been established.");
//			Statement stmt = conn.createStatement();
			
			String sql = "select device_super_name, device_name, probability, used_to_create_model, recording_id, startTime, actual_confirmed, predictedByModel,  strftime('%m', recordingDateTime) as month, strftime('%Y', recordingDateTime) as year " +
				   "from model_run_result " +
//				    "where modelRunName = ? and actual_confirmed is not null " +
					"where modelRunName = ? and actual_confirmed is not null and device_super_name = ? " +
				    "order by probability DESC";				    

			PreparedStatement pstmt  = conn.prepareStatement(sql);
        	pstmt.setString(1,modelRunName); 
        	pstmt.setString(2,device_super_name); 
        	ResultSet rs    = pstmt.executeQuery();      
        	
        	
        	        	
			while (rs.next()) {	
				numberOfResults++;
				
				//String device_super_name = rs.getString("device_super_name");
				String device_name = rs.getString("device_name");
				double probability = rs.getDouble("probability");
				int used_to_create_model_int = rs.getInt("used_to_create_model");
				boolean used_to_create_model = (used_to_create_model_int == 1);
				int recording_id = rs.getInt("recording_id");
				double startTime = rs.getDouble("startTime");
				String actual_confirmed = rs.getString("actual_confirmed");
				String predictedByModel = rs.getString("predictedByModel");
				int month = rs.getInt("month");
				int year = rs.getInt("year");
				
											
			ModelRunResult modelRunResult = new ModelRunResult(device_super_name,
				 device_name,
				 probability,
				 used_to_create_model,
				 recording_id,
				 startTime,
				 actual_confirmed,
				 predictedByModel,
				 month,
				 year);
			
			if (modelRunResult.isPositive()) {
				runningTotalPositives++;				
			}else {
				runningTotalNegatives++;
			}
			
			if (modelRunResult.isTruePositive()) {
				runningTotalTruePositives++;
				
			}
			
			if (modelRunResult.isTrueNegative()) {
				runningTotalTrueNegatives++;
				
			}
			
			if (modelRunResult.isFalsePositive()) {
				runningTotalFalsePositives++;
				
			}
			
			if (modelRunResult.isFalseNegative()) {
				runningTotalFalseNegatives++;
				
			}
			
					
			modelRunResult.setRunningTotalPositives(runningTotalPositives);
			modelRunResult.setRunningTotalPositives(runningTotalNegatives);
			
			modelRunResult.setRunningTotalTruePositives(runningTotalTruePositives);
			modelRunResult.setRunningTotalTrueNegatives(runningTotalTrueNegatives);
			modelRunResult.setRunningTotalFalsePositives(runningTotalFalsePositives);
			modelRunResult.setRunningTotalFalseNegatives(runningTotalFalseNegatives);
			
			if (runningTotalPositives > 0) {
				
				truePositiveRate =  runningTotalTruePositives/(double)runningTotalPositives;
				modelRunResult.setTruePositiveRate(truePositiveRate);
			}
			
			
			
			//System.out.println(modelRunResult);
			
			modelRunResults.add(modelRunResult);

			}
		conn.close();
		
		System.out.println("There are " + numberOfResults + " rows for " + device_super_name);
		
		// Can now do calculations that require totals
		
		// Rate of incorrect morepork predictions if do not use model but always predict morepork - if no model then can not use model probability:   (total of not actual morepork)/(total of  actual morepork + total of not actual morepork)
		// Only calculate falsePositveRateIfAlwaysPredictMorePork once as it stays constant
		double falsePositveRateIfAlwaysPredictMorePork = runningTotalNegatives / (double)(runningTotalPositives + runningTotalNegatives);
		
		double probabilityCutOff = -1;
		
		for (ModelRunResult modelRunResult : modelRunResults) { 	
			// Coverage: Rate (out of 1)  of Actual moreporks correctly tagged as moreporks: (Running total of TP) / Total of actual moreporks)
			double coverageRate =  modelRunResult.getRunningTotalTruePositives()/(double)runningTotalPositives;
			modelRunResult.setCoverageRate(coverageRate);
			
			// Rate (out of 1) of incorrect morepork predictions: (Running total of FP) / (Running total of TP + FP)
			double incorrectMoreporkPredictionRate = modelRunResult.getRunningTotalFalsePositives() / (double)(runningTotalTruePositives + runningTotalFalsePositives);
			modelRunResult.setIncorrectMoreporkPredictionRate(incorrectMoreporkPredictionRate);
			
			modelRunResult.setFalsePositveRateIfAlwaysPredictMorePork(falsePositveRateIfAlwaysPredictMorePork);
			
			if (probabilityCutOff == -1) {
				if (incorrectMoreporkPredictionRate < 0.05) {
					probabilityCutOff = modelRunResult.getProbability();
					System.out.println(probabilityCutOff);
				}
			}
		}
		
				
		// Create csv file 
		// https://stackabuse.com/reading-and-writing-csvs-in-java/
		FileWriter csvWriter = new FileWriter(resultCSVFilePath, false);
		
		int count = 0;
		csvWriter.append("Probability, True Positive rate (TP/Total number of positives), Coverage rate (Fraction of actual morepork tagged as morepork), Rate (out of 1) of incorrect morepork predictions, Rate of incorrect morepork predictions if do not use model but always predict morepork - if no model then can not use model probability: (total of not actual morepork)/(total of  actual morepork + total of not actual morepork)," + numberOfResults + " rows, Probability cutoff " + probabilityCutOff);          
        csvWriter.append("\n");
        
        
        
        // See the following for creating Excel chart with first colunm used as x-asis for all other columns
        
		for (ModelRunResult modelRunResult : modelRunResults) { 	
			count++;
//			if (count > 256) {
//				System.out.println("Count is " + count); 
//			}
	           
	           csvWriter.append(modelRunResult.dataToPlot());          
	           csvWriter.append("\n");
	      }
		
		csvWriter.flush();
		csvWriter.close();
		
		
		
		System.out.println("Finished");

		} catch (Exception e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
		}
	}
}
