from application_logging import logger
from Training_Raw_Data_Validation.rawValidate import Raw_Data_Validation
from Data_Transform_Training.DataTransformation import dataTransformation
from Data_Type_Validation_Insertion_Training.dataType_Validation import dBOperation

class train_validation:

    def __init__(self, path):
        self.log_file = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = logger.app_logger()
        self.raw_data = Raw_Data_Validation(path)
        self.dataTransform = dataTransformation()
        self.dBOperation = dBOperation()


    def train_validation(self):
        try:

            self.log_writer.log(self.log_file, 'Start of Validation on files!!')
            # extracting values from prediction schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns = self.raw_data.valuesFromSchema()
            # getting the regex defined to validate filename
            regex = self.raw_data.manualRegex()
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            # validating column length in the file
            self.raw_data.validateColumnLength(NumberofColumns)
            # validating if any column has all values missing
            self.raw_data.validateMissingValueInWholeColumn()
            self.log_writer.log(self.log_file, "Raw Data Validation Complete!!")
            # starting Tranformation

            self.log_writer.log(self.log_file, "Starting Data Transformation !!")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.log_file, "Data Transformation Completed!!")

            self.log_writer.log(self.log_file,  "Creating Training_Database and tables on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb('Training', 'Good Data')
            self.log_writer.log(self.log_file, "Table creation Completed!!")
            self.log_writer.log(self.log_file, "Insertion of Data into Table started!!!!")
            # insert csv files in the table
            self.dBOperation.insertIntoTableGoodData('Training', 'Good Data')
            self.log_writer.log(self.log_file, "Insertion in Table completed!!!")
            self.log_writer.log(self.log_file, "Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.log_file, "Good_Data folder deleted!!!")
            self.log_writer.log(self.log_file, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.log_file, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.log_file, "Validation Operation completed!!")
            self.log_writer.log(self.log_file, "Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Training', 'Good Data')
            self.log_file.close()

        except Exception as e:
            print(e)
            raise e










