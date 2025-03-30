import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='dashboard',
            user='yashraj',
            password='hello'
        )
        return conn
    except psycopg2.Error as e:
        print("Database connection error:", e)
        return None  

@app.route('/')
def index():
    conn = get_db_connection()
    conn.set_client_encoding('UTF8')
    if conn is None:
        return "Error: Unable to connect to the database"
    
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT * FROM data;')
            data = cur.fetchall()
    
    conn.close()
    return render_template('index.html', data=data)

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM data;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.route('/api/kpi-metrics')
def get_kpi_metrics():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                COUNT(*) as total_entries,
                AVG(intensity) as avg_intensity,
                AVG(likelihood) as avg_likelihood,
                COUNT(CASE WHEN sector = 'Energy' THEN 1 END) as energy_count,
                COUNT(CASE WHEN pestle = 'Industries' THEN 1 END) as industry_count,
                COUNT(DISTINCT region) as region_count
            FROM data
        """)
        metrics = cur.fetchone()
        
        return jsonify({
            "total_entries": metrics[0],
            "avg_intensity": float(metrics[1]) if metrics[1] else 0,
            "avg_likelihood": float(metrics[2]) if metrics[2] else 0,
            "energy_sector": metrics[3],
            "industry_focus": metrics[4],
            "regions_covered": metrics[5]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
        

# Intensity Distribution
@app.route('/api/intensity-distribution')
def intensity_dist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT intensity, COUNT(*) as count 
        FROM data 
        GROUP BY intensity 
        ORDER BY intensity;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'intensity': row[0], 'count': row[1]} for row in rows])

# Topic Frequency
@app.route('/api/topic-frequency')
def topic_freq():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT topic, COUNT(*) as count 
        FROM data 
        WHERE topic IS NOT NULL AND topic != '' 
        GROUP BY topic 
        ORDER BY count DESC 
        LIMIT 10;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'topic': row[0], 'count': row[1]} for row in rows])

# Sector Distribution
@app.route('/api/sector-distribution')
def sector_dist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sector, COUNT(*) as count 
        FROM data 
        WHERE sector IS NOT NULL AND sector != '' 
        GROUP BY sector 
        ORDER BY count DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'sector': row[0], 'count': row[1]} for row in rows])

# Region Distribution
@app.route('/api/region-distribution')
def region_dist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT region, COUNT(*) as count 
        FROM data 
        WHERE region IS NOT NULL AND region != '' 
        GROUP BY region 
        ORDER BY count DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'region': row[0], 'count': row[1]} for row in rows])

# PESTLE Analysis
@app.route('/api/pestle-distribution')
def pestle_dist():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT pestle, COUNT(*) as count 
        FROM data 
        WHERE pestle IS NOT NULL AND pestle != '' 
        GROUP BY pestle 
        ORDER BY count DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'pestle': row[0], 'count': row[1]} for row in rows])

# Geographical Heatmap
@app.route('/api/geo-heatmap')
def get_geo_heatmap_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                country,
                AVG(intensity) as avg_intensity,
                AVG(relevance) as avg_relevance,
                COUNT(*) as record_count,
                STRING_AGG(DISTINCT topic, ', ') as topics,
                STRING_AGG(DISTINCT region, ', ') as regions
            FROM data
            WHERE country IS NOT NULL AND country != ''
            GROUP BY country
            HAVING AVG(intensity) IS NOT NULL
            ORDER BY avg_intensity DESC;
        """)
        
        rows = cur.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "country": row[0],
                "avg_intensity": float(row[1]) if row[1] is not None else 0,
                "avg_relevance": float(row[2]) if row[2] is not None else 0,
                "record_count": row[3],
                "topics": row[4] if row[4] is not None else "",
                "regions": row[5] if row[5] is not None else ""
            })
            
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)