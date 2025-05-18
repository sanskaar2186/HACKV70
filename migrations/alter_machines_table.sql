-- Add line_id column to machines table
ALTER TABLE machines ADD COLUMN line_id INTEGER REFERENCES production_lines(id);

-- Update existing machines with line_id
UPDATE machines SET line_id = 1 WHERE id = 1;
UPDATE machines SET line_id = 1 WHERE id = 2;
UPDATE machines SET line_id = 2 WHERE id = 3;

-- Add assigned_worker_id column to machines table
ALTER TABLE machines
ADD COLUMN assigned_worker_id INTEGER REFERENCES users(id);

-- Create index for faster lookups
CREATE INDEX idx_machines_worker ON machines(assigned_worker_id); 