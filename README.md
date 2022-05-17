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
    D RUN^grafanaserver(<region>,<secs>)
    
Where region is the region you are looking to attain statistics for i.e. **DEFAULT** and secs is the interval between statistic gathers (default 10 seconds)

**NOTE** - This will create two globals **grafanametrics** and **grafanametrics1** Be mindful of the fact that these globals can quickly in size depending on the interval between statistics gathers.





