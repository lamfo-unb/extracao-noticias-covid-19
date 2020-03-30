# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:35:05 2020

@author: piphi
"""
from datetime import datetime
import os.path
import traceback


class Error_Logger:
    """
    This Error_Logger class logs whenever the main program starts and any scraper errors encountered 
    """
    
    def __init__(self, output_file): 
        self.path = output_file
        # creates new file if output file doesn't exist
        if not os.path.isfile(self.path):
            with open(self.path, "w+") as file:
                file.write("Logger File")     
    def _get_timestamp(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
    def log_error(self, name, e):
        with open(self.path, "a") as file:
            file.write("\n" + name + " failed at: " + self._get_timestamp() + "\n")
            for line in traceback.format_exception(type(e), e, e.__traceback__):
                file.write(line)
                
            file.write("--------------------")
    def start_log(self):
        with open(self.path, "a") as file:
            file.write("\nBegan logging at: " + self._get_timestamp() + "\n")
            file.write("--------------------")
        
    def end_log(self):
        with open(self.path, "a") as file:
            file.write("\nEnded Logging at: " + self._get_timestamp() + "\n")
            file.write("--------------------")

