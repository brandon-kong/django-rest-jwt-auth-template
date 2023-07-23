from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

def index(request):
    return Response({"message": "Hello, world!"})

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})