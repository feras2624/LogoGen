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
		serializer.save()
		businessDescription =request.data["desc"]
		name = request.data["name"]
		keywords = request.data["desc"]
		color = request.data["color"] 
		number = int(request.data["number"]) if int(request.data["number"])<=25 else 25
		q="businessDescription="+urllib.parse.quote_plus(businessDescription)+"&FilterByTags=&Colors="+urllib.parse.quote_plus(color)+"&text="+urllib.parse.quote_plus(name)+"&searchText="+urllib.parse.quote_plus(keywords.replace(' ',','))+"&customPrompt=&isFromAILogoGenerator=true"
		url=baseurl+q
		response = requests.get(url)
		res=[]
		for i in range(number):
			res.append(response.json()['assets'][i].get('imageUrl'))
		return Response(res)
	return Response("Unvalid Data")