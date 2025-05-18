-- Add client_id column to work_orders table
ALTER TABLE work_orders 
ADD COLUMN client_id UUID REFERENCES users(uid);

-- Create index for better query performance
CREATE INDEX idx_work_orders_client ON work_orders(client_id); 