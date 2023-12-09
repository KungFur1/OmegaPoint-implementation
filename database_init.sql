CREATE DATABASE IF NOT EXISTS OmegaPoint;
USE OmegaPoint;



-- User data
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Does not work for some reason
    phone_number VARCHAR(15) DEFAULT NULL,
    first_name VARCHAR(50) DEFAULT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    address TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    user_id INT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_users_data (
    user_id INT PRIMARY KEY,
    company_id INT NOT NULL,
    position INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    created_by_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    users_read BOOLEAN NOT NULL,
    users_manage BOOLEAN NOT NULL,
    inventory_read BOOLEAN NOT NULL,
    inventory_manage BOOLEAN NOT NULL,
    services_read BOOLEAN NOT NULL,
    services_manage BOOLEAN NOT NULL,
    items_read BOOLEAN NOT NULL,
    items_manage BOOLEAN NOT NULL,
    payments_read BOOLEAN NOT NULL,
    payments_manage BOOLEAN NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS assigned_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);



-- Company data
CREATE TABLE IF NOT EXISTS company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);




SELECT * FROM users;
SELECT * FROM admins;
SELECT * FROM company;
SELECT * FROM company_users_data;
SELECT * FROM roles;
SELECT * FROM assigned_roles;

DROP schema omegapoint;
















-- Inserting into Users
INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address)
VALUES 
('john.doe@example.com', 'hash_johndoe', '1234567890', 'John', 'Doe', '123 Baker Street'),
('jane.smith@example.com', 'hash_janesmith', '0987654321', 'Jane', 'Smith', '456 Oak Avenue'),
('mike.jones@example.com', 'hash_mikejones', '1122334455', 'Mike', 'Jones', '789 Pine Road'),
('alice.wilson@example.com', 'hash_alicewilson', '1233211234', 'Alice', 'Wilson', '321 Cedar Lane'),
('bob.brown@example.com', 'hash_bobbrown', '9876543210', 'Bob', 'Brown', '654 Maple Street');

-- Inserting into Admins
INSERT INTO admins (user_id)
VALUES 
((SELECT id FROM users WHERE email = 'jane.smith@example.com'));

INSERT INTO admins (user_id)
VALUES 
((SELECT id FROM users WHERE email = 'user@example.com'));

-- Inserting into Company
INSERT INTO company (email, `name`)
VALUES 
('company1@example.com', 'Tech Solutions'),
('company2@example.com', 'Gourmet Foods');

-- Inserting into Company Users Data
-- Assuming company positions as 1 (Owner), 2 (Manager), 3 (Employee)
INSERT INTO company_users_data (user_id, company_id, position)
VALUES 
((SELECT id FROM users WHERE email = 'john.doe@example.com'), (SELECT id FROM company WHERE `name` = 'Tech Solutions'), 1),
((SELECT id FROM users WHERE email = 'mike.jones@example.com'), (SELECT id FROM company WHERE `name` = 'Gourmet Foods'), 2),
((SELECT id FROM users WHERE email = 'alice.wilson@example.com'), (SELECT id FROM company WHERE `name` = 'Tech Solutions'), 3),
((SELECT id FROM users WHERE email = 'bob.brown@example.com'), (SELECT id FROM company WHERE `name` = 'Gourmet Foods'), 3);

-- Inserting into Roles
INSERT INTO roles (company_id, created_by_id, name, description, users_read, users_manage, inventory_read, inventory_manage, services_read, services_manage, items_read, items_manage, payments_read, payments_manage)
VALUES 
((SELECT id FROM company WHERE `name` = 'Tech Solutions'), (SELECT id FROM users WHERE email = 'john.doe@example.com'), 'Tech Manager', 'Full access to tech management', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),
((SELECT id FROM company WHERE `name` = 'Gourmet Foods'), (SELECT id FROM users WHERE email = 'mike.jones@example.com'), 'Food Manager', 'Manage food-related services', TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE);

-- Inserting into Assigned Roles
INSERT INTO assigned_roles (user_id, role_id)
VALUES 
((SELECT id FROM users WHERE email = 'alice.wilson@example.com'), (SELECT id FROM roles WHERE name = 'Tech Manager')),
((SELECT id FROM users WHERE email = 'bob.brown@example.com'), (SELECT id FROM roles WHERE name = 'Food Manager'));





