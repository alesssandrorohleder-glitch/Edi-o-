# Gera a marca d'água de prévia (pra mandar ao cliente antes do pagamento): faixa diagonal repetida "PRÉVIA · @alecreator_motion"
import sys
from PIL import Image,ImageDraw,ImageFont
def wm(w,h,out):
    big=Image.new('RGBA',(w*2,h*2),(0,0,0,0));d=ImageDraw.Draw(big);f=ImageFont.truetype('fonts/Poppins-Medium.ttf',54)
    s='PRÉVIA  ·  @alecreator_motion  ·  '
    for y in range(0,h*2,230):
        x0=-((y//230)%2)*300
        for x in range(x0,w*2,int(d.textlength(s,font=f))):d.text((x,y),s,font=f,fill=(255,255,255,80),stroke_width=2,stroke_fill=(40,10,20,70))
    big=big.rotate(28,resample=Image.BICUBIC).crop((w//2,h//2,w//2+w,h//2+h))
    d=ImageDraw.Draw(big);fb=ImageFont.truetype('fonts/Poppins-Medium.ttf',90);t='PRÉVIA';tw=d.textlength(t,font=fb)
    d.text(((w-tw)/2,h*.5-60),t,font=fb,fill=(255,255,255,110),stroke_width=4,stroke_fill=(40,10,20,90));big.save(out)
wm(1080,1920,'out/wm_reels.png');wm(1080,1350,'out/wm_carrossel.png')
