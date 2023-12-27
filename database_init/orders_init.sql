
USE OmegaPoint;

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

CREATE TABLE IF NOT EXISTS items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  company_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(200),
  price DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (company_id) REFERENCES company(id)
);

CREATE TABLE IF NOT EXISTS order_item (
  id INT AUTO_INCREMENT PRIMARY KEY,
  item_id INT NOT NULL,
  order_id INT NOT NULL,
  quantity INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS discounts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  order_id INT,
  percentage_discount DECIMAL(5, 2),
  amount_discount DECIMAL(10, 2),
  created_at DATETIME NOT NULL,
  CONSTRAINT at_least_one_discount CHECK (percentage_discount IS NOT NULL OR amount_discount IS NOT NULL),
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT INTO items (company_id, name, description, price) VALUES
  (1, 'Item 1', 'Description 1', 10.00),
  (1, 'Item 2', 'Description 2', 20.00),
  (1, 'Item 7', 'Description 7', 70.00),
  (1, 'Item 8', 'Description 8', 80.00),
  (1, 'Item 9', 'Description 9', 90.00),
  (1, 'Item 16', 'Description 16', 160.00),
  (1, 'Item 17', 'Description 17', 170.00),
  (1, 'Item 18', 'Description 18', 180.00),
  (1, 'Item 19', 'Description 19', 190.00)

