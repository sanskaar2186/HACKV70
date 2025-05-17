-- Add line_id column to worker_shifts table
ALTER TABLE worker_shifts
ADD COLUMN line_id INTEGER REFERENCES production_lines(id);

-- Create index for faster lookups
CREATE INDEX idx_worker_shifts_line ON worker_shifts(line_id);

-- Add current_task column if it doesn't exist
ALTER TABLE worker_shifts
ADD COLUMN IF NOT EXISTS current_task TEXT;

-- Add status column if it doesn't exist
ALTER TABLE worker_shifts
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active'; 