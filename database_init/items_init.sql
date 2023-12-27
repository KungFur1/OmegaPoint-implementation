-- Items SQL

USE OmegaPoint;

CREATE TABLE IF NOT EXISTS Items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
	description VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
    tax_percentage DOUBLE NOT NULL
);

INSERT INTO Items (name, description, price, tax_percentage) 
VALUES 
	('Classic Facial', 'A basic facial treatment', 50, 5),
	('Gourmet Dinner', 'Exquisite gourmet dining experience', 100, 7),
	('Massage Therapy', 'Relaxing full-body massage', 55.5, 3),
	('Cocktail Mixology Class', 'Learn the art of crafting cocktails', 500, 8);


CREATE TABLE IF NOT EXISTS ItemDiscounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    discount_amount DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE
);

INSERT INTO ItemDiscounts (item_id, discount_amount)
VALUES
	(1, 5.00),
	(2, 10.00);

CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    store_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
);

INSERT INTO Inventory (item_id, store_id, quantity)
VALUES
    (1, 2, 100),
    (2, 3, 50);

