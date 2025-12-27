"""
Database queries script.
Contains functions for querying the database.
Each query should be in a separate function named query_NUM where NUM is the query number.
Treat input parameters as inputs provided by the user.
"""
import mysql.connector
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def get_connection():
    """
    Create and return a database connection using config settings.
    """
    return mysql.connector.connect(
        host=config.DB_CONFIG['host'],
        port=config.DB_CONFIG['port'],
        user=config.DB_CONFIG['user'],
        database=config.DB_CONFIG['database'],
        password=config.DB_CONFIG['password'],
    )


def query_1(search_term, cursor):
    """
    Query 1: Full-text search query
    (Should be one of the 2 full-text queries required)
    
    Args:
        search_term: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # TODO: Implement query
    query = """
    -- Add your query here
    """
    cursor.execute(query, (search_term,))
    return cursor.fetchall()


def query_2(search_term, cursor):
    """
    Query 2: Full-text search query
    (Should be one of the 2 full-text queries required)
    
    Args:
        search_term: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # TODO: Implement query
    query = """
    -- Add your query here
    """
    cursor.execute(query, (search_term,))
    return cursor.fetchall()


def query_3(param1, param2, cursor):
    """
    Query 3: Complex query
    (Should be one of the 3 complex queries required - e.g., nested queries, group by, aggregations, EXISTS)
    
    Args:
        param1: User input parameter
        param2: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # TODO: Implement query
    query = """
    -- Add your query here
    """
    cursor.execute(query, (param1, param2))
    return cursor.fetchall()


def query_4(param1, cursor):
    """
    Query 4: Complex query
    (Should be one of the 3 complex queries required - e.g., nested queries, group by, aggregations, EXISTS)
    
    Args:
        param1: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # TODO: Implement query
    query = """
    -- Add your query here
    """
    cursor.execute(query, (param1,))
    return cursor.fetchall()


def query_5(param1, param2, cursor):
    """
    Query 5: Complex query
    (Should be one of the 3 complex queries required - e.g., nested queries, group by, aggregations, EXISTS)
    
    Args:
        param1: User input parameter
        param2: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # TODO: Implement query
    query = """
    -- Add your query here
    """
    cursor.execute(query, (param1, param2))
    return cursor.fetchall()

