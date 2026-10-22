import json, math, os, random, subprocess, datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
topics=json.loads((ROOT/'content/topics.json').read_text(encoding='utf-8'))
index=int(datetime.datetime.now(datetime.timezone.utc).strftime('%j'))%len(topics)
topic=topics[index]
out=ROOT/'output';out.mkdir(exist_ok=True)
(out/'metadata.json').write_text(json.dumps(topic,ensure_ascii=False),encoding='utf-8')
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(font_path,48)
small=ImageFont.truetype(font_path,27)
W,H=720,1280
frames=out/'frames';frames.mkdir(exist_ok=True)
def wrap(draw,text,limit=580):
    words=text.split();lines=[];line=''
    for word in words:
        trial=(line+' '+word).strip()
        if draw.textbbox((0,0),trial,font=font)[2]>limit and line:
            lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    return lines
for n in range(18):
    im=Image.new('RGB',(W,H),(7,12,35));d=ImageDraw.Draw(im)
    random.seed(31)
    for k in range(95):
        x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,2])
        d.ellipse((x,y,x+r,y+r),fill=(125,145,200))
    cx,cy=360,520
    for r in range(230,0,-1):
        t=r/230
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(int(220-80*t),int(118-65*t),int(46-25*t)))
    d.text((W//2,125),'SPACE FACTS',font=small,anchor='mm',fill='#a6d5ff')
    line=topic['lines'][min(n//5,len(topic['lines'])-1)]
    lines=wrap(d,line)
    y=850-(len(lines)-1)*33
    for s in lines:
        d.text((W//2,y),s,font=font,anchor='mm',fill='white',stroke_width=2,stroke_fill='#16213e')
        y+=70
    d.text((W//2,1140),'FOLLOW FOR MORE',font=small,anchor='mm',fill='#ffd68a')
    im.save(frames/f'{n:03}.png')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ffmpeg,'-y','-framerate','1','-i',str(frames/'%03d.png'),'-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-t','18','-c:v','libx264','-pix_fmt','yuv420p','-r','30','-c:a','aac','-shortest',str(out/'short.mp4')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
print('Rendered',out/'short.mp4')
