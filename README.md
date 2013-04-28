pycyborg
========

Python library for the cyborg ambx gaming lights 
(http://www.cyborggaming.com/prod/ambx.htm)


Status:
 - protocol reverse engineering: done
 - simple demo without library: done
 - library: done
 - boblight interface: done
 - installer: todo
 - tested plattforms: Linux

Requires : 
 - pyusb 1.0 ( https://github.com/walac/pyusb/ )


scripts
-------

"colortransitiondemo.py" : a quick test of a single cyborg gaming light (doesn't use the full library - this was the first test script)

"identify.py" : to activate all cyborg gaming lights and print out some information (position, intensity)

"setcolor.py" : control the gaming lights from the shell (from bash scripts etc) 


getting started
---------------

* install pyusb 1.0 ( use your distros package or directly from  github: https://github.com/walac/pyusb/ )
*  (optional) create a udev rule to make the gaming lights accessible for non-root users

put a file '80-cyborg.rules' in /etc/udev/rules.d with the following content:

    SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0dc5", MODE="666"
    
activate the rule:
 
    sudo udevadm trigger

* check out pycyborg from github:

from your home directory:

    git clone git://github.com/gryphius/pycyborg.git

* test

this should flash your gaming lights and print out some info. 
if you skipped step 2 you must run this as root, eg. sudo python identify.py or you will get USBError: [Errno 13] Access denied (insufficient permissions)

    cd pycyborg
    python identify.py
 

console output should be similar to this:

    found and initialized 2 cyborg ambx gaming lights
    	
    Cyborg 1: 
    <Cyborg position=NW v_pos=low intensity=50%>
    
    Cyborg 2: 
    <Cyborg position=S v_pos=low intensity=50%>


boblight
--------

To control the cyborg lights from boblight (http://code.google.com/p/boblight/), use a config file like below
(change the path in 'output' to where you checked out pycyborg)


	[global]
	interface 127.0.0.1
	port 19333
	
	[device]
	name cyborg_ambx
	output /home/gryphius/gitspace/pycyborg/boblight.py
	channels 6
	type popen
	interval 500000
	
	[color]
	name red
	rgb FF0000
	
	[color]
	name green
	rgb 00FF00
	
	[color]
	name blue
	rgb 0000FF
	
	[light]
	name cyborg-left
	color red cyborg_ambx 1
	color green cyborg_ambx 2
	color blue cyborg_ambx 3
	hscan 0 49.9
	vscan 0 100
	
	[light]
	name cyborg-right
	color red cyborg_ambx 4
	color green cyborg_ambx 5
	color blue cyborg_ambx 6
	hscan 50 100
	vscan 0 100

