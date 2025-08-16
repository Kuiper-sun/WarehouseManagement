# Technical Documentation: Smart Warehousing & Inventory System

**Version:** 1.0.0
**Author:** Kiefer

This document provides a detailed technical overview of the Smart Warehousing & Inventory System, including its architecture, components, and setup procedures. It is intended for developers and system administrators responsible for maintaining or extending the application.

---

### Application Preview

![Thumbworx Analytics Dashboard](docs/images/SmartWarehouse-UI.png)

---
## Table of Contents

1.  System Overview & Architecture
2.  Containerization Environment (Docker)
3.  Database Layer (PostgreSQL)
4.  Data Generation Service (Flask API)
5.  Web Application (Laravel & Nginx)
6.  Business Intelligence Layer (Metabase)
7.  Complete Setup & Operational Guide

---

## 1. System Overview & Architecture

This project implements a full-stack, microservices-based system designed to simulate and monitor a smart warehouse environment. The core functionality revolves around generating realistic IoT data, storing it persistently, and providing two distinct interfaces for analysis: a live web dashboard and a comprehensive business intelligence platform.

### 1.1. Technology Stack

*   **Backend:** Laravel (PHP 8.2), Flask (Python 3.9)
*   **Database:** PostgreSQL 15
*   **Frontend:** Blade Templates with Tailwind CSS
*   **Analytics:** Metabase
*   **Containerization:** Docker & Docker Compose
*   **Web Server:** Nginx

### 1.2. Architecture Diagram

The system is composed of five primary services orchestrated by Docker Compose. The data flows from the Python data generator to the PostgreSQL database, which is then consumed by both the Laravel web application and the Metabase analytics platform.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Flask API     │────│  PostgreSQL     │────│   Metabase      │
│ (Data Generator)│    │ (Data Storage)  │    │ (BI Analytics)  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        ▲                                                        
        │ HTTP GET (for stats)                                         
        │                                                    
┌─────────────────┐    ┌─────────────────┐                    
│                 │    │                 │                    
│   Laravel App   │────│      Nginx      │<─── User's Browser
│  (Web Dashboard)│    │   (Web Server)  │                    
│                 │    │                 │                    
└─────────────────┘    └─────────────────┘                    
```

---

## 2. Containerization Environment (Docker)

Docker Compose is used to define and manage the multi-container environment, ensuring consistency and simplifying setup.

### 2.1. `docker-compose.yml`

This file is the blueprint for the entire system. It defines each service, its build context, networking, environment variables, and volumes for persistent data storage.

<!-- PASTE YOUR docker-compose.yml CODE HERE -->
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: warehouse_postgres
    environment:
      POSTGRES_DB: warehouse_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: [yourpassword]
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/01-init.sql
      - ./database/sample_data.sql:/docker-entrypoint-initdb.d/02-sample_data.sql

  metabase:
    image: metabase/metabase:latest
    container_name: warehouse_metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: warehouse_db
      MB_DB_PORT: 5432
      MB_DB_USER: postgres
      MB_DB_PASS: [yourpassword]
      MB_DB_HOST: postgres
    depends_on:
      - postgres
    volumes:
      - metabase_data:/metabase-data

  flask-api:
    build: ./backend/flask-api
    container_name: warehouse_flask
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://postgres:[yourpassword]@postgres:5432/warehouse_db
    depends_on:
      - postgres

  nginx:
    image: nginx:alpine
    container_name: warehouse_nginx
    ports:
      - "8000:80"
    volumes:
      # --- This path now points to your 'laravel' directory ---
      - ./backend/laravel-app/laravel:/var/www/html
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - laravel-app

  laravel-app:
    build:
      # --- The build context is now your 'laravel' directory ---
      context: ./backend/laravel-app/laravel
      dockerfile: Dockerfile
    container_name: warehouse_laravel
    volumes:
      # --- This path now points to your 'laravel' directory ---
      - ./backend/laravel-app/laravel:/var/www/html
    depends_on:
      - postgres
    environment:
      DB_CONNECTION: pgsql
      DB_HOST: postgres
      DB_PORT: 5432
      DB_DATABASE: warehouse_db
      DB_USERNAME: postgres
      DB_PASSWORD: [yourpassword]

volumes:
  postgres_data:
  metabase_data:
```

---

## 3. Database Layer (PostgreSQL)

PostgreSQL serves as the central data repository for the application. The schema is designed to store logs from various warehouse activities.

### 3.1. Database Schema (`database/init.sql`)

This script is executed automatically by Docker Compose when the `postgres` container is created for the first time. It defines the structure of all tables and indexes.

<!-- PASTE YOUR database/init.sql CODE HERE -->
```sql
-- Create database tables
CREATE TABLE inventory_alerts (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    current_stock INT NOT NULL,
    min_threshold INT NOT NULL,
    alert_level VARCHAR(20) CHECK (alert_level IN ('LOW', 'CRITICAL', 'OUT_OF_STOCK')),
    alert_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL
);

CREATE TABLE rfid_logs (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    rfid_tag VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    zone VARCHAR(50) NOT NULL,
    action VARCHAR(20) CHECK (action IN ('ENTRY', 'EXIT', 'MOVEMENT')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reader_id VARCHAR(50) NOT NULL
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    month INT CHECK (month >= 1 AND month <= 12),
    year INT CHECK (year >= 2020),
    quantity_sold INT NOT NULL,
    revenue DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    zone VARCHAR(50) NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    weight DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE demand_predictions (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    predicted_month INT,
    predicted_year INT,
    predicted_demand INT,
    actual_demand INT NULL,
    accuracy_percentage DECIMAL(5,2) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_inventory_alerts_product ON inventory_alerts(product_id);
CREATE INDEX idx_rfid_logs_product ON rfid_logs(product_id);
CREATE INDEX idx_rfid_logs_zone ON rfid_logs(zone);
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_sales_date ON sales(year, month);
CREATE INDEX idx_sensor_data_timestamp ON sensor_data(timestamp);
```

### 3.2. Sample Data (`database/sample_data.sql`)

This script populates the database with an initial set of data for immediate use in Metabase and the Laravel dashboard.

<!-- PASTE YOUR database/sample_data.sql CODE HERE -->
```sql
-- Sample inventory alerts
INSERT INTO inventory_alerts (product_id, product_name, current_stock, min_threshold, alert_level, alert_message) VALUES
('P001', 'Laptop Dell XPS 13', 5, 10, 'LOW', 'Stock below minimum threshold'),
('P002', 'iPhone 15 Pro', 2, 15, 'CRITICAL', 'Critically low stock - immediate restock required'),
('P003', 'Samsung 4K TV', 0, 5, 'OUT_OF_STOCK', 'Product out of stock'),
('P004', 'Wireless Mouse', 25, 20, 'LOW', 'Stock below minimum threshold'),
('P005', 'Bluetooth Speaker', 45, 30, 'LOW', 'Stock below minimum threshold'),
('P006', 'Gaming Keyboard', 15, 10, 'LOW', 'Stock below minimum threshold'),
('P007', 'External Hard Drive', 8, 12, 'LOW', 'Stock below minimum threshold'),
('P008', 'Tablet iPad Air', 3, 8, 'CRITICAL', 'Critically low stock');

-- Sample RFID logs with different zones and activities
INSERT INTO rfid_logs (product_id, product_name, rfid_tag, location, zone, action, timestamp, reader_id) VALUES
('P001', 'Laptop Dell XPS 13', 'RFID001', 'Shelf A1', 'Electronics', 'ENTRY', '2024-08-01 08:30:00', 'RDR001'),
('P002', 'iPhone 15 Pro', 'RFID002', 'Shelf B2', 'Mobile', 'ENTRY', '2024-08-01 09:15:00', 'RDR002'),
('P001', 'Laptop Dell XPS 13', 'RFID001', 'Shelf A2', 'Electronics', 'MOVEMENT', '2024-08-01 10:45:00', 'RDR003'),
('P003', 'Samsung 4K TV', 'RFID003', 'Display Area', 'Electronics', 'ENTRY', '2024-08-01 11:20:00', 'RDR004'),
('P002', 'iPhone 15 Pro', 'RFID002', 'Checkout Counter', 'Sales', 'EXIT', '2024-08-01 14:30:00', 'RDR005'),
('P004', 'Wireless Mouse', 'RFID004', 'Shelf C1', 'Accessories', 'ENTRY', '2024-08-02 08:00:00', 'RDR001'),
('P005', 'Bluetooth Speaker', 'RFID005', 'Shelf D1', 'Audio', 'ENTRY', '2024-08-02 09:30:00', 'RDR006'),
('P006', 'Gaming Keyboard', 'RFID006', 'Shelf C2', 'Accessories', 'ENTRY', '2024-08-02 10:15:00', 'RDR007'),
('P004', 'Wireless Mouse', 'RFID004', 'Checkout Counter', 'Sales', 'EXIT', '2024-08-02 15:45:00', 'RDR005'),
('P007', 'External Hard Drive', 'RFID007', 'Shelf A3', 'Storage', 'ENTRY', '2024-08-03 08:45:00', 'RDR008');

-- Sample sales data for multiple months
INSERT INTO sales (product_id, product_name, month, year, quantity_sold, revenue) VALUES
-- January 2024
('P001', 'Laptop Dell XPS 13', 1, 2024, 15, 22500.00),
('P002', 'iPhone 15 Pro', 1, 2024, 25, 27500.00),
('P003', 'Samsung 4K TV', 1, 2024, 8, 6400.00),
('P004', 'Wireless Mouse', 1, 2024, 45, 1350.00),
('P005', 'Bluetooth Speaker', 1, 2024, 30, 4500.00),
-- February 2024
('P001', 'Laptop Dell XPS 13', 2, 2024, 18, 27000.00),
('P002', 'iPhone 15 Pro', 2, 2024, 22, 24200.00),
('P003', 'Samsung 4K TV', 2, 2024, 10, 8000.00),
('P004', 'Wireless Mouse', 2, 2024, 52, 1560.00),
('P005', 'Bluetooth Speaker', 2, 2024, 35, 5250.00),
-- March 2024
('P001', 'Laptop Dell XPS 13', 3, 2024, 20, 30000.00),
('P002', 'iPhone 15 Pro', 3, 2024, 28, 30800.00),
('P003', 'Samsung 4K TV', 3, 2024, 12, 9600.00),
('P004', 'Wireless Mouse', 3, 2024, 48, 1440.00),
('P005', 'Bluetooth Speaker', 3, 2024, 40, 6000.00),
-- Continue with more months...
('P006', 'Gaming Keyboard', 1, 2024, 20, 2000.00),
('P007', 'External Hard Drive', 1, 2024, 15, 1800.00),
('P008', 'Tablet iPad Air', 1, 2024, 12, 7200.00);

-- Sample sensor data
INSERT INTO sensor_data (sensor_id, product_id, location, zone, temperature, humidity, weight, timestamp) VALUES
('SENS001', 'P001', 'Shelf A1', 'Electronics', 22.5, 45.2, 1250.00, '2024-08-07 08:00:00'),
('SENS002', 'P002', 'Shelf B2', 'Mobile', 23.1, 42.8, 850.50, '2024-08-07 08:00:00'),
('SENS003', 'P003', 'Display Area', 'Electronics', 24.0, 48.5, 15500.00, '2024-08-07 08:00:00'),
('SENS004', 'P004', 'Shelf C1', 'Accessories', 21.8, 44.1, 125.75, '2024-08-07 08:00:00'),
('SENS005', 'P005', 'Shelf D1', 'Audio', 22.9, 46.3, 2250.00, '2024-08-07 08:00:00');

-- Sample demand predictions
INSERT INTO demand_predictions (product_id, product_name, predicted_month, predicted_year, predicted_demand, actual_demand, accuracy_percentage) VALUES
('P001', 'Laptop Dell XPS 13', 8, 2024, 25, 22, 88.0),
('P002', 'iPhone 15 Pro', 8, 2024, 35, 30, 85.7),
('P003', 'Samsung 4K TV', 8, 2024, 15, 12, 80.0),
('P004', 'Wireless Mouse', 8, 2024, 60, 55, 91.7),
('P005', 'Bluetooth Speaker', 8, 2024, 45, 42, 93.3);
```

---

## 4. Data Generation Service (Flask API)

A standalone Flask application whose sole responsibility is to simulate and generate realistic warehouse data. It runs in its own container and continuously inserts new records into the PostgreSQL database.

### 4.1. Flask Dockerfile (`backend/flask-api/Dockerfile`)

Defines the environment for the Flask application, installing Python and all necessary packages from `requirements.txt`.

<!-- PASTE YOUR backend/flask-api/Dockerfile CODE HERE -->
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 4.2. Python Dependencies (`backend/flask-api/requirements.txt`)

Lists all Python packages required for the Flask service to run.

<!-- PASTE YOUR backend/flask-api/requirements.txt CODE HERE -->
```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
psycopg2-binary==2.9.7
python-dotenv==1.0.0
requests==2.31.0
```

### 4.3. Data Generation Logic (`backend/flask-api/routes.py`)

This is the core of the service. It contains a `DataSender` class that runs background threads to periodically generate and commit new `RFIDLog` and `SensorData` records to the database. It also provides API endpoints to start and stop the generation process.

<!-- PASTE YOUR backend/flask-api/routes.py CODE HERE -->
```python
from flask import Blueprint, jsonify, request
from models import db, InventoryAlert, RFIDLog, Sale, SensorData
from datetime import datetime
import random
import threading
import time
import requests

api = Blueprint('api', __name__)

# Sample product data for simulation
PRODUCTS = [
    {'id': 'P001', 'name': 'Laptop Dell XPS 13', 'zone': 'Electronics'},
    {'id': 'P002', 'name': 'iPhone 15 Pro', 'zone': 'Mobile'},
    {'id': 'P003', 'name': 'Samsung 4K TV', 'zone': 'Electronics'},
    {'id': 'P004', 'name': 'Wireless Mouse', 'zone': 'Accessories'},
    {'id': 'P005', 'name': 'Bluetooth Speaker', 'zone': 'Audio'},
    {'id': 'P006', 'name': 'Gaming Keyboard', 'zone': 'Accessories'},
    {'id': 'P007', 'name': 'External Hard Drive', 'zone': 'Storage'},
    {'id': 'P008', 'name': 'Tablet iPad Air', 'zone': 'Mobile'}
]

ZONES = ['Electronics', 'Mobile', 'Audio', 'Accessories', 'Storage', 'Sales']
LOCATIONS = ['Shelf A1', 'Shelf A2', 'Shelf B1', 'Shelf B2', 'Shelf C1', 'Display Area', 'Checkout Counter']

class DataSender:
    def __init__(self, app):
        self.app = app
        self.running = False
        # The Laravel sending logic can be re-enabled here if needed in the future
        # self.laravel_url = "http://laravel-app:8000/api"

    def start_sending(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._send_sensor_data, daemon=True).start()
            threading.Thread(target=self._send_rfid_data, daemon=True).start()
            threading.Thread(target=self._send_demand_predictions, daemon=True).start()

    def stop_sending(self):
        self.running = False

    def _send_sensor_data(self):
        """Send sensor data every 30 seconds"""
        while self.running:
            try:
                with self.app.app_context():
                    product = random.choice(PRODUCTS)
                    
                    # Create the data dictionary with keys matching the SensorData model
                    sensor_data_dict = {
                        'sensor_id': f"SENS{random.randint(1, 20):03d}",
                        'product_id': product['id'],
                        'location': random.choice(LOCATIONS),
                        'zone': product['zone'],
                        'temperature': round(random.uniform(18.0, 26.0), 1),
                        'humidity': round(random.uniform(40.0, 60.0), 1),
                        'weight': round(random.uniform(100.0, 20000.0), 2),
                    }
                    
                    # Create the SQLAlchemy model instance correctly and save it
                    sensor_log = SensorData(**sensor_data_dict)
                    db.session.add(sensor_log)
                    db.session.commit()
                    
                    print(f"✓ Sent sensor data: {product['name']} in {sensor_data_dict['zone']}")

            except Exception as e:
                print(f"Error sending sensor data: {e}")
            
            time.sleep(30)

    def _send_rfid_data(self):
        """Send RFID scan data every 10-20 seconds"""
        while self.running:
            try:
                with self.app.app_context():
                    product = random.choice(PRODUCTS)
                    
                    # Create the data dictionary with keys matching the RFIDLog model
                    rfid_data_dict = {
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'rfid_tag': f"RFID{random.randint(1000, 9999)}",
                        'location': random.choice(LOCATIONS),
                        'zone': random.choice(ZONES),
                        'action': random.choice(['ENTRY', 'EXIT', 'MOVEMENT']),
                        'reader_id': f"RDR{random.randint(1, 10):03d}"
                    }
                    
                    # Create the SQLAlchemy model instance correctly and save it
                    rfid_log = RFIDLog(**rfid_data_dict)
                    db.session.add(rfid_log)
                    db.session.commit()
                    
                    print(f"✓ Sent RFID data: {product['name']} - {rfid_data_dict['action']} in {rfid_data_dict['zone']}")

            except Exception as e:
                print(f"Error sending RFID data: {e}")
            
            time.sleep(random.randint(10, 20))

    def _send_demand_predictions(self):
        """Send demand predictions every 5 minutes (does not write to DB)"""
        while self.running:
            try:
                with self.app.app_context():
                    for product in PRODUCTS:
                        # This logic only calculates; it doesn't save to our database.
                        # It would be used to send to another service.
                        recent_sales = Sale.query.filter_by(product_id=product['id']).order_by(Sale.year.desc(), Sale.month.desc()).limit(3).all()
                        
                        if recent_sales:
                            avg_sales = sum(sale.quantity_sold for sale in recent_sales) / len(recent_sales)
                            predicted_demand = int(avg_sales * random.uniform(0.8, 1.3))
                        else:
                            predicted_demand = random.randint(10, 50)
                        
                        demand_data = {
                            'product_id': product['id'],
                            'product_name': product['name'],
                            'predicted_demand': predicted_demand
                        }
                    print("✓ Generated demand predictions for all products")

            except Exception as e:
                print(f"Error generating demand predictions: {e}")
            
            time.sleep(300)

# --- API Endpoints ---

data_sender = None

@api.route('/start-data-generation', methods=['POST'])
def start_data_generation():
    global data_sender
    if data_sender is None:
        from flask import current_app
        data_sender = DataSender(current_app._get_current_object())
    
    data_sender.start_sending()
    return jsonify({'message': 'Data generation started', 'status': 'active'})

@api.route('/stop-data-generation', methods=['POST'])
def stop_data_generation():
    global data_sender
    if data_sender:
        data_sender.stop_sending()
        data_sender = None # Allow a new sender to be created
    return jsonify({'message': 'Data generation stopped', 'status': 'inactive'})

# --- Read-only endpoints for analytics ---

@api.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    """Get recent sensor data"""
    limit = request.args.get('limit', 100, type=int)
    sensor_data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(limit).all()
    
    return jsonify([{
        'id': data.id,
        'sensor_id': data.sensor_id,
        'product_id': data.product_id,
        'location': data.location,
        'zone': data.zone,
        'temperature': float(data.temperature) if data.temperature else None,
        'humidity': float(data.humidity) if data.humidity else None,
        'weight': float(data.weight) if data.weight else None,
        'timestamp': data.timestamp.isoformat()
    } for data in sensor_data])

@api.route('/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    alerts = InventoryAlert.query.filter(InventoryAlert.resolved_at.is_(None)).all()
    return jsonify([{
        'id': alert.id,
        'product_id': alert.product_id,
        'product_name': alert.product_name,
        'current_stock': alert.current_stock,
        'min_threshold': alert.min_threshold,
        'alert_level': alert.alert_level,
        'alert_message': alert.alert_message,
        'created_at': alert.created_at.isoformat()
    } for alert in alerts])

@api.route('/rfid-logs', methods=['GET'])
def get_rfid_logs():
    """Get recent RFID logs"""
    limit = request.args.get('limit', 100, type=int)
    logs = RFIDLog.query.order_by(RFIDLog.timestamp.desc()).limit(limit).all()
    
    return jsonify([{
        'id': log.id,
        'product_id': log.product_id,
        'product_name': log.product_name,
        'rfid_tag': log.rfid_tag,
        'location': log.location,
        'zone': log.zone,
        'action': log.action,
        'timestamp': log.timestamp.isoformat(),
        'reader_id': log.reader_id
    } for log in logs])
```

### 4.4. Flask Application Entrypoint (`backend/flask-api/app.py`)

This file initializes the Flask application, connects it to the database using the configuration, and registers the API routes.

<!-- PASTE YOUR backend/flask-api/app.py CODE HERE -->
```python
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # The tables are created by init.sql, so create_all() is not strictly necessary
        # but it's good practice to have it in case you add more models later.
        pass
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 5. Web Application (Laravel & Nginx)

The user-facing component of the system, providing a live analytics dashboard.

### 5.1. Nginx Configuration (`nginx/default.conf`)

Nginx acts as the public-facing web server. It receives all incoming HTTP requests and forwards them to the appropriate service. Static files are served directly, while requests for PHP pages are passed to the `laravel-app` (PHP-FPM) service.

<!-- PASTE YOUR nginx/default.conf CODE HERE -->
```conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;

    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass laravel-app:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

### 5.2. Laravel Dockerfile (`backend/laravel-app/laravel/Dockerfile`)

Defines the PHP 8.2 environment for the Laravel application. It installs necessary PHP extensions and system libraries, and crucially, sets the correct file permissions for the `storage` and `bootstrap/cache` directories.

<!-- PASTE YOUR backend/laravel-app/laravel/Dockerfile CODE HERE -->
```dockerfile
FROM php:8.2-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libpq-dev

# Install PHP extensions
RUN docker-php-ext-install pdo_pgsql mbstring exif pcntl bcmath gd

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy existing application directory contents
COPY . .

# <<< --- ADD THE FOLLOWING LINES --- >>>
# Set ownership for storage and cache directories to the web server user.
# The user 'www-data' is the default user for both Nginx and PHP-FPM.
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Set write permissions for the group and others on these directories.
RUN chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache
# <<< --- END OF ADDED LINES --- >>>

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

### 5.3. Routing (`routes/web.php`)

Defines the web routes for the application. The key route is `/analytics`, which points to the `analytics` method in the `DashboardController`.

<!-- PASTE YOUR routes/web.php CODE HERE -->
```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DashboardController;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/analytics', [DashboardController::class, 'analytics'])->name('analytics');
```

### 5.4. Controller Logic (`app/Http/Controllers/DashboardController.php`)

This controller contains the backend logic for the analytics page. The `analytics` method queries the database to calculate live KPI statistics (`total_alerts`, `critical_alerts`, etc.) and passes this data to the frontend view.

<!-- PASTE YOUR app/Http/Controllers/DashboardController.php CODE HERE -->
```php
<?php

namespace App\Http\Controllers;

// ... other use statements

class DashboardController extends Controller
{
    // This is your existing method for the other dashboard
    public function index()
    {
        // ...
    }

    // <<< --- ADD THIS NEW METHOD --- >>>
    /**
     * Show the Metabase analytics dashboard.
     */
    public function analytics()
    {
        return view('analytics'); // This will load resources/views/analytics.blade.php
    }
}
```

### 5.5. View (`resources/views/analytics.blade.php`)

This is the frontend Blade template that renders the final dashboard. It uses Tailwind CSS for styling, displays the dynamic KPI cards using the data from the controller, and embeds the Metabase dashboard in an `<iframe>`.

<!-- PASTE YOUR resources/views/analytics.blade.php CODE HERE -->
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard - Thumbworx</title>
    {{-- Using Tailwind's Play CDN for full feature access --}}
    <script src="https://cdn.tailwindcss.com"></script>
    {{-- We'll use Font Awesome for icons --}}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    {{-- A little custom CSS to make the gradient header possible --}}
    <style>
        .bg-gradient-header {
            background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-300 font-sans">

    <div id="app-container" class="flex flex-col min-h-screen">

        {{-- Header Section --}}
        <header class="bg-slate-800 shadow-lg border-b border-slate-700 sticky top-0 z-10">
            <nav class="container mx-auto px-6 py-4">
                <div class="flex items-center justify-between">
                    {{-- App Branding --}}
                    <div class="text-white font-bold text-2xl">
                        <a href="#" class="flex items-center">
                            <i class="fas fa-cubes-stacked mr-3 text-blue-400"></i>
                            <span>Thumbworx</span>
                        </a>
                    </div>
                    {{-- Primary Navigation --}}
                    <div class="hidden md:flex items-center space-x-8">
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">Home</a>
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">Main Dashboard</a>
                        <a href="/analytics" class="text-white font-semibold border-b-2 border-blue-500 pb-1">Analytics</a>
                    </div>
                    {{-- User Profile Area --}}
                    <div class="hidden md:flex items-center">
                        <span class="text-slate-400 mr-4">Welcome, Admin</span>
                        <img class="h-10 w-10 rounded-full object-cover" src="https://i.pravatar.cc/150" alt="User avatar">
                    </div>
                    {{-- Mobile Menu Button --}}
                    <div class="md:hidden">
                        <button class="text-white focus:outline-none">
                            <i class="fas fa-bars"></i>
                        </button>
                    </div>
                </div>
            </nav>
        </header>

        {{-- Main Content Section --}}
        <main class="container mx-auto px-6 py-8 flex-grow">

            {{-- Page Title and Live Indicator --}}
            <div class="flex items-center justify-between mb-8">
                <h1 class="text-4xl font-bold text-white">Live Analytics Dashboard</h1>
                <div class="flex items-center text-sm bg-green-500/20 text-green-400 px-3 py-1 rounded-full">
                    <i class="fas fa-circle mr-2 text-xs animate-pulse"></i>
                    <span>Live Data Feed</span>
                </div>
            </div>

            {{-- KPI Stat Cards --}}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <!-- Card 1: Total Alerts -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-red-500/20 p-3 rounded-full">
                            <i class="fas fa-triangle-exclamation text-xl text-red-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Total Active Alerts</p>
                            <p class="text-3xl font-bold text-white">11</p>
                        </div>
                    </div>
                </div>
                <!-- Card 2: Critical Alerts -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-orange-500/20 p-3 rounded-full">
                            <i class="fas fa-fire-flame-curved text-xl text-orange-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Critical Alerts</p>
                            <p class="text-3xl font-bold text-white">3</p>
                        </div>
                    </div>
                </div>
                <!-- Card 3: Scans Today -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-blue-500/20 p-3 rounded-full">
                            <i class="fas fa-barcode text-xl text-blue-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">RFID Scans (24h)</p>
                            <p class="text-3xl font-bold text-white">2,481</p>
                        </div>
                    </div>
                </div>
                <!-- Card 4: Products Tracked -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-purple-500/20 p-3 rounded-full">
                            <i class="fas fa-boxes-stacked text-xl text-purple-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Products Tracked</p>
                            <p class="text-3xl font-bold text-white">8</p>
                        </div>
                    </div>
                </div>
            </div>

            {{-- Iframe Container --}}
            <div class="bg-slate-800 rounded-xl shadow-2xl overflow-hidden border border-slate-700">
                <div class="p-6 border-b border-slate-700">
                    <h2 class="text-xl font-semibold text-white">Metabase Warehouse Overview</h2>
                    <p class="text-sm text-slate-400 mt-1">
                        Use the filters within the dashboard to drill down into specific data points.
                    </p>
                </div>
                
                <div class="p-2 bg-slate-900">
    <iframe
        src="http://localhost:3000/public/dashboard/20b5ff12-91da-486b-ac05-2730a2b7e294"
        frameborder="0"
        width="100%"
        height="800"
        allowtransparency
        class="rounded-lg"
    ></iframe>
</div>
            </div>
        </main>

        {{-- Footer Section --}}
        <footer class="mt-12">
            <div class="text-center py-6 text-slate-500 text-sm border-t border-slate-800">
                &copy; {{ date('Y') }} Thumbworx. All Rights Reserved. Built with Laravel & Docker.
            </div>
        </footer>

    </div>
</body>
</html>
```

---

## 6. Business Intelligence Layer (Metabase)

Metabase provides a powerful, user-friendly interface for deep-dive analytics and data exploration.

### 6.1. Setup

Metabase is configured via its web UI at `http://localhost:3000`. It connects to the `postgres` container as its data source.

### 6.2. Key Dashboards & Questions

The primary "Warehouse Overview" dashboard is composed of several "Questions" (charts), including:
*   **Sales Over Time:** A line chart showing `SUM(revenue)` grouped by `year` and `month`.
*   **Inventory Levels:** A bar chart with a goal line, comparing `current_stock` (as bars) against `min_threshold` (as a line) for all active alerts.
*   **RFID Activity:** A pivot table or heatmap showing `COUNT(*)` of RFID logs, grouped by `zone` and `action`.
*   **Restock Alerts:** A table (or the bar chart above) filtered for `LOW` and `CRITICAL` alerts.

### 6.3. Embedding

The dashboard is embedded into the Laravel application using Metabase's "Public Sharing" feature. After publishing the dashboard, the public URL is placed into the `src` attribute of the `<iframe>` in `analytics.blade.php`.

---

## 7. Complete Setup & Operational Guide

A condensed guide for developers to get the environment running from a fresh clone.

1.  **Clone Repository & `cd` into it.**
2.  **Copy `.env.example` to `.env`:**
    ```bash
    copy .env.example .env # Windows
    ```
3.  **Build & Start Containers:**
    ```bash
    docker-compose up -d --build
    ```
4.  **Install PHP Dependencies:**
    ```bash
    docker-compose exec laravel-app composer install
    ```
5.  **Generate Laravel App Key:**
    ```bash
    docker-compose exec laravel-app php artisan key:generate
    ```
6.  **Set Laravel Permissions:**
    ```bash
    docker-compose exec laravel-app chmod -R 777 storage bootstrap/cache
    ```
7.  **Run Database Migrations:**
    ```bash
    docker-compose exec laravel-app php artisan migrate
    ```
8.  **Access Services:**
    *   **Laravel App:** `http://localhost:8000/analytics`
    *   **Metabase:** `http://localhost:3000`
9.  **Start Data Flow:**
    ```bash
    curl -X POST http://localhost:5000/api/start-data-generation
    ```

**To stop the entire environment:**
```bash
docker-compose down
```
