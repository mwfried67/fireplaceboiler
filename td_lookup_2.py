#!/usr/bin/env python3
#Python 3.2.3
#This Works!!!!

class td_lookup: #Two dimensinal look up.
    def __init__(self, tdarray):
        self.tdarray = tdarray

    def td_lu(self, xin):
        #print (self.tdarray[1][3])# array references start with 0.
        #print ('xin = ', xin)
        lg = len(self.tdarray[1]) # determine number of elements
        #print ('length =  ', lg)
        i= 0
        tp = 1 #Inlialize to ascending x input
        if (self.tdarray[0][0] > self.tdarray[0][lg-1]):
            tp = 0 # decending x input.
            
        if (xin > self.tdarray[0][lg-1] and tp == 1):  #Ascending  out of range high end.
            return self.tdarray[1][lg-1]

        elif (xin < self.tdarray[0][0] and tp == 1):  #Ascending  out of range low end.
            return self.tdarray[1][0]
        
        elif (xin > self.tdarray[0][0] and tp == 0):  #Decending  out of range high end.
            return self.tdarray[1][0]
        
        elif (xin < self.tdarray[0][lg-1] and tp == 0):  #Decending  out of range low end.
            return self.tdarray[1][lg-1]
        
        else:
            while (((self.tdarray[0][i] <= xin) and (self.tdarray[0][i+1]>= xin))or\
                   ((self.tdarray[0][i] >= xin) and (self.tdarray[0][i+1]<= xin)))== False:
                i=i+1
                #print (i+1)
            return self.tdarray[1][i]+(self.tdarray[1][i+1]-self.tdarray[1][i])*((xin-self.tdarray[0][i])/(self.tdarray[0][i+1]-self.tdarray[0][i]))
        
#This is for a Mouser 527-0503-10k with 5V V+ and 5K pulldown.
#myarray = [[0.2419, 0.3175, 0.4112, 0.5254, 0.6619, 0.8207, 1.0028, 1.2059, 1.4285, 1.6666, 1.9149, 2.1686, 2.4217, 2.6695, 2.9073, \
#            3.1316, 3.3395, 3.530, 3.7026, 3.8568, 3.9948, 4.1165, 4.2237, 4.3178, 4.4001, 4.4717, 4.5344, 4.5889, 4.6365], \
#           [-4, 5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 95, 104, 113, 122, 131, 140, 149, 158, 167, 176, 185, 194, 203, 212, 221, 230, 239, 248]]
        
#myarray = [[1,2,3,4.3,6.1,10],[40.1,50.2,60.3,70.1,80.2,90]] #Ascending example
#myarray = [[10,6.1,4.3,3,2,1],[40.1,50.2,60.3,70.1,80.2,90]] #Descending example
#print (myarray[2])
#lu = td_lookup(myarray)
#tmp = lu.td_lu(2.99)
#print (tmp)
#print (myarray[0][1]) # Works
