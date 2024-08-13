# Installation
```
pip install psycopg2
```
```
pip install geopandas
```
```
pip install contextily
```
# How to use
Add connection to your database server
```
host = localhost
dbname = xxx
user = xxx
password = xxx
port = 5432
```
Create a connection to the database
```
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
```
Use SQL query layers in the database
For example:
```
sql_fire = "SELECT * FROM district WHERE name = 'PhayaThai';"
```
(Optional) Print all rows of a query results and returns a list of tuples. 
```
print(cursor.fetchall())
```
Close the connection when the work is done.
```
conn.close()
```
# Requirements
```
contextily==1.6.0
geopandas==0.13.2
matplotlib==3.7.2
numpy==1.25.1
pandas==2.0.3
psycopg2==2.9.9
```
# Data source for the example dataset
[NASA FIRMS: Active Fire Data](https://firms.modaps.eosdis.nasa.gov/active_fire/)

[Esri: Sentinel-2 Land Cover Explorer](https://livingatlas.arcgis.com/landcoverexplorer/#mapCenter=122.35363%2C63.85442%2C11&mode=step&timeExtent=2017%2C2023&year=2023)

![Rimberio Podcast](https://github.com/user-attachments/assets/4022e5bc-d3af-42a9-aac4-f08518f726da)
