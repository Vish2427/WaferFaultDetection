import shutil
import pymongo
from datetime import datetime
from os import listdir
import os
import csv
from application_logging.logger import app_logger
import pandas as pd
import json

class dBOperation:
    """
    This class shall be used for handling all the DB operations
    """
    def __init__(self):
        self.path = 'Prediction_Database/'
        self.badFilePath = "Prediction_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Prediction_Raw_files_validated/Good_Raw"
        self.url = "mongodb+srv://mongodb:mongodb@practice.lgq8z4v.mongodb.net/?retryWrites = true&w = majority"
        self.logger = app_logger()

    def dataBaseConnection(self):
        """
        Method Name: dataBaseConnection
        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
        Output: Connection to the DB
        On Failure: Raise ConnectionError
        """
        try:
            mongo_client = pymongo.MongoClient(self.url)
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Connected to mongo_client successfully" )
            file.close()
        except ConnectionError:
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to mongoDB: %s" % ConnectionError)
            file.close()
            raise ConnectionError

        return mongo_client

    def createDataBase(self, DatabaseName):
        """
        Method Name : createDataBase
        Description : This method creates database which will use to insert Good collection
        :return: Data Base created
        On Failure: Raise Exception
        """
        try:
            cnn = self.dataBaseConnection()
            database = cnn[DatabaseName]
            cnn.close()
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "%s database created successfully" % DatabaseName)
            file.close()
            return database
        except Exception as e:
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while creating database: %s" % Exception)
            file.close()
            raise Exception

    def createTableDb(self, DatabaseName, Good_Raw_Data):
        """
        Method Name: createTableDb
        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
        :return:  None
        On Failure: Raise Exception

        """
        conn = self.dataBaseConnection()
        try:

            database = conn[DatabaseName]
            if Good_Raw_Data in database.list_collection_names():
                database[Good_Raw_Data].drop()
                collection = database[Good_Raw_Data]
                conn.close()
                file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "%s created successfully!!" % collection)
                file.close()

                file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
            else:
                collection = database[Good_Raw_Data]
                conn.close()

                file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "%s created successfully!!" % collection)
                file.close()

                file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e


    def getcollection(self, DatabaseName, Good_Raw_Data):
        """
        Method Name : getcollection
        Description: This method gets the collection/table from DB

        """


    def insertIntoTableGoodData(self, DatabaseName, Good_Raw_Data):
        """
        Method Name: insertIntoTableGoodData
        Description: This method inserts the Good data files from the Good_Raw folder into the
                     above created table.
        :return:  None
        On Failure: Raise Exception

        """
        conn = self.dataBaseConnection()
        database = conn[DatabaseName]
        collection = database[Good_Raw_Data]
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                df=pd.read_csv(goodFilePath+'/'+file)
                dataframe_dict = json.loads(df.T.to_json())
                try:
                    collection.insert_many(list(dataframe_dict.values()))
                    self.logger.log(log_file, " %s: File loaded successfully!!" % file)
                except Exception as e:
                    raise e

            except Exception as e:

                self.logger.log(log_file, "Error while creating table: %s " % e)
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()

        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, DatabaseName, Good_Raw_Data):
        """
        Method Name: selectingDatafromtableintocsv
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
                     above created .
        Output: None
        On Failure: Raise Exception

        """
        self.fileFromDb = 'Prediction_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')

        try:
            conn = self.dataBaseConnection()
            database = conn[DatabaseName]
            collection = database[Good_Raw_Data]
            allresult = collection.find()

            # Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Write to CSV file
            result = pd.DataFrame(allresult)
            result1 = result.drop(columns='_id')
            result1.to_csv(self.fileFromDb + self.fileName, index=False)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()







