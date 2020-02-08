package main;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
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

public class ClassifyOnsets {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		String modelRunName = "2020_02_08_1";
		String modelName = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/" + modelRunName
				+ "/weka_model/model.model";

		try {
			Connection conn = null;

//		String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
//			String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Temp/audio_analysis_db2.db";
			String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db";
			// create a connection to the database

			conn = DriverManager.getConnection(url);

			System.out.println("Connection to SQLite has been established.");
			Statement stmt = conn.createStatement();
			// String sql = "UPDATE onsets SET version = 999 WHERE ID = 3939";
//        String sql = "SELECT ID, recording_id, start_time_seconds, duration_seconds from onsets WHERE MPEG7_Edge_Histogram0 IS NULL";
			String sql = "SELECT " + "MPEG7_Edge_Histogram0, " + "MPEG7_Edge_Histogram1, " + "MPEG7_Edge_Histogram2, "
					+ "MPEG7_Edge_Histogram3, " + "MPEG7_Edge_Histogram4, " + "MPEG7_Edge_Histogram5, "
					+ "MPEG7_Edge_Histogram6, " + "MPEG7_Edge_Histogram7, " + "MPEG7_Edge_Histogram8, "
					+ "MPEG7_Edge_Histogram9, " +

					"MPEG7_Edge_Histogram10,  " + "MPEG7_Edge_Histogram11, " + "MPEG7_Edge_Histogram12, "
					+ "MPEG7_Edge_Histogram13, " + "MPEG7_Edge_Histogram14, " + "MPEG7_Edge_Histogram15, "
					+ "MPEG7_Edge_Histogram16, " + "MPEG7_Edge_Histogram17, " + "MPEG7_Edge_Histogram18, "
					+ "MPEG7_Edge_Histogram19, " +

					"MPEG7_Edge_Histogram20, " + "MPEG7_Edge_Histogram21, " + "MPEG7_Edge_Histogram22, "
					+ "MPEG7_Edge_Histogram23, " + "MPEG7_Edge_Histogram24, " + "MPEG7_Edge_Histogram25, "
					+ "MPEG7_Edge_Histogram26, " + "MPEG7_Edge_Histogram27, " + "MPEG7_Edge_Histogram28, "
					+ "MPEG7_Edge_Histogram29, " +

					"MPEG7_Edge_Histogram30, " + "MPEG7_Edge_Histogram31, " + "MPEG7_Edge_Histogram32, "
					+ "MPEG7_Edge_Histogram33, " + "MPEG7_Edge_Histogram34, " + "MPEG7_Edge_Histogram35, "
					+ "MPEG7_Edge_Histogram36, " + "MPEG7_Edge_Histogram37, " + "MPEG7_Edge_Histogram38, "
					+ "MPEG7_Edge_Histogram39, " +

					"MPEG7_Edge_Histogram40,  " + "MPEG7_Edge_Histogram41, " + "MPEG7_Edge_Histogram42, "
					+ "MPEG7_Edge_Histogram43, " + "MPEG7_Edge_Histogram44, " + "MPEG7_Edge_Histogram45, "
					+ "MPEG7_Edge_Histogram46, " + "MPEG7_Edge_Histogram47, " + "MPEG7_Edge_Histogram48, "
					+ "MPEG7_Edge_Histogram49, " +

					"MPEG7_Edge_Histogram50,  " + "MPEG7_Edge_Histogram51, " + "MPEG7_Edge_Histogram52, "
					+ "MPEG7_Edge_Histogram53, " + "MPEG7_Edge_Histogram54, " + "MPEG7_Edge_Histogram55, "
					+ "MPEG7_Edge_Histogram56, " + "MPEG7_Edge_Histogram57, " + "MPEG7_Edge_Histogram58, "
					+ "MPEG7_Edge_Histogram59, " +

					"MPEG7_Edge_Histogram60, " + "MPEG7_Edge_Histogram61, " + "MPEG7_Edge_Histogram62, "
					+ "MPEG7_Edge_Histogram63, " + "MPEG7_Edge_Histogram64, " + "MPEG7_Edge_Histogram65, "
					+ "MPEG7_Edge_Histogram66, " + "MPEG7_Edge_Histogram67, " + "MPEG7_Edge_Histogram68, "
					+ "MPEG7_Edge_Histogram69, " +

					"MPEG7_Edge_Histogram70, " + "MPEG7_Edge_Histogram71, " + "MPEG7_Edge_Histogram72, "
					+ "MPEG7_Edge_Histogram73, " + "MPEG7_Edge_Histogram74, " + "MPEG7_Edge_Histogram75, "
					+ "MPEG7_Edge_Histogram76, " + "MPEG7_Edge_Histogram77, " + "MPEG7_Edge_Histogram78, "
					+ "MPEG7_Edge_Histogram79,  " +

					"recording_id,  " + "start_time_seconds,  " + "duration_seconds,  " + "device_super_name,  "
					+ "device_name,  " + "recordingDateTime,  " + "actual_confirmed   " +
					
					"FROM onsets " +

					"WHERE MPEG7_Edge_Histogram0 IS NOT NULL " +
					
					"AND NOT EXISTS ( " +
						// Don't reclassify onsets that have already been classified for this modelRunName
						"SELECT ID FROM model_run_result WHERE modelRunName = ? AND model_run_result.recording_id = onsets.recording_id AND model_run_result.startTime = onsets.start_time_seconds AND model_run_result.duration = onsets.duration_seconds) " +

					"ORDER BY recording_id DESC";

			ArrayList<Attribute> attributes = new ArrayList<Attribute>();

			for (int i = 0; i < 80; i++) {
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

			Instances data = new Instances(modelRunName, attributes, 0);
			data.setClassIndex(data.numAttributes() - 1);

			CostSensitiveClassifier myModel = (CostSensitiveClassifier) weka.core.SerializationHelper.read(modelName);

//			ResultSet rs = stmt.executeQuery(sql);
			PreparedStatement pstmt  = conn.prepareStatement(sql);
        	pstmt.setString(1,modelRunName); 
        	ResultSet rs    = pstmt.executeQuery();  

			// loop through the result set
			int processedSoFar = 0;
			while (rs.next()) {
				processedSoFar++;

				int recording_id = rs.getInt("recording_id");
				double start_time_seconds = rs.getDouble("start_time_seconds");
				double duration_seconds = rs.getDouble("duration_seconds");
				String device_super_name = rs.getString("device_super_name");
				String device_name = rs.getString("device_name");
				String recordingDateTime = rs.getString("recordingDateTime");
				String actual_confirmed = rs.getString("actual_confirmed");

				double[] vals = new double[data.numAttributes()];

				for (int i = 0; i < 80; i++) {
					vals[i] = rs.getInt(i + 1);
				}

				vals[80] = deviceSuperNameLabels.indexOf(device_super_name);
				vals[81] = classLabels.indexOf("music"); // Seems you need to give it any class name

				Instance instanceToClassify = new DenseInstance(1.0, vals);
				instanceToClassify.setDataset(data);

//				System.out.println(instanceToClassify);

				int result = (int) myModel.classifyInstance(instanceToClassify);
				String predictedByModel = classLabels.get(result);

				double probablility = myModel.distributionForInstance(instanceToClassify)[result];

				System.out.println(result + "," + predictedByModel + "," + probablility);

				// Now update database model_run_result

				String sql2 = "INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime) VALUES(?,?,?,?,?,?,?,?,?,?)";

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

					pstmt2.executeUpdate();
					
					if (processedSoFar % 1000 == 0) {						
						System.out.println("Have processed " + processedSoFar);
						System.out.println("\n\n");
					}
				} catch (SQLException e) {
					System.out.println(e.getMessage());
				}

			}

			conn.close();
			System.out.println("Finished");

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
