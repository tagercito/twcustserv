
#mi codigo
replydm = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed feugiat enim id pretium imperdiet. Maecenas fringilla ut ligula vel posuere. Phasellus scelerisque, massa id egestas hendrerit, nibh lectus hendrerit sapien, a rutrum ligula enim non nibh. Etiam id arcu urna. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pulvinar nibh ac.'
replydm_splitted=[]
continua=' (cont)'
"""
def split(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]

for each in split(replydm, 133):
		replydm_splitted.append(each)

for splits in replydm_splitted:
	if splits != replydm_splitted[-1]:
		print splits+continua 
	else:
		print splits 

"""
def split(s, l):
  l.append(s[:130])
  if len(s) < 130:return l
  return split(s[130:], l)
#print split(replydm, []))

for splits in split(replydm, []):
  if splits != split(replydm, [])[-1]:
    print splits+continua 
  else:
    print splits

#tager's code
'''
string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed feugiat enim id pretium imperdiet. Maecenas fringilla ut ligula vel posuere. Phasellus scelerisque, massa id egestas hendrerit, nibh lectus hendrerit sapien, a rutrum ligula enim non nibh. Etiam id arcu urna. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed pulvinar nibh ac.'
lis = []
while 1:
       l = string[:140]
       lis.append(l)
       string = string[140:]
       if len(string) < 140:
               lis.append(l)
               break

print lis'''