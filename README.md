# 3D Printer Plotter
This repo contains a little python postprocessor script based on [svg2gcode](https://github.com/sameer/svg2gcode).
It only works for window. If you want it for linux, you know how.

## Usage

 1. Find some way to mount a spring loaded pen to your printer
	 - I like to use a pilot g2 with the rotating cam removed and the spring put above the cartridge [Picture(https://github.com/qwirty123/3d-printer-Plotter/blob/main/pics/1000004080.jpg)
 2. Make a svg design the size of your build plate minus about 5mm on each side
	 - If you're using inkscape, make sure that when you export, use the Page tab and not the Document tab. If you don't, the plot will be on the bottom left side of the print bed.
	 - If you want to plot text, you must convert the font to a path
	 - If you use a regular font, it will draw the outline of the text. [Photo](/pics/1000004072.jpg)
	 - If you want to draw text in a single stroke, use the **Hershey Text** extension in inkscape and use a stroke font.
 3. Edit main.py with your file and settings
	 - Z_HOP_THRESH: svg2gcode will put a z-hop for every path stroke. This will take a long time. This setting removes z-hops below a set threshold. This is great for writing text.
       - See [Picture](/pics/1000004074.jpg)
	 - The settings file contains settings for svg2gcode.
		 - Tool on and tool off are for starting and stopping strokes. I set them to raise and lower by 5mm.
		 - Feedrate is speed in mm/min
		 - Begin sequence only homes the X and Y axes. Whatever height the gcodes starts at is z=0.
 4. Run main.py and transfer the resulting gcode file to your printer
	 - You can preview gcode using [ncviewer](https://ncviewer.com/). For some reason prusa gcode viewer doesn't work.
 5. Put a piece of paper on your printbed
 6. Manually move the z axis such that the pen is touching the paper. Moving the gantry should write on the paper. Make sure it is not too low. Raising the pen by 5mm should make it no longer be writing.
 7. Run the gcode file. The following should happen
	 - Pen moves up by 10mm
	 - X and Y axes home
	 - Plotter starts to draw
 8. If you're using default marlin, make sure you don't click 'cancel print' in the middle of a plot. It will home the x and y axes, drawing a giant line across your page. Just power it off
	 - If you want to change that, compile you own marlin firmware and change EVENT_GCODE_SD_ABORT in configurations_adv.h to something like G0 Z20
