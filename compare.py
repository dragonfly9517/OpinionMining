import re
from stemming.porter2 import stem

pos = open('positive-words.txt', 'r+')
neg = open('negative-words.txt', 'r+')
inc = open('increasingorder.txt', 'r+')
dec = open('decreasingorder.txt', 'r+')

pos = [line.strip() for line in open('positive-words.txt')]
neg = [line.strip() for line in open('negative-words.txt')]
inc = [line.strip() for line in open('increasingorder.txt')]
dec = [line.strip() for line in open('decreasingorder.txt')]

for i in range (len(pos)):
	pos[i]=stem(pos[i])
for i in range (len(neg)):
	neg[i]=stem(neg[i])
for i in range (len(inc)):
	inc[i]=stem(inc[i])
for i in range (len(dec)):
	dec[i]=stem(dec[i])

lineno = 1
outfile = open('Output.txt', 'w')

with open('input.txt') as input:


	#Getting the words out:
	for line in input:
		word1 = []
		word2 = []
		word3 = []
		word4 = []

		i = 0

		while i<len(line):
			if line[i]=='(':
				st=i
				while i<=len(line)-1:
					i+=1
					if line[i]==')':
						word4.append(line[st+1:i])
						break

			if line[i]=='1' and line[i+1]=='_':
				st=i
				while i<len(line)-1:
					i+=1
					if ((line[i]=='1' or line[i]=='2' or line[i]=='3')and line[i+1]=='_') or line[i]=='(':
						word1.append(line[st+2:i-1])
						break
				if i ==len(line)-2:
					word1.append(line[st+2:])
				if i<len(line)-1:
					i = i-2
			if line[i]=='2' and line[i+1]=='_':
				st = i
				while i<len(line)-1:
					i+=1
					if ((line[i]=='1' or line[i]=='2' or line[i]=='3')and line[i+1]=='_') or line[i]=='(':
						word2.append(line[st+2:i-1])
						break
				if i ==len(line)-2:
					word2.append(line[st+2:])
				if i<len(line)-1:
					i=i-2
			if line[i]=='3' and line[i+1]=='_':
				st=i
				while i<len(line)-1:
					i+=1
					if ((line[i]=='1' or line[i]=='2' or line[i]=='3')and line[i+1]=='_') or line[i]=='(':
						word3.append(line[st+2:i-1])
						break
				if i ==len(line)-2:
					word3.append(line[st+2:])
				if i<len(line)-1:
					i = i-2
			i+=1


		#Handling exception: only one entity present
		if len(word1) == 0:
			if len(word2)== 0:
				print 'No entities to compare'
				if len(word3)>0 and len(word4)>0:
					outfile.write(str(lineno)+'_notmatch_(1_< >2_< >3_<' + word3[0] +  '>4_<'+ word4[0]+'>\n')
				else:
					outfile.write(str(lineno)+'_notmatch_(1_< >2_< >3_<>4_<>\n')
			else:
				print word2[0]
				outfile.write(str(lineno) + '_' +  word2[0] + '\n')
			lineno = lineno +1
			continue

		if len(word2) == 0:
			if len(word1)==0:
				print 'No entities to compare'
				if len(word3)>0 and len(word4)>0:
					outfile.write(str(lineno)+'_notmatch_(1_< >2_< >3_<' +word3[0]+ '>4_<'+word4[0]+'>\n')
				else:
					outfile.write(str(lineno)+'_notmatch_(1_< >2_< >3_<>4_<>\n')
			else:
				print word1[0]
				outfile.write(str(lineno) + '_' +  word1[0] + '\n')
			lineno = lineno +1
			continue

		en1 = word1[0]
		en2 = word2[0]

		#Handling exception: more than one c or f
		if len(word4)>1:
			foo = 0
			while foo < len(word4):
				if stem(word4[foo]) in pos or stem(word4[foo]) in neg:
					c = word4[foo]
					break
				foo = foo + 1
			if foo == len(word4):
				c= word4[0]
		elif len(word4)==1:
			c = word4[0]
		else:
			c = ''
		
		if len(word3)==0 and len(word4)>0:
			if stem(word4[0]) in pos:
				outfile.write(str(lineno)+'_'+ word1[0]+'\n')
			elif stem(word4[0]) in neg:
				outfile.write(str(lineno)+'_'+ word2[0]+'\n')
			lineno = lineno + 1
			continue

		if len(word3)>1:
			foo = 0
			while foo < len(word3):
				if stem(word3[foo]) in pos or stem(word3[foo]) in neg:
					f= word3[foo]
					break
				foo = foo + 1
			if foo == len(word3):
				f= word3[0]
		elif len(word3)==1:
			f= word3[0]
		else:
			f = ''
		if stem(c) in pos:
			print en1
			outfile.write(str(lineno)+'_'+en1+'\n')
		elif stem(c) in neg:
			print en2
			outfile.write(str(lineno)+'_'+en2+'\n')
		else:
			if stem(f) in pos:
				if stem(c) in inc:
					print en2
					outfile.write(str(lineno) + '_' +  en2 + '\n')
				elif stem(c) in dec:
					print en1
					outfile.write(str(lineno) + '_' +  en1 + '\n')
				else:
					print 'No match found'
					outfile.write(str(lineno)+'_notmatch_(1_<')
					st=''
					for s in word1:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>2_<')
					st=''
					for s in word2:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>3_<')
					st=''
					for s in word3:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>4_<')
					for s in word4:
						outfile.write(s)
					outfile.write('>')
					outfile.write("\n")


			elif stem(f) in neg:
				if stem(c) in inc:
					print en1
					outfile.write(str(lineno) + '_' +  en1 + '\n')
				elif stem(c) in dec:
					print en2
					outfile.write(str(lineno) + '_' +  en2 + '\n')
				else:
					print 'No match found'
					outfile.write(str(lineno)+'_notmatch_(1_<')
					st=''
					for s in word1:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>2_<')
					st=''
					for s in word2:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>3_<')
					st=''
					for s in word3:
						st=st+s
						st=st+','
					outfile.write(st[:-1])
					outfile.write('>4_<')
					for s in word4:
						outfile.write(s)
					outfile.write('>')
					outfile.write("\n")
			else:
				print 'No match found'
				outfile.write(str(lineno)+'_notmatch_(1_<')
				st=''
				for s in word1:
					st=st+s
					st=st+','
				outfile.write(st[:-1])
				outfile.write('>2_<')
				st=''
				for s in word2:
					st=st+s
					st=st+','
				outfile.write(st[:-1])
				outfile.write('>3_<')
				st=''
				for s in word3:
					st=st+s
					st=st+','
				outfile.write(st[:-1])
				outfile.write('>4_<')
				for s in word4:
					outfile.write(s)
				outfile.write('>')
				outfile.write("\n")

		lineno = lineno+1
