import os
import yaml
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix
import joblib
from logger import App_Logger

file_object=open("Training_Logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def train_test(config_path):
    config = read_params(config_path)
    train_class_path=config["balanced_data"]["train_class"]
    train_label_path=config["balanced_data"]["train_label"]
    test_class_path=config["balanced_data"]["test_class"]
    test_label_path=config["balanced_data"]["test_label"]
    report_path=config["metrics"]["report"]
    
    train_class=pd.read_csv(train_class_path)
    train_label=pd.read_csv(train_label_path)
    test_class=pd.read_csv(test_class_path)
    test_label=pd.read_csv(test_label_path)
 
    try:
       model=RandomForestClassifier(n_estimators=150,
                                criterion="gini",
                                max_depth=10)
    
       model.fit(train_label,train_class)
       logger_object.log(file_object,'model is fitted')
    
       # Metrics (Classification_report)

       y_pred=model.predict(test_label)
    
       cl_report=pd.DataFrame(classification_report(test_class, y_pred, output_dict=True)).transpose()
       cl_report.to_csv(report_path,index=True)
       logger_object.log(file_object,'Classification report done')

       joblib.dump(model,open("models/model.pkl", 'wb'))
       logger_object.log(file_object,'Saved as model.pkl successfully')
    
    except Exception as e:
       logger_object.log(file_object,'Exception occurred in train_test. Exception message: '+str(e))
       logger_object.log(file_object,'train_test unsuccessful')
       raise Exception()


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=train_test(config_path=parsed_args.config)