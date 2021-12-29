from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, Staff, Tour, Category, Blog, Comment, Tag, Bill, Action, Rating


class UserSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, tour):
        request = self.context['request']
        name = tour.image.name
        if name.startswith('static/'):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields =['id', 'first_name', 'last_name', 'email', 'username', 'password', 'image', 'number', 'address']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'description', 'active']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields =['id', 'name', 'active']


class TourSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, tour):
        request = self.context['request']
        name = tour.image.name
        if name.startswith('static/'):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    tags = TagSerializer() #(many=True hien thi nhieu the) hien thi ten cu the

    class Meta:
        model = Tour
        fields = ['id', 'title', 'created_date', 'image', 'category', 'active', 'tags']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'name', 'active']


class BlogSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, tour):
        request = self.context['request']
        name = tour.image.name
        if name.startswith('static/'):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'image', 'description', 'created_date']


class CommentSerializer(ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, comment):
        return UserSerializer(comment.author, context={"request": self.context.get('request')}).data

    class Meta:
        model = Comment
        fields = ['id', 'author', 'description', 'created_date']


class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rate", "created_date"]


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = ["id", "user", "tour", "total_price"]