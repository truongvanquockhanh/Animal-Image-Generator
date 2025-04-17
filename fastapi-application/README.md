# FastAPI Bug Tracker

This is a **FastAPI-based bug tracking system** using **SQLAlchemy, Alembic, and PostgreSQL**.

## 🚀 Installation Guide

### 1️⃣ Install **Pyenv** and **Python 3.11.11**

Make sure you have **Pyenv** installed:

```sh
curl https://pyenv.run | bash
```

```sh

pyenv install 3.11.11
pyenv virtualenv 3.11.11 bugtrackerenv
pyenv activate bugtrackerenv
```

- U had venv for project

# 📦 Install Project Dependencies

Install requirements from the file:

```sh
pip install -r requirements.txt
```

# ⚙️ Environment Configuration

Create a .env file in your project root:

```sh
DATABASE_URL=postgresql+psycopg2://your_user:your_password@localhost:5432/your_db_name
SECRET_KEY=your_secret_key_here
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
```

Replace with your actual PostgreSQL connection details.

# 🛠 Alembic Database Migrations

Initialize Alembic (only once):

```sh
alembic init migrations
```

Set the correct DB URL in alembic.ini or env.py.

Generate and apply migrations:

```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

# 🧪 Run the App

```sh
fastapi dev main.py
```

# 📚 API Documentation

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

# Deployment ( gubicorn and nginx )

```sh
pip install gunicorn
```

Create a systemd service file /etc/systemd/system/fastapi.service:

```sh
[Unit]
Description=FastAPI app with Gunicorn
After=network.target

[Service]
User=yourusername
Group=yourusername
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000
Restart=always

[Install]
WantedBy=multi-user.target
```

then:

```sh
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

- Now, you app are running at post: 9000
- After that, u need config nginx to connect to app at port: 9000

# Nginx

- Install nginx:

```sh
sudo apt update
sudo apt install nginx
```

- Then create two Nginx config files:
- 📁 /etc/nginx/sites-available/your_file.space:

```file
server {
    listen 80;
    server_name your_domain;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the sites:

```sh

sudo ln -s /etc/nginx/sites-available/your_file.space /etc/nginx/sites-enabled/
```

Check Nginx and restart:

```sh
sudo nginx -t
sudo systemctl restart nginx
```
