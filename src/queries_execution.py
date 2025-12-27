"""
Queries execution script.
Provides example usages of the queries from queries_db_script.py with invocation parameters.
"""
import mysql.connector
import sys
import os

# Add parent directory to path to import config and queries
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from queries_db_script import get_connection, query_1, query_2, query_3, query_4, query_5


def print_query_results(query_name, results):
    """
    Helper function to print query results in a readable format.
    
    Args:
        query_name: Name of the query
        results: List of tuples containing query results
    """
    print(f"\n{'='*60}")
    print(f"Query: {query_name}")
    print(f"{'='*60}")
    if results:
        for row in results:
            print(row)
        print(f"\nTotal results: {len(results)}")
    else:
        print("No results found.")
    print(f"{'='*60}\n")


def main():
    """
    Main function that executes example queries.
    """
    try:
        # Connect to database
        connection = get_connection()
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        print(f"Database: {config.DB_CONFIG['database']}")
        print(f"Host: {config.DB_CONFIG['host']}")
        
        # TODO: Add example query executions here
        # Example 1: Query 1
        # print("\n" + "="*60)
        # print("EXAMPLE QUERY 1: Description of query")
        # print("="*60)
        # results = query_1("example_param", cursor)
        # print_query_results("Query 1", results)
        
        # Example 2: Query 2
        # print("\n" + "="*60)
        # print("EXAMPLE QUERY 2: Description of query")
        # print("="*60)
        # results = query_2("example_param", cursor)
        # print_query_results("Query 2", results)
        
        # Example 3: Query 3
        # print("\n" + "="*60)
        # print("EXAMPLE QUERY 3: Description of query")
        # print("="*60)
        # results = query_3("param1", "param2", cursor)
        # print_query_results("Query 3", results)
        
        # Example 4: Query 4
        # print("\n" + "="*60)
        # print("EXAMPLE QUERY 4: Description of query")
        # print("="*60)
        # results = query_4("example_param", cursor)
        # print_query_results("Query 4", results)
        
        # Example 5: Query 5
        # print("\n" + "="*60)
        # print("EXAMPLE QUERY 5: Description of query")
        # print("="*60)
        # results = query_5("param1", "param2", cursor)
        # print_query_results("Query 5", results)
        
        print("\nNo queries executed yet. Implement queries in queries_db_script.py and uncomment examples here.")
        
        cursor.close()
        connection.close()
        print("\nDatabase connection closed.")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

