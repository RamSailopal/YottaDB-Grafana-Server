# YottaDB-Grafana-Server

The back-end components of the YottaDB metrics Grafana plugin

This back end server running using Python Flask, takes data out of YottaDB globals and then converts then to a format that can be interpreted by Grafana through API end points.

# Setting Up

The infrastructure uses **Chris Munt's** **mg_python** and so this will first need setting up both on the YottaDB and also the server running this Grafana backend server:

https://github.com/chrisemunt/mg_python

On completion of the steps outlined, make sure that a yottadb process is listening on port 7041:
   
     ss -lnp | grep 7041
     
Also ensure that the mg_python Python library is installed as outlined in the guide.

Once this is set up, the next stage is to load the routines in the routines folder into your YottaDB environment:

    cd /usr/local
    git clone https://github.com/RamSailopal/YottaDB-Grafana-Server.git
    cd YottaDB-Grafana-Server
    cp routines/* <path to YottaDB routines directory>
    <path to yottadb install directory>/ydb
    ZL "gvstat.m"
    ZL "grafanaserver.m"
    J JOB^grafanaserver(<region>,<secs>)
    
Where region is the region you are looking to attain statistics for i.e. **DEFAULT** and secs is the interval between statistic gathers (default 10 seconds)

**NOTE** - This will create two globals **grafanametrics** and **grafanametrics1** Be mindful of the fact that these globals can quickly in size depending on the interval between statistics gathers.

Install the requirements for the run the Grafana back end server process:

    pip install -r requirements/requirements.txt
    
With the mg_python dependancy installed as outlined in the mg_python Github page (see above) run the server process:

    python yottametrics.py
    
# Metrics Returned

Metrics will be returned in 3 categories:

1) CUM - Cumulative metrics over time
2) POT - Metrics in a single point of time
3) CUS - This allows you to setup and call your own metrics

Further details relating to the metrics returned by the CUM and POt categories can be found here:

https://docs.yottadb.com/ProgrammersGuide/commands.html#zshow

The metrics for the individual categories will be exposed through 3 separate endpoints as demonstrated in the graphic below:

![Alt text](Grafanaserver.JPG?raw=true "Backend server")

Additional parameters can be passed for the region to attain metrics for and the number of records/objects to return i.e.

http://192.168.240.21:5000?region=TEST&cnt=100

A cnt=all will return all records available

**NOTE** The number of records returned will effect performance.







