# usage: stufe2.sh d  -> pass2 fuer neue Seiten aus rein/d nach reinp/d
d=$1; cd arbeit/nach; mkdir -p reinp/$d; st=$(mktemp -d)
for f in rein/$d/*.txt; do b=$(basename $f); [ -f reinp/$d/$b ] || cp $f $st/; done
[ -n "$(ls $st)" ] && python3 sk/pass2.py $st >/dev/null && cp $st/*.txt reinp/$d/; rm -rf $st; ls reinp/$d | wc -l
