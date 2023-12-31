# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GroceryappCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    cid = models.CharField(unique=True, max_length=20, db_collation='Arabic_CI_AI')
    title = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=True, null=True)
    img = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GroceryApp_category'


class GroceryappProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    pid = models.CharField(unique=True, max_length=20, db_collation='Arabic_CI_AI')
    title = models.CharField(max_length=100, db_collation='Arabic_CI_AI')
    img = models.CharField(max_length=100, db_collation='Arabic_CI_AI', blank=True, null=True)
    p_description = models.TextField(db_collation='Arabic_CI_AI', blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    old_price = models.DecimalField(max_digits=20, decimal_places=2)
    specifications = models.TextField(db_collation='Arabic_CI_AI', blank=True, null=True)
    product_status = models.CharField(max_length=10, db_collation='Arabic_CI_AI')
    status = models.BooleanField()
    in_stock = models.BooleanField()
    featured = models.BooleanField()
    digital = models.BooleanField()
    sku = models.CharField(unique=True, max_length=20, db_collation='Arabic_CI_AI')
    date = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(GroceryappCategory, models.DO_NOTHING, to_field='cid', blank=True, null=True)
    user = models.ForeignKey('UserauthsUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GroceryApp_product'


class GroceryappProductimages(models.Model):
    id = models.BigAutoField(primary_key=True)
    images = models.CharField(max_length=100, db_collation='Arabic_CI_AI')
    date = models.DateTimeField()
    product = models.ForeignKey(GroceryappProduct, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GroceryApp_productimages'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='Arabic_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='Arabic_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='Arabic_CI_AI')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='Arabic_CI_AI', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='Arabic_CI_AI')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='Arabic_CI_AI')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserauthsUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='Arabic_CI_AI')
    model = models.CharField(max_length=100, db_collation='Arabic_CI_AI')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='Arabic_CI_AI')
    name = models.CharField(max_length=255, db_collation='Arabic_CI_AI')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='Arabic_CI_AI')
    session_data = models.TextField(db_collation='Arabic_CI_AI')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GroceryappAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserauthsUser', models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=100, db_collation='Arabic_CI_AI')
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'groceryapp_address'


class GroceryappCartorder(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserauthsUser', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    paid_status = models.BooleanField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    product_status = models.CharField(max_length=30, db_collation='Arabic_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groceryapp_cartorder'


class GroceryappCartorderitems(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(GroceryappCartorder, models.DO_NOTHING, blank=True, null=True)
    product_status = models.CharField(max_length=200, db_collation='Arabic_CI_AI', blank=True, null=True)
    item = models.CharField(max_length=200, db_collation='Arabic_CI_AI', blank=True, null=True)
    image = models.CharField(max_length=200, db_collation='Arabic_CI_AI', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groceryapp_cartorderitems'


class GroceryappWishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('UserauthsUser', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(GroceryappProduct, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groceryapp_wishlist'


class UserauthsUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, db_collation='Arabic_CI_AI')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=23, db_collation='Arabic_CI_AI')
    last_name = models.CharField(max_length=23, db_collation='Arabic_CI_AI')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254, db_collation='Arabic_CI_AI')
    username = models.CharField(max_length=23, db_collation='Arabic_CI_AI')

    class Meta:
        managed = False
        db_table = 'userauths_user'


class UserauthsUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserauthsUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'userauths_user_groups'
        unique_together = (('user', 'group'),)


class UserauthsUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserauthsUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'userauths_user_user_permissions'
        unique_together = (('user', 'permission'),)
