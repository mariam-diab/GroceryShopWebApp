EXEC sp_rename 'dbo.GroceryApp_address', 'GroceryApp_BillingDetails';

ALTER TABLE dbo.GroceryApp_BillingDetails
ADD apartment NVARCHAR(100),
    governorate NVARCHAR(100),
    city NVARCHAR(100),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    payment_method NVARCHAR(50),
    payment_status BIT,
	order_id BIGINT;

ALTER TABLE dbo.GroceryApp_BillingDetails
ADD CONSTRAINT FK_BillingDetails_order_id
FOREIGN KEY (order_id) REFERENCES dbo.GroceryApp_cartorder(ct_ord_id);

EXEC sp_rename 'dbo.GroceryApp_BillingDetails.status', 'delivered_status', 'COLUMN';
