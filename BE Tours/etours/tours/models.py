from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m', default=None)
    number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)


class ItemBase(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.tour


class Staff(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='staffs/%Y/%m', default=None)
    active = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Tag(ItemBase):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Tour(ItemBase):
    title = models.CharField(max_length=100, null=False, unique=True)#ke thua ItemBase
    image = models.ImageField(upload_to='tours/%Y/%m', default=None)
    price_adult = models.IntegerField(null=True, blank=True) #nguoi lon
    price_child = models.IntegerField(null=True, blank=True) #tre em
    time = models.CharField(max_length=50) #VD: 3N2Đ
    departure = models.DateTimeField() #khởi hành
    description = RichTextField()
    note = RichTextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)


class Blog(ItemBase):
    title = models.CharField(max_length=100, null=False, unique=True, default=None)
    image = models.ImageField(upload_to='blogs/%Y/%m', default=None)
    description = models.TextField()


class Comment(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, related_name='tours')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, related_name='blogs')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # liên kết với bảng user để biết ai là người cmt
    # rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True)
    description = models.TextField()  # nd cmt
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class ActionBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Action(ActionBase):
    LIKE = range(1)
    ACTIONS = [
        ('LIKE', 'like'),
    ]
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(ActionBase):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0)


class Bill(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.DO_NOTHING, null=True, related_name='bill')



