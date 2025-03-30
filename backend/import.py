import json
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="dashboard",
    user="yashraj",
    password="hello",
    host="localhost",
    port="5432"
)

def parse_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%B, %d %Y %H:%M:%S")
    except (ValueError, TypeError):
        return None

with open('jsondata.json', encoding="utf-8") as f:
    data = json.load(f)
    
cursor = conn.cursor()

create_table_query = """
    CREATE TABLE IF NOT EXISTS data (
        id SERIAL PRIMARY KEY,
        end_year INT,
        intensity FLOAT,
        sector VARCHAR(255),
        topic VARCHAR(255),
        insight TEXT,
        url TEXT,
        region VARCHAR(255),
        start_year INT,
        impact FLOAT,
        added TIMESTAMP,
        published TIMESTAMP,
        country VARCHAR(255),
        relevance FLOAT,
        pestle VARCHAR(255),
        source VARCHAR(255),
        title TEXT,
        likelihood FLOAT
    );
"""
cursor.execute(create_table_query)

insert_query = """
    INSERT INTO data (
        end_year, intensity, sector, topic, insight, url, region,
        start_year, impact, added, published, country, relevance,
        pestle, source, title, likelihood
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

for item in data:
    cursor.execute(insert_query, (
        int(item.get('end_year') or 0),
        int(item.get('intensity') or 0), 
        item.get('sector'),
        item.get('topic'),
        item.get('insight'),
        item.get('url'),
        item.get('region'),
        int(item.get('start_year') or 0),
        int(item.get('impact') or 0),
        parse_datetime(item.get('added')),
        parse_datetime(item.get('published')),
        item.get('country'),
        int(item.get('relevance') or 0),
        item.get('pestle'),
        item.get('source'),
        item.get('title'),
        int(item.get('likelihood') or 0)
    ))

conn.commit()
cursor.close()
conn.close()

print("Data imported")
