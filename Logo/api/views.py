from rest_framework.response import Response
from rest_framework.decorators import api_view
from LogoGen.models import Logo
from .serializers import LogoSerializer
from . import utils




@api_view(['POST'])
def GenLogo(request):
	serializer = LogoSerializer(data=request.data)
	if serializer.is_valid():
		if Logo.objects.filter(desc=serializer.validated_data['desc']):
			return Response(utils.exist(serializer))
		utils.savetodb(serializer)
		return Response(utils.exist(serializer))

	return Response("Unvalid Data")
