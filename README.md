# Data Visualization Dashboard (Flask + PostgreSQL)

![ss1](https://github.com/user-attachments/assets/d07d14ca-86ed-4dd7-ad62-d90faf3ee38d)
![ss2](https://github.com/user-attachments/assets/4405978f-73cf-4522-a9c5-e2ca57b0d590)

## 🛠 Setup Instructions

### Set up Python environment
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 🐘 PostgreSQL Setup
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

## ⚙️ Backend (Flask)

```
# Install dependencies
pip install flask psycopg2-binary flask-cors python-dotenv

# Import data (run once)
python import.py

# Start server
python app.py
```

## 💻 Frontend Setup
### Navigate to frontend directory
`cd frontend`

### Install dependencies
`npm install`

### Start development server
`npm start`

## 📦 Dependencies

### Backend (Python/Flask)
```python
# requirements.txt
flask==2.3.2
psycopg2-binary==2.9.6
flask-cors==3.0.10
python-dotenv==1.0.0
```

### Frontend (React.js)
![ss3](https://github.com/user-attachments/assets/69d128a3-a04b-4a24-8843-82bffa61931a)


