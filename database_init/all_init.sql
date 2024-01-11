-- INITIALIZE ALL DB


CREATE DATABASE IF NOT EXISTS OmegaPoint;
USE OmegaPoint;


-- USER AND COMPANY SQL


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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


-- LOYALTY


CREATE TABLE IF NOT EXISTS loyalty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    created_by_id INT NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(200) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    discount_percent FLOAT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
    -- FOREIGN KEY (created_by_id) REFERENCES users(id) ON DELETE CASCADE
);


INSERT INTO loyalty (company_id, created_by_id, name, description, discount_percent) 
VALUES 
((SELECT id FROM company WHERE email = 'company1@example.com'), (SELECT id FROM users WHERE email = 'owner1@example.com'), 'Galactic Rewards', 'Exclusive rewards for our innovative customers', 10.0),
((SELECT id FROM company WHERE email = 'company1@example.com'), (SELECT id FROM users WHERE email = 'manager1@example.com'), 'Innovation Club', 'Join our club of innovators and enjoy special benefits', 15.0),
((SELECT id FROM company WHERE email = 'company2@example.com'), (SELECT id FROM users WHERE email = 'owner2@example.com'), 'Quantum Perks', 'Loyalty program for our esteemed clients', 12.0),
((SELECT id FROM company WHERE email = 'company2@example.com'), (SELECT id FROM users WHERE email = 'manager2@example.com'), 'Leap Loyalty', 'A leap to savings and exclusive offers', 8.0);


-- STORES


CREATE TABLE IF NOT EXISTS stores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    UNIQUE KEY (company_id, name)
);

-- some sample stores for testing
INSERT INTO stores (company_id, name, location) 
VALUES 
((SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), 'Main Street Store', '123 Main St'),
((SELECT id FROM company WHERE name = 'Galactic Innovations Inc.'), 'Downtown Store', '456 Downtown Rd'),
((SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), 'Uptown Store', '789 Uptown Ave'),
((SELECT id FROM company WHERE name = 'Quantum Leap Enterprises'), 'Suburb Store', '101 Suburb Lane');


-- ITEMS


CREATE TABLE IF NOT EXISTS items (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  company_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(200),
  price DECIMAL(10, 2) NOT NULL,
  tax_percentage DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (company_id) REFERENCES company(id)
);


INSERT INTO items (company_id, name, description, price, tax_percentage) VALUES
  (1, 'Item 1', 'Description 1', 10.00, 2.00),
  (1, 'Item 2', 'Description 2', 20.00, 3.00),
  (1, 'Item 7', 'Description 7', 70.00, 2.00),
  (1, 'Item 8', 'Description 8', 80.00, 4.00),
  (1, 'Item 9', 'Description 9', 90.00, 2.00),
  (1, 'Item 16', 'Description 16', 160.00, 1.00),
  (1, 'Item 17', 'Description 17', 170.00, 3.00),
  (1, 'Item 18', 'Description 18', 180.00, 2.00),
  (1, 'Item 19', 'Description 19', 190.00, 2.00);

CREATE TABLE IF NOT EXISTS ItemDiscounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    discount_amount_percentage DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);

INSERT INTO ItemDiscounts (item_id, discount_amount_percentage)
VALUES
	(1, 5.00),
	(2, 10.00);

CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    store_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
);

INSERT INTO Inventory (item_id, store_id, quantity)
VALUES
    (1, 2, 100),
    (2, 3, 50);


-- ORDERS


CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  assignee_id INT DEFAULT NULL,
  company_id INT NOT NULL,
  total_price DECIMAL(10, 2) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME,
  status INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (company_id) REFERENCES company(id),
  FOREIGN KEY (assignee_id) REFERENCES users(id)
);


CREATE TABLE IF NOT EXISTS order_item (
  id INT AUTO_INCREMENT PRIMARY KEY,
  item_id INT NOT NULL,
  order_id INT NOT NULL,
  assignee_id INT DEFAULT NULL,
  quantity INT NOT NULL,
  status INT,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (item_id) REFERENCES items(item_id),
  FOREIGN KEY (assignee_id) REFERENCES users(id)
);


-- SERVICES


CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company_id INT NOT NULL,
    description VARCHAR(200),
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

INSERT INTO services (company_id,name,description,price) VALUES
(1,'Name1','Description 1', 10.00),
(1,'Name2','Description 2', 100.00),
(1,'Name3','Description 3', 15.50),
(1,'Name4','Description 4', 9.99),
(1,'Name5','Description 5', 16.54);

CREATE TABLE IF NOT EXISTS service_availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

INSERT INTO service_availability (service_id,start_date,end_date) VALUES
(1,'2024-01-08 08:00:00', '2024-01-08 16:00:00'),
(2,'2024-01-10 11:00:00', '2024-01-08 20:30:00'),
(3,'2024-01-20 7:30:00', '2024-01-20 15:30:00');



-- APPOINTMENTS


CREATE TABLE IF NOT EXISTS appointments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    company_id INT NOT NULL,
    user_id INT NOT NULL,
    appointment_date DATE,
    start_time varchar(200) NOT NULL,
    end_time varchar(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO appointments(service_id,company_id,user_id,appointment_date,start_time, end_time,price) VALUES
(1,1,1,'2024-01-08','14:30:00','15:00:00',10.00),
(1,1,1,'2024-01-09','16:00:00','16:30:00',100.00),
(1,1,1,'2024-01-10','16:30:00','17:00:00',15.50),
(1,1,1,'2024-01-11','10:00:00','10:15:00',9.99),
(1,1,1,'2024-01-12','09:00:00','09:45:00',16.54);


-- PAYMENTS

CREATE TABLE IF NOT EXISTS payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  user_id INT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  tip DECIMAL(10, 2) DEFAULT 0.00,
  discount_percentage DECIMAL(5, 2) DEFAULT 0.00,  
  payment_method VARCHAR(50) NOT NULL,  
  payment_status INT NOT NULL,  
  created_at DATETIME NOT NULL,
  updated_at DATETIME,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

