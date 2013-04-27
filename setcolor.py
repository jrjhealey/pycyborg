#!/usr/bin/python2

#setcolor r g b  -> sets for all devices
#setcolor -n 1  r g b -> sets only for first device
#setcolor -p center r g b -> sets for all devices in center
#setcolor  -i 100 r g b -> sets intensity

from optparse import OptionParser
import sys
from pycyborg import get_all_cyborgs,POSITION

if __name__=='__main__':
    optionparser=OptionParser()
    optionparser.add_option("-n",type="int", dest="num",help="only change n-th device color (start at 0)")
    optionparser.add_option("-p",dest="position",help="only search for devices at the specified position. possible values are: center,n,ne,e,se,s,sw,w,nw")
    optionparser.add_option("-i",type="int", dest="intensity",help="set intensity (0-100)")
    
    (options,pargs) = optionparser.parse_args()
    
    #pargs must be 3 values
    if len(pargs)!=3:
        print "missing r/g/b values"
        optionparser.print_help()
        sys.exit(1)
    
    try:
        r,g,b=int(pargs[0]),int(pargs[1]),int(pargs[2])
    except:
        print "r g b must be integers 0-255"
        optionparser.print_help()
        sys.exit(1)
        
    
    if r<0 or r>255 or g<0 or g>255 or b<0 or b>255:
        print "r g b must be integers 0-255"
        optionparser.print_help()
        sys.exit(1)
    
    if options.intensity!=None:
        if options.intensity<0 or options.intensity>100:
            print "intensity must be 0-100"
            optionparser.print_help()
            sys.exit(1)
    
    pos=None
    if options.position!=None:
        pos=options.position.upper()
        if pos not in POSITION:
            print "position must be one of: center,n,ne,e,se,s,sw,w,nw"
            optionparser.print_help()
            sys.exit(1)
        
    #end arg checking
    
    
    cyborgs=get_all_cyborgs(lights_off=False)
    
    #filter by position
    if pos!=None:
        lst=[]
        for cyborg in cyborgs:
            if cyborg.position==pos:
                lst.append(cyborg)
        
        cyborgs=lst
        
    if options.num!=None:
        try:
            onlyone=cyborgs[options.num]
            cyborgs=[onlyone,]
        except:
            print "can not select index %s from cyborgs. I have %s"(options.num,len(cyborgs))
            sys.exit(1)
    
    
    #cyborg candidate list complete, perform the update
    for cy in cyborgs:
        if options.intensity!=None:
            cy.set_intensity(options.intensity)
        
        cy.set_rgb_color(r,g,b)
            
    
    
    
    
            
        
    
    
    