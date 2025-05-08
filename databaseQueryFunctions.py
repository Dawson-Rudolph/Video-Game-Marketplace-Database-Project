# This file contains the 6 total queries for the 3 databases (2 queries for each DB)

# Imports
from pymongo import MongoClient
import psycopg2
from neo4j import GraphDatabase


# Replace with the actual connection details
MONGO_URI = "mongodb://localhost:1234"
POSTGRES_PARAMS = {
    "host": "cs440.campus-quest.com",
    "port": 28101,
    "dbname": "postgres",
    "user": "postgres",
    "password": "Academic2025T1!"
}
NEO4J_URI = "bolt://localhost:1234"
NEO4J_AUTH = ("neo4j", "your_password")


def mongoQueries():
    client = None
    try:
        client = MongoClient(MONGO_URI)
        db = client['your_database_name']
        collection = db['collection_name']

        # Add queries here

    except Exception as e:
        print(f"MongoDB error: {e}")
    finally:
        if client:
            client.close()


def neo4jQueries():
    driver = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

        with driver.session() as session:
            pass

            # Add queries here

            # Query 1: Games Released on PC
            result = session.run("""
                MATCH (g:Game)-[:RELEASED_ON]->(p:Platform {name: "PC"})
                RETURN g.name AS game, g.released AS release_date
                ORDER BY release_date DESC
            """)
            print("\nGames Released on PC:")
            for record in result:
                print(f"{record['game']} (Released: {record['release_date']})")


            # Query 2: Recommend Similar Games by Shared Genre and Higher Rating
            result = session.run("""
                MATCH (target:Game {name: "Tomb Raider (2013)"})
                MATCH (target)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(other:Game)
                WHERE other <> target AND other.rating > target.rating
                WITH other, count(g) AS shared_genres, other.rating AS rating
                ORDER BY shared_genres DESC, rating DESC
                LIMIT 5
                RETURN other.name AS recommended_game, shared_genres, rating
                """)
            print("\nRecommended Games Similar to 'Tomb Raider (2013)' (based on shared genres and higher " \
            "rating):")
            for record in result:
                print(f"{record['recommended_game']} (Shared Genres: {record['shared_genres']}, Rating: {record['rating']})")

    except Exception as e:
        print(f"Neo4j error: {e}")
    finally:
        if driver:
            driver.close()


def postgreSQLQueries():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**POSTGRES_PARAMS)
        cursor = connection.cursor()

        # Add queries here
        cursor.execute("""
            SELECT g.title, COUNT(d.id) AS download_count
            FROM download_history d
            JOIN games g ON d.game_id = g.id
            GROUP BY g.title
            ORDER BY download_count DESC
            LIMIT 1;
        """)

        result = cursor.fetchone()
        if result:
            print(f"Most Downloaded Game: {result[0]}, Downloads: {result[1]}")
        else:
            print("No downloads found.")

        cursor.execute("""
        SELECT payment_method, COUNT(*) AS method_count
        FROM purchases
        GROUP BY payment_method
        ORDER BY method_count DESC
        LIMIT 1;
        """)

        result = cursor.fetchone()
        if result:
            print(f"Most Common Payment Method: {result[0]} (used {result[1]} times)")
        else:
            print("No payment records found.")

    except Exception as e:
        print(f"PostgreSQL error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    mongoQueries()
    neo4jQueries()
    postgreSQLQueries()
        

if __name__ == "__main__":
    main()