c=v=0
for l in open("i").read().split("\n"):
    s,e,q,r=map(int,l.replace(",","-").split("-"))
    c+=(s>=q)&(e<=r)|(q>=s)&(r<=e)
    v+=(e>=q)&(r>=s)
print(c,v)