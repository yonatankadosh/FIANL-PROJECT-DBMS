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
    Plot/Concept Analysis
    Target Audience Value: Allows producers to search for plot keywords (e.g., "apocalypse", "wedding")
    to see the financial performance of similar past movies.
    
    Args:
        search_term: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    query = """
    SELECT 
        title, 
        release_year, 
        CONCAT('$', FORMAT(budget, 0)) as budget_formatted, 
        CONCAT('$', FORMAT(revenue, 0)) as revenue_formatted,
        ROUND(revenue / NULLIF(budget, 0), 2) as roi_ratio
    FROM movies 
    WHERE 
        MATCH(overview) AGAINST (%s IN NATURAL LANGUAGE MODE)
        AND budget > 0 
        AND revenue > 0
    ORDER BY revenue DESC
    LIMIT 20;
    """
    cursor.execute(query, (search_term,))
    return cursor.fetchall()


def query_2(search_term, cursor):
    """
    Query 2: Full-text search query
    Title Competitor Check
    Target Audience Value: Search for specific phrases in titles to analyze popularity 
    and viewer reception.
    
    Args:
        search_term: User input parameter
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    query = """
    SELECT 
        title, 
        popularity, 
        vote_average, 
        vote_count 
    FROM movies 
    WHERE MATCH(title) AGAINST (%s IN NATURAL LANGUAGE MODE)
    ORDER BY popularity DESC
    LIMIT 20;
    """
    cursor.execute(query, (search_term,))
    return cursor.fetchall()


def query_3(min_movies_together, cursor):
    """
    Query 3: Complex query
    Best Actor Combinations (Pairs) by Rating
    Target Audience Value: Producers want to know which 'Power Couples' work best together.
    
    Note: This query performs a self-join which is computationally expensive.
    Limiting to top 5 cast members (cast_order < 5) reduces computation significantly.
    
    Args:
        min_movies_together: Minimum number of movies the pair acted in together (to ensure statistical significance).
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    # Optimized: Filter cast_order early using a subquery/CTE-like approach
    # This reduces the number of rows before the expensive self-join
    query = """
    SELECT 
        p1.name AS actor_1,
        p2.name AS actor_2,
        COUNT(*) AS movies_together,
        ROUND(AVG(m.vote_average), 2) AS avg_rating
    FROM (
        SELECT movie_id, person_id, cast_order
        FROM movie_cast
        WHERE cast_order < 10
    ) mc1
    JOIN (
        SELECT movie_id, person_id, cast_order
        FROM movie_cast
        WHERE cast_order < 10
    ) mc2 ON mc1.movie_id = mc2.movie_id AND mc1.person_id < mc2.person_id
    JOIN people p1 ON mc1.person_id = p1.person_id
    JOIN people p2 ON mc2.person_id = p2.person_id
    JOIN movies m ON mc1.movie_id = m.movie_id
    GROUP BY p1.person_id, p2.person_id, p1.name, p2.name
    HAVING COUNT(*) >= %s
    ORDER BY avg_rating DESC
    LIMIT 15;
    """
    cursor.execute(query, (int(min_movies_together),))
    return cursor.fetchall()


def query_4(limit_num, cursor):
    """
    Query 4: Complex query
    Best Director by Revenue
    Target Audience Value: Identifies the most commercially successful directors.
    
    Args:
        limit_num: Number of directors to show.
        cursor: Database cursor
    Returns:
        List of tuples containing query results
    """
    query = """
    SELECT 
        p.name AS director_name,
        COUNT(m.movie_id) AS movies_directed,
        CONCAT('$', FORMAT(SUM(m.revenue), 0)) AS total_revenue
    FROM people p
    JOIN movie_crew mc ON p.person_id = mc.person_id
    JOIN movies m ON mc.movie_id = m.movie_id
    WHERE mc.job = 'Director' AND m.revenue > 0
    GROUP BY p.person_id, p.name
    ORDER BY SUM(m.revenue) DESC
    LIMIT %s;
    """
    cursor.execute(query, (int(limit_num),))
    return cursor.fetchall()


def query_5(min_revenue_threshold, cursor):
    """
    Query 5: Complex query
    Best Genre Combinations by Revenue
    Target Audience Value: Helps producers decide on genre mashups (e.g., "Action-Comedy" vs "Horror-Romance").
    Complexity: Uses Self-Join on movie_genres to find combinations.
    
    Args:
        min_revenue_threshold: Filter to consider only movies making significant money.
        cursor: Database cursor
    
    Returns:
        List of tuples containing query results
    """
    query = """
    SELECT 
        g1.name AS genre_1,
        g2.name AS genre_2,
        COUNT(m.movie_id) AS movie_count,
        CONCAT('$', FORMAT(AVG(m.revenue), 0)) AS avg_revenue
    FROM movie_genres mg1
    JOIN movie_genres mg2 ON mg1.movie_id = mg2.movie_id
    JOIN genres g1 ON mg1.genre_id = g1.genre_id
    JOIN genres g2 ON mg2.genre_id = g2.genre_id
    JOIN movies m ON mg1.movie_id = m.movie_id
    WHERE mg1.genre_id < mg2.genre_id 
      AND m.revenue >= %s
    GROUP BY g1.genre_id, g2.genre_id, g1.name, g2.name
    ORDER BY AVG(m.revenue) DESC
    LIMIT 15;
    """
    cursor.execute(query, (int(min_revenue_threshold),))
    return cursor.fetchall()

