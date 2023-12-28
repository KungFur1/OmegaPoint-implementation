USE OmegaPoint;

CREATE TABLE IF NOT EXISTS appointments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company_id INT NOT NULL,
    user_id INT NOT NULL,
    appointment_date DATETIME DEFAULT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id), REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (name), REFERENCES services(name) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO appointments(name,company_id,user_id,appointment_date,price) VALUES
('Name1',1,1,2024-01-08 15:00:00,10.00),
('Name2',1,1,2024-01-09 16:30:00,100.00),
('Name3',1,1,2024-01-10 17:00:00,15.50),
('Name4',1,1,2024-01-11 10:15:00,9.99),
('Name5',1,1,2024-01-12 09:45:00,16.54),
