import mysql.connector
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def create_movies_table(cursor):
    """
    Create the 'movies' table to store movie information.
    Optimized indexes for Query 1, 2, 4, 5.
    """
    query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id            INT PRIMARY KEY,
        title               VARCHAR(255),
        original_title      VARCHAR(255),
        original_language   VARCHAR(10),
        release_date        DATE,
        release_year        INT,
        runtime             INT,
        budget              BIGINT,
        revenue             BIGINT,
        popularity          DECIMAL(10, 6),
        vote_average        DECIMAL(3, 1),
        vote_count          INT,
        tagline             TEXT,
        overview            TEXT,
        -- Index for sorting/filtering by revenue (Queries 1, 4, 5)
        INDEX idx_revenue (revenue),
        -- Index for Query 3: sorting by vote_average (rating)
        INDEX idx_vote_average (vote_average),
        -- Fulltext for Title Search (Query 2)
        FULLTEXT idx_ft_title (title),
        -- Fulltext for Plot Analysis (Query 1)
        FULLTEXT idx_ft_overview (overview)
    );
    """
    cursor.execute(query)

def create_genres_table(cursor):
    """
    Create the 'genres' table, storing genre info (e.g., 'Animation', 'Comedy').
    """
    query = """
    CREATE TABLE IF NOT EXISTS genres (
        genre_id    INT PRIMARY KEY,
        name        VARCHAR(100) NOT NULL UNIQUE
    );
    """
    cursor.execute(query)

def create_movie_genres_table(cursor):
    """
    Create the many-to-many linkage between 'movies' and 'genres'.
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id    INT,
        genre_id    INT,
        PRIMARY KEY (movie_id, genre_id),
        CONSTRAINT fk_movie_genres_movie
            FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_movie_genres_genre
            FOREIGN KEY (genre_id)
            REFERENCES genres(genre_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """
    cursor.execute(query)

def create_people_table(cursor):
    """
    Create the 'people' table to store person information (actors, directors, etc.).
    """
    query = """
    CREATE TABLE IF NOT EXISTS people (
        person_id   INT PRIMARY KEY,
        name        VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(query)

def create_movie_cast_table(cursor):
    """
    Create the 'movie_cast' table to link movies with cast members.
    Optimized indexes for Query 3 (actor pairs analysis).
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id        INT,
        person_id       INT,
        cast_order      INT,
        character_name  VARCHAR(500),
        PRIMARY KEY (movie_id, person_id, cast_order),
        -- Index to optimize Query 3: allows filtering cast_order early and efficient join on movie_id
        INDEX idx_movie_cast_order (movie_id, cast_order, person_id),
        CONSTRAINT fk_movie_cast_movie
            FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_movie_cast_person
            FOREIGN KEY (person_id)
            REFERENCES people(person_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """
    cursor.execute(query)

def create_movie_crew_table(cursor):
    """
    Create the 'movie_crew' table to link movies with crew members.
    Optimized index for Query 4 (Director search).
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_crew (
        movie_id    INT,
        person_id   INT,
        department  VARCHAR(100),
        job         VARCHAR(255),
        PRIMARY KEY (movie_id, person_id, department, job),
        -- Index specifically for filtering by Job (e.g., 'Director')
        INDEX idx_job (job),
        CONSTRAINT fk_movie_crew_movie
            FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_movie_crew_person
            FOREIGN KEY (person_id)
            REFERENCES people(person_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """
    cursor.execute(query)

def create_keywords_table(cursor):
    """
    Create the 'keywords' table to store movie keywords.
    """
    query = """
    CREATE TABLE IF NOT EXISTS keywords (
        keyword_id  INT PRIMARY KEY,
        name        VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(query)

def create_movie_keywords_table(cursor):
    """
    Create the many-to-many linkage between 'movies' and 'keywords'.
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_keywords (
        movie_id    INT,
        keyword_id  INT,
        PRIMARY KEY (movie_id, keyword_id),
        CONSTRAINT fk_movie_keywords_movie
            FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_movie_keywords_keyword
            FOREIGN KEY (keyword_id)
            REFERENCES keywords(keyword_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """
    cursor.execute(query)

def create_movie_ratings_summary_table(cursor):
    """
    Create the 'movie_ratings_summary' table to store aggregated rating information.
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_ratings_summary (
        movie_id        INT PRIMARY KEY,
        rating_avg      DECIMAL(3, 2),
        rating_count    INT,
        CONSTRAINT fk_movie_ratings_summary_movie
            FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """
    cursor.execute(query)


def create_all_tables():
    """
    Connect to the database, create each table in a logical sequence,
    then commit and close the connection.
    """
    try:
        # Connect to MySQL server using config
        connection = mysql.connector.connect(
            host=config.DB_CONFIG['host'],
            port=config.DB_CONFIG['port'],
            user=config.DB_CONFIG['user'],
            database=config.DB_CONFIG['database'],
            password=config.DB_CONFIG['password'],
        )
        cursor = connection.cursor()

        # Create tables in an order that respects foreign key dependencies.
        # 1. Base tables (no foreign keys)
        create_movies_table(cursor)
        create_genres_table(cursor)
        create_people_table(cursor)
        create_keywords_table(cursor)
        
        # 2. Tables that reference base tables
        create_movie_genres_table(cursor)
        create_movie_cast_table(cursor)
        create_movie_crew_table(cursor)
        create_movie_keywords_table(cursor)
        create_movie_ratings_summary_table(cursor)

        connection.commit()
        cursor.close()
        connection.close()
        print("All tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

if __name__ == "__main__":
    create_all_tables()

