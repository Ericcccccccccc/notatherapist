-- Initialize NotATherapist Database

-- Create the input_table with timestamp and metadata
CREATE TABLE IF NOT EXISTS input_table (
    id SERIAL PRIMARY KEY,
    input TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    conversation_id VARCHAR(255),
    processed BOOLEAN DEFAULT FALSE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_input_created_at ON input_table(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_input_conversation_id ON input_table(conversation_id);
CREATE INDEX IF NOT EXISTS idx_input_processed ON input_table(processed);

-- Grant permissions (for the notatherapist user)
GRANT ALL PRIVILEGES ON TABLE input_table TO notatherapist;
GRANT USAGE, SELECT ON SEQUENCE input_table_id_seq TO notatherapist;

-- Insert a test record
INSERT INTO input_table (input, conversation_id) 
VALUES ('System initialized', 'system_init_' || EXTRACT(EPOCH FROM NOW()));

-- Verify the table was created
SELECT 'Input table created successfully' as status, COUNT(*) as row_count FROM input_table;