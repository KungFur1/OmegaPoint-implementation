
USE OmegaPoint;

CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  company_id INT NOT NULL,
  total_price DECIMAL(10, 2) NOT NULL,
  created_at DATETIME NOT NULL,
  status INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (company_id) REFERENCES company(id)
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

