from datetime import datetime

class app_logger:
    def __init__(self):
        pass


    def log(self, log_file, log_message):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        log_file.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message + "\n")



