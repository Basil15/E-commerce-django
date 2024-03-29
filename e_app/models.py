from django.db import models

# Create your models here.
class product(models.Model):
    product_id = models.AutoField
    Product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image=models.ImageField(upload_to='shop/images',default="")


    def __str__(self):
        return self.Product_name
    

class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=90)
    address1=models.CharField(max_length=200)   
    address2=models.CharField(max_length=200) 
    city=models.CharField(max_length=100)  
    state=models.CharField(max_length=100)  
    zip_code=models.CharField(max_length=100)  
    oid=models.CharField(max_length=100)  
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name
    


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models,models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+"..."    

