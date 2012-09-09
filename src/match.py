import sys, os
sys.path.append('../pychallonge/')
sys.path.append('.')
import challonge, player

class Match(object):
	def __init__(self, p1, p2, game, event, gameRound, number):
		self.player1 = p1
		self.player2 = p2
		self.game = game
		self.event = event
		self.bracketRound = gameRound
		self.isWinners = "True"
		self.matchNumber = number
		self.winner = "None"

	def getPlayer1(self):
		return self.player1
	
	def getPlayer2(self):
		return self.player2
	
	def getGame(self):
		return self.game
	
	def getEvent(self):
		return self.event
	
	def getBracketRound(self):
		return self.bracketRound
	
	def getMatchNumber(self):	
		return self.matchNumber

	def getWinner(self):
		return self.winner

	def setPlayer1(self, player1):
		self.player1 = player1

	def setPlayer2(self, player2):
		self.player2 = player2
		
	def setGame(self, game):
		self.game = game
	
	def setEvent(self, event):
		self.event = event
	
	def setBracketRound(bracket):
		self.bracketRound = bracket
	
	def setWinner(self, player):
		self.winner = player
