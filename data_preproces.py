import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from logger import app_logger

class preprocessing:
    def __init__(self):
        self.logger=app_logger()

    def preprocessing(self,data,file_name):
        '''' data preprocessing  replaceing ? value with the null value using np.nan after that labeled the columns 
        if there is less than 5 categories is avaibler 
    data : enter the load data file

    file_name : when we preprocess has done so data save with the file_name'''
        file_object=open('logger.txt','a')
        try: 
            for row in data.columns:
                count=len(data[row][data[row]=="?"])
                
                if count!=0:
                    data[row]=data[row].replace('?',np.nan)
            self.logger.log(file_object,"all ? replaced by the np.nan value")
                
            # all data conver to labels
            for row in data.columns:
                t=data[row].unique()
                if len(t)==2:
                    data[row]=data[row].replace({t[0]:0,t[1]:1})
                elif len(t)==3:
                    data[row]=data[row].replace({t[0]:0,t[1]:1,t[2]:2})
                elif len(t)==4:
                    data[row]=data[row].replace({t[0]:0,t[1]:1,t[2]:2,t[3]:3})
                elif len(t)==5:
                    data[row]=data[row].replace({t[0]:0,t[1]:1,t[2]:2,t[3]:3,t[4]:4})
                else:
                    pass
                new_data=data
            self.logger.log(file_object,'All data convert into labes')
            
            #replaceing all nan value with imputer
            imputer=KNNImputer(n_neighbors=5, weights='uniform',missing_values=np.nan)
            new_arry=imputer.fit_transform(data)
            data_input_data=pd.DataFrame(data=np.round(new_arry),columns=data.columns)
            data_input_data.to_csv(file_name,index=False)
            self.logger.log(file_object,'all np.nan value filled using KNNimputer')
        except Exception as e:
            self.logger.log(file_object,'error '+ str(e))
            raise Exception()
        