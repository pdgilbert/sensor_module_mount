# Simple support to mount sensor module onto outlet plate.
#  X shaped frame with mounting points on end of each leg.
# For sensor module with mount
# holes 43.5mm apart in x direction and 66.5 mm in y direction

# Open GUI interface and copy/paste to python console
# or
#   FreeCAD  --run  mount.py
# or (see  https://wiki.freecad.org/index.php?title=Flatpak )
# /usr/bin/flatpak --branch=stable --arch=x86_64 run --command=FreeCADCmd org.freecad.FreeCAD -c <mount.py

# The mount.stl output file goes to ./mount.stl  
# which will be ~/mount.stl if run in freecad started from the desktop menu.

# with GUI add
#import PartDesignGui, MeshPartGui

import Part, Mesh, MeshPart
import math

########################################################
############### construction parameters ################
########################################################

V = FreeCAD.Vector
ORIGIN   = V(0.0,   0.0, 0.0)    
DR = V(0,0,1)  # default direction specifying parts

#####  parameters In mm, 

Width             = 43.5   # hole centers
Length            = 66.5   # hole centers
FrameWidth        = 3.0 
FrameHeight       = 3.0 
PostLowerDia      = 3.0
PostUpperDia      = 1.8     #CHECK DIA OF MOUNT HOLES
PostLowerHeight   = FrameHeight + 5.0   
PostUpperHeight   = FrameHeight + 5.0 + 6.0  #CHECK 

#####  dimension check   #####

#print("tag thickness (mm)", Thickness)
#
#if not (0.0 < Thickness )  : complain0A    # 


#######################################
######     construction            #####
#######################################

diagional = (Length**2 + Width**2)**0.5

center1 = ORIGIN 
center2 = ORIGIN + V(0.0,     Width, 0.0)
center3 = ORIGIN + V(Length,  Width, 0.0)
center4 = ORIGIN + V(Length,   0.0,  0.0)

#dr = math.degrees(math.sin(Width/Length))    #34.862951896923214
#dr = math.degrees(math.sin(Width/diagional)) #29.821595155477542
dr = 33.2   # adjusted manually. There is something I do not understand about rotate.

cross1 = Part.makeBox(         
   diagional,     
   FrameHeight,
   FrameWidth,
   ORIGIN, 
   DR   
) 

cross2 = cross1.copy()

z = cross1.Placement.Base = center1 - V(0.0, FrameWidth/2.0,  0.0)
z = cross2.Placement.Base = center2 - V(0.0, FrameWidth/2.0,  0.0)

z = cross1.rotate(center1, DR,  dr)
z = cross2.rotate(center2, DR, -dr)

#z = Part.show(cross1)
#z = Part.show(cross2)

posts   = []
   
for c in [center1, center2, center3, center4] :
   posts.append(Part.makeCylinder(  #lower
      PostLowerDia/2.0,
      PostLowerHeight,   
      c,   #pnt
      DR    #direction
      )
   )
   posts.append(Part.makeCylinder(  #upper
      PostUpperDia/2.0,
      PostUpperHeight,  
      c,    #pnt
      DR     #direction
      )
   )
#for p in posts :
#   z = Part.show(p)

mount = cross1.fuse(cross2)
for p in posts :
   mount = mount.fuse(p)

#z = Part.show(mount)

#######################################
#####  Mesh
#######################################
outfile = "./" + "mount.stl"  #in ~ if kicad opened from menu
mount.exportStl(outfile) 

#######################################
#####  
#######################################

print("done")

print("Now to generate gcode do")
#print("slic3r " + outfile)  This does not work well. It does not seem to use defaults set for printer.
print("start  slic3r ")
print("   and open file " + outfile)
print("or examine with ")
print("meshlab " + outfile + " & ")
