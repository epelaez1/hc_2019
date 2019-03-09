from datetime import datetime


class PersonalLogger():


    @staticmethod
    def _print_log(type_: str, msg: str):
        timestamp = datetime.now().ctime()
        text = "{0}  {1}:  {2}".format(
                                        timestamp,
                                        type_,
                                        msg
                                        )
        print(text)

    @staticmethod
    def start(conditions: str = "", msg: str = ""):
        text = "Starting application"
        if msg:
            text += " {} || ".format(msg)
        if conditions:
            text += " {}".format(conditions)

        PersonalLogger._print_log(type_= "INIT", msg= text)
    
    @staticmethod
    def progress_msg(msg:str):
        PersonalLogger._print_log(type_="PROGRESS", msg= msg)
    
    @staticmethod
    def event_msg(msg:str):
        PersonalLogger3ants._print_log(type_="EVENT", msg= msg)

    @staticmethod
    def warning(msg:str):
        PersonalLogger._print_log(type_="WARNING", msg= msg)

    @staticmethod
    def debug(msg:str):
        if True:
            PersonalLogger._print_log(type_="DEBUG", msg=msg)

    @staticmethod
    def error(msg: str):
        PersonalLogger._print_log(type_="ERROR", msg= msg)
    
    @staticmethod
    def finish(results: list, msg:str):
        PersonalLogger._print_log(type_ = "FINISHED", msg=msg)
        for result in results:
            PersonalLogger._print_log(type_ = "RESULT", msg = result)            
