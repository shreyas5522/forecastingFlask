# Project Setup Guide

This guide provides instructions for setting up a Python Flask project with MySQL database support.

## Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3](https://www.python.org/downloads/)
- [pip (Python package installer)](https://pip.pypa.io/en/stable/installation/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [libmysqlclient-dev](https://packages.ubuntu.com/search?keywords=libmysqlclient-dev) (for Ubuntu/Debian-based systems)

## Installation

```bash
git clone https://github.com/shreyas5522/forecastingFlask.git
cd forecastingFlask
```

### 1. Installation of Required Packages

```bash
sudo apt-get install python-is-python3
sudo apt-get install python3-pip
sudo apt-get install pkg-config libmysqlclient-dev
sudo apt-get install python3-mysqldb
sudo apt install mysql-server
sudo apt-get install python3-venv
sudo apt install python3-dev nginx
sudo apt install gunicorn
```
### 2. Setup of MySQL

```bash
sudo mysql -u root -p 
```
#### MySQL Commands
> **Note:**
> Replace with your password in new_password.
```bash
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';
```
```bash
FLUSH PRIVILEGES;
```
##### Login to MySQL With Updated Commands
1. Create a MySQL database:

    ```bash
    mysql -u your_username -p
    ```

2. Create the database:

    ```sql
    CREATE DATABASE IF NOT EXISTS login;
    USE login;
    ```

3. Create the users table:

    ```sql
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(60) NOT NULL
    );
    ```

4. Exit the MySQL shell:

    ```sql
    exit
    ```

### 3. Installation of Python Packages
> **Note:**
> If want Virtual Environment for Python.

1. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

#### Install the required dependencies:

```bash

pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-WTF
pip install WTForms
pip install Flask-Login
pip install mysqlclient
pip install flask gunicorn

```

> **Note:**
> Also change the password in app.py Like -> app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:YOUR_PASSWORD@localhost/login'

### 4. Run the Python Package
```bash
python app.py
```
Ctrl + C after this because it only for teting whether all lib installed or not


## **Deployment**

1. **Allow Port:**
   ```bash
   sudo ufw allow 5000
   sudo ufw allow 80

   ```
2. **Create Gunicorn Service File:**
   ```bash
   sudo nano /etc/systemd/system/gunicorn.service
   ```
   Add the following content:
   ```ini
    [Unit]
    Description=Gunicorn instance to serve forecastingFlask
    After=network.target

    [Service]
    User=azureuser
    Group=azureuser
    WorkingDirectory=/home/azureuser/forecastingFlask
    ExecStart=/home/azureuser/forecastingFlask/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

    [Install]
    WantedBy=multi-user.target

   ```
3. **Manage Gunicorn Service:**
   ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
   ```
   Check the status:
   ```bash
   sudo systemctl status forecastingFlask
   ```

4. **Adjust Gunicorn Socket Permissions:**
   ```bash
   sudo chown your_username:www-data /home/your_username/forecastingFlask/forecastingFlask.sock
   sudo chmod 660 /home/your_username/forecastingFlask/forecastingFlask.sock
   ```

5. **NGINX Configuration:**
   ```bash
   sudo nano /etc/nginx/sites-available/forecastingFlask
   ```
   Add the following server block:
   ```nginx
   server {
        listen 80;
        server_name webforecast.tech www.webforecast.tech;  # Replace with your actual domain

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static {
            alias /home/azureuser/forecastingFlask/static;
        }

        location /media {
            alias /path/to/forecastingFlask/media;
        }

        location /uploads {
            alias /home/azureuser/forecastingFlask/uploads;
        }

        error_page 500 502 503 504 /500.html;
                    location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
   ```

6. **Create a symbolic link to enable the Nginx server block:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/forecastingFlask /etc/nginx/sites-enabled
   ```
   If there are no errors, restart Nginx:
   ```bash
    sudo nginx -t
    sudo systemctl restart nginx
   ```

7.  **Adjust Directory Permissions:**
    ```bash
    sudo chmod +x /home
    sudo chmod +x /home/azureuser
    sudo chmod +x /home/azureuser/forecastingFlask
    ```
