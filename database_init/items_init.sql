-- Items SQL

USE OmegaPoint;


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

