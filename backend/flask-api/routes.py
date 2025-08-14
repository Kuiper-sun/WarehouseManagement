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