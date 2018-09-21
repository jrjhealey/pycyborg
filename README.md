# pycyborg

Python library for the mad catz cyborg ambx gaming lights
(http://www.ambx.com/product/cyborg-gaming-lights)

## Status
 - protocol reverse engineering: done
 - simple demo without library: done
 - library: done
 - boblight interface: done
 - installer: done
 - tested platforms: Linux(Arch,Ubuntu,OpenElec,Raspbian) , Mac OS X, Win10

## Requires :
 - libusb 1.0 ( http://www.libusb.org/ ) or libusb-win32 (http://zadig.akeo.ie/)
 - pyusb  ( https://github.com/walac/pyusb/ )

## Scripts

* ```identify.py``` : activate all cyborg gaming lights and print out some information
* ```setcolor.py``` : control the gaming lights from the shell (from bash scripts etc)
* ```boblight.py``` : boblight interface
* ```lightpack-prismatik.py``` : [lightpack](http://lightpack.tv/index.php) client
* a few demo scripts are available in the ```demo``` folder

## getting started

* install libusb-1.0 (or libusb-win32 via zadig)
* install pyusb 1.0 ( use your distro's package or directly from  github: https://github.com/walac/pyusb/ )
* get the source

### Install either as a package:

    wget http://github.com/gryphius/pycyborg/tarball/master -O pycyborg.tar.gz
    tar -xvzf pycyborg.tar.gz
    cd gryphius-pycyborg*

### or clone git repo

    git clone git://github.com/gryphius/pycyborg.git
    cd pycyborg


#### Install

install the package and reload udev rules

    python setup.py install
    sudo udevadm trigger   # unix only

#### Test

this should flash your gaming lights and print out some info.
if you skipped step 2 you must run this as root, eg. sudo python identify.py or you will get ```USBError: [Errno 13] Access denied``` (insufficient permissions)

    python identify.py


console output should be similar to this:

    found and initialized 2 cyborg ambx gaming lights

    Cyborg 1:
    <Cyborg position=NW v_pos=low intensity=50%>

    Cyborg 2:
    <Cyborg position=S v_pos=low intensity=50%>


## boblight

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


there is also a simple wizard that can automatically generate a config file. this is especially useful if you have more than two lights:


    python boblight.py --makeconfig


## Other useful/interesting resources
http://projects.stephenklancher.com/project/id/89/amBX_Usability_Enhancements

## sprint113's Reddit instructions for PyCyborg
#### 1. Install Python

#### 2. Download and extract the pycyborg files.

#### 3. Install the AMBX cyborg lights w/libusb-win32 drivers. Download Zadig and open it. Options -> List all devices. Then from the main dropdown menu, I found the Cyborg lights, and to the right of the green arrow, I selected libusb-win32 and installed that driver.

#### 4. Install pyusb. This is done by opening a command prompt and entering

    pip install pyusb

#### 5. Test if the lights work, in a command prompt, change directory to where you extracted the pycyborg files and enter the line

    python setup.py install

Some text will show up. Keep an eye out for any error messages. Next run the command:

    python identify.py

This runs the identification script. Your connected light(s) will one by one cycle through some colors. Some text will be shown, and you will likely see a light with Location. This is a useful tool for solving the bug where the lights disappear from the Ambx control panel. This happens because the Location can sometimes become `[None]` and there doesn't appear to be any other real way to resolve this directly.

We now need to manually change the location. I ended up doing a hack job of a modification to one of the existing scripts in the folder. In a text editor (IDLE will be installed by default), open the setcolor.py file. Save it as a new file, e.g. setlocation.py.

At the end of the file, you will have the lines of code:

    for cy in cyborgs:
    if options.verbose:
        print("Changing : %s"%cy)
    if options.intensity!=None:
        cy.set_intensity(options.intensity)
    cy.set_rgb_color(r,g,b,force=True)

which I changed to:

    for cy in cyborgs:
    if options.verbose:
        print("Changing : %s"%cy)
    cy.set_position("N")
    cy.set_intensity(100)

**NB** I've written my own slightly less hacky version of this which is in the repo as `resetlights.py`. It now includes an option to specify a location, and so it may be invoked as:

    python resetlights.py -n <lightnumber> -i <intensity> -l <location> 255 255 255

### Old README content
-----
>If you know which position you want the light to be, use that instead of cy.set_position. Valid entries are N, NE, NW, E, W, SE, SW, S, CENTER (case sensitive). You may want to change the intensity value if you normally use something that isn't 100. Save the file.
>In the command prompt, run
>   python setlocation.py 255 255 255
>or whatever new file name you used. In this case, I was lazy and didn't change anything else, so the script is still expecting 3 numbers, but won't do anything with them. This should write the location you specified to the light.
>Now if you either go back to your computer with the ambx lights, or uninstall the libusb-32 drivers and reinstall the cyborg drivers, you the lights should now show up in the ambx control panel.
----

# How to revert from `libusb` to MadCatz drivers on Windows 10 (since Zadig can't do it)

1. Find the 2 light devices in device manager (it might be easier to switch the default View to `by connection` rather than `by type`).
 - They are normally called something like "amBX Cyborg Gaming Lights"

2. Click on the device and `Update Driver` -> `Browse my computer...` ->  `Let me pick from a list...` -> `USB Input Device` (or similar `HID`)
 - This should restore their default drivers (assuming you've installed them from the MadCatz driver utility at least once in the first place)

3. They should revert to using the correct drivers now (and will no longer be visible to `pycyborg`.


# glOW for amBX by Matt Callaghan
Also included in the repo is Matt Callaghan's excellent glOW tool, which can essentially replace all the amBX suite. I'm adding it here (if he has no objections), for posterity.

http://mattcallaghan.blogspot.com/2016/01/ambx-glow.html


# How to alter the registry power-off status (prevents lights from flickering/cutting out)

Modified with my own observations from Stere0man's Reddit Instructions (https://www.reddit.com/r/ambx/comments/4ebmbg/cyborg_lights_windows_10/):

First you need to download the drivers from the madcatz site here http://madcatz.com/downloads/

the drivers are listed under windows 7/8 drivers, there are currently no official windows 10 drivers so just download the x86 or x64 windows 7/8 drivers depending on your OS, (for windows 10 64 get the x64 version and for windows 10 32 get the x86 version)

Once downloaded extract and install the drivers by running Cyborg_amBX_LightPod_SD7_00000025_64_Full_pfw.exe

this will install both the drivers and the Ambx software, once they are installed run ambx control panel and check for updates, you may have to check a few times until its fully updated.

once updated reboot the computer, on reboot the lights will not work, they come on for a second then switch off, this is where it gets tricky:

1. Open up Device Manager. Once in, locate the cyborg lights under Human Interface Devices, right click `Cyborg amBX Gaming Light (HID)` and select properties, this will open a properties window, from there select `Details` and from the drop down menu select `Hardware Ids`. Note down the Hardware ID's for all the lights you have.

They look something like:
HID\VID_06A3&PID_0DC5&REV_0110

2. Open the Windows Registry Editor (`Win + R` followed by typing `regedit` will suffice). You can search for the hardware IDs, but it took me to the wrong part of the registry. Ensure that you end up in a path that looks like this:

        HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB\VID_06A3&PID_0DC5\6&10488bfd&0&1\Device Parameters
                                                                   ^ This should match each light hardware ID

3. Click on Device Parameters and in the right window pane you should see 3 Dword strings

        AllowIdleIrpInD3

        DeviceSelectiveSuspended

        EnhancedPowerManagementEnabled

##### *Disable* all of these by editing its hexadecimal value from 1 to 0 and save the changes.

4. Rinse and repeat the above steps for all the lights (they should be listed under one another, but double check your hardware IDs to be safe, its easy to break things when messing about in the registry).

5. Reboot the computer and the lights should now stay illuminated (this can be tested with amBX Illuminate, or glOW).

If they are still not working you may need to go into device manager again and click Universal Serial Bus Controllers and open properties on each USB Root hub and select Power Management and make sure there's no ticks in Allow the computer to turn off this device to save power.
