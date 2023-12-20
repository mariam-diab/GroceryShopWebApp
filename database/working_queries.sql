select * from GroceryApp_wishlist wl 
join GroceryApp_product p
on wl.product_id =p.id 
where wl.user_id in 
(select id from userauths_user 
where id =4)


select * from GroceryApp_wishlist

select * from GroceryApp_product