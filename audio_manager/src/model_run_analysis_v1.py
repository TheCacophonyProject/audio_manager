'''
Created on 19 Aug. 2020

@author: tim
'''

# import functions
import math
import sqlite3
from sqlite3 import Error



MODEL_RUN_NAME = "2020_10_06a_vgg16_lr0.0004_multi_class"
db_file = "/media/tim/HDD1/Work/Cacophony/audio_analysis/audio_analysis_db3_testing.db"

conn = None

def get_database_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    # https://stackoverflow.com/questions/8587610/unboundlocalerror-local-variable-conn-referenced-before-assignment
    global conn
    if conn is None:
        try:
            conn = sqlite3.connect(db_file)           
        except Error as e:
            print(e)
  
    return conn    

def does_test_data_overlap_a_morepork_prediction(modelRunName, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds):
    
    cur = get_database_connection().cursor()
#     cur.execute("SELECT ID, modelRunName, recording_id, predicted_startTime, predicted_duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination from sensitivity_specificity WHERE modelRunName = ? AND recording_id = ? AND predictedByModel IS NOT NULL", (modelRunName, recording_id)) # predictedByModel IS NOT NULL to just check against predictions
    cur.execute("SELECT ID, modelRunName, recording_id, predicted_startTime, predicted_duration, predictedByModel from sensitivity_specificity WHERE modelRunName = ? AND recording_id = ? AND predictedByModel IS NOT NULL", (modelRunName, recording_id)) # predictedByModel IS NOT NULL to just check against predictions
   
    sensitivity_specificity_results = cur.fetchall()
    overlap = False
    for sensitivity_specificity_result in sensitivity_specificity_results:
        ID = sensitivity_specificity_result[0]
        modelRunName = sensitivity_specificity_result[1]
        recording_id = sensitivity_specificity_result[2]
        predicted_startTime = sensitivity_specificity_result[3]
        predicted_duration = sensitivity_specificity_result[4]
        predictedByModel = sensitivity_specificity_result[5]
        
        predicted_endTime = predicted_startTime + predicted_duration
        
        if predicted_startTime > test_data_start_time_seconds and predicted_startTime < test_data_finish_time_seconds:
            overlap = True
            break
        elif predicted_endTime > test_data_start_time_seconds and predicted_endTime < test_data_finish_time_seconds:
            overlap = True
            break
    
    if overlap:   
        return overlap, ID, predictedByModel 
    else:
        return overlap, None, None 
    
def get_march_2020_test_data_for_like_morepork():
    cur = get_database_connection().cursor()
    cur.execute("SELECT recording_id, start_time_seconds, finish_time_seconds, what, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ from test_data WHERE what LIKE '%morepork%'")
    march_2020_test_data = cur.fetchall()
    return march_2020_test_data

def get_model_run_results_simple(model_run_name):        
    cur = get_database_connection().cursor()
    cur.execute("SELECT recording_id, startTime, duration, predicted_by_model, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ FROM model_run_result WHERE model_run_name = '" + model_run_name + "'") 
    model_run_results = cur.fetchall()    
    
    return model_run_results

def copy_model_run_results_to_sensitivity_specificity_table(MODEL_RUN_NAME):
        # 1)Get all predictions (morepork and other) from model_run_results    
    model_run_results = get_model_run_results_simple(MODEL_RUN_NAME)
     
    # 2) For each model_run_result, put morepork predictions into the sensitivity_specificity table as initially False Positive 
    count = 0
    number_of_results = len(model_run_results)
    for model_run_result in model_run_results:
        count+=1
        print("Processing ", count, " of ", number_of_results)
        recording_id = model_run_result[0]
        predicted_startTime = model_run_result[1]
        predicted_duration = model_run_result[2]
        predictedByModel = model_run_result[3]
        probability = model_run_result[4]
        device_super_name = model_run_result[5]
        device_name = model_run_result[6]
        recordingDateTime = model_run_result[7]
        recordingDateTimeNZ = model_run_result[8]
         
        # 2b) put morepork predictions into the sensitivity_specificity table as initially False Positive
        if predictedByModel == 'morepork_more-pork':
            determination = "false_positive"
             
        else:
            # 2c) and the other predictions into the sensitivity_specificity table as initially True Negatives
            determination = "true_negative"
             
        cur = get_database_connection().cursor() 
        sql = ''' INSERT INTO sensitivity_specificity (modelRunName, recording_id, predicted_startTime, predicted_duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur.execute(sql, (MODEL_RUN_NAME, recording_id, predicted_startTime, predicted_duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination))
        get_database_connection().commit()
           
def get_determination_count(determination_type):
    cur = get_database_connection().cursor() 
    cur.execute("SELECT COUNT(*) from sensitivity_specificity WHERE modelRunName = ? AND determination = ?", (MODEL_RUN_NAME, determination_type)) 
   
    determination_count = cur.fetchall()
    
    return determination_count[0][0]

def part_2_calculate_statistics():
#     https://en.wikipedia.org/wiki/Sensitivity_and_specificity
    TP = get_determination_count("true_positive")
    print("TP ", TP)
    
    TN = get_determination_count("true_negative")
    print("TN ", TN)
    
    FP = get_determination_count("false_positive")
    print("FP ", FP)
    
    FN = get_determination_count("false_negative")
    print("FN ", FN)
    
    
    
    TPR = TP / (TP + FN)   
    print("Sensitivity, recall, hit rate, or true positive rate, TPR = TP / (TP + FN) ", round(TPR,4))
    
    TNR = TN / (TN + FP)
    print("specificity, selectivity or true negative rate, TNR = TN / (TN + FP) ", round(TNR,4))
    
    PPV = TP / (TP + FP)
    print("precision or positive predictive value, PPV = TP / (TP + FP) ", round(PPV,4))
    
    NPV = TN / (TN + FN)
    print("negative predictive value, NPV = TN / (TN + FN) ", round(NPV,4))
    
    FNR = FN / (FN + TP)
    print("miss rate or false negative rate, FNR = FN / (FN + TP) ", round(FNR,4))
    
    FPR = FP / (FN + TN)
    print("fall-out or false positive rate, FPR = FP / (FN + TN) ", round(FPR,4))
    
    FDR = FP / (FP + TP)
    print("false discovery rate, FDR = FP / (FP + TP) ", round(FDR,4))
    
    FOR = FN / (FN + TN)
    print("false omission rate, FOR = FN / (FN + TN) ", round(FOR,4))
    
    PT = (math.sqrt(TPR * (-TNR + 1)) + TNR - 1)/(TPR + TNR - 1)
    print("Prevalence Threshold, PT = (math.sqrt(TPR * (-TNR + 1)) + TNR - 1)/(TPR + TNR - 1) ", round(PT,4))
    
    TS = TP / (TP + FN + FP)
    print("Threat score (TS) or critical success index (CSI), TS = TP / (TP + FN + FP) ", round(TS,4))
    
    ACC = (TP + TN)/(TP + TN + FP + FN)
    print("Accuracy, ACC = (TP + TN)/(TP + TN + FP + FN) ", round(ACC,4))
    
    BA = (TPR + TNR)/2
    print("balanced accuracy, BA = (TPR + TNR)/2 ", round(BA,4))
    
    F1_score = (2 * TP)/(2 * TP + FP + FN)
    print("F1_score = (2 * TP)/(2 * TP + FP + FN)  ", round(F1_score,4))
    
    MCC = (TP * TN - FP * FN)/(math.sqrt((TP + FP)*(TP + FN)*(TN + FP)*(TN + FN))) # https://en.wikipedia.org/wiki/Matthews_correlation_coefficient
    print("Matthews correlation coefficient, MCC = (TP * TN - FP * FN)/(math.sqrt((TP + FP)*(TP + FN)*(TN + FP)*(TN + FN))) ", round(MCC,4))
    
    FM = math.sqrt(PPV*TPR)
    print("Fowlkes–Mallows index, FM = math.sqrt(PPV*TPR) ", round(FM,4))
    
    BM = TPR + TNR - 1
    print("informedness or bookmaker informedness, BM = TPR + TNR - 1 ", round(BM,4))
    
    MK = PPV + NPV - 1
    print("markedness (MK) or deltaP, MK = PPV + NPV - 1 ", round(MK,4))


def part_1_copy_and_assign():
    # 1) Get all predictions (morepork and other) from model_run_results     
    
    # 2) For each model_run_result, 
    # 2b) put morepork predictions into the sensitivity_specificity table as initially False Positive 
    # 2c) and the other predictions into the sensitivity_specificity table as initially True Negatives
        
    # 3) Get all march 2020 test data for morepork and maybe_morepork and part_morepork (use SQL LIKE '%morepork%')
    # 3a) For each of these, 
    # 3b)     if it matches (overlaps) a morepork prediction then update the prediction to being a True Positive
    # 3c)     else if it matches an 'other' prediction 
    # 3d)          if the test data is a morepork (ignore the maybe_porks and part_morepork) update the entry to be False Negative
    # 3e)     else if it doesn't overlap a prediction, and JUST for the morepork (not the maybe_morepork or part_morepork) write a new entry to the database as a False Negative
    
    copy_model_run_results_to_sensitivity_specificity_table(MODEL_RUN_NAME)

    # 3) Get all march 2020 test data for morepork and maybe_morepork and part_morepork (use SQL LIKE '%morepork%')
    march_2020_test_data = get_march_2020_test_data_for_like_morepork()
    
    # 3a) For each of these, 
    count = 0
    number_of_rows = len(march_2020_test_data)
    for march_2020_test_datum in march_2020_test_data:
        count+=1
        print("Processing march_2020_test_data: ", count, " of ", number_of_rows)
        recording_id = march_2020_test_datum[0]
        test_data_start_time_seconds = march_2020_test_datum[1]
        test_data_finish_time_seconds = march_2020_test_datum[2]
        test_data_what = march_2020_test_datum[3]
        device_super_name = march_2020_test_datum[4]
        device_name = march_2020_test_datum[5]
        recordingDateTime = march_2020_test_datum[6]
        recordingDateTimeNZ = march_2020_test_datum[7]
        
        # 3b)     if it matches (overlaps) a morepork prediction then update the prediction to being a True Positive
        overlap, ID, predictedByModel   = does_test_data_overlap_a_morepork_prediction(MODEL_RUN_NAME, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds)
        
        cur = get_database_connection().cursor()
        if overlap:
            if predictedByModel == 'morepork_more-pork':
                determination = 'true_positive'   
                sql = "UPDATE sensitivity_specificity SET determination = ?, test_data_start_time_seconds = ?, test_data_finish_time_seconds = ?, test_data_what = ?  WHERE ID = ?"
                cur.execute(sql, (determination, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, ID,))        
                get_database_connection().commit() 
            
            # 3c)     else if it matches an 'other' prediction ### It will be other as predictions are just morepork or other
            else:        
            
                # 3d)          if the test data is a morepork (ignore the maybe_porks and part_morepork) update the entry to be False Negative
                if test_data_what == 'morepork_more-pork':
                    determination = 'false_negative' 
                    sql = "UPDATE sensitivity_specificity SET determination = ?, test_data_start_time_seconds = ?, test_data_finish_time_seconds = ?, test_data_what = ?  WHERE ID = ?"
                    cur.execute(sql, (determination, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, ID,))        
                    get_database_connection().commit()
        
        
        # 3e)     else if it doesn't overlap a prediction, and JUST for the morepork (not the maybe_morepork or part_morepork) write a new entry to the database as a False Negative
        else:
            if test_data_what == 'morepork_more-pork':
                determination = "false_negative"
                sql = ''' INSERT INTO sensitivity_specificity (modelRunName, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination)
                    VALUES(?,?,?,?,?,?,?,?,?,?) '''
                cur.execute(sql, (MODEL_RUN_NAME, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination))
                get_database_connection().commit()
                
    print("Finished Processing")

def run():
    
    part_1_copy_and_assign()     
     
#     part_2_calculate_statistics()
                

run()