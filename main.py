#!/usr/bin/python3
import psycopg2


def exec_query(query):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def query1():
    query = """
    SELECT articles.title, COUNT(*) AS views
	FROM articles, log
	WHERE log.path LIKE concat('%', articles.slug)
	GROUP BY articles.title
	ORDER BY views DESC LIMIT 3;
    """
    result = exec_query(query)

    print('\n---- Most popular three articles of all time ----')
    print("\t Title \t \t\t |  Views")
    print("---------------------------------+---------")
    for r in result:
        print("{0} |   {1}".format(r[0], r[1]))


def query2():
    query = """
    SELECT name, COUNT(*) AS views 
    FROM authors, articles, log 
    WHERE authors.id = articles.author 
    AND log.path LIKE concat('%', articles.slug) 
    GROUP BY authors.name 
    ORDER BY views DESC;
    """
    result = exec_query(query)

    print('\n---- Most popular article authors of all time ----')
    print("\t Author \t|  Views")
    print("------------------------+---------")
    for r in result:
        print("{0} \t| {1}".format(r[0], r[1]))


def query3():

    # Count all requests valid and invalid
    view = """
    CREATE VIEW total_req_view AS
    SELECT time::timestamp::date AS date,
    COUNT(*) AS total_requests
    FROM log
    GROUP BY date
    ORDER BY date;
    """
    # Count invalid requests with status code 404
    view = """
    
    """

    # Get days with more than 1% of requests lead to errors
    query = """
    SELECT total_req_view.date, 
    ROUND(((100.0*invalid_req_view.invalid_requests)/total_req_view.total_requests),4) AS percentage
    FROM total_req_view, invalid_req_view
    WHERE total_req_view.date = invalid_req_view.date 
    AND (((100.0*invalid_req_view.invalid_requests)/total_req_view.total_requests) > 1.0)
    ORDER BY percentage;
    """
    result = exec_query(query)

    print('\n---- Days that have more than 1\% of requests lead to errors ----')
    print("\t Day \t    |\tError Percentage")
    print("--------------------+--------------------")
    for r in result:
        print("{0} \t    |     {1}".format(r[0], r[1]))


if __name__ == '__main__':
    print('\n##-------- Logs Analysis Tool --------##')
    print('----------------------------------------')
    query1()
    query2()
    query3()
    print('\n')
