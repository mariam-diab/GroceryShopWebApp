CREATE TABLE groceryapp_cartorder(
	id BIGINT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	user_id BIGINT REFERENCES userauths_user(id) ON DELETE CASCADE,
	price DECIMAL(14, 2) DEFAULT 0.99,
	paid_status BIT DEFAULT 0,
	order_date DATETIME DEFAULT GETDATE(),
	product_status VARCHAR(30) DEFAULT 'processing',
	CONSTRAINT check_productstatus CHECK (product_status IN ('processing', 'shipped', 'delivered'))

);

CREATE TABLE groceryapp_cartorderitems(
	id BIGINT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	order_id BIGINT REFERENCES groceryapp_cartorder(id) ON DELETE CASCADE,
	product_status VARCHAR(200),
	item VARCHAR(200),
	image NVARCHAR(200),
	quantity INT DEFAULT 0,
	price DECIMAL(14, 2) DEFAULT 0.99,
	total AS (quantity*price),
);

CREATE TABLE groceryapp_wishlist(
	id BIGINT IDENTITY(1,1) NOT NULL,
	user_id BIGINT REFERENCES userauths_user(id),
	product_id BIGINT REFERENCES GroceryApp_product(id),
	date DATETIME DEFAULT GETDATE(),
	PRIMARY KEY (id)
);

CREATE TABLE groceryapp_address(
	id BIGINT IDENTITY(1,1) NOT NULL,
	user_id BIGINT REFERENCES userauths_user(id) ON DELETE SET NULL,
	address VARCHAR(100) NOT NULL,
	status BIT NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
);

