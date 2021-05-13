from silk import *
import json
import datetime
import pandas
import numpy
import mpld3
import matplotlib.pyplot as plt
import matploblib

def parse_records():
    ffile = 'tmp/tcp5.rw'
    flow = SilkFile(ffile,READ)
    f = open('tmp/query1.json','w')
    d = {}
    l = []
    
    for rec in flow:
        d['timestamp'] = rec.stime.strftime("%Y-%m-%d %H:%M:%S")
        d['stime'] = rec.stime.strftime("%Y-%m-%d %H:%M:%S")
        d['etime'] = rec.stime.strftime("%Y-%m-%d %H:%M:%S")
        d['icmpcode'] = rec.icmpcode
        d['sip'] = str(rec.sip)
        d['protocol'] = rec.protocol
        d['output'] = rec.output
        d['packets'] = rec.packets
        d['bytes'] = rec.bytes
        d['application'] = rec.application
        d['sensor_id'] = rec.sensor_id
        d['classtype_id'] = rec.classtype_id
        d['nhip'] = str(rec.nhip)
        d['input'] = rec.input
        d['icmptype'] = rec.icmptype
        d['dip'] = str(rec.dip)
        d['sport'] = rec.sport
        d['dport'] = rec.dport
    
        f.write(json.dumps(d))
        f.write("\n")
    f.close()
    with open('tmp/query1.json','rb') as f:
        data = f.readlines()
    data = map(lambda x: x.rstrip(), data)
    data_json_str = "[" + ",".join(data)+"]"
    
    data_df = pandas.read_json(data_json_str)
    return data_df
netflow_df = parse_records()
netflow_df["timestamp"] = pandas.to_datetime(netflow_df['timestamp'])
netflow_df.set_index('timestamp')
netflow_df = netflow_df.sort_values(by = 'timestamp')
netflow_df = netflow_df.set_index(netflow_df['timestamp'])

netflow_df["packets"] = netflow_df["packets"].astype(int)

netflow_df["packets"].replace(0,numpy.NaN)

netflow_df["packets"] = netflow_df["packets"].resample('1s').sum()

matploblib.rcParams['figure.figsize'] = (10.0,4.0)

matploblib.style.use('fivethirtyeight')

ax = netflow_df[["timestamp","packets"]].set_index('timestamp').resample('1s').mean().plot(title='packet/s', lw=1, colormap = 'jet', marker = '.', markersize = 3)
ax.set_xlabel("Time UTC")
ax.set_ylabel("packet/s")
ax.grid('on', which = 'minor', axis ='x')
ax.grid('on', which = 'major', axis ='y')

mylabels = ["packet/s"]
ax.legend(labels=mylabels, loc='best')

mpl3.save_html(ax.get_figure(), "tmp/testTCP5.html")