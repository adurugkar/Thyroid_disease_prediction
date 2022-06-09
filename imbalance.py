import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from logger import app_logger

class balance:
    def __init__(self):
        self.logger=app_logger()

    def balance_imbal(self,x,y):
        '''doing balance the unbalance data
    x : is a independent variable

    y : is dependent variable'''
        file_object=open('logger.txt','a')
        try:
            x_train,x_test,y_train,y_test=train_test_split(x,y, train_size=0.8, shuffle=True, random_state=123)
            ros=RandomOverSampler(sampling_strategy='all')
            x_train_res,y_train_res=ros.fit_resample(x_train,y_train)
            x_train_res.to_csv('balance_x_train',index=False)
            y_train_res.to_csv('balance_y_train',index=False)

            x_test_res, y_test_res = ros.fit_resample(x_test,y_test)
            x_test_res.to_csv("balance_x_test",index=False)
            y_test_res.to_csv("balance_y_test",index=False)
            self.logger.log(file_object,'now data is balanced')
            self.logger.log(file_object,'balance train file save with name "balance_x_train","balance_y_train"')
            
        except Exception as e:
            self.logger.log(file_object,'error occure'+str(e))
            raise Exception()