-- Add supervisor_id column to production_lines table
ALTER TABLE production_lines
ADD COLUMN supervisor_id UUID REFERENCES users(uid);

-- Create index for faster lookups
CREATE INDEX idx_production_lines_supervisor ON production_lines(supervisor_id);

-- Update existing production lines to assign supervisors
UPDATE production_lines
SET supervisor_id = (SELECT uid FROM users WHERE role = 'supervisor' LIMIT 1)
WHERE supervisor_id IS NULL; 