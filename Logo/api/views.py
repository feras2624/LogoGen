from rest_framework.response import Response
from rest_framework.decorators import api_view
from LogoGen.models import Logo
from .serializers import LogoSerializer
from . import utils
from googletrans import Translator

#FEEDBACK_URL = 'https://namelix.com/app/info_feedback2.php'

@api_view(['POST'])
def GenLogo(request):
	serializer = LogoSerializer(data=request.data)
	if serializer.is_valid():
		trans=Translator()
		trans.raise_Exception = True
		translated = trans.translate(serializer.data["desc"],dest='en').text
		if ('from_db' in request.data) and request.data['from_db']=="true":
			print(request.data['from_db'])
			if Logo.objects.filter(desc=translated):
				return Response(utils.exist(serializer,translated))
			utils.savetodb(serializer,translated)
			return Response(utils.exist(serializer,translated))
		return Response(utils.LogoFromUrl(request,translated))

	return Response("Unvalid Data")

@api_view(['POST'])
def GenName(request):
	if not 'keywords' in request.data:
		return Response("Unvalid Data")
	return Response(utils.getname(request))
