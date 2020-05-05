package main;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

import weka.classifiers.meta.CostSensitiveClassifier;
import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instance;
import weka.core.Instances;

public class ClassifyOnsetsDirectFromAudio {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String modelRunName = "2020_05_04_1"; // Change this to same as parameters.modelRunName in python code
		
		
		
		String modelName = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/" + modelRunName
				+ "/weka_model/model.model";
		
		try {
			Connection conn = null;
			
			String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db3.db";
			// create a connection to the database

			conn = DriverManager.getConnection(url);
			System.out.println("Connection to SQLite has been established.");
			Statement stmt = conn.createStatement();
			
			String sql = "SELECT ";
			
			for (int i=0;i<44;i++) {
				sql += "rms" + i + ", ";
			}
			
			for (int i=0;i<44;i++) {
				sql += "spectral_centroid" + i + ", ";
			}
			
			for (int i=0;i<44;i++) {
				sql += "spectral_bandwidth" + i + ", ";
			}
			
			for (int i=0;i<44;i++) {
				sql += "spectral_rolloff" + i + ", ";
			}
			
			for (int i=0;i<44;i++) {
				sql += "zero_crossing_rate" + i + ", ";
			}
			
			sql += "recording_id, start_time_seconds, duration_seconds, device_super_name, device_name, recordingDateTime, actual_confirmed ";
			
//			sql += "FROM features WHERE rms0 IS NOT NULL ";
//			sql += "FROM features WHERE rms0 IS NOT NULL AND actual_confirmed = 'morepork_more-pork'";
//			sql += "FROM features WHERE rms43 IS NOT NULL AND actual_confirmed = 'morepork_more-pork'"; // If rms43 is null, then there isn't a full call/clip so ignore
			sql += "FROM features WHERE rms43 IS NOT NULL "; // If rms43 is null, then there isn't a full call/clip so ignore
			
			sql += "AND NOT EXISTS ( ";
			// Don't reclassify onsets that have already been classified for this modelRunName
			sql += "SELECT ID FROM model_run_result WHERE modelRunName = ? AND model_run_result.recording_id = features.recording_id AND model_run_result.startTime = features.start_time_seconds AND model_run_result.duration = features.duration_seconds) ";
			
			sql += "ORDER BY recording_id DESC";
			
			ArrayList<Attribute> attributes = new ArrayList<Attribute>();

			for (int i = 0; i < 44; i++) {
				attributes.add(new Attribute("rms" + i));
			}
			
			for (int i = 0; i < 44; i++) {
				attributes.add(new Attribute("spectral_centroid" + i));
			}
			
			for (int i = 0; i < 44; i++) {
				attributes.add(new Attribute("spectral_bandwidth" + i));
			}
			
			for (int i = 0; i < 44; i++) {
				attributes.add(new Attribute("spectral_rolloff" + i));
			}
			
			for (int i = 0; i < 44; i++) {
				attributes.add(new Attribute("zero_crossing_rate" + i));
			}
			
//			System.out.println(sql);
			
//			ArrayList<String> deviceSuperNameLabels = new ArrayList<String>();
//			deviceSuperNameLabels.add("Hammond_Park");
//			deviceSuperNameLabels.add("grants_shed");
//			deviceSuperNameLabels.add("Living_Springs");
//			deviceSuperNameLabels.add("Kerikeri_Peninsula_Pest_Control");
//			deviceSuperNameLabels.add("Motuihe");
////			deviceSuperNameLabels.add("Predator_Free_Miramar");
//			deviceSuperNameLabels.add("predatorfreemiramar");
//			deviceSuperNameLabels.add("Te_Motu_Kairangi-Miramar_Ecological_Restoration");
//			deviceSuperNameLabels.add("Elorosa");
//			deviceSuperNameLabels.add("Lochmara");
//			deviceSuperNameLabels.add("Fale_monitor");
//			deviceSuperNameLabels.add("karaka_bay");
//			deviceSuperNameLabels.add("Somerfield");
//			deviceSuperNameLabels.add("boyle_field_project");
//			deviceSuperNameLabels.add("chow");
//			deviceSuperNameLabels.add("livingsprings");
//			deviceSuperNameLabels.add("Te_Motu_Kairangi-Predator_Free_Miramar");
//			//deviceSuperNameLabels.add("other");
//
//			attributes.add(new Attribute("deviceSuperName", deviceSuperNameLabels));

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
			classLabels.add("hand_saw");
			classLabels.add("music");

			attributes.add(new Attribute("class", classLabels));
			
			Instances data = new Instances(modelRunName, attributes, 0);
			data.setClassIndex(data.numAttributes() - 1);

			CostSensitiveClassifier myModel = (CostSensitiveClassifier) weka.core.SerializationHelper.read(modelName);
			
			// First need to do a separate query to get size of result set // https://stackoverflow.com/questions/13103067/correct-way-to-find-rowcount-in-java-jdbc
			String sqlForSize = "SELECT COUNT(*) as rowcount FROM features WHERE rms43 IS NOT NULL AND NOT EXISTS ( SELECT ID FROM model_run_result WHERE modelRunName = ? AND model_run_result.recording_id = features.recording_id AND model_run_result.startTime = features.start_time_seconds AND model_run_result.duration = features.duration_seconds)"; 
					
			PreparedStatement pstmtForSize  = conn.prepareStatement(sqlForSize);				
        	pstmtForSize.setString(1,modelRunName); 
        	
        	ResultSet rsForSize    = pstmtForSize.executeQuery();
        	rsForSize.next();
        	int size = rsForSize.getInt("rowcount");
        	rsForSize.close();
        	        	
        	PreparedStatement pstmt  = conn.prepareStatement(sql);	
        	pstmt.setString(1,modelRunName);         	
        	        	
        	ResultSet rs    = pstmt.executeQuery();  
        	

			// loop through the result set
			int processedSoFar = 0;
			while (rs.next()) {
				System.out.println("Processed " + processedSoFar + " of " + size);
				processedSoFar++;

				int recording_id = rs.getInt("recording_id");
				double start_time_seconds = rs.getDouble("start_time_seconds");
				double duration_seconds = rs.getDouble("duration_seconds");
				String device_super_name = rs.getString("device_super_name");
				String device_name = rs.getString("device_name");
				String recordingDateTime = rs.getString("recordingDateTime");
				String actual_confirmed = rs.getString("actual_confirmed");

				double[] vals = new double[data.numAttributes()];		
				
				int numberOfFeatures = 5*44;
				int index = 0;
				for (int i = 0; i < numberOfFeatures; i++) {
					vals[i] = rs.getInt(i + 1);
					index = i;
				}
				
//				System.out.print("Index is " + index);
				
//				// When there is a new location that hasn't yet been seen by the model, just change the location to Hammond_Park.
//				// Will note in the database, the actual location and the location used by the model
//				String actual_device_super_name = device_super_name;
//				String device_super_name_used_by_model = device_super_name;
//								
//				if (!deviceSuperNameLabels.contains(device_super_name)) {          
//					device_super_name_used_by_model = "Hammond_Park";
//				}
				
//				vals[numberOfFeatures] = deviceSuperNameLabels.indexOf(device_super_name_used_by_model);
				
//				vals[numberOfFeatures + 1] = classLabels.indexOf("music"); // Seems you need to give it any class name
				
				index++;
				vals[index] = classLabels.indexOf("music"); // Seems you need to give it any class name

				Instance instanceToClassify = new DenseInstance(1.0, vals);
				instanceToClassify.setDataset(data);

//				System.out.println(instanceToClassify);

				int result = (int) myModel.classifyInstance(instanceToClassify);
				String predictedByModel = classLabels.get(result);

				double probablility = myModel.distributionForInstance(instanceToClassify)[result];

				System.out.println(result + "," + predictedByModel + "," + probablility);
				
				// Now update database model_run_result
				
				ZonedDateTime date = ZonedDateTime.now();
				DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
				String resultCreatedDateTime = date.format(formatter);
				 

				//String sql2 = "INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime) VALUES(?,?,?,?,?,?,?,?,?,?)";
//				String sql2 = "INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, resultCreatedDateTime, device_super_name_used_by_model) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)";
				String sql2 = "INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, resultCreatedDateTime) VALUES(?,?,?,?,?,?,?,?,?,?,?)";


				try (PreparedStatement pstmt2 = conn.prepareStatement(sql2)) {
					pstmt2.setString(1, modelRunName);
					pstmt2.setDouble(2, recording_id);
					pstmt2.setDouble(3, start_time_seconds);
					pstmt2.setDouble(4, duration_seconds);
					pstmt2.setString(5, predictedByModel);
					pstmt2.setDouble(6, probablility);
					pstmt2.setString(7, actual_confirmed);
					pstmt2.setString(8, device_super_name);					
					pstmt2.setString(9, device_name);
					pstmt2.setString(10, recordingDateTime);					
					pstmt2.setString(11, resultCreatedDateTime);
//					pstmt2.setString(12, device_super_name_used_by_model);
					

					pstmt2.executeUpdate();
					
					if (processedSoFar % 1000 == 0) {						
						System.out.println("Have processed " + processedSoFar);
						System.out.println("\n\n");
					}
				} catch (SQLException e) {
					System.out.println(e.getMessage());
				}
				
			}
			rs.close();
			
			conn.close();
			System.out.println("Finished");
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
