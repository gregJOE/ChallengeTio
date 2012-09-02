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
					print "Player found:" + players.find('.Nickname').text
					self.playerList[players.find('.ID').text] = player.Player(players.find('.Nickname').text, game, "", pID, "")
					participants.create(self.challongeID, self.playerList[players.find('ID').text].name)
					self.createPlayerChallongeIDs(self.playerList[players.find('ID').text])

			self.playerList[NULL_PLAYER] = "N/A"
			self.playerList[MATCH_BYE] = "Bye"

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
			
			matchDesc = match.Match(player1, player2, "SampleGame", "Sample", gameRound, number)
			matchDesc.setWinner(playerList[matches.find('.Winner').text]) 
			if matchDesc.getWinner() == "N/A":
				# this needs to make a new Match object
				# and push into the array
				self.unfinishedMatches.append(matchDesc)
				
			else:
				self.completedMatches.append(matchDesc)	

	
	def createPlayerChallongeIDs(self, player):
		challongePlayers = participants.index(self.challongeID)
		for players in challongePlayers:
			if player.name == players['name']:
				player.challongeID = players['id']
				print player.challongeID
		
	def swapIDs(self, playerAName, playerBName):
		playerA = None
		playerB = None

		for players in self.playerList:
			print players
			if type(self.playerList[players]) == player.Player:
				if self.playerList[players].name == playerAName:
					playerA = self.playerList[players]
			
				if self.playerList[players].name == playerBName:
					playerB = self.playerList[players]
				
				print type(playerA)	
				if type(playerA) == type(playerB) and type(playerA) != None:
					break;

		participants.update(self.challongeID, playerB.challongeID, name="PlaceHolderA")
		participants.update(self.challongeID, playerA.challongeID, name="PlaceHolderB")
                participants.update(self.challongeID, playerB.challongeID, name=playerA.name)
                participants.update(self.challongeID, playerA.challongeID, name=playerB.name)
	
	def swapIDsViaChallongeID(self, playerAcID, palyerBcID):
                playerA = None
                playerB = None

                for players in self.playerList:
                        print players
                        if type(self.playerList[players]) == player.Player:
                                if self.playerList[players].challongeID == playerAcID:
                                        playerA = self.playerList[players]

                                if self.playerList[players].name == playerBcID:
                                        playerB = self.playerList[players]

                                print type(playerA)
                                if type(playerA) == type(playerB) and type(playerA) != None:
                                        break;

                participants.update(self.challongeID, playerB.challongeID, name="PlaceHolderA")
                participants.update(self.challongeID, playerA.challongeID, name="PlaceHolderB")
                participants.update(self.challongeID, playerB.challongeID, name=playerA.name)
                participants.update(self.challongeID, playerA.challongeID, name=playerB.name)


	def verifyBracket(self):
		print "Verify"
		challongeBracket = matches.index("RKtest_tourney")
		for matchesChallonge in challongeBracket:
			print matchesChallonge['id']
			for cMatches in self.completedMatches:
				if cMatches.player1.challongeID != matchesChallonge['player1-id'] and cMatches.player2.challongeID == matchesChallonge['player2-id']:
					swapIDsViaChallongeID(cMatches.player1.challongeID, matchesChallonge['player1-id'])

				elif cMatches.player1.challongeID == matchesChallonge['player1-id'] and cMatches.player2.challongeID != matchesChallonge['player2-id']:
					swapIDsViaChallongeID(cMatches.player2.challongeID, matchesChallonge['player2-id'])
