import sys, os
sys.path.append('../pychallonge/')
sys.path.append('../pychallonge/challonge')
import challonge, match, player, tournament
import matches, tournaments, participants
import xml.etree.ElementTree as XMLParseTree

NULL_PLAYER = "00000000-0000-0000-0000-000000000000"
MATCH_BYE = "00000001-0001-0001-0101-010101010101"
class Tournament(object):
	
	# come up with better names for gameTree / tioDoc
	def __init__(self, url, cID, game, event, bracketStyle, gameTree, tioDoc):

		self.initializeLists()
		self.challongeID = cID
		self.game = game
		self.event = event
		self.bracketType = bracketStyle
		self.url = url
		
		self.setChallongeCredentials("ThaBlackFlash", 'o8w2yznrifwmp58koxfcyd7om4yrwv6czj38x2pu')
		self.challongeID = createChallongeTournament("RKtest_tourney", "double elimination")
		# xml = root of xml tree
		# entrantList = players in the event
		# game played in the tournament (tournament =/= event)
		self.setupTournament(gameTree, tioDoc)

	def setChallongeCredentials(self, username, challongeKey):
		challonge.set_credentials(username, challongeKey)
	
	def initializeLists(self):
		self.unfinishedMatches = []
		self.completedMatches = []
		self.allMatches = []
		self.playerList = {}
		
	def createChallongeTournament(self, name, bracketStyle):
		challongeTournament = tournaments.create(self.event, "RKtest_tourney", "double elimination")
		return challongeTournament["id"]
		
	def setupTournament(self, gameTree, tioDoc):
		self.createPlayersFromEntrantList(gameTree, root.find('.PlayerList/Players'), game)
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
	
	def addToMatchList(self, match):
		self.matches.push(match)
	
	def createPlayersFromEntrantList(self, xml, entrantList, game):
		# xml: top of the tree containing current game tournament information
		print "Creating players"
		entrantTree = xml.find('.Entrants')
		entrants = []
		for entrant in entrantTree:
			pID = entrant.text
			for players in entrantList:
				if players.find('.ID').text == pID:
					#print "Player found:" + players.find('.Nickname').text
					self.playerList[players.find('.ID').text] = player.Player(players.find('.Nickname').text, game, "", pID, "")
					self.addPlayerToChallongeTournament(self.playerList[players.find('.ID').text].name)
					
			self.playerList[NULL_PLAYER] = player.Player("N/A", game, "None", NULL_PLAYER, "") 
			self.playerList[MATCH_BYE] = player.Player("Bye", game, "None", MATCH_BYE, "")

	def createSpecialPlayersNullAndBye(self)
	
	def assignPlayerChallongeID(self, playerName):
		player.challongeID = findPlayerIDInChallonge(self, player.name):
	
	def addPlayerToChallongeTournament(self, playerName):
		participants.create(self.challongeID, playerName)
		self.assignPlayerChallongeID(playerName)
		
	def findPlayerIDInChallonge(self, name):
		challongePlayers = participants.index(self.challongeID)
		for players in challongePlayers:
			if player.name == players['name']:
				return players['id']

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


	def setWinnersOrLosersBracket(self, gameRound, matchInfo):
		if int(gameRound) < 0:
			matchInfo.isWinners = False
			matchInfo.bracketRound = matchDesc.bracketRound * -1
			
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

		for i in range(0, length):
			self.checkP1(challongeRound1[i], tioRound1[i])
			tioRound1[i].matchID = challongeRound1[i]['id']
			if tioRound1[i].getWinner().name != "N/A":
				updateWinnerToChallonge(self, tioRound1[i])
				
		length = len(challongeRound2)     
		for i in range(0, length):
			self.checkP1(challongeRound2[i], tioRound2[i])
			tioRound2[i].matchID = challongeRound2[i]['id']
			if tioRound2[i].getWinner().name != "N/A":
				updateWinnerToChallonge(self, tioRound2[i])

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
			matchData = obtainMatchFromXML(self, matchNumber, xmlDoc)
				if matchData.find('.Winner').text != NULL_PLAYER:
					print "Found!"
					matchInfo.winner = self.playerList[matchesXML.find('.Winner').text]
					matches.update(self.url, matchInfo.cID, scores_csv="2-0", winner_id=matchInfo.winner.cID) 
					break
		print "end"

	def obtainMatchFromXML(self, matchNumber, xmlDoc)
		for matchesXML in xml.findall('.Bracket/Matches/Match'):
				if matchesXML.find('.Number').text == matchInfo.matchNumber:
					return matchXML
		return None
		
	def updateWinnerToChallonge(self, matchData)
		if matchData.getWinner().challongeID == matchData.player1.challongeID:
			matches.update(self.challongeID, matchData.matchID, scores_csv='2-0', winner_id=matchData.getWinner().challongeID)
		else:
			matches.update(self.challongeID, matchData.matchID, scores_csv='0-2', winner_id=matchData.getWinner().challongeID)
		
		matchData.reported = True