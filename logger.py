#class for loger file
file_object= open('Logger.txt','w')
from datetime import datetime


class app_logger:
    def __init__(self):
        pass

    def log(self,file_object,log_message):
        self.now=datetime.now()
        self.date=self.now.date()
        self.current_time=self.now.strftime("%H:%M:%S")
        file_object.write(str(self.date)+"/"+ str(self.current_time)+"\t\t"+ log_message +"\n" )