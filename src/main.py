import os, sys
from xml.dom.minidom import parse, parseString

print sys.argv

tioFile = parse(sys.argv[1])

for Node in tioFile.getElementsByTagName('EventList'):
	print Node.childNodes[0].nodeValue
