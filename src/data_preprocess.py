import os
import numpy as np
import yaml
import pandas as pd
import argparse
from sklearn.impute import KNNImputer
from logger import App_Logger

file_object=open("Training_Logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def preprocessing(config_path):
    config = read_params(config_path)
    train_data_path=config["split_data"]["train_path"]
    test_data_path=config["split_data"]["test_path"]
    train_processed_path=config["processed"]["train_path"]
    test_processed_path=config["processed"]["test_path"]

    train_data=pd.read_csv(train_data_path)
    test_data=pd.read_csv(test_data_path)

#"?" is replaced with nan in train data
    try:
       for column in train_data.columns:
           count = train_data[column][train_data[column]=='?'].count()
           if count!=0:
               train_data[column] = train_data[column].replace('?',np.nan)
 
       for column in train_data.columns:
           if len(train_data[column].unique())==2:
               train_data[column] = train_data[column].replace({'f' : 0, 't' : 1})
           elif len(train_data[column].unique())==1:
               train_data[column] = train_data[column].replace({'f' : 0})

       train_data["sex"]=train_data["sex"].replace({'F' : 0, 'M' : 1})

       train_data['Class'] = train_data['Class'].replace({'negative' : 0,'compensated_hypothyroid' : 1,'primary_hypothyroid' : 2, 'secondary_hypothyroid': 3})
       train_data["Class"] = train_data["Class"].apply(lambda value : 1 if value >=1 else 0) 

       imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
       new_array=imputer.fit_transform(train_data)
       train_impu_data=pd.DataFrame(data=np.round(new_array),columns=train_data.columns)
       train_impu_data.to_csv(train_processed_path,index=False)
       logger_object.log(file_object,'Preprocessing successful for train data')
    
    
#"?" is replaced with nan in test data
    
       for column in test_data.columns:
           count = test_data[column][test_data[column]=='?'].count()
           if count!=0:
               test_data[column] = test_data[column].replace('?',np.nan)
 
       for column in test_data.columns:
           if len(test_data[column].unique())==2:
              test_data[column] = test_data[column].replace({'f' : 0, 't' : 1})
           elif len(test_data[column].unique())==1:
               test_data[column] = test_data[column].replace({'f' : 0})

       test_data["sex"]=test_data["sex"].replace({'F' : 0, 'M' : 1})

       test_data['Class'] = test_data['Class'].replace({'negative' : 0,'compensated_hypothyroid' : 1,'primary_hypothyroid' : 2, 'secondary_hypothyroid': 3})
       test_data['Class'] = test_data['Class'].apply(lambda value : 1 if value >=1 else 0) 

       imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
       new_array=imputer.fit_transform(test_data)
       test_impu_data=pd.DataFrame(data=np.round(new_array),columns=test_data.columns)
       test_impu_data.to_csv(test_processed_path,index=False) 
       logger_object.log(file_object,'Preprocessing successful for test data')

    except Exception as e:
       logger_object.log(file_object,'Exception occurred in preprocessing. Exception message: '+str(e))
       logger_object.log(file_object,'Data preprocessing unsuccessful')
       raise Exception()

if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=preprocessing(config_path=parsed_args.config)