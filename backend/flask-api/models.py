from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class InventoryAlert(db.Model):
    __tablename__ = 'inventory_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    current_stock = db.Column(db.Integer, nullable=False)
    min_threshold = db.Column(db.Integer, nullable=False)
    alert_level = db.Column(db.String(20), nullable=False)
    alert_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class RFIDLog(db.Model):
    __tablename__ = 'rfid_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    rfid_tag = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reader_id = db.Column(db.String(50), nullable=False)

class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Numeric(5, 2))
    humidity = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(10, 2))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)