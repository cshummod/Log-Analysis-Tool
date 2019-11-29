#!/usr/bin/python3
import psycopg2


def exec_query(query):
    """
    exec_query returns the results of an SQL query.

    exec_query takes an SQL query as a parameter,
    executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def top_three_articles():
    """
    Print the most popular three articles of all time

    args:
    none

    returns:
    None
    """

    query = "SELECT articles.title, COUNT(*) AS views FROM articles, log "\
        "WHERE log.path = '/article/' || articles.slug "\
        "GROUP BY articles.title "\
        "ORDER BY views DESC LIMIT 3;"

    result = exec_query(query)

    print('\n---- Most popular three articles of all time ----')
    print("\t Title \t \t\t |  Views")
    print("---------------------------------+---------")
    for r in result:
        print("{0:<33}|{1:>8}".format(r[0], r[1]))


def most_popular_authors():
    """
    Print the most popular article authors of all time

    args:
    none

    returns:
    None
    """
    query = "SELECT name, COUNT(*) AS views FROM authors, articles, log "\
        "WHERE authors.id = articles.author AND "\
        "log.path = '/article/' || articles.slug "\
        "GROUP BY authors.name "\
        "ORDER BY views DESC;"

    result = exec_query(query)

    print('\n---- Most popular article authors of all time ----')
    print("\t Author\t\t\t |  \tViews")
    print("---------------------------------+------------------")
    for r in result:
        print("{0:<33}|{1:>8}".format(r[0], r[1]))


def error_percentage():
    """
    Print days with more than 1% of requests lead to errors

    args:
    none

    returns:
    None
    """
    query = "SELECT total_req_view.date, "\
        "ROUND(((100.0*invalid_req_view.invalid_requests) "\
        "/total_req_view.total_requests), 4) AS percentage "\
        "FROM total_req_view, invalid_req_view "\
        "WHERE total_req_view.date = invalid_req_view.date "\
        "AND(((100.0*invalid_req_view.invalid_requests) "\
        "/ total_req_view.total_requests) > 1.0) "\
        "ORDER BY percentage;"

    result = exec_query(query)

    print('\n-- Days that have more than 1\% of requests lead to errors --')
    print("\tDay \t| Error Percentage")
    print("----------------+--------------------")
    for r in result:
        print("{0}\t|{1:>12}".format(r[0], r[1]))


if __name__ == '__main__':
    print('\n##-------- Logs Analysis Tool --------##')
    print('----------------------------------------')
    top_three_articles()
    most_popular_authors()
    error_percentage()
    print('\n')
