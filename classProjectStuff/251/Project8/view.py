#Owen Goldthwaite
#2/27/19

import numpy as np
import sys
import math

class View:					#extent, screen and offset can also be matrixes
	def __init__(self, vrp = np.matrix([0.5,0.5,1]), vpn = np.matrix([0,0,-1]), vup =
				np.matrix([0,1,0]), u = np.matrix([-1,0,0]), extent = [1.,1.,1.],
				screen = [400.,400.], offset = [20.,20.]): 
		#reset()		
		self.vrp = vrp
		self.vpn = vpn
		self.vup = vup
		self.u = u
		self.extent = extent
		self.screen = screen
		self.offset = offset
	
	def reset(self):
		self.vrp = np.matrix([0.5,0.5,1])
		self.vpn = np.matrix([0,0,-1])
		self.vup = np.matrix([0,1,0])
		self.u = np.matrix([-1,0,0])
		self.extent = [1.,1.,1.]
		self.screen = [400.,400.]
		self.offset = [20.,20.]

	#returns a normalized vector of the input vector
	def normalize(self, vector):
		length = math.sqrt(vector[0,0]*vector[0,0]+vector[0,1]*vector[0,1]+
											   vector[0,2]*vector[0,2])
		return np.matrix([vector[0,0]/length, vector[0,1]/length, vector[0,2]/length])

	def makeTranslationMat(self, val1, val2, val3):
		return np.matrix( [[1, 0, 0, val1],
                    	   [0, 1, 0, val2],
                    	   [0, 0, 1, val3],
                    	   [0, 0, 0, 1] ] )

	def makeScaleMat(self, val1, val2, val3):
		return np.matrix( [[val1, 0, 0, 0],
                    	   [0, val2, 0, 0],
                    	   [0, 0, val3, 0],
                    	   [0, 0, 0, 1] ] )	

	def build(self):
		vtm = np.identity(4, float)
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
                    		[0, 1, 0, -self.vrp[0, 1]],
                    		[0, 0, 1, -self.vrp[0, 2]],
                    		[0, 0, 0, 1] ] )

		vtm = t1 * vtm
		tu = np.cross(self.vup, self.vpn)
		tvup = np.cross(self.vpn, tu)
		tvpn = self.vpn.copy()
		
		tu = self.normalize(tu)
		tvup = self.normalize(tvup)
		tvpn = self.normalize(tvpn)
		self.u = tu
		self.vup = tvup
		self.vpn = tvpn		
		r1 = np.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
                    		[ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
                    		[ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
                    		[ 0.0, 0.0, 0.0, 1.0 ] ] )
		vtm = r1 * vtm

		vtm = self.makeTranslationMat(0.5*self.extent[0], 0.5*self.extent[1], 0) * vtm

		vtm = self.makeScaleMat(-self.screen[0] / self.extent[0], -self.screen[1] /
								 self.extent[1], 1.0 / self.extent[2]) * vtm
		vtm = self.makeTranslationMat(self.screen[0] + self.offset[0], self.screen[1] +
									  self.offset[1], 0) * vtm
		
		return vtm

	def clone(self):
		newView = View(self.vrp, self.vpn, self.vup, self.u, self.extent, self.screen, 						   self.offset)
		return newView

	def getVRP(self):
		return self.vrp

def main(argv):
	v = View()
	testmat1 = v.build()
	v2 = v.clone()
	testmat2 = v2.build()
	print(v)
	print(v2)
	print(testmat1)
	print(testmat2)
	
	


if __name__ == "__main__":
    main(sys.argv)


		
		
