from flask import request
from flask import make_response
import pandas as pd
from pandas.io.json import json_normalize
from io import BytesIO

from flask import Flask
app = Flask(__name__)


@app.route('/excel', methods=['POST'])
def excel():
    '''Basically takes a nested json object list and produces an excel out of it
    For best results, its best for the nested object not to contain lists
    Internally, this function makes use of json_normalize
    '''
    output = BytesIO()
    filename = request.headers.get('filename', 'excel.xlsx')
    data = request.get_json()
    if len(data) > 0:
        df = json_normalize(data)
    else:
        meta = data[0].keys()
        df = json_normalize(data, meta=meta)
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    xlsx_data = output.getvalue()
    response = make_response(xlsx_data)
    response.headers.set('Content-Type', 'application/vnd.ms-excel')
    response.headers.set('Content-Disposition',
    'attachment; filename=%s.xlsx' % filename)
    return response


@app.route('/csv', methods=['POST'])
def csv():
    '''Basically takes a nested json object list and produces an csv out of it
    For best results, its best for the nested object not to contain lists
    Internally, this function makes use of json_normalize
    '''
    output = BytesIO()
    filename = request.headers.get('filename', 'converted.csv')
    data = request.get_json()
    if len(data) > 0:
        df = json_normalize(data)
    else:
        meta = data[0].keys()
        df = json_normalize(data, meta=meta)
    df.to_csv(output, index=False)
    csv_data = output.getvalue()
    response = make_response(csv_data)
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set('Content-Disposition',
    'attachment; filename=%s.csv' % filename)
    return response
