select * from GroceryApp_product p
join GroceryApp_wishlist wl
on wl.product_id =p.id 
where wl.user_id in 
(select id from userauths_user 
where id =4)


select * from GroceryApp_wishlist
select * from GroceryApp_productimages



select * from GroceryApp_product


select * from GroceryApp_product p
join GroceryApp_wishlist wl
on wl.product_id =p.id 
where wl.user_id in 
(select id from userauths_user 
where id =4)

select count(product_id) from GroceryApp_wishlist
where user_id= 4 and product_id=1;



select * from GroceryApp_product p 
join GroceryApp_cartorderitems ct
on ct.product_id =p.id
join GroceryApp_cartorder co
on co.ct_ord_id= ct.order_id
where co.order_status = 'process'
and co.user_id in 
(select id from userauths_user 
where id =4)


select * from GroceryApp_product p
join GroceryApp_cartorderitems ct
on ct.product_id =p.id
join GroceryApp_cartorder co
on co.ct_ord_id= ct.order_id
where co.order_status = 'process' 
and ct.quantity >0 
and co.user_id in (select id from userauths_user where id =4)



select SUM(p.price* ct.quantity) from GroceryApp_product p
join GroceryApp_cartorderitems ct
on ct.product_id =p.id
join GroceryApp_cartorder co
on co.ct_ord_id= ct.order_id
where co.order_status = 'process' 
and ct.quantity >0 
and co.user_id in (select id from userauths_user where id =4)


select * from GroceryApp_cartorderitems;


UPDATE GroceryApp_cartorderitems
SET quantity = 4
WHERE order_id = 1;


SELECT COUNT(*)
FROM GroceryApp_product p
JOIN GroceryApp_cartorderitems ct ON ct.product_id = p.id
JOIN GroceryApp_cartorder co ON co.ct_ord_id = ct.order_id
WHERE co.order_status = 'process'
  AND ct.quantity > 0
  AND co.user_id IN (SELECT id FROM userauths_user WHERE id = 4)
  AND p.id =2;

SELECT * FROM GroceryApp_cartorderitems
SELECT * FROM GroceryApp_cartorder WHERE user_id= 4;
SELECT * FROM GroceryApp_cartorder;


INSERT INTO GroceryApp_cartorder (user_id, paid_status, order_date, order_status)
VALUES (5, 0, GETDATE(), 'processing');

INSERT INTO GroceryApp_cartorder (user_id, paid_status, order_date, order_status)
VALUES (5, 0, GETDATE(), 'processing');

SELECT ct_ord_id FROM GroceryApp_cartorder WHERE user_id=5;

INSERT INTO GroceryApp_cartorderitems (product_id, order_id, invoice_number)
VALUES (2, 5, 'abcdefgh12345');



select count(p.id) from GroceryApp_product p 
join GroceryApp_cartorderitems 
ct on ct.product_id =p.id
join GroceryApp_cartorder
co on co.ct_ord_id= ct.order_id 
where co.order_status = 'processing' 
and ct.quantity >0 and 
co.user_id in
(select id from userauths_user where id =4)
