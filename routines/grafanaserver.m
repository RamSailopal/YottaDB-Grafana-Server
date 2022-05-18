proc(region)
  K ^gvstatinc
  D gatherdb^gvstat(,0)
  S tim=""
  SET stat=""
  FOR  SET tim=$O(^gvstatinc(region,tim)) QUIT:tim=""  DO
  .FOR  SET stat=$O(^gvstatinc(region,tim,stat)) QUIT:stat=""  DO
  ..S ^gvstatinctot(region,"tot",stat)=^gvstatinc(region,tim,stat)+$G(^gvstatinctot(region,"tot",stat),0)
  ..S ^grafanastats1(region,$zdate($H,"YEAR-MM-DD")_"T"_$zdate($H,"24:60:SS")_".000Z",stat)=$G(^gvstatinc(region,tim,stat),0)
  ..Q
  .Q
  S tim=""
  SET stat=""
  FOR  SET tim=$O(^gvstatinctot(region,tim)) QUIT:tim=""  DO
  .FOR  SET stat=$O(^gvstatinctot(region,tim,stat)) QUIT:stat=""  DO
  ..S ^grafanastats(region,$zdate($H,"YEAR-MM-DD")_"T"_$zdate($H,"24:60:SS")_".000Z",stat)=^gvstatinctot(region,tim,stat)
  QUIT
JOB(region,secs)
  S ^grafanaconf("PID",region)=$J
  I '$D(secs) S secs=60
  S TYPE=""
  F  D
  .I $D(^grafanaconf("PURGE"))  D
  ..F  S TYPE=$O(^grafanaconf("PURGE",region,TYPE)) Q:TYPE=""  D
  ...I TYPE="CUM" K ^grafanastats(region) K ^grafanaconf("PURGE",region)
  ...E  I TYPE="POT" K ^grafanastats(region) K ^grafanaconf("PURGE",region)
  ...Q
  ..Q
  .D proc(region)
  .H secs
  .Q 
  Quit
START(region,secs) 
  I '$D(secs) S secs=60
  I '$D(region) S region="DEFAULT"
  J JOB^grafanaserver(region,secs)
  Quit
STOP(region)
  I '$D(region) W !,"Please enter a region to stop the server for" Q
  I '$D(^grafanaconf("PID",region)) W !,"Grafana server is not running"
  E  D
  .S PID=^grafanaconf("PID",region)
  .S CMD="kill -9 "_PID
  .zsystem CMD
  .K ^grafanaconf("PID",region)
  Quit
STATUS(region)
  I '$D(region) W !,"Please enter a region to check the server status for" Q
  I $D(^grafanaconf("PID",region)) W !,"Grafana server is running as process - "_^grafanaconf("PID",region)
  E  W !,"Grafana server is not running"
  Quit
PURGE(TYPE,region)
  I '$D(TYPE) W !,"Please enter CUM for Cumulative stats or POT for point in time stats"
  I (TYPE'="CUM")&(TYPE'="POT") W !,"Please enter CUM for Cumulative stats or POT for point in time stats"
  I '$D(region) W !,"Please enter a region for stats to delete"
  S ^grafanaconf("PURGE",region,TYPE)=1
  Quit
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
  S txt="Time,Temperature@Time#"_$zdate($H,"YEAR-MM-DD")_"T00:00:00,Temperature#22;Time#"_$zdate($H-1,"YEAR-MM-DD")_"T00:00:00,Temperature#20;Time#"_$zdate($H-2,"YEAR-MM-DD")_"T00:00:00,Temperature#18;Time#"_$zdate($H-3,"YEAR-MM-DD")_"T00:00:00,Temperature#24;Time#"_$zdate($H-4,"YEAR-MM-DD")_"T00:00:00,Temperature#15"
  quit (txt)
  

