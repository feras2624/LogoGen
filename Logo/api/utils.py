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
MAX=10
Colors=['grayscale','blue','purple','pink','red','orange','yellow','green']

def savefile(data):
	nd=data[1:].replace('\'','')
	tmp=os.path.join(settings.BASE_DIR,'LogoGen','tmp')
	random.seed(datetime.now().timestamp())
	ran=str(random.randint(1, 1000))
	n=os.path.join(tmp, ran + '.png')
	with open(n,'wb') as f:
		#print(nd)
		f.write(base64.b64decode(nd))
	return HOST+os.path.join(settings.MEDIA_URL,'tmp', ran + '.png')


def savetodb(serializer,translated):
	businessDescription = translated
	name = "TP22L"
	keywords = translated
	for c in Colors:
		color =  c
		q="businessDescription="+urllib.parse.quote_plus(businessDescription)+"&FilterByTags=&Colors="+urllib.parse.quote_plus(color)+"&text="+urllib.parse.quote_plus(name)+"&searchText="+urllib.parse.quote_plus(keywords.replace(' ',','))+"&customPrompt=&isFromAILogoGenerator=true"
		url=baseurl+q
		response = requests.get(url)
		res=[]
		for i in range(MAX):
			res.append(response.json()['assets'][i].get('imageUrl').replace("TP22L","    ")+"&slogan=    ")
	#for i in response.json()['assets']:
	#	res.append(i.get('imageUrl'))
		for r in res:
			d=requests.get(r)
			if d.status_code == 200:
				obj = Logo.objects.create(name=serializer.data["name"],desc=translated,color=c,img=base64.b64encode(d.content))
				obj.save()


def exist(serializer,translated):
			if serializer.validated_data['color'] not in Colors:
				return "Invalid Color"

			values = Logo.objects.filter(desc__contains=translated,color=serializer.validated_data['color']).values('img')
			lis=[]
			for i in range(MAX-1):
				#random.seed(datetime.now().timestamp())
				lis.append(savefile(values[i]['img']))
				#print(values[i]['desc'])
			return lis