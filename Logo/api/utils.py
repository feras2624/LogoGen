from LogoGen.models import Logo
from .serializers import LogoSerializer
import requests
import urllib.parse
import base64
import os
import random
from datetime import datetime
from django.conf import settings


NAMELIX_URL = 'https://namelix.com/app/load2.php'

HOST = os.environ.get("HOST", default="http://localhost:8000")
baseurl='https://www.design.com/api/logo/more/1?'
MAX=10
Colors=['grayscale','blue','purple','pink','red','orange','yellow','green']

def LogoFromUrl(request,translated):
	businessDescription = translated
	name = request.data['name']
	keywords = translated
	lis=[]
	for c in Colors:
		color =  c
		q="businessDescription="+urllib.parse.quote_plus(businessDescription)+"&FilterByTags=&Colors="+urllib.parse.quote_plus(color)+"&text="+urllib.parse.quote_plus(name)+"&searchText="+urllib.parse.quote_plus(keywords.replace(' ',','))+"&customPrompt=&isFromAILogoGenerator=true"
		url=baseurl+q
		response = requests.get(url)
		res=[]
		for i in range(MAX):
			res.append(response.json()['assets'][i].get('imageUrl')+"&slogan=    ")
	#for i in response.json()['assets']:
	#	res.append(i.get('imageUrl'))
		for r in res:
			d=requests.get(r)
			if d.status_code == 200:
				data = str(base64.b64encode(d.content))
				nd = data[1:].replace('\'','')
				lis.append(nd)
	return lis


def getname(request):
		keywords=request.data['keywords']
		data=dict()
		data['keywords'] = ' '.join(keywords) if isinstance(keywords, list) else keywords
		data['styles[]'] = 'brandable'  # multiword, brandable, language, wordmix, spelling, dictionary, rhyme, person
		data['lengths[]'] = 'medium'  # short, medium, long
		resp = requests.post(NAMELIX_URL, data=data)
		sug=[]
		for i in range(MAX):
			sug.append(resp.json()[i].get('title'))
		return sug


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
				data = str(base64.b64encode(d.content))
				nd = data[1:].replace('\'','')
				print('\n',nd,'\n')
				obj = Logo.objects.create(name=serializer.data["name"],desc=translated,color=c,img=nd)
				obj.save()


def exist(serializer,translated):
			if serializer.validated_data['color'] not in Colors:
				return "Invalid Color"

			values = Logo.objects.filter(desc__contains=translated,color=serializer.validated_data['color']).values('img')
			lis=[]
			for v in values:
				#random.seed(datetime.now().timestamp())
				lis.append(v['img'])
				#print(values[i]['desc'])
			return lis