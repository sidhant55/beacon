import os
from subprocess import Popen

def Main():
	text='TT:EE:SS:TT:OO:KK'
	ar=["<xpml><page quantity='0' pitch='15.0 mm'></xpml>SIZE 60 mm, 15 mm\r\n", 'GAP 3 mm, 0 mm\r\n', 'SPEED 3\r\n', 'DENSITY 15\r\n', 'SET RIBBON ON\r\n', 'DIRECTION 0,0\r\n', 'REFERENCE 0,0\r\n', 'OFFSET 0 mm\r\n', 'SET PEEL OFF\r\n', 'SET CUTTER OFF\r\n', 'SET PARTIAL_CUTTER OFF\r\n', "<xpml></page></xpml><xpml><page quantity='1' pitch='15.0 mm'></xpml>SET TEAR ON\r\n", 'CLS\r\n', 'BARCODE 464,86,"128",46,0,180,1,2,"{}"\r\n', 'CODEPAGE 1252\r\n', 'TEXT 448,34,"ROMAN.TTF",180,1,8,"{}"\r\n', 'BARCODE 224,86,"128",46,0,180,1,2,"{}"\r\n', 'TEXT 208,34,"ROMAN.TTF",180,1,8,"{}"\r\n', 'PRINT 1,1\r\n', '<xpml></page></xpml><xpml><end/></xpml>']
	ar[13]=ar[13].format(text)
	ar[15]=ar[15].format(text)
	ar[16]=ar[16].format(text)
	ar[17]=ar[17].format(text)

	with open("dumy.txt", "w") as text_file:
		for ro in ar:
			st=str(ro)
			text_file.write(st)

	p = Popen("testp.bat", cwd=r"C:\Users\Distronix\Desktop")
	stdout, stderr = p.communicate()	
	print(stderr,stdout)

if __name__ == '__main__':
	Main()