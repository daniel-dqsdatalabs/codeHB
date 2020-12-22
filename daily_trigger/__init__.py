
#==============================================================================
# filename          : __init__.py
# description       : download json file
# author            : daniel
# email             : daniel@dqsdatalabs.com
# date              : 19/12/2020
# version           : 0.01
#==============================================================================

import os
import sys
import time
import json
import logging
import requests
import itertools
import functools
import pandas as pd
from datetime import datetime

import azure.functions as func
from azure.storage.blob import ContainerClient

DAY = str(datetime.today().day).zfill(2)
YEAR = str(datetime.today().year).zfill(4)
MONTH = str(datetime.today().month).zfill(2)

BASE_URL = 'https://dadosabertos.poa.br'
NEXT_URL = '/api/3/action/datastore_search?offset=0&resource_id=5579bc8e-1e47-47ef-a06e-9f08da28dec8'

APP_STR = os.environ['AzureWebJobsStorage']

def process_request(next_url, result):
    '''
        recursivelly iterate over pages
    '''
    headers = { 
        'User-Agent': 'curl/7.58.0',
        'accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    
    logging.info('url: %s', next_url)
    r = requests.get(next_url, headers=headers).json()
    
    if len(r["result"]["records"]) > 0:
        result.append(r["result"]["records"])
        process_request(BASE_URL + r["result"]["_links"]["next"], result)
        
    return result


def save_json_file(result_json):
    '''
        save the json file
    ''' 
    container_client = ContainerClient.from_connection_string(
        conn_str=APP_STR,
        container_name='results/{}/{}/{}'.format(YEAR, MONTH, DAY)
    )
    
    filename = "lista_escolas_{ts}.json".format(
        ts=datetime.now().timestamp()
    )
    
    container_client.upload_blob(
        name=filename,
        data=(json.dumps(result_json, ensure_ascii=False)),
        blob_type="BlockBlob"
    )

    logging.info('Json salvo com sucesso...')
        
        
def flatten_results(result_list):
    '''
        flattening the results
    '''
    return functools.reduce(lambda x,y: x + y, result_list)


def process_results():
    '''
        process results
    '''
    result = []
    r = process_request(BASE_URL + NEXT_URL, result)
    if r is not None: result.append(flatten_results(r))
    result_json =  {"escolas":  flatten_results(result)}
    save_json_file(result_json)

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.perf_counter()
    logging.info('processamento iniciado em: %s', datetime.now())
    try:
        process_results()
        return json.dumps({'status_code': 200})
    except Exception:
        return func.HttpResponse(Exception.message, status_code=500)
    duration = time.perf_counter() - start
    logging.info('tempo de processamento: %s', duration)