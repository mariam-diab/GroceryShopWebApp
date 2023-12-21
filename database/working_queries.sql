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