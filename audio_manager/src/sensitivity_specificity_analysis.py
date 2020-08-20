'''
Created on 19 Aug. 2020

@author: tim
'''

import functions
import math


MODEL_RUN_NAME = "2020_08_18a"



def copy_model_run_results_to_sensitivity_specificity_table(MODEL_RUN_NAME):
        # 1)Get all predictions (morepork and other) from model_run_results    
    model_run_results = functions.get_model_run_results_simple(MODEL_RUN_NAME)
     
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
             
        cur = functions.get_database_connection().cursor() 
        sql = ''' INSERT INTO sensitivity_specificity (modelRunName, recording_id, predicted_startTime, predicted_duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur.execute(sql, (MODEL_RUN_NAME, recording_id, predicted_startTime, predicted_duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination))
        functions.get_database_connection().commit()
           
def get_determination_count(determination_type):
    cur = functions.get_database_connection().cursor() 
    cur.execute("SELECT COUNT(*) from sensitivity_specificity WHERE modelRunName = ? AND determination = ?", (MODEL_RUN_NAME, determination_type)) 
   
    determination_count = cur.fetchall()
    
    return determination_count[0][0]

def calculate_statistics():
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
    print("Sensitivity, recall, hit rate, or true positive rate (TPR) ", round(TPR,4))
    
    TNR = TN / (TN + FP)
    print("specificity, selectivity or true negative rate (TNR) ", round(TNR,4))
    
    PPV = TP / (TP + FP)
    print("precision or positive predictive value (PPV) ", round(PPV,4))
    
    NPV = TN / (TN + FN)
    print("negative predictive value (NPV) ", round(NPV,4))
    
    FNR = FN / (FN + TP)
    print("miss rate or false negative rate (FNR) ", round(FNR,4))
    
    FPR = FP / (FN + TN)
    print("fall-out or false positive rate (FPR) ", round(FPR,4))
    
    FDR = FP / (FP + TP)
    print("false discovery rate (FDR) ", round(FDR,4))
    
    FOR = FN / (FN + TN)
    print("false omission rate (FOR) ", round(FOR,4))
    
    PT = (math.sqrt(TPR * (-TNR + 1)) + TNR - 1)/(TPR + TNR - 1)
    print("Prevalence Threshold (PT) ", round(PT,4))
    
    TS = TP / (TP + FN + FP)
    print("Threat score (TS) or critical success index (CSI) ", round(TS,4))
    
    ACC = (TP + TN)/(TP + TN + FP + FN)
    print("Accuracy (ACC) ", round(ACC,4))
    
    BA = (TPR + TNR)/2
    print("balanced accuracy (BA) ", round(BA,4))
    
    F1_score = (2 * TP)/(2 * TP + FP + FN)
    print("F1 score ", round(F1_score,4))
    
    MCC = (TP * TN - FP * FN)/(math.sqrt((TP + FP)*(TP + FN)*(TN + FP)*(TN + FN)))
    print("Matthews correlation coefficient (MCC) ", round(MCC,4))
    
    FM = math.sqrt(PPV*TPR)
    print("Fowlkes–Mallows index (FM) ", round(FM,4))
    
    BM = TPR + TNR - 1
    print("informedness or bookmaker informedness (BM) ", round(BM,4))
    
    MK = PPV + NPV - 1
    print("markedness (MK) or deltaP ", round(MK,4))


def part_1():
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
    march_2020_test_data = functions.get_march_2020_test_data_for_like_morepork()
    
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
        overlap, ID, predictedByModel   = functions.does_test_data_overlap_a_morepork_prediction(MODEL_RUN_NAME, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds)
        
        cur = functions.get_database_connection().cursor()
        if overlap:
            if predictedByModel == 'morepork_more-pork':
                determination = 'true_positive'   
                sql = "UPDATE sensitivity_specificity SET determination = ?, test_data_start_time_seconds = ?, test_data_finish_time_seconds = ?, test_data_what = ?  WHERE ID = ?"
                cur.execute(sql, (determination, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, ID,))        
                functions.get_database_connection().commit() 
            
            # 3c)     else if it matches an 'other' prediction ### It will be other as predictions are just morepork or other
            else:        
            
                # 3d)          if the test data is a morepork (ignore the maybe_porks and part_morepork) update the entry to be False Negative
                if test_data_what == 'morepork_more-pork':
                    determination = 'false_negative' 
                    sql = "UPDATE sensitivity_specificity SET determination = ?, test_data_start_time_seconds = ?, test_data_finish_time_seconds = ?, test_data_what = ?  WHERE ID = ?"
                    cur.execute(sql, (determination, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, ID,))        
                    functions.get_database_connection().commit()
        
        
        # 3e)     else if it doesn't overlap a prediction, and JUST for the morepork (not the maybe_morepork or part_morepork) write a new entry to the database as a False Negative
        else:
            if test_data_what == 'morepork_more-pork':
                determination = "false_negative"
                sql = ''' INSERT INTO sensitivity_specificity (modelRunName, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination)
                    VALUES(?,?,?,?,?,?,?,?,?,?) '''
                cur.execute(sql, (MODEL_RUN_NAME, recording_id, test_data_start_time_seconds, test_data_finish_time_seconds, test_data_what, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ, determination))
                functions.get_database_connection().commit()
                
    print("Finished Processing")

def run():
    
#     part_1()      
    calculate_statistics()
                

run()