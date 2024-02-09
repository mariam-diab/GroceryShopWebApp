from GroceryApp.models import Category, Product, ProductImages, CartOrder, CartOrderItems
from csv import reader
from random import randint
from datetime import date, timedelta
import os

# name - Brand - Price - image_url
def run():
  
    # ProductImages.objects.all().delete()
    # Product.objects.all().delete()
    # Category.objects.all().delete()

    upload_carrefour_data()


    
     
def upload_carrefour_data():
    CSV_DATA_FILES = ['products_beverages-egyptian.csv', 'products_dairy-products.csv',
                      'products_delicatessen-egyptian.csv', 'products_frozen-egyptian.csv',
                      'products_fruits-veg-egyptian.csv', 'products_grocery-egyption.csv']
    fi = 0

    categories = {0: 'beverages', 1: 'dairy-products', 2: 'delicatessen', 3: 'frozen-egyptian', 4: 'fruits-veg', 5:'grocery'  }
    

    for file_name in CSV_DATA_FILES:
        with open(file_name, 'r', encoding='utf-8') as file:
            csvreader = reader(file, delimiter=',')
            next(csvreader)

            cnt = 0
            
            for row in csvreader:
            #  try:
                product_name, brand_name, price, image_url, country = row[0], row[1], row[2], row[3], row[4]

                

                if product_name == 'Unknown':
                    continue
                price = price[:-4:]
                if price == '':
                    price = '10'
                
                
                price = float(price)

                if cnt%2==0: 
                    old_price = price
                    feat = True
                else:
                    old_price = float(price) + 10
                    feat = False

                print(product_name)

                if (cnt==10):
                    break

            

            
                cat = Category.objects.get_or_create(title =categories[fi])[0]

                
                product = Product.objects.get_or_create(title = product_name[0:255:], 
                price = float(price),
                old_price = float(old_price),
                in_stock = True,
                featured = feat, 
                category = cat,
                exp_date = date.today() + timedelta(days = randint(20, 90)),
                brand_name = brand_name,
                brand_nationality = country,
                unit_type = "Piece",
                img = image_url
                )
                
                image = ProductImages.objects.get_or_create(images=image_url, product=product[0])

                cnt+=1
                # print(product)
                
                
            #  except:
            #      continue
        fi+=1

