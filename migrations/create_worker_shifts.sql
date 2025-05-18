CREATE TABLE IF NOT EXISTS worker_shifts (
    id SERIAL PRIMARY KEY,
    worker_id INTEGER NOT NULL,
    line_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('active', 'completed', 'cancelled')) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (worker_id) REFERENCES users(id),
    FOREIGN KEY (line_id) REFERENCES production_lines(id)
);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_worker_shifts_updated_at
    BEFORE UPDATE ON worker_shifts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();