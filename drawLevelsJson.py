import matplotlib.pyplot as plt
import numpy as np
import json
from PIL import Image, ImageDraw, ImageFont


class drawDiag:
	##############################################################################################################
	### This class contains almost all of the relevant vectors for calculation (except for the xSpace vector). ###
	### The logic behind this class is that none of its class variables change during the calculation, they    ###
	### are only calculated once - at the beginning.														   ###
	##############################################################################################################
	def __init__(self, font=None, size=(800,600), nManifold=50, manifoldSizePercent=.9, manifoldERange=10.,
		nAcceptor=10, acceptorOffset=1., acceptorERange=1., nBridge=5, bridgeOffset=-1.):

		if (font):
			self.font=font
		else:
			self.font=ImageFont.truetype("Courier New Bold.ttf", 13)

		self.size=size
		self.fill=(256,256,256)
		self.siteWidth=self.size[0]*.075 #width of a site

		self.lMargin=self.size[0]*.01
		self.rMargin=self.size[0]*.05

		self.nManifold=nManifold #number of manifold states
		self.manifoldSizePercent=manifoldSizePercent #percentage of the screen the manifold will take up
		self.manifoldERange=manifoldERange #energy range of manifold

		self.nAcceptor=nAcceptor #number of acceptor states
		self.acceptorOffset=acceptorOffset #energy offset of acceptor levels from center of manifold
		self.acceptorERange=acceptorERange #energy range of acceptor

		self.nBridge=nBridge #number of bridge states
		self.bridgeOffset=bridgeOffset #energy offset of bridge levels from center of manifold

		self.pic = Image.new('RGB', self.size, self.fill)

	def makePic(self):
		self.drawManifold()
		self.drawAcceptor()
		self.drawBridge()
		self.pic.save('pic.png', "png")

	def drawManifold(self):

		draw = ImageDraw.Draw(self.pic)

		### X coords of the left and right of the manifold states ###
		manifoldLeft=self.lMargin
		manifoldRight=self.siteWidth+manifoldLeft

		### figure out the spacing to fit the entire manifold in 90% of the height of the box ###
		manifoldSpacing=self.size[1]/self.nManifold*self.manifoldSizePercent

		### The center of the manifold is the center of the picture ###
		manifoldCenter=self.size[1]*0.5

		### make a list of sites (with spacing normalized to 1) ###
		spacingList=np.linspace(-self.nManifold/2., self.nManifold/2., self.nManifold)

		for n in spacingList:
			### the X coord is fixed, Y is the normalized site*spacing + center
			leftCoord=(manifoldLeft,n*manifoldSpacing+manifoldCenter)
			rightCoord=(manifoldRight,n*manifoldSpacing+manifoldCenter)

			draw.line((leftCoord,rightCoord), fill=0, width=2)

		#### Draw Midline for reference ####
		draw.line((0,manifoldCenter,self.size[0],manifoldCenter), fill=(135,206,250), width=1)

		#### Write nSites ####
		draw.text((self.lMargin, self.size[1]-self.lMargin*3), "nManifold="+str(self.nManifold), fill=0, font=self.font)
		#### Write Erange ####
		draw.text((self.lMargin, self.lMargin*1), "Erange="+str(self.manifoldERange), fill=0, font=self.font)



	def drawAcceptor(self):
		draw = ImageDraw.Draw(self.pic)

		### X coords of the left and right of the manifold states ###
		acceptorLeft=self.size[0]-(self.siteWidth+self.rMargin)
		acceptorRight=self.size[0]-self.rMargin

		### multiply the manifoldSpacing (from above) by the ratio of acceptorRange/manifoldRange ###
		acceptorSpacing=self.size[1]/self.nAcceptor*(self.acceptorERange/self.manifoldERange)*self.manifoldSizePercent

		### Convert the offset height (in energy) to pixels###
		offsetPixels=self.size[1]*(self.acceptorOffset/self.manifoldERange)*self.manifoldSizePercent

		acceptorCenter=self.size[1]*0.5-offsetPixels

		### make a list of sites (with spacing normalized to 1) ###
		spacingList=np.linspace(-self.nAcceptor/2., self.nAcceptor/2., self.nAcceptor)

		for n in spacingList:
			### the X coord is fixed, Y is the normalized site*spacing + center
			leftCoord=(acceptorLeft,n*acceptorSpacing+acceptorCenter)
			rightCoord=(acceptorRight,n*acceptorSpacing+acceptorCenter)

			draw.line((leftCoord,rightCoord), fill=0, width=2)

		#### Write nSites ####
		draw.text((self.size[0]-self.rMargin*4, self.size[1]-self.lMargin*3), "nAcceptor="+str(self.nAcceptor), fill=0, font=self.font)
		draw.text((self.size[0]-self.rMargin*4, self.size[1]-self.lMargin*6), "Spacing="+str(self.acceptorERange/self.nAcceptor), fill=0, font=self.font)

		#### Write Erange ####
		draw.text((self.size[0]-self.rMargin*4,self.lMargin*1), "Erange="+str(self.acceptorERange), fill=0, font=self.font)
		draw.text((self.size[0]-self.rMargin*4,self.lMargin*4), "Offset="+str(self.acceptorOffset), fill=0, font=self.font)



	def drawBridge(self):
		draw = ImageDraw.Draw(self.pic)

		### the space we have to work with is in between the rightmost part of the donor and the leftmost part of the acceptor ###
		availSpace= self.size[0]-(self.siteWidth+self.lMargin+self.rMargin)

		### the leftmost coord of the available space
		leftLim=self.size[0]*0.5-availSpace*0.5
		### the rightmost coord of the available space
		rightLim=self.size[0]*0.5+availSpace*0.5

		### make a list of coordinates (not normalized!) for the center of the bridges. nBridge+2 to improve spacing ###
		bridgeCenters=np.linspace(leftLim,rightLim, self.nBridge+2)

		bridgeWidth=self.siteWidth*0.75

		### Convert the offset height (in energy) to pixels###
		offsetPixels=self.size[1]*(self.bridgeOffset/self.manifoldERange)*self.manifoldSizePercent

		### the ycoord of the bridge is just center minus offset ###
		yCoord=self.size[1]*0.5-offsetPixels

		### skip the fake leftmost and rightmost bridge sites ###
		for num, n in enumerate(bridgeCenters[1:-1]):

			### xCoords are just site (n) minus/plus half the bridge width
			leftCoord=(n-bridgeWidth*0.5,yCoord)
			rightCoord=(n+bridgeWidth*0.5,yCoord)

			draw.line((leftCoord,rightCoord), fill=0, width=4)

			### write bridge properties ###
			draw.text((n-bridgeWidth*0.5,yCoord-20),"f="+str(num),font=self.font, fill=0)


		### write the coupling values, and use the fake bridge site to let us put stuff in between bridges ###
		for i in range(len(bridgeCenters[:-1])):
			### average location of this and the next bridge
			avgLoc=(bridgeCenters[i]+bridgeCenters[i+1])*0.5

			### xCoord is set to the left of the bridges
			draw.text((avgLoc-bridgeWidth*0.5, yCoord-20) ,"Vs="+str(i), fill=0, font=self.font)
			draw.text((avgLoc-bridgeWidth*0.5, yCoord+10) ,"Vp="+str(i), fill=0, font=self.font)

		#### Write Brige offset ####
		draw.text((self.size[0]*0.4,self.lMargin*1), "Bridge Offset="+str(self.bridgeOffset), fill=0, font=self.font)



######################
### Set Parameters ###
######################

json_data=open('ins/input.json')
data = json.load(json_data)

imageParams={}

### Set the font, must be in same folder (or give path) ###
imageParams["font"]=ImageFont.truetype("Courier New Bold.ttf", 13)

imageParams["size"]=(800,600) #size of image

imageParams["nManifold"]=data["subunits"]["donor"]["n"] #number of manifold states
imageParams["manifoldSizePercent"]=.9 #percentage of the screen the manifold will take up
imageParams["manifoldERange"]=data["subunits"]["donor"]["bandWidth"] #energy range of manifold

imageParams["nAcceptor"]=data["subunits"]["acceptor"]["n"] #number of acceptor states
imageParams["acceptorOffset"]=data["subunits"]["acceptor"]["bandEdge"] #energy offset of acceptor levels from center of manifold
imageParams["acceptorERange"]=data["subunits"]["acceptor"]["bandWidth"] #energy range of acceptor

imageParams["nBridge"]=data["subunits"]["bridge"]["n"] #number of bridge states
imageParams["bridgeOffset"]=data["subunits"]["bridge"]["energy"] #energy offset of bridge levels from center of manifold


levelDiag=drawDiag(**imageParams)
levelDiag.makePic()

