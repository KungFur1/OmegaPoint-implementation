USE OmegaPoint;

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
)

INSERT INTO service_availability (service_id,start_date,end_date) VALUES
(1,'2024-01-08 08:00:00', '2024-01-08 16:00:00'),
(2,'2024-01-10 11:00:00', '2024-01-08 20:30:00'),
(3,'2024-01-20 7:30:00', '2024-01-20 15:30:00');
