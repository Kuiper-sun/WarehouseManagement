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