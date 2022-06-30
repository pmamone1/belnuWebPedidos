from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Variation, Product
from .serializers import VariationSerializer

class VariationApiView(APIView):
    
    def get(self, request):
        if request.is_ajax and request.method == "GET":
            product=request.GET.get('titulo',None)
            edicion=request.GET.get('edicion',None)
            variations = Variation.objects.get(variation_value=edicion, product=product)
            serializer = VariationSerializer(variations)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
