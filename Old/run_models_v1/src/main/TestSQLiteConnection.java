package main;

import java.sql.Connection;  
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;  

public class TestSQLiteConnection {
	
	public static Connection connect() {  
        Connection conn = null;  
        try {  
            // db parameters  
//            String url = "jdbc:sqlite:C:/sqlite/JTP.db";  
        	String url = "jdbc:sqlite:/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db2.db";
            // create a connection to the database  
            conn = DriverManager.getConnection(url);  
              
            System.out.println("Connection to SQLite has been established.");  
            
              
        } catch (SQLException e) {  
            System.out.println(e.getMessage());  
        } 
		return conn;  
    }  
	
	public static void selectAll(){  
//        String sql = "SELECT * FROM onsets";  
//		 cur.execute("UPDATE recordings SET processed_for_onsets = 1 WHERE recording_id = ?", (recording_id,))  
        String sql = "UPDATE onsets SET version = 999 WHERE ID = 3939"; 
          
        try {  
            Connection conn = connect();  
            Statement stmt  = conn.createStatement();  
            ResultSet rs    = stmt.executeQuery(sql);  
              
//            // loop through the result set  
//            while (rs.next()) {  
//                System.out.println(rs.getInt("ID") +  "\t" +   
//                                   rs.getString("recording_id") + "\t" +  
//                                   rs.getString("device_name"));  
            
            conn.close();
            System.out.println("Finished");
             
        } catch (SQLException e) {  
            System.out.println(e.getMessage());  
        }  
    }  

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		 connect();
		 selectAll();
		 
		 
	}

}
