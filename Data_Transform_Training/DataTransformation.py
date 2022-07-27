from os import listdir
from application_logging.logger import app_logger
import pandas

class dataTransformation:
    """
    This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
    """

    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = app_logger()

    def replaceMissingWithNull(self):
        """
        Method Name: replaceMissingWithNull
        Description: This method replaces the missing values in columns with "NULL" to
                    store in the table. We are using substring in the first column to
                    keep only "Integer" data for ease up the loading.
                    This column is anyways going to be removed during training.

        :return: None
        """
        log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pandas.read_csv(self.goodDataPath + "/" + file)
                csv.fillna('NULL', inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)
        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
        log_file.close()

