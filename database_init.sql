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
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Roles will be saved in a separate table
CREATE TABLE IF NOT EXISTS company_users_data (
    user_id INT PRIMARY KEY,
    company_id INT,
    position INT NOT NULL DEFAULT 1,
    FOREIGN KEY (company_id) REFERENCES company(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


-- Company data
CREATE TABLE IF NOT EXISTS company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



-- Example data:
INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) 
VALUES 
('jane.doe@example.com', 'hashedpassword123', '123-456-7890', 'Jane', 'Doe', '123 Main St, Anytown'),
('john.smith@example.com', 'hashedpassword456', '987-654-3210', 'John', 'Smith', '456 Oak St, Villagetown');

INSERT INTO admins (user_id) 
VALUES (1); -- Jane Doe

INSERT INTO admins (user_id) 
VALUES (3); -- user@exm

INSERT INTO company (email, `name`) 
VALUES 
('info@techcorp.com', 'TechCorp'),
('contact@greenenergy.com', 'GreenEnergy');

INSERT INTO company_users_data (user_id, company_id, position) 
VALUES 
(1, 1, 2),  -- Jane Doe at TechCorp
(2, 2, 1);  -- John Smith at GreenEnergy




SELECT * FROM users;
SELECT * FROM admins;
SELECT * FROM company;
SELECT * FROM company_users_data;
