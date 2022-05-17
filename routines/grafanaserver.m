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
  I '$D(secs) S secs=60
  F  D
  .D proc(region)
  .H secs
  .Q 
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
  

