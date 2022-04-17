def B_Count(T):
    s=set(T)
    return len(s)


COMB=[]
Base=["A","C","T","G"]


for b1 in Base:
    for b2 in Base:
        for b3 in Base:
            for b4 in Base:
                COMB.append((b1,b2,b3,b4))

yes=[]

for c in COMB:
    
    if B_Count(c)==3:
        
        yes.append(c)
    

for c in yes:
    print(c if "A" in c else None)
print(len(yes))