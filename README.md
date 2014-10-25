MusicalMap
========
### Discovering musical taste around the globe.
 
MusicalMap is intended to be the best tool to visualize the relations between different genres, artists and tracks and their popularities accross different countries throught the world.


Installation
========
### CumulusRDF
The SPARQL endpoint for the application runs on top of CumulusRDF simple server.
The installation of this could be done as follow (including the Unix commands):
 
1. Clone this repository and enter the folder. 

2. Uncompress Apache Cassandra
```
 tar -zxvf server/apache-cassandra-1.2.19-bin.tar.gz -C server/
```
3. Uncompress Apache Tomcat
```
 tar -zxvf server/apache-tomcat-7.0.56.tar.gz -C server/
```
4. Deploy CumulusRDF war file
```
unzip server/cumulusrdf-1.0.1.war -d server/apache-tomcat-7.0.56/webapps/ROOT/
```
5. Start Apache Cassandra
```
sudo server/apache-cassandra-1.2.19/bin/cassandra -f
```
6. Start Apache Tomcat
```
server/apache-tomcat-7.0.56/bin/catalina.sh run
```
7. Load the ontology (NTriples format) on the page
http://localhost:8080/addOrLoad

The file can be found at
https://raw.githubusercontent.com/tdopires/musicmap/master/musical-taste-schema.nt


Accessing the application
========
The application runs locally, since it's just need web browser processing.
Just open the file 'app/index.html' in your Firefox and enjoy :)