from rest_framework.response import Response
from rest_framework.decorators import api_view
from LogoGen.models import Logo
from .serializers import LogoSerializer
from . import utils
from googletrans import Translator



@api_view(['POST'])
def GenLogo(request):
	serializer = LogoSerializer(data=request.data)
	if serializer.is_valid():
		trans=Translator()
		trans.raise_Exception = True
		translated = trans.translate(serializer.data["desc"],dest='en').text
		if Logo.objects.filter(desc=translated):
			return Response(utils.exist(serializer,translated))
		utils.savetodb(serializer,translated)
		return Response(utils.exist(serializer,translated))

	return Response("Unvalid Data")
