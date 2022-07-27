import pandas as pd

class Data_Getter:
    """
    This class shall  be used for obtaining the data from the source for training.

    """
    def __init__(self, log_file, logger_object):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.log_file = log_file
        self.logger_object = logger_object

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

        """
        self.logger_object.log(self.log_file, 'Entered the get_data method of the Data_Getter class')
        try:
            self.data= pd.read_csv(self.training_file) # reading the data file
            self.logger_object.log(self.log_file, 'Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.log_file, 'Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            self.logger_object.log(self.log_file, 'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')

            raise Exception()