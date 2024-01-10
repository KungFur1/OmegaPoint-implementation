USE OmegaPoint;

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