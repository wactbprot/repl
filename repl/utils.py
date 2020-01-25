import json
import datetime
import requests
from urllib.parse import urlparse

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
    

def get_jobs(server, port):
    try:
        req = requests.get("http://{}:{}/_scheduler/jobs".format(server, port))
        return req.json().get("jobs", [])
    except:
        return []

def gen_count():
    i = 0
    while True:
        yield i
        i = i + 1
    
def get_info(url):
    p = urlparse(url)
    db = p.path.replace("/","")
    host = p.hostname.split(".")[0]
    return db, host

def gen_ext_name(d, h):
    return "{}@{}".format(d, h)

def get_nodes_and_edges(jobs, gen, hosts, dbs):
    nodes = []
    edges = []
    idx = 0
    for job in jobs:
        s = job.get("source")
        t = job.get("target")
        if s and t:
            s_db, s_host = get_info(s)
            t_db, t_host = get_info(t)
            s_ext_db_name = gen_ext_name(s_db, s_host)
            t_ext_db_name = gen_ext_name(t_db, t_host)

            if s_host not in hosts:
                hosts[s_host] = gen.__next__()
                nodes.append({"id": hosts[s_host], "label": s_host, "group": "server" })
                 
            if t_host not in hosts:
                hosts[t_host] = gen.__next__()
                nodes.append({"id": hosts[t_host], "label": t_host, "group": "server"})

            if s_ext_db_name not in dbs:
                dbs[s_ext_db_name] = gen.__next__()
                nodes.append({"id": dbs[s_ext_db_name], "label": s_db, "group": "db"})

            if t_ext_db_name not in dbs:
                dbs[t_ext_db_name] = gen.__next__()
                nodes.append({"id": dbs[t_ext_db_name], "label": t_db, "group": "db"})
                
                
            edges.append({"from": dbs[s_ext_db_name] , "to":dbs[t_ext_db_name] , "arrow_type": "to"})
            edges.append({"from": hosts[s_host] , "to":dbs[s_ext_db_name], "arrow_type":"box"})
            edges.append({"from": hosts[t_host] , "to":dbs[t_ext_db_name], "arrow_type":"box"})

    return nodes, edges