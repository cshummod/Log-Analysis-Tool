# Log Analysis Tool v1.0

## Overview
In this project, I build a reporting tool that will use information from news database to discover what kind of articles the readers like.The database contains newspaper's authors, articles and web server log. Using these tables the tool will analyze the site's user activity.

## Database Schema
News database has three tables:
- authors
  - name -> text
  - bio -> text
  - id -> integer (Primary Key)
- articles
  - author -> integer (Forigen Key)
  - title -> text
  - slug -> text
  - lead -> text
  - body -> text
  - time -> timestamp
  - id -> integer (Primary key)
- log
  - path -> text
  - ip -> inet
  - method -> text
  - status -> text\  
  - time -> timestamp
  - id -> integer (Primary Key)

## Analysis Options
The tool currently can perfrom three types of analysis:
1. Get the most popular three articles of all time
2. Get the most popular article authors of all time
3. Get which days did more than 1% of requests lead to errors

## Requirements 
1. Python 3
2. PostgreSQL
3. Psycopg2
4. [News Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## Setup
1. Download/Clone the repository
2. Install Psycopg2 module by runing the following command
   
   `pip install psycopg2`

3. Create the news database in PostgreSQL
4. Download and unzip [News Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
5. Run the following command to load the data:

   `psql -d news -f newsdata.sql`
6. Create the following view that count all requests valid and invalid: 
   
   ```sql 
   CREATE VIEW total_req_view AS
   SELECT time::timestamp::date AS date, 
   COUNT(*) AS total_requests 
   FROM log 
   GROUP BY date 
   ORDER BY date;
   ```
7. Create the following view that count invalid requests with status code 404:
   
   ```sql
   CREATE VIEW invalid_req_view AS 
   SELECT time::timestamp::date AS date, 
   COUNT(*) AS invalid_requests 
   FROM log WHERE status LIKE '%404%' 
   GROUP BY date 
   ORDER BY date;
   ```
8. Run main.py 
   
   `python main.py`

## Output
See the attached file

## Contributors
Mohammed Mahdi Ibrahim

## Support
For any related questions about the tool you can contact me at wmm@hotmail.it
