-- STORES SQL

USE OmegaPoint;

-- Stores data
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

