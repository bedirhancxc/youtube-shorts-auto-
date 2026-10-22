import json, os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

root=Path(__file__).resolve().parents[1]
meta=json.loads((root/'output/metadata.json').read_text(encoding='utf-8'))
needed=['YOUTUBE_CLIENT_ID','YOUTUBE_CLIENT_SECRET','YOUTUBE_REFRESH_TOKEN']
missing=[x for x in needed if not os.getenv(x)]
if missing:raise SystemExit('Missing GitHub Actions secrets: '+', '.join(missing))
creds=Credentials(token=None,refresh_token=os.environ['YOUTUBE_REFRESH_TOKEN'],token_uri='https://oauth2.googleapis.com/token',client_id=os.environ['YOUTUBE_CLIENT_ID'],client_secret=os.environ['YOUTUBE_CLIENT_SECRET'],scopes=['https://www.googleapis.com/auth/youtube.upload'])
service=build('youtube','v3',credentials=creds,cache_discovery=False)
request=service.videos().insert(part='snippet,status',body={'snippet':{'title':meta['title'],'description':meta['description'],'tags':meta['tags'],'categoryId':'28'},'status':{'privacyStatus':'private','selfDeclaredMadeForKids':False}},media_body=MediaFileUpload(str(root/'output/short.mp4'),mimetype='video/mp4',resumable=True))
response=None
while response is None:_,response=request.next_chunk()
print('Uploaded private video:',response['id'])
