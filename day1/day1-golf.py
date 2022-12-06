e=[sum([int(i)for i in j])for j in[k.split("\n")for k in open("input").read().split("\n\n")]]
print(max(e),sum(sorted(e,reverse=True)[:3]))
