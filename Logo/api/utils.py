from LogoGen.models import Logo
from .serializers import LogoSerializer
import requests
import urllib.parse
import base64
import os
import random
from datetime import datetime
from django.conf import settings


HOST = os.environ.get("HOST", default="http://localhost:8000")
baseurl='https://www.design.com/api/logo/more/1?'
MAX=5

def savefile(data):
	nd=data[1:].replace('\'','')
	tmp=os.path.join(os.getcwd(),'LogoGen','tmp')
	random.seed(datetime.now().timestamp())
	ran=str(random.randint(1, 1000))
	n=os.path.join(tmp, ran + '.png')
	with open(n,'wb') as f:
		#print(nd)
		f.write(base64.b64decode(nd))
	return HOST+os.path.join(settings.MEDIA_URL,'tmp', ran + '.png')


def savetodb(serializer):
	businessDescription =serializer.data["desc"]
	name = serializer.data["name"]
	keywords = serializer.data["desc"]
	color = serializer.data["color"] 
	q="businessDescription="+urllib.parse.quote_plus(businessDescription)+"&FilterByTags=&Colors="+urllib.parse.quote_plus(color)+"&text="+urllib.parse.quote_plus(name)+"&searchText="+urllib.parse.quote_plus(keywords.replace(' ',','))+"&customPrompt=&isFromAILogoGenerator=true"
	url=baseurl+q
	response = requests.get(url)
	res=[]
	for i in response.json()['assets']:
		res.append(i.get('imageUrl'))
	for r in res:
		d=requests.get(r)
		if d.status_code == 200:
			obj = Logo.objects.create(name=serializer.data["name"],desc=serializer.data["desc"],color=serializer.data["color"],img=base64.b64encode(d.content))
			obj.save()


def exist(serializer):
			values = Logo.objects.filter(desc=serializer.validated_data['desc']).values('img')
			lis=[]
			for i in range(MAX):
				random.seed(datetime.now().timestamp())
				r=random.randint(0,19)
				lis.append(savefile(values[r+random.randint(0,19)]['img']))
			return lis