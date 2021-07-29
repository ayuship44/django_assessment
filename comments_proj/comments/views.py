# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def comments_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()

        author = request.query_params.get('author', None)
        if author is not None:
            tutorials = comments.filter(title__icontains=title)

        comments_serializer = CommentSerializer(comments, many=True)
        return JsonResponse(comments_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        comments_data = JSONParser().parse(request)
        comments_serializer = CommentSerializer(data=comments_data)
        if comments_serializer.is_valid():
            comments_serializer.save()
            return JsonResponse(comments_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(comments_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Comment.objects.all().delete()
        return JsonResponse({'message': '{} Comment were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def comments_detail(request, pk):
    try:
        comments = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments_serializer = CommentSerializer(comments)
        return JsonResponse(comments_serializer.data)

    elif request.method == 'PUT':
        comments_data = JSONParser().parse(request)
        comments_serializer = CommentSerializer(comments, data=comments_data)
        if comments_serializer.is_valid():
            comments_serializer.save()
            return JsonResponse(comments_serializer.data)
        return JsonResponse(comments_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comments.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)