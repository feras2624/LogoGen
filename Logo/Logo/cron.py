from pathlib import Path
import os
from django.conf import settings
tmp=os.path.join(settings.BASE_DIR,'LogoGen','tmp/')

def removetmp():
	print(tmp)
	[f.unlink() for f in Path(tmp).glob("*") if f.is_file()]