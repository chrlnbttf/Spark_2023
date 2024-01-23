Notes "exam Scala Spark - "NBA" project"

1) Obstacles / Solutions or need help

"Need help"
- priority :
        1. point 7.2 : result incomplete
           Csv result file is incomplete as the extracted statsAtl_full.json file includes only one game
           due to a mistake in the loop present in extract_Atl_stats.py. May you help me with this code to get all games ?
        2. point 11.1 : result incomplete
           I have provided with the result of 1 team only instead of 4.
        3. points 6.2 and 7.3 : problem of form (Scala)
           Could you provide me with the full scala extract file, as mine are a mix of python and scala ?
        4. point 10.1 : no archive from transform.scala (SparkSession)
           There is a fail in loading the class
- others : 1.4, 8.1, 10.2, 11.2

"Points"
1 Visualisation of API request results :
        1 Postman : success => ok, but insufficient
        2 Terminal bash : curl -L get "https://balldontlie.io/api/v1/stats?game_ids[]=473607" | jq '.' : OK, but insufficient
                Note : Installation de jq through sudo apt-get install jq
                Note : -L used to force redirections following the error <H1>301 Moved</H1> The document has moved
        3 sbt compile and sbt run using the scala library request and a scala file => ok, but heavy and long method
        4 Launch of a scala file with scalac and scala =>  import requests doesn't work => need help
        5 Library request with Python => easy-to-use and quick execution of a python file 
2. file extract_Atl_games.py : Build loops to iterate on pages :
        - by default, display of 25 pages and param keys limited to 100 pages => loop OK
3. file extract_Atl_games.py : Presence of unwanted "data" and "meta" in json files
        => select dictionary["data"] in loops
4. file extract.scala : Extraction of games ids list from json files "Games", as parameter team_ids doesn't work
        1 necessity to use Scala Spark df => ok
        2 pb of method => ok use of getstring function + import spark.sqlContext.implicits._ to convert object in df (?)
        3 pb of cast : need string to use getstring function => ok change of types needed
        4 pb of duplicated match ids (1 per player) to create the list of mactch ids => ok use of .distinct()
5. file .scala : Version conflict with dependencies
        => ok solution brought on support.datascientest.com : Some libraries have common packages :
        “com.lihaoyi” %% “requests” % “0.1.8”,
        “com.lihaoyi” %% “ujson” % “0.7.1”,
        “com.lihaoyi” %% “os-lib” % “0.9.0”
6 file extract_Atl_stats.py and extract.scala : Write json file :
        1 méthod found in Python
        2 method not found in Scala => need help
7 file extract_Atl_stats.py : Buid loops to execute iterative API requests based on game ids list
        1 Former method to iterage pages applied
        2 Iteration on API request based on games ids list doesn't fully work => need help
                => I have extract only the last games to move ahead on the exam and supply with deliverables
        3 Same iteration on scala => need help
8 repositories and file duplicates :
        1 Do we have to create 2 repositories one for data extraction and one for data transformation,
          in order to get results as there is 2 scala code files (extract.scala and transform.scala) ?
          Problem : we need to copy in the 2 repos the json files => need help
9 file transform.scala : Data manipulation on dataFrame :
        1 Pb with renaming nested columns 
                - withColumnRenamed : Would force us to define other dfs and merge them : too fastidious
                - chaining subkey.map(x => col(s"col.$x") impossible as several consecutive .select not-accepted
                => ok, use of withColumns having a syntax for nested columns (.withColumn("id", col("B.id")))
        2 Pb with a function making it possible to choose among 2 columns the values to inject in a new one :
                val idList = List("idHome", "idVisitor")
                val add_col = (x:org.apache.spark.sql.Column,y:org.apache.spark.sql.Column) => (if (x==1) x else y)
                val gamesAtl = gamesAtl_aux.withColumn("id", idList.map(col(_)).reduce(add_col(_,_))).show(2)
                => Why ?
                => Solution found : df.withColumn("A", when(col("B") === value, col("C")))
10 files extract.scala and transform.scala : charline.salahun@gmail.comSparkSession :
        1 Failed to load class Transformation when launching the spark-submit command => need help
        2 I still don't see the utility of using the SparkSession instead of spark REPL, as we can get the archives
                in other faster ways (the obtention of a result from sbt compile + spark-submit combined needs in
                average 5 minutes compared to an immediate execution through the REPL) and that is the main advantage
                that was expressed on support.datascientest.com => need help
11 Efficiency
        1  Iteration on the 4 teams : is there a solution doing it without adapting 4 times the same codes ? => need help
        2. Cache requested ? => need help


2) API request notes :

Team Ids :
        Atlanta Hawks : 1, Los Angeles Lakers : 14, Milwaukee Bucks : 17, Phoenix Suns : 24

Model of requests :
        Games : https://balldontlie.io/api/v1/games?seasons[]=2021&team_ids[]=1
        Stats : https://balldontlie.io/api/v1/stats?game_ids[]=473607


3) Deliverables:

- file extract_Atl_games.py (extract games info on json file)
        COMMAND : python3 <file_name>
- file Extract.scala (extract list of game_ids from games json file)
        COMMAND : sbt compile
        COMMAND = sbt run
- file extract_Atl_stats.py (extract stats info on json file)
        COMMAND : python3 <file_name>
- file Transform.scala (dataFrame manipulation to load particular data from Games.json and Stats.json files)
        COMMAND = sbt package
        COMMAND = spark-submit --class "Transform" --master local[2] target/scala-2.12/nba-tranform_2.12-1.0.jar
- file Atl_output.csv
