import os, sys
sys.path.append('../pychallonge/')

import xml.etree.ElementTree as XMLParseTree

import challonge, tournament, tournaments, matches

NULL_PLAYER = "00000000-0000-0000-0000-000000000000"

print sys.argv

tioTree = XMLParseTree.parse(sys.argv[1])
tioRoot = tioTree.getroot()

for child in tioRoot.findall('.//Event/Games/'):
	# if child.find('./Name').text == sys.argv[2]
	#	requestedBracket = child.find('.
	#	break
	exitLoop = 0
	subchild = child.findall('.Name')
	for requestedTourney in subchild:
		if requestedTourney.text == sys.argv[2]:
			exitLoop = 1
			break
	if exitLoop == 1:
		break


bracketSize = child.find('.Bracket/Size').text
tioTournament = tournament.Tournament("", child.find('.ID').text, child.find('.Name'), "Sample", child.find('.BracketType').text, child, tioRoot)
#challonge.tournaments.publish(tioTournament.challongeID)
print "Created Tournament"
tournaments.publish(tioTournament.challongeID)
tournaments.start(tioTournament.challongeID)
print tioTournament.challongeID

#array = matches.index(tioTournament.challongeID)

tioTournament.verifyBracket()
tioTournament.updateBracket(child)
