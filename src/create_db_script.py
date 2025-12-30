import mysql.connector
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def create_movies_table(cursor):
    """
    Create the 'movies' table to store movie information.
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
        FULLTEXT (title, overview),
        FULLTEXT (title)
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
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id        INT,
        person_id       INT,
        cast_order      INT,
        character_name  VARCHAR(500),
        PRIMARY KEY (movie_id, person_id, cast_order),
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
    """
    query = """
    CREATE TABLE IF NOT EXISTS movie_crew (
        movie_id    INT,
        person_id   INT,
        department  VARCHAR(100),
        job         VARCHAR(255),
        PRIMARY KEY (movie_id, person_id, department, job),
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

def create_indices(cursor):
    """
    Create additional B-Tree indices to optimize specific queries (WHERE, JOIN, ORDER BY).
    Note: FULLTEXT indices are already defined in the table creation.
    """
    print("Creating indices...")
    
    # Q1 & Q2: Optimize filtering by year (very common filter)
    cursor.execute("CREATE INDEX idx_movies_release_year ON movies(release_year)")
    
    # Q3: Optimize Budget Tier Analysis (filtering and sorting by budget)
    cursor.execute("CREATE INDEX idx_movies_budget ON movies(budget)")
    
    # Q2: Optimize 'Flop' detection (filtering by revenue and votes)
    cursor.execute("CREATE INDEX idx_movies_revenue_vote ON movies(revenue, vote_average)")
    
    # Q4: Optimize searching for Directors in the huge crew table
    cursor.execute("CREATE INDEX idx_crew_job ON movie_crew(job)")
    
    # Q5: Optimize Genre filtering by name
    cursor.execute("CREATE INDEX idx_genres_name ON genres(name)")
    
    print("Indices created successfully.")

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

        # 3. Create Indices
        create_indices(cursor)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("All tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

if __name__ == "__main__":
    create_all_tables()

