# $1 input, $2 output pattern/file, extra args
G="scale=1080:1920:flags=lanczos,gblur=sigma=0.55,huesaturation=hue=0:saturation=-0.22:intensity=0:colors=r+y:strength=1,eq=saturation=0.88:contrast=0.93,curves=all='0/0.045 0.2/0.19 0.5/0.49 0.8/0.78 1/0.93',colorbalance=rs=-0.03:gs=0.0:bs=0.035:rh=0.025:gh=0.01:bh=-0.03,colortemperature=temperature=6200:mix=0.25,vignette=angle=PI/5.5"
echo "$G"
