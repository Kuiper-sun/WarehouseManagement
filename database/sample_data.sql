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