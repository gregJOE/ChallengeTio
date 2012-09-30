import sys, os
sys.path.append('../pychallonge/')
sys.path.append('../pychallonge/challonge')
import challonge, match, player, tournament
import matches, tournaments, participants
import xml.etree.ElementTree as XMLParseTree

NULL_PLAYER = "00000000-0000-0000-0000-000000000000"
MATCH_BYE = "00000001-0001-0001-0101-010101010101"
class Tournament(object):
	
	def __init__(self, url, cID, game, event, bracketStyle, gameTree, root):
		self.unfinishedMatches = []
		self.completedMatches = []
		self.allMatches = []
		self.challongeID = cID
		self.game = game
		self.event = event
		self.bracketType = bracketStyle
		self.playerList = {}
		self.url = url
		challonge.set_credentials("ThaBlackFlash", 'o8w2yznrifwmp58koxfcyd7om4yrwv6czj38x2pu')
		challongeTournament = tournaments.create(self.event, "RKtest_tourney", "double elimination")
		self.challongeID = challongeTournament["id"]
		# xml = root of xml tree
		# entrantList = players in the event
		# game played in the tournament (tournament =/= event)
		self.createPlayers(gameTree, root.find('.PlayerList/Players'), game)
		
		self.fillBracket(gameTree, self.playerList)

	def startTournament():
		create(self.event, self.url, self.bracketType)
		publish(self.challongeID)
		start(self.challongeID)
		print "Tournament has been started. URL is " + url
	
	def setUrl(self, url):
		self.url = url

	def finish(self):
		print "finished"
	
	def restart(self):
		restart(self.challongeID)
		print "Tournament has been reset. Remember to start tournament again"
	def addMatch(self, match):
		self.matches.push(match)
	
	def createPlayers(self, xml, entrantList, game):
		entrantTree = xml.find('.Entrants')
		entrants = []
		for entrant in entrantTree:
			pID = entrant.text
			for players in entrantList:
				if players.find('.ID').text == pID:
					#print "Player found:" + players.find('.Nickname').text
					self.playerList[players.find('.ID').text] = player.Player(players.find('.Nickname').text, game, "", pID, "")
					participants.create(self.challongeID, self.playerList[players.find('ID').text].name)
					self.createPlayerChallongeIDs(self.playerList[players.find('ID').text])

			self.playerList[NULL_PLAYER] = player.Player("N/A", game, "None", NULL_PLAYER, "") 
			self.playerList[MATCH_BYE] = player.Player("Bye", game, "None", MATCH_BYE, "")

	def fillBracket(self, xml, playerList):
		# find matches in xml head
		print "fill bracket"
		for matches in xml.findall('.Bracket/Matches/Match'):
			p1 = matches.find('.Player1').text
			p2 = matches.find('.Player2').text
			gameRound = matches.find('.Round').text
			number = matches.find('.Number').text
			player1 = playerList[p1]
			player2 = playerList[p2]
			# is there a mapping function for finding stuff in arrays without loops
			matchDesc = match.Match(player1, player2, "SampleGame", "Sample", int(gameRound), number)
			if int(gameRound) < 0:
				matchDesc.isWinners = False
				matchDesc.bracketRound = matchDesc.bracketRound * -1

			matchDesc.setWinner(playerList[matches.find('.Winner').text]) 
			self.allMatches.append(matchDesc)
			if matchDesc.getWinner().name == "N/A":
				# this needs to make a new Match object
				# and push into the array
				self.unfinishedMatches.append(matchDesc)
			else:
				#print matchDesc.player1.name, " ", matchDesc.player2.name, " ", matchDesc.bracketRound, " ", matchDesc.matchNumber
				if matchDesc.player1.name != "Bye" and matchDesc.player2.name != "Bye":
					#print "Add!"
					self.completedMatches.append(matchDesc)

	
	def createPlayerChallongeIDs(self, player):
		challongePlayers = participants.index(self.challongeID)
		for players in challongePlayers:
			if player.name == players['name']:
				player.challongeID = players['id']
				print player.challongeID
		
	# Note, this function only really works if there are no byes in either bracket
	def swapIDsViaChallongeID(self, playerAID, playerBID):
		playerA = None
		playerB = None
		print "Ids to be swapped:", playerAID, playerBID
		if str(playerAID) == "None" and str(playerBID) == "None":
			return

		for players in self.playerList:
			print self.playerList[players].name, self.playerList[players].challongeID
			if self.playerList[players].challongeID == playerAID:
				playerA = self.playerList[players]
			
			if self.playerList[players].challongeID == playerBID:
				playerB = self.playerList[players]
	
		print "Swapping players"
		print playerA.name, " as player 2"
		print playerB.name, " as player 1"
                participants.update(self.challongeID, playerB.challongeID, name="PlaceHolderA")
                participants.update(self.challongeID, playerA.challongeID, name="PlaceHolderB")
                participants.update(self.challongeID, playerB.challongeID, name=playerA.name)
                participants.update(self.challongeID, playerA.challongeID, name=playerB.name)
		
		temp = self.playerList[playerA.tioID].challongeID
		self.playerList[playerA.tioID].challongeID = playerB.challongeID
		self.playerList[playerB.tioID].challongeID = temp
		print "-----------------------------------"

	def verifyBracket(self):
		print "Verify"
		print self.challongeID
		challongeBracket = matches.index(self.challongeID)
		
		# for now, since the tournament just started, assume the max round is 2
		(challongeRound1, tioRound1) = self.fillRoundArrays(1, challongeBracket)
                (challongeRound2, tioRound2) = self.fillRoundArrays(2, challongeBracket)
		
		length = len(challongeRound1)
		print "Challonge Length: ", length
		print "Tio Length: ", len(tioRound1)

		for i in range(0, length):
			print i
			print "Round:", tioRound1[i].bracketRound
			print challongeRound1[i]['player1-id'], challongeRound1[i]['player2-id']
			print tioRound1[i].player1.challongeID, tioRound1[i].player2.challongeID, tioRound1[i].player1.name, tioRound1[i].player2.name
			self.checkP1(challongeRound1[i], tioRound1[i])
			tioRound1[i].matchID = challongeRound1[i]['id']
			print "Is there a Winner?", tioRound1[i].getWinner().name
			if tioRound1[i].getWinner().name != "N/A":
				print "Updating match"
				if tioRound1[i].getWinner().challongeID == tioRound1[i].player1.challongeID:
					matches.update(self.challongeID, tioRound1[i].matchID, scores_csv='2-0', winner_id=tioRound1[i].getWinner().challongeID)
				else:
					matches.update(self.challongeID, tioRound1[i].matchID, scores_csv='0-2', winner_id=tioRound1[i].getWinner().challongeID)
				tioRound1[i].reported = True
		
		print "Bracket 2"
		length = len(challongeRound2) 
		print "Challonge Length: ", length
		print "Tio Length: ", len(tioRound2)        
		for i in range(0, length):
			print i
			print tioRound2[i]
			print "Round:", tioRound2[i].bracketRound
			print challongeRound2[i]['player1-id'], challongeRound2[i]['player2-id']
			print "cID p1 tio", tioRound2[i].player1.challongeID, "cID p2 tio", tioRound2[i].player2.challongeID, tioRound2[i].player1.name, tioRound2[i].player2.name
			self.checkP1(challongeRound2[i], tioRound2[i])
			tioRound2[i].matchID = challongeRound2[i]['id']
			print "Is there a Winner?", tioRound2[i].getWinner().name
			if tioRound2[i].getWinner().name != "N/A":
				print "Updating match"
				# combine these two statements into a Match function
				if tioRound2[i].getWinner().challongeID == tioRound2[i].player1.challongeID:
					matches.update(self.challongeID, tioRound2[i].matchID, scores_csv='2-0', winner_id=tioRound2[i].getWinner().challongeID)
				else:
					matches.update(self.challongeID, tioRound2[i].matchID, scores_csv='0-2', winner_id=tioRound2[i].getWinner().challongeID)
				tioRound2[i].reported = True

	def checkP1(self, challongeMatch, tioMatch):
		if challongeMatch['player1-id'] == tioMatch.player1.challongeID:
			self.checkP2(challongeMatch, tioMatch, True)
		else:
			if challongeMatch['player1-id'] == tioMatch.player2.challongeID:
				self.checkP2(challongeMatch, tioMatch, False)

			else:
                                self.swapIDsViaChallongeID(challongeMatch['player1-id'], tioMatch.player1.challongeID)
				self.checkP2(challongeMatch, tioMatch, True)
	
	def checkP2(self, challongeMatch, tioMatch, checkP2Con):
		if checkP2Con == True:
			if challongeMatch['player2-id'] != tioMatch.player2.challongeID:
				self.swapIDsViaChallongeID(challongeMatch['player2-id'], tioMatch.player2.challongeID)
		
		else:
			if challongeMatch['player2-id'] != tioMatch.player1.challongeID:
                                self.swapIDsViaChallongeID(challongeMatch['player2-id'], tioMatch.player1.challongeID)

	def fillRoundArrays(self, roundNum, data):
		# data == challonge stuff
		print "filling array ", roundNum
		challongeArray = []
		tioArray = []
		for challongeMatches in data:
			if roundNum == challongeMatches['round']:
				challongeArray.append(challongeMatches)
			else:
				if roundNum < challongeMatches['round']:
					break
		for matchInfo in self.unfinishedMatches:
			print "Match: ", matchInfo.matchNumber
			if roundNum == matchInfo.bracketRound:
				tioArray.append(matchInfo)
			else:
				if roundNum < matchInfo.bracketRound:
					break
					
		for matchInfo in self.completedMatches:
			print "Completed Match: ", matchInfo.matchNumber
			if roundNum == matchInfo.bracketRound:
				print "adding"
				tioArray.append(matchInfo)
			else:
				if roundNum < matchInfo.bracketRound:
					break
		return challongeArray, tioArray
	
	def updateBracket(self, xml):
		newUnfinishedMatches = []
		#xml should be the Match subtree
		for matchInfo in self.unfinishedMatches:
			print matchInfo.matchNumber
			for matchesXML in xml.findall('.Bracket/Matches/Match'):
				if matchesXML.find('.Number').text == matchInfo.matchNumber:
					if matchesXML.find('.Winner').text != NULL_PLAYER:
						print "Found!"
						matchInfo.winner = self.playerList[matchesXML.find('.Winner').text]
						matches.update(self.url, matchInfo.cID, scores_csv="2-0", winner_id=matchInfo.winner.cID) 
						break
		print "end"
