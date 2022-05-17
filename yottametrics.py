import mg_python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
mg_python.m_set_host(0, os.environ.get('YOTTAADD'), int(os.environ.get('YOTTAPORT')), "", "")

@app.route('/CUM')
def get_cum_metrics():  
   limit=request.args.get('cnt')
   region=request.args.get('region') or "DEFAULT"
   if limit=="all":
      limit=1000000000000000000000000000000000
   try:
      limit=int(limit)
   except:
      limit=60
   cnt=0
   result = []   
   fields = [
            { "name": 'BTD', "type": "FieldType.number" },
            { "name": "CAT", "type": "FieldType.number" },
            { "name": "CFE", "type": "FieldType.number" },
            { "name": "CFS", "type": "FieldType.number" },
            { "name": 'CFT', "type": "FieldType.number" },
            { "name": 'CFavg', "type": "FieldType.number" },
            { "name": 'CFsigma', "type": "FieldType.number" },
            { "name": 'CFvar', "type": "FieldType.number" },
            { "name": 'CQS', "type": "FieldType.number" },
            { "name": 'CQT', "type": "FieldType.number" },
            { "name": 'CQAvg', "type": "FieldType.number" },
            { "name": 'CQsigma', "type": "FieldType.number" },
            { "name": 'CQvar', "type": "FieldType.number" },
            { "name": 'CTN', "type": "FieldType.number" },
            { "name": 'CYS', "type": "FieldType.number" },
            { "name": 'CYT', "type": "FieldType.number" },
            { "name": 'CYavg', "type": "FieldType.number" },
            { "name": 'CYsigma', "type": "FieldType.number" },
            { "name": 'CYvar', "type": "FieldType.number" },
            { "name": 'DEX', "type": "FieldType.number" },
            { "name": 'DFL', "type": "FieldType.number" },
            { "name": 'DFS', "type": "FieldType.number" },
            { "name": 'DRD', "type": "FieldType.number" },
            { "name": 'DTA', "type": "FieldType.number" },
            { "name": 'DWT', "type": "FieldType.number" },
            { "name": 'GET', "type": "FieldType.number" },
            { "name": 'JBB', "type": "FieldType.number" },
            { "name": 'JEX', "type": "FieldType.number" },
            { "name": 'JFB', "type": "FieldType.number" },
            { "name": 'JFL', "type": "FieldType.number" },
            { "name": 'JFS', "type": "FieldType.number" },
            { "name": 'JFW', "type": "FieldType.number" },
            { "name": 'JRE', "type": "FieldType.number" },
            { "name": 'JRI', "type": "FieldType.number" },
            { "name": 'JRL', "type": "FieldType.number" },
            { "name": 'JRO', "type": "FieldType.number" },
            { "name": 'JRP', "type": "FieldType.number" },
            { "name": 'KIL', "type": "FieldType.number" },
            { "name": 'LKF', "type": "FieldType.number" },
            { "name": 'LKS', "type": "FieldType.number" },
            { "name": 'LKfrate', "type": "FieldType.number" },
            { "name": 'NBR', "type": "FieldType.number" },
            { "name": 'NBW', "type": "FieldType.number" },
            { "name": 'NR0', "type": "FieldType.number" },
            { "name": 'NR1', "type": "FieldType.number" },
            { "name": 'NR2', "type": "FieldType.number" },
            { "name": 'NR3', "type": "FieldType.number" },
            { "name": 'NTR', "type": "FieldType.number" },
            { "name": 'NTW', "type": "FieldType.number" },
            { "name": 'ORD', "type": "FieldType.number" },
            { "name": 'QRY', "type": "FieldType.number" },
            { "name": 'SET', "type": "FieldType.number" },
            { "name": 'TBR', "type": "FieldType.number" },
            { "name": 'TBW', "type": "FieldType.number" },
            { "name": 'TC0', "type": "FieldType.number" },
            { "name": 'TC1', "type": "FieldType.number" },
            { "name": 'TC2', "type": "FieldType.number" },
            { "name": 'TC3', "type": "FieldType.number" },
            { "name": 'TC4', "type": "FieldType.number" },
            { "name": 'TR0', "type": "FieldType.number" },
            { "name": 'TR1', "type": "FieldType.number" },
            { "name": 'TR2', "type": "FieldType.number" },
            { "name": 'TR3', "type": "FieldType.number" },
            { "name": 'TR4', "type": "FieldType.number" },
            { "name": 'TRB', "type": "FieldType.number" },
            { "name": 'TTR', "type": "FieldType.number" },
            { "name": 'TTW', "type": "FieldType.number" },
            { "name": 'ZPR', "type": "FieldType.number" },
            { "name": 'ZTR', "type": "FieldType.number" },
            { "name": 'time', "type": "FieldType.time" },

          ]

   tmstamp = mg_python.m_previous(0, "^grafanastats", region, "")
   while (tmstamp != "" and cnt < limit):
       cnt=cnt+1
       metrics_data = {}
       metrics_data['time'] = tmstamp[0:10] +  " " + tmstamp[11:19]
       stat = mg_python.m_previous(0, "^grafanastats", region, tmstamp, "")
       while (stat != ""):
          dta=mg_python.m_get(0, "^grafanastats", region, tmstamp, stat)
          metrics_data[stat] = float(dta)
          stat = mg_python.m_previous(0, "^grafanastats", region, tmstamp, stat) 
       result.append(metrics_data)
       tmstamp = mg_python.m_previous(0, "^grafanastats", region, tmstamp)
   return jsonify( { "fields":fields, "metrics":result } )

@app.route('/POT')
def get_pot_metrics():
   region=request.args.get('region') or "DEFAULT"
   limit=request.args.get('cnt')
   if limit=="all":
      limit=1000000000000000000000000000000000
   try:
      limit=int(limit)
   except:
      limit=60
   cnt=0
   result = []
   fields = [
            { "name": 'BTD', "type": "FieldType.number" },
            { "name": "CAT", "type": "FieldType.number" },
            { "name": "CFE", "type": "FieldType.number" },
            { "name": "CFS", "type": "FieldType.number" },
            { "name": 'CFT', "type": "FieldType.number" },
            { "name": 'CFavg', "type": "FieldType.number" },
            { "name": 'CFsigma', "type": "FieldType.number" },
            { "name": 'CFvar', "type": "FieldType.number" },
            { "name": 'CQS', "type": "FieldType.number" },
            { "name": 'CQT', "type": "FieldType.number" },
            { "name": 'CQAvg', "type": "FieldType.number" },
            { "name": 'CQsigma', "type": "FieldType.number" },
            { "name": 'CQvar', "type": "FieldType.number" },
            { "name": 'CTN', "type": "FieldType.number" },
            { "name": 'CYS', "type": "FieldType.number" },
            { "name": 'CYT', "type": "FieldType.number" },
            { "name": 'CYavg', "type": "FieldType.number" },
            { "name": 'CYsigma', "type": "FieldType.number" },
            { "name": 'CYvar', "type": "FieldType.number" },
            { "name": 'DEX', "type": "FieldType.number" },
            { "name": 'DFL', "type": "FieldType.number" },
            { "name": 'DFS', "type": "FieldType.number" },
            { "name": 'DRD', "type": "FieldType.number" },
            { "name": 'DTA', "type": "FieldType.number" },
            { "name": 'DWT', "type": "FieldType.number" },
            { "name": 'GET', "type": "FieldType.number" },
            { "name": 'JBB', "type": "FieldType.number" },
            { "name": 'JEX', "type": "FieldType.number" },
            { "name": 'JFB', "type": "FieldType.number" },
            { "name": 'JFL', "type": "FieldType.number" },
            { "name": 'JFS', "type": "FieldType.number" },
            { "name": 'JFW', "type": "FieldType.number" },
            { "name": 'JRE', "type": "FieldType.number" },
            { "name": 'JRI', "type": "FieldType.number" },
            { "name": 'JRL', "type": "FieldType.number" },
            { "name": 'JRO', "type": "FieldType.number" },
            { "name": 'JRP', "type": "FieldType.number" },
            { "name": 'KIL', "type": "FieldType.number" },
            { "name": 'LKF', "type": "FieldType.number" },
            { "name": 'LKS', "type": "FieldType.number" },
            { "name": 'LKfrate', "type": "FieldType.number" },
            { "name": 'NBR', "type": "FieldType.number" },
            { "name": 'NBW', "type": "FieldType.number" },
            { "name": 'NR0', "type": "FieldType.number" },
            { "name": 'NR1', "type": "FieldType.number" },
            { "name": 'NR2', "type": "FieldType.number" },
            { "name": 'NR3', "type": "FieldType.number" },
            { "name": 'NTR', "type": "FieldType.number" },
            { "name": 'NTW', "type": "FieldType.number" },
            { "name": 'ORD', "type": "FieldType.number" },
            { "name": 'QRY', "type": "FieldType.number" },
            { "name": 'SET', "type": "FieldType.number" },
            { "name": 'TBR', "type": "FieldType.number" },
            { "name": 'TBW', "type": "FieldType.number" },
            { "name": 'TC0', "type": "FieldType.number" },
            { "name": 'TC1', "type": "FieldType.number" },
            { "name": 'TC2', "type": "FieldType.number" },
            { "name": 'TC3', "type": "FieldType.number" },
            { "name": 'TC4', "type": "FieldType.number" },
            { "name": 'TR0', "type": "FieldType.number" },
            { "name": 'TR1', "type": "FieldType.number" },
            { "name": 'TR2', "type": "FieldType.number" },
            { "name": 'TR3', "type": "FieldType.number" },
            { "name": 'TR4', "type": "FieldType.number" },
            { "name": 'TRB', "type": "FieldType.number" },
            { "name": 'TTR', "type": "FieldType.number" },
            { "name": 'TTW', "type": "FieldType.number" },
            { "name": 'ZPR', "type": "FieldType.number" },
            { "name": 'ZTR', "type": "FieldType.number" },
            { "name": 'time', "type": "FieldType.time" },

          ]

   tmstamp = mg_python.m_previous(0, "^grafanastats1", region, "")
   while (tmstamp != "" and cnt < 60):
       cnt=cnt+1
       metrics_data = {}
       metrics_data['time'] = tmstamp[0:10] +  " " + tmstamp[11:19]
       stat = mg_python.m_previous(0, "^grafanastats", region, tmstamp, "")
       while (stat != ""):
          dta=mg_python.m_get(0, "^grafanastats1", region, tmstamp, stat)
          if (dta == ""):
             dta="0"
          metrics_data[stat] = float(dta)
          stat = mg_python.m_previous(0, "^grafanastats1", region, tmstamp, stat)
       result.append(metrics_data)
       tmstamp = mg_python.m_previous(0, "^grafanastats1", region, tmstamp)
   return jsonify( { "fields":fields, "metrics":result } )

@app.route('/CUS')
def get_cust_metrics():
   limit=request.args.get('cnt')
   try:
      limit=int(limit)
   except:
      limit=60
   dbfunct=request.args.get('dbfunc')
   fdsep=request.args.get('fdsep') or "@"
   datasep=request.args.get('datasep') or ","
   fieldsep=request.args.get('fieldsep') or ","
   recordsep=request.args.get('recordsep') or ";"
   keyvalsep=request.args.get('keyvalsep') or "#"
   cnt=0
   result = []
   result1 = []
   try:
      yottresult = mg_python.m_function(0, dbfunct)
   except:
      return jsonify( { "error":"An error occured, check for the function/routine name" } )
   derfields=yottresult.split(fdsep)
   derfields1=derfields[0].split(fieldsep)
   for derfield in derfields1:
      fields={}
      fields["name"] = derfield
      fields["type"] = "FieldType.string"
      result1.append(fields) 
   try:
      derdat=derfields[1].split(recordsep)
   except:
      return jsonify( { "error":"An error occured, check the field separator" } )
   for derdatlin in derdat:
     derdat1=derdatlin.split(datasep)
     metrics_data={}
     for some in derdat1:
       some1=some.split(keyvalsep)
       try:
          metrics_data[some1[0]]=some1[1]
       except:
          return jsonify( { "error":"An error occured, check the key value separator" } )
     result.append(metrics_data)   
   return jsonify( { "fields":result1, "metrics":result } )

