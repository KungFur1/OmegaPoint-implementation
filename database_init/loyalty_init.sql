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
