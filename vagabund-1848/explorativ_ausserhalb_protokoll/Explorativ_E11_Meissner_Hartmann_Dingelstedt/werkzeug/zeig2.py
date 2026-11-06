import sys
from PIL import Image
ps=[x.split(':') for x in sys.argv[1].split(',')]; out=sys.argv[2]
ims=[Image.open(f'arbeit/nach/img/{d}/{p}.png') for d,p in ps]
H=1300
ims=[im.resize((im.width*H//im.height,H)) for im in ims]
W=sum(i.width for i in ims)
c=Image.new('L',(W,H),255); x=0
for i in ims: c.paste(i,(x,0)); x+=i.width
c.save(out)
