import sys, os
sys.path.append('../pychallonge/')
import challonge

class Player(object):
	def __init__(self, name, game, challongeID, tioID, seed):
		self.name = name
		self.game = game
		self.challongeID = challongeID
		self.tioID = tioID
		self.seed = seed

	def getName():
		return self.name
	
	def getGamePlaying():
		return self.game
	
	def getChallongeID():
		return self.challongeID
		
	def getTioID():
		return self.tioID
	
	def getSeed():
		return self.seed

	def setName(name):
		self.name = name
	
	def setGamePlaying(game):
		self.game = game
	
	def setChallongeID(cID):
		self.challongeID = cID
	
	def setTioID(tID):
		self.tioID = tID

