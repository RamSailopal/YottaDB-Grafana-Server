# YottaDB-Grafana-Server

The back-end components of the YottaDB metrics Grafana plugin

This back end server running using Python Flask, takes data out of YottaDB globals and then converts then to a format that can be interpreted by Grafana through API end points.

Details of the YottaDB Grafana plugin can be found here - https://github.com/RamSailopal/YottaDB-Grafana-Plugin

# Setting Up

**YottaDB server**

The infrastructure uses **Chris Munt's** **mg_python** and so this will first need setting up both on the YottaDB and also the server running this Grafana backend server:

https://github.com/chrisemunt/mg_python

On completion of the steps outlined, make sure that a yottadb process is listening on port 7041:
   
     ss -lnp | grep 7041
     
Ensure that the mg_python Python library is installed as outlined in the guide.

Once this is set up, the next stage is to load the routines in the routines folder into your YottaDB environment:

    cd /usr/local
    git clone https://github.com/RamSailopal/YottaDB-Grafana-Server.git
    cd YottaDB-Grafana-Server
    cp routines/* <path to YottaDB routines directory>
    <path to yottadb install directory>/ydb
    ZL "gvstat.m"
    ZL "grafanaserver.m"
    D START^grafanaserver(<region>,<secs>)
    
Where region is the region you are looking to attain statistics for i.e. **DEFAULT** and secs is the interval between statistic gathers (default 10 seconds)

**NOTE** - This will create two globals **grafanametrics** and **grafanametrics1** Be mindful of the fact that these globals can quickly in size depending on the interval between statistics gathers.

Statistics can be purged at any time by issuing the command:

    D PURGE^grafanaserver(<type>,<region>)
    
Where type is the type of metrics to purge, **CUM** to cumulative and **POT** for point in time

Other options:

    D STOP^grafanaserver(<region>) # Stop the server for a given region
    D STATUS^grafanaserver(<region>) # Check the status of the server for a given region

**Grafana Back end server**

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

http://192.168.240.21:5000/CUM?region=TEST&cnt=100

A cnt=**all** will return all records available

**NOTE** Although http response compression has been implemented, the number of records returned will effect performance.

These API endpoints can then be consumed by the Grafana YottaDB datasource plugin:

https://github.com/RamSailopal/YottaDB-Grafana-Plugin

# Custom Metric

The **CUS** endpoint allows custom/bespoke metrics to be returned from the Yotta database.

The endpoint calls a YottaDB function/routine using mg_python and then expects data in a specific format.

Taking the **EXAMPLE** function in the **grafanaserver.m** routine:

    EXAMPLE()
    ;
    ; Field/Data separator - "@"
    ; Field separator - ","
    ; Data separator - ","
    ; Record separator - ";"
    ; Key value separator - "#"
    ;
    ; Use $zdate($H,"YEAR-MM-DD")_"T"_$zdate($H,"24:60:SS") to get the current timestamp from M
    ;
    S txt="Time,Temperature@Time#"_$zdate($H,"YEAR-MM-DD")_"T00:00:00,Temperature#22\;Time#"_$zdate($H-1,"YEAR-MM-DD")_"T00:00:00,Temperature#20\;Time#"_$zdate($H-2,"YEAR-MM-DD")_"T00:00:00,Temperature#18\;Time#"_$zdate($H-3,"YEAR-MM-DD")_"T00:00:00,Temperature#24\;Time#"_$zdate($H-4,"YEAR-MM-DD")_"T00:00:00,Temperature#15"
    quit (txt)
    
The text:

**Time,Temperature@Time#"_$zdate($H,"YEAR-MM-DD")_"T00:00:00,Temperature#22\;Time#"_$zdate($H-1,"YEAR-MM-DD")_"T00:00:00,Temperature#20\;Time#"_$zdate($H-2,"YEAR-MM-DD")_"T00:00:00,Temperature#18\;Time#"_$zdate($H-3,"YEAR-MM-DD")_"T00:00:00,Temperature#24\;Time#"_$zdate($H-4,"YEAR-MM-DD")_"T00:00:00,Temperature#15** 

is returned by the function to the back end server.

The text before **@** represents the field headers:

**Time,Temperature**

each separated by **,**:

**Time**

**Temperature**

The text after **@** is the actual data:

**Time#"_$zdate($H,"YEAR-MM-DD")_"T00:00:00,Temperature#22\;Time#"_$zdate($H-1,"YEAR-MM-DD")_"T00:00:00,Temperature#20\;Time#"_$zdate($H-2,"YEAR-MM-DD")_"T00:00:00,Temperature#18\;Time#"_$zdate($H-3,"YEAR-MM-DD")_"T00:00:00,Temperature#24\;Time#"_$zdate($H-4,"YEAR-MM-DD")_"T00:00:00,Temperature#15**


Each record in the data is separated with **;** i.e:

**Time#"_$zdate($H,"YEAR-MM-DD")_"T00:00:00,Temperature#22**

**NOTE - The last record doesn't have a trailing ;**

Each entry is separated by a **,** i.e.:

**Temperature#22**

and each key/value combination **,** The separator between the actual key and value is **#** i.e.

key -  **Temperature**

Value - **22**

To call the example function/routine on the back end server using the CUS endpoint we would use example:

http://192.168.240.21:5000/CUS?dbfunc=EXAMPLE^grafanaserver

The above referenced separators are the default configured and separators but separators can be reconfigured so that they are referenced when making the API call to the back end server.

Taking the example of the following seperators:

Field/Data separator - "^"

Field separator - "*"

Data separator - "|"

Record separator - "#"
 
Key value separator - "@"

When making the API request we would send additional parameters and so:

http://192.168.240.21:5000/CUS?dbfunc=EXAMPLE^grafanaserver&fdsep=^&datasep=|&fieldsep=*&recordsep=#&ketvalsep=@

The following URL parameters therefore translate as follows:

**fdsep** - Field/Data separator

**datasep** - Data separator

**fieldsep** - Field separator

**recordsep** - Record separator

**keyvalsep** - Key value separator


# References

YottaDB - https://yottadb.com/

mg_python - https://github.com/chrisemunt/mg_python






