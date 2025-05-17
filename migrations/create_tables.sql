-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uid UUID DEFAULT gen_random_uuid() UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on uid for faster lookups
CREATE INDEX idx_users_uid ON users(uid);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Create index on role for faster lookups
CREATE INDEX idx_users_role ON users(role);

-- Production Lines Table
CREATE TABLE production_lines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    capacity_per_hour INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Work Orders Table
CREATE TABLE work_orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    estimated_time INTEGER NOT NULL, -- in minutes
    status VARCHAR(50) NOT NULL,
    completion_percentage INTEGER DEFAULT 0,
    assigned_line_id INTEGER REFERENCES production_lines(id),
    assigned_worker_id INTEGER REFERENCES users(id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    unit VARCHAR(20) NOT NULL,
    reorder_level INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Transactions Table
CREATE TABLE inventory_transactions (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventory(id),
    transaction_type VARCHAR(20) NOT NULL, -- 'in' or 'out'
    quantity INTEGER NOT NULL,
    work_order_id INTEGER REFERENCES work_orders(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Machine Table
CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    last_maintenance_date TIMESTAMP,
    next_maintenance_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Machine Logs Table
CREATE TABLE machine_logs (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER REFERENCES machines(id),
    status VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Worker Shifts Table
CREATE TABLE worker_shifts (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER REFERENCES users(id),
    shift_date DATE NOT NULL,
    shift_type VARCHAR(20) NOT NULL, -- 'morning', 'afternoon', 'night'
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Worker Productivity Table
CREATE TABLE worker_productivity (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER REFERENCES users(id),
    work_order_id INTEGER REFERENCES work_orders(id),
    quantity_completed INTEGER NOT NULL,
    time_taken INTEGER NOT NULL, -- in minutes
    quality_score INTEGER, -- 1-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- KPI Table
CREATE TABLE kpi_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    metric_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reports Table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_name VARCHAR(100) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    report_data JSONB NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 