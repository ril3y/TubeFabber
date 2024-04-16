﻿# TubeFabber
This program output's gcode for a 2 axis tube notching / bending marking machine I have designed.
## Operation:
 ### Initialize the PipeCutter instance with appropriate parameters
    # Note: You'll need to adjust the cut_pipe_diameter and mount_pipe_diameter to match your actual tube specifications.
    cut_pipe_diameter = 2.0  # Example diameter in inches
    mount_pipe_diameter = 2.0  # Example mount diameter in inches (might not be needed for bend marking)
    angle_in_degrees = 15  # Not directly relevant for bend marking but required for initialization
    chordal_tolerance = 0.1  # Not directly relevant for bend marking but required for initialization
    units = 'inches'  # Working in inches
    pierce_time = 1  # Not directly relevant for bend marking but required for initialization
    
    die_diameter=3
    cutter = PipeCutter(cut_pipe_diameter, mount_pipe_diameter, angle_in_degrees, chordal_tolerance, die_diameter)




    cutter.add_bend(offset=24, angle=0, line_length=.5)
    cutter.add_bend(offset=12, angle=0, line_length=.5)
    # Generate the G-code for the added bend
    gcode = cutter.generate_bend_gcode()
    cutter.copy_gcode_to_clipboard(gcode)  # Uncomment to copy G-code to clipboard
