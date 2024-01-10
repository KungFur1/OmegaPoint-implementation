USE OmegaPoint;

CREATE TABLE IF NOT EXISTS payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  user_id INT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  tip DECIMAL(10, 2) DEFAULT 0.00,
  discount_percentage DECIMAL(5, 2) DEFAULT 0.00,  -- Added this line for discount percentage
  payment_method VARCHAR(50) NOT NULL,  -- e.g., 'cash', 'card'
  payment_status INT NOT NULL,  -- e.g., 1 = 'pending', 2 = 'completed'
  created_at DATETIME NOT NULL,
  updated_at DATETIME,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);


