# This file contains the 6 total queries for the 3 databases (2 queries for each DB)

# Imports
from pymongo import MongoClient
import psycopg2
from neo4j import GraphDatabase


# Replace with the actual connection details
MONGO_URI = "mongodb://localhost:1234"
POSTGRES_PARAMS = {
    "host": "localhost",
    "port": 1234,
    "dbname": "your_postgres_db",
    "user": "your_username",
    "password": "your_password"
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