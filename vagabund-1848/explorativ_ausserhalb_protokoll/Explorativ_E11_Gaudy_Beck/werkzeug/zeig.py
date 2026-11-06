import sys
from PIL import Image
d=sys.argv[1]; ps=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]
ims=[Image.open(f'arbeit/nach/img/{d}/{p}.png') for p in ps]
ims=[im.resize((im.width*55//100,im.height*55//100)) for im in ims]
W=sum(i.width for i in ims); H=max(i.height for i in ims)
c=Image.new('L',(W,H),255); x=0
for i in ims: c.paste(i,(x,0)); x+=i.width
c.save(out)
