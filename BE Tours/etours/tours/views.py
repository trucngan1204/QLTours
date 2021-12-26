from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Blog, Comment, Tour, Staff, Tag, Category, Action, Rating
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .serializers import (
    TourSerializer,
    StaffSerializer,
    TagSerializer,
    CategorySerializer,
    BlogSerializer,
    UserSerializer,
    CommentSerializer,
    ActionSerializer,
    RatingSerializer)
from django.http import HttpResponseRedirect, HttpResponse
from .paginator import BasePagination
from django.conf import settings


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)


class TourViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active=True)
    serializer_class = TourSerializer
    pagination_class = BasePagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['add_comment', 'rate']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # def get_queryset(self):
    #     tours = Tour.objects.filter(active=True)
    #
    #     q = self.request.query_params.get('q')
    #     if q is not None:
    #         tours = tours.filter(subject__icontains=q)
    #
    #     cate_id = self.request.query_params.get('category_id')
    #     if cate_id is not None:
    #         tours = tours.filter(category_id=cate_id)
    #
    #     return tours

    @action(methods=['post'], detail=True)
    def hide_tour(self, request, pk):
        try:
            t = Tour.objects.get(pk=pk)
            t.active = False
            t.save()
        except Tour.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST) #gui id khi khong co trong he thong

        return Response(data=TourSerializer(t, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        description = request.data.get('description')
        if description:
            c = Comment.objects.create(description=description,
                                       tour=self.get_object(),
                                       author=request.user)

            return Response(CommentSerializer(c).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating,
                                      author=request.user,
                                      tour=self.get_object())

            return Response(RatingSerializer(r).data,
                            status=status.HTTP_200_OK)


class StaffViewSet(viewsets.ViewSet,
                   generics.ListAPIView):
    queryset = Staff.objects.filter(active=True)
    serializer_class = StaffSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class CategoryViewSet(viewsets.ViewSet,
                      generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class TagViewSet(viewsets.ViewSet,
                 generics.ListAPIView):
    queryset = Tag.objects.filter(active=True)
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class BlogViewSet(viewsets.ViewSet,
                  generics.ListAPIView):
    queryset = Blog.objects.filter(active=True)
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.action in ['add-comment', 'take_action']:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        description = request.data.get('description')
        if description:
            c = Comment.objects.create(description=description,
                                       tour=self.get_object(),
                                       author=request.user)

            return Response(CommentSerializer(c).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='like')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action =Action.objects.create(type=action_type,
                                          author=request.user,
                                          blog=self.get_object())

            return Response(ActionSerializer(action).data,
                            status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet,
                     generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


def index(request):
    return HttpResponse('e-tours app')