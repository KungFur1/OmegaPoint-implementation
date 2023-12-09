CREATE DATABASE IF NOT EXISTS OmegaPoint;
USE OmegaPoint;


-- USER AND COMPANY SQL

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

-- Company data
CREATE TABLE IF NOT EXISTS company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS company_users_data (
    user_id INT PRIMARY KEY,
    company_id INT NOT NULL,
    position INT NOT NULL, -- EMPLOYEE = 1, MANAGER = 2, OWNER = 3
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
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
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
    -- FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS assigned_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);



-- TEST DATA

INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) 
VALUES 
('owner1@example.com', 'abc', '1111111111', 'Aurora', 'Borealis', '101 Visionary Lane'),
('manager1@example.com', 'abc', '2222222222', 'Maximus', 'Innovatus', '102 Leadership Plaza'),
('employee1@example.com', 'abc', '3333333333', 'Leo', 'Craft', '103 Artisan Street'),
('owner2@example.com', 'abc', '4444444444', 'Elena', 'Majesty', '201 Entrepreneurial Way'),
('manager2@example.com', 'abc', '5555555555', 'Isaac', 'Newton', '202 Wisdom Drive'),
('employee2@example.com', 'abc', '6666666666', 'Marie', 'Curie', '203 Scientist Alley'),
('regularuser@example.com', 'abc', '7777777777', 'Amelia', 'Earhart', '404 Adventure Road'),
('adminuser@example.com', 'abc', '8888888888', 'Leonardo', 'Vinci', '505 Creative Blvd');

-- Inserting an Admin
INSERT INTO admins (user_id) 
VALUES 
((SELECT id FROM users WHERE email = 'adminuser@example.com'));

-- Inserting Companies
INSERT INTO company (email, name) 
VALUES 
('company1@example.com', 'Galactic Innovations Inc.'),
('company2@example.com', 'Quantum Leap Enterprises');

-- Inserting Company Users Data
INSERT INTO company_users_data (user_id, company_id, position) 
VALUES 
((SELECT id FROM users WHERE email = 'owner1@example.com'), (SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), 3),
((SELECT id FROM users WHERE email = 'manager1@example.com'), (SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), 2),
((SELECT id FROM users WHERE email = 'employee1@example.com'), (SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), 1),
((SELECT id FROM users WHERE email = 'owner2@example.com'), (SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), 3),
((SELECT id FROM users WHERE email = 'manager2@example.com'), (SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), 2),
((SELECT id FROM users WHERE email = 'employee2@example.com'), (SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), 1);

-- Inserting Roles
INSERT INTO roles (company_id, created_by_id, name, description, users_read, users_manage, inventory_read, inventory_manage, services_read, services_manage, items_read, items_manage, payments_read, payments_manage) 
VALUES 
((SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), (SELECT id FROM users WHERE email = 'owner1@example.com'), 'Innovator', 'Key role driving innovation and change', TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE),
((SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), (SELECT id FROM users WHERE email = 'manager1@example.com'), 'Strategist', 'Focuses on strategic planning and execution', FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE),
((SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), (SELECT id FROM users WHERE email = 'owner2@example.com'), 'Visionary', 'Responsible for shaping the future direction', TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE),
((SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), (SELECT id FROM users WHERE email = 'manager2@example.com'), 'Executor', 'Ensures operational excellence and efficiency', FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, TRUE);

-- Assigning Roles
INSERT INTO assigned_roles (user_id, role_id) 
VALUES 
((SELECT id FROM users WHERE email = 'employee1@example.com'), (SELECT id FROM roles WHERE name = 'Innovator' AND company_id = (SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'))),
((SELECT id FROM users WHERE email = 'employee1@example.com'), (SELECT id FROM roles WHERE name = 'Strategist' AND company_id = (SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'))),
-- ((SELECT id FROM users WHERE email = 'employee2@example.com'), (SELECT id FROM roles WHERE name = 'Visionary' AND company_id = (SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'))),
((SELECT id FROM users WHERE email = 'employee2@example.com'), (SELECT id FROM roles WHERE name = 'Executor' AND company_id = (SELECT id FROM company WHERE name = 'Quantum Leap Enterprises')));


