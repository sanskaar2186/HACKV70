-- First, insert sample users (required for foreign keys)
INSERT INTO users (email, password_hash, name, role) VALUES
('admin@kaamchore.com', 'hashed_password_here', 'Admin User', 'admin'),
('worker1@kaamchore.com', 'hashed_password_here', 'Worker One', 'worker'),
('worker2@kaamchore.com', 'hashed_password_here', 'Worker Two', 'worker');

-- Then insert production lines (required for work orders)
INSERT INTO production_lines (name, status, capacity_per_hour) VALUES
('Line 1', 'active', 100),
('Line 2', 'idle', 150),
('Line 3', 'maintenance', 120);

-- Now insert work orders (depends on production_lines and users)
INSERT INTO work_orders (order_number, product_name, quantity, estimated_time, status, completion_percentage, assigned_line_id, assigned_worker_id, start_time, end_time) VALUES
('WO-001', 'Product A', 500, 120, 'in_progress', 45, 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '2 hours'),
('WO-002', 'Product B', 300, 90, 'pending', 0, 2, 3, NULL, NULL),
('WO-003', 'Product C', 200, 60, 'completed', 100, 1, 2, CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP);

-- Insert inventory items
INSERT INTO inventory (item_name, category, quantity, unit, reorder_level) VALUES
('Raw Material X', 'Raw Materials', 50, 'kg', 100),
('Component Y', 'Components', 20, 'pcs', 50),
('Material Z', 'Raw Materials', 5, 'kg', 30);

-- Insert inventory transactions (depends on inventory and work_orders)
INSERT INTO inventory_transactions (inventory_id, transaction_type, quantity, work_order_id, notes) VALUES
(1, 'out', 20, 1, 'Used in Product A production'),
(2, 'in', 50, NULL, 'New stock received'),
(3, 'out', 5, 1, 'Used in Product A production');

-- Insert machines
INSERT INTO machines (name, type, status, last_maintenance_date, next_maintenance_date, line_id) VALUES
('Machine 1', 'Assembly', 'active', CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP + INTERVAL '20 days', 1),
('Machine 2', 'Packaging', 'maintenance', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP + INTERVAL '25 days', 1),
('Machine 3', 'Testing', 'idle', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP + INTERVAL '29 days', 2);

-- Insert machine logs (depends on machines)
INSERT INTO machine_logs (machine_id, status, start_time, end_time, notes) VALUES
(1, 'running', CURRENT_TIMESTAMP - INTERVAL '4 hours', NULL, 'Normal operation'),
(2, 'maintenance', CURRENT_TIMESTAMP - INTERVAL '2 hours', NULL, 'Scheduled maintenance'),
(3, 'idle', CURRENT_TIMESTAMP - INTERVAL '1 hour', NULL, 'Waiting for work order');

-- Insert worker shifts (depends on users)
INSERT INTO worker_shifts (worker_id, shift_date, shift_type, start_time, end_time, status) VALUES
(2, CURRENT_DATE, 'morning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '8 hours', 'active'),
(3, CURRENT_DATE, 'afternoon', CURRENT_TIMESTAMP + INTERVAL '8 hours', CURRENT_TIMESTAMP + INTERVAL '16 hours', 'scheduled');

-- Insert worker productivity (depends on users and work_orders)
INSERT INTO worker_productivity (worker_id, work_order_id, quantity_completed, time_taken, quality_score) VALUES
(2, 1, 225, 60, 95),
(3, 1, 150, 45, 92);

-- Insert KPI metrics
INSERT INTO kpi_metrics (metric_name, metric_value, metric_date, category) VALUES
('revenue', 50000.00, CURRENT_DATE, 'financial'),
('efficiency', 85.50, CURRENT_DATE, 'production'),
('quality', 94.20, CURRENT_DATE, 'quality');

-- Insert reports (depends on users)
INSERT INTO reports (report_name, report_type, report_data, created_by) VALUES
('Daily Production Report', 'production', '{"total_orders": 3, "completed_orders": 1, "in_progress": 1}', 1),
('Inventory Status Report', 'inventory', '{"low_stock_items": 2, "total_items": 3}', 1); 