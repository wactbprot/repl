import json
import datetime

def get_config_dict():
    ## sollte vielleicht doch xml-datei werden
    with open('./config.json') as json_config_file:
        config = json.load(json_config_file)

    return config

def path_file(path, file):
    return "{path}/{file}".format(path=path, file=file)

def get_current_year(short=False):
    y = "{}".format(datetime.datetime.today().year)
    if short:
        return y[-2:]
    else:
        return y

def get_current_date(short=False):
    return   "{}".format(datetime.datetime.today().date())
    
