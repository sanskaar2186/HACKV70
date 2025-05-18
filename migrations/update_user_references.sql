-- First, drop existing foreign key constraints
ALTER TABLE work_orders DROP CONSTRAINT IF EXISTS work_orders_assigned_worker_id_fkey;
ALTER TABLE worker_shifts DROP CONSTRAINT IF EXISTS worker_shifts_worker_id_fkey;
ALTER TABLE worker_productivity DROP CONSTRAINT IF EXISTS worker_productivity_worker_id_fkey;
ALTER TABLE machines DROP CONSTRAINT IF EXISTS machines_assigned_worker_id_fkey;
ALTER TABLE reports DROP CONSTRAINT IF EXISTS reports_created_by_fkey;

-- Create temporary columns
ALTER TABLE work_orders ADD COLUMN assigned_worker_uid UUID;
ALTER TABLE worker_shifts ADD COLUMN worker_uid UUID;
ALTER TABLE worker_productivity ADD COLUMN worker_uid UUID;
ALTER TABLE machines ADD COLUMN assigned_worker_uid UUID;
ALTER TABLE reports ADD COLUMN created_by_uid UUID;

-- Update the temporary columns with UUID values
UPDATE work_orders wo 
SET assigned_worker_uid = u.uid 
FROM users u 
WHERE wo.assigned_worker_id = u.id;

UPDATE worker_shifts ws 
SET worker_uid = u.uid 
FROM users u 
WHERE ws.worker_id = u.id;

UPDATE worker_productivity wp 
SET worker_uid = u.uid 
FROM users u 
WHERE wp.worker_id = u.id;

UPDATE machines m 
SET assigned_worker_uid = u.uid 
FROM users u 
WHERE m.assigned_worker_id = u.id;

UPDATE reports r 
SET created_by_uid = u.uid 
FROM users u 
WHERE r.created_by = u.id;

-- Drop old columns
ALTER TABLE work_orders DROP COLUMN assigned_worker_id;
ALTER TABLE worker_shifts DROP COLUMN worker_id;
ALTER TABLE worker_productivity DROP COLUMN worker_id;
ALTER TABLE machines DROP COLUMN assigned_worker_id;
ALTER TABLE reports DROP COLUMN created_by;

-- Rename new columns to original names
ALTER TABLE work_orders RENAME COLUMN assigned_worker_uid TO assigned_worker_id;
ALTER TABLE worker_shifts RENAME COLUMN worker_uid TO worker_id;
ALTER TABLE worker_productivity RENAME COLUMN worker_uid TO worker_id;
ALTER TABLE machines RENAME COLUMN assigned_worker_uid TO assigned_worker_id;
ALTER TABLE reports RENAME COLUMN created_by_uid TO created_by;

-- Re-add foreign key constraints
ALTER TABLE work_orders 
    ADD CONSTRAINT work_orders_assigned_worker_id_fkey 
    FOREIGN KEY (assigned_worker_id) REFERENCES users(uid);

ALTER TABLE worker_shifts 
    ADD CONSTRAINT worker_shifts_worker_id_fkey 
    FOREIGN KEY (worker_id) REFERENCES users(uid);

ALTER TABLE worker_productivity 
    ADD CONSTRAINT worker_productivity_worker_id_fkey 
    FOREIGN KEY (worker_id) REFERENCES users(uid);

ALTER TABLE machines 
    ADD CONSTRAINT machines_assigned_worker_id_fkey 
    FOREIGN KEY (assigned_worker_id) REFERENCES users(uid);

ALTER TABLE reports 
    ADD CONSTRAINT reports_created_by_fkey 
    FOREIGN KEY (created_by) REFERENCES users(uid);

-- Create indexes for the new UUID columns
CREATE INDEX idx_work_orders_worker ON work_orders(assigned_worker_id);
CREATE INDEX idx_worker_shifts_worker ON worker_shifts(worker_id);
CREATE INDEX idx_worker_productivity_worker ON worker_productivity(worker_id);
CREATE INDEX idx_machines_worker ON machines(assigned_worker_id);
CREATE INDEX idx_reports_creator ON reports(created_by); 