import string as i
q=open("input").read().split("\n")
p={k:v for k,v in zip(i.ascii_lowercase+i.ascii_uppercase,range(1,53))}
s=t=0;z=set;x=list
for r in q:
    n=len(r)//2
    s+=p[x(z(r[:n])&z(r[n:]))[0]]
for g in range(0,len(q),3):
    a,b,c=q[g:g+3]
    t+=p[x(z(a)&z(b)&z(c))[0]]
print(s,t)