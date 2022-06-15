import yaml
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from logger import App_Logger

file_object=open("Training_Logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data(config_path):
    config = read_params(config_path)
    train_data_path=config["split_data"]["train_path"]
    test_data_path=config["split_data"]["test_path"]
    source_data_path=config["data_source"]["source"]
    split_ratio=config["split_data"]["text_size"]
    random_state=config["base"]["random_state"]

    try:
       df=pd.read_csv(source_data_path)
       data= df.filter(['TSH','FTI','TT4','T3','query_hypothyroid','on_thyroxine','sex','pregnant','psych','Class'])
       train,test=train_test_split(data,test_size=split_ratio,random_state=random_state)
       train.to_csv(train_data_path,index=False)
       test.to_csv(test_data_path,index=False)
       logger_object.log(file_object,'Data is splitted and get_data done successfully')

    except Exception as e:
       logger_object.log(file_object,'Exception occurred in get_data. Exception message: '+str(e))
       logger_object.log(file_object,'get_data unsuccessful')
       raise Exception()

if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=get_data(config_path=parsed_args.config)