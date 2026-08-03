-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Active', 'Locked', 'Disabled')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (username, full_name, email, status)
VALUES
('jdoe', 'John Doe', 'john.doe@example.com', 'Active'),
('asmith', 'Alice Smith', 'alice.smith@example.com', 'Locked'),
('bjohnson', 'Bob Johnson', 'bob.johnson@example.com', 'Disabled'),
('mjones', 'Mary Jones', 'mary.jones@example.com', 'Active'),
('rbrown', 'Robert Brown', 'robert.brown@example.com', 'Locked');