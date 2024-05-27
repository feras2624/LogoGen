from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Logo
from .serializers import LogoSerializer
import requests
import urllib.parse
baseurl='https://www.design.com/api/logo/more/1?'
@api_view(['POST'])
def GenLogo(request):
	serializer = LogoSerializer(data=request.data)
	if serializer.is_valid():
		if Logo.objects.filter(desc=serializer.validated_data['desc']):
			return Response('Exist')
		serializer.save()
		businessDescription =serializer.data["desc"]
		name = serializer.data["name"]
		keywords = serializer.data["desc"]
		color = serializer.data["color"] 
		number = int(serializer.data["number"])
		q="businessDescription="+urllib.parse.quote_plus(businessDescription)+"&FilterByTags=&Colors="+urllib.parse.quote_plus(color)+"&text="+urllib.parse.quote_plus(name)+"&searchText="+urllib.parse.quote_plus(keywords.replace(' ',','))+"&customPrompt=&isFromAILogoGenerator=true"
		url=baseurl+q
		response = requests.get(url)
		res=[]
		for i in range(number):
			res.append(response.json()['assets'][i].get('imageUrl'))
		return Response(res)
	return Response("Unvalid Data")