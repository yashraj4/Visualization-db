# Data Visualization Dashboard (Flask + PostgreSQL)

![Dashboard Screenshot](frontend/public/assets/ss1.jpg)
![Dashboard Screenshot](frontend/public/assets/ss2.jpg)

## 🛠 Setup Instructions

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 🐘 PostgreSQL Setup
```sql
-- Login to PostgreSQL
sudo -u postgres psql

-- Create database
CREATE DATABASE db_name;

-- Create user with password
CREATE USER user_name WITH PASSWORD 'pswd';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;

-- Exit psql
\q
```

# ⚙️ Backend (Flask)

```
# Install dependencies
pip install flask psycopg2-binary flask-cors python-dotenv

# Import data (run once)
python import.py

# Start server
python app.py
```

## 💻 Frontend Setup
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

## 📦 Dependencies

# Backend (Python/Flask)
```python
# requirements.txt
flask==2.3.2
psycopg2-binary==2.9.6
flask-cors==3.0.10
python-dotenv==1.0.0
```

# Python (React.js)

![Dashboard Screenshot](frontend/public/assets/ss3.jpg)

