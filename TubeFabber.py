import numpy as np
import matplotlib.pyplot as plt
import pyperclip

class PipeCutter:
    def __init__(self, cut_pipe_diameter, mount_pipe_diameter, angle_in_degrees, chordal_tolerance, pierce_time=1, bends=None, units='inches'):
        self.cut_pipe_diameter = cut_pipe_diameter
        self.mount_pipe_diameter = mount_pipe_diameter
        self.angle_in_degrees = angle_in_degrees
        self.chordal_tolerance = chordal_tolerance
        self.units = units
        self.pierce_time = pierce_time
        self.bends = bends if bends is not None else []
        self.die_diameter = die_diameter  # Add die diameter to the class attributes


    def add_bend(self, offset, angle, line_length):
        """
        Add a bend mark to the list.
        :param offset: Distance from the starting notch to where the bend line starts, in the unit specified during class initialization.
        :param angle: The angle around the cylinder where the bend line should be drawn, in degrees.
        :param line_length: Length of the line to be drawn, in the unit specified during class initialization.
        """
        # Convert offset and line_length to the class's unit system if necessary
        if self.units == 'mm':
            # Assuming offset and line_length are provided in inches, convert them to mm
            offset_in_mm = offset * 25.4
            line_length_in_mm = line_length * 25.4
            self.bends.append({'offset': offset_in_mm, 'angle': angle, 'line_length': line_length_in_mm})
        else:
            # If the class is already using inches, no conversion is needed
            self.bends.append({'offset': offset, 'angle': angle, 'line_length': line_length})

    def generate_bend_gcode(self):
        """
        Generate G-code for marking the bends on the tube, accurately calculating the rotational degrees.
        """
        gcode = ["G90 ; Absolute positioning",
                "G21 ; Set units to mm" if self.units == 'mm' else "G20 ; Set units to inches",
                "G0 Z1 ; Lift marker off the pipe initially"]

        # Calculate the tube's circumference in the same units as the line length
        tube_circumference = np.pi * self.cut_pipe_diameter * (25.4 if self.units == 'inches' else 1)

        for bend in self.bends:
            # Convert the line length to the same units as the tube's circumference for accurate calculation
            line_length_units = bend['line_length'] * (25.4 if self.units == 'inches' else 1)
            
            # Calculate the rotational degrees for the specified line length on the tube's surface
            rotation_degrees_for_line = (line_length_units / tube_circumference) * 360

            # Adjust the offset position
            adjusted_offset_units = bend['offset'] * (25.4 if self.units == 'mm' else 1)

            # G-code commands to position and draw the line
            gcode.append(f"G0 X{adjusted_offset_units:.3f} ; Move to adjusted offset position")
            gcode.append("G0 Z0 ; Lower marker to touch the pipe")
            
            # Calculate start and end angles to center the line at the specified angle
            start_angle = bend['angle'] - (rotation_degrees_for_line / 2)
            end_angle = bend['angle'] + (rotation_degrees_for_line / 2)
            
            gcode.append(f"G1 A{start_angle:.3f} ; Rotate to start angle")
            gcode.append(f"G1 A{end_angle:.3f} ; Draw the line by rotating to end angle")
            
            gcode.append("G0 Z1 ; Lift marker off the pipe")

        gcode += ["M2 ; End of program"]
        return gcode





    def plot_cutting_path(self):
        angle_in_radians = np.radians(self.angle_in_degrees)
        cut_pipe_circumference = np.pi * self.cut_pipe_diameter
        angles = np.linspace(0, 2 * np.pi, 360)

        if self.cut_pipe_diameter < self.mount_pipe_diameter:
            offset = (self.mount_pipe_diameter - self.cut_pipe_diameter) / 2
        else:
            offset = 0

        x = cut_pipe_circumference * angles / (2 * np.pi)
        y = offset + self.cut_pipe_diameter / 2 * np.sin(angle_in_radians / 2) * (1 + np.cos(angles))

        plt.figure(figsize=(12, 6))
        plt.plot(x, y)
        plt.xlim(0, cut_pipe_circumference)
        plt.ylim(0, self.mount_pipe_diameter)
        plt.title(f"Cutting Path for {self.angle_in_degrees} degrees")
        plt.xlabel("Unwrapped Circumference")
        plt.ylabel("Cut Depth")
        plt.grid(True)
        plt.show()

    def generate_gcode(self):
        x, y = self.get_cutting_path()
        gcode = ["G21" if self.units == 'mm' else "G20", "G90", "G92 X0 A0", "M3"]

        for i in range(len(x)):
            a = np.degrees(y[i] / np.pi)
            gcode.append(f"G1 X{x[i]:.3f} A{a:.3f}")
            if i == 0:
                gcode.append(f"G4 P{self.pierce_time}")

        gcode += ["M5", "M2"]
        return gcode

    def get_cutting_path(self):
        angle_in_radians = np.radians(self.angle_in_degrees)
        cut_pipe_circumference = np.pi * self.cut_pipe_diameter
        segment_length = self.chordal_tolerance
        total_length = cut_pipe_circumference * (1 + np.sin(angle_in_radians / 2))
        num_segments = max(int(total_length / segment_length), 1)

        angles = np.linspace(0, 2 * np.pi, num_segments)

        if self.cut_pipe_diameter < self.mount_pipe_diameter:
            offset = (self.mount_pipe_diameter - self.cut_pipe_diameter) / 2
        else:
            offset = 0

        x = cut_pipe_circumference * angles / (2 * np.pi)
        y = offset + self.cut_pipe_diameter / 2 * np.sin(angle_in_radians / 2) * (1 + np.cos(angles))
        return x, y

    def copy_gcode_to_clipboard(self, gcode=""):
        if gcode is None:
            gcode = self.generate_gcode()
        gcode_str = "\n".join(gcode)
        pyperclip.copy(gcode_str)
        print("G-code copied to clipboard.")
            
    def save_plot_as_svg(self, filename):
        x, y = self._calculate_path()
        fig, ax = plt.subplots()
        ax.plot(x, y, 'r')  # 'r' for red line, change as needed
        ax.set_axis_off()
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.set_position([0, 0, 1, 1])
        ax.set_aspect('auto')
        fig.savefig(filename, format='svg', bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close(fig)

    def _calculate_path(self):
        angle_in_radians = np.radians(self.angle_in_degrees)
        cut_pipe_circumference = np.pi * self.cut_pipe_diameter
        angles = np.linspace(0, 2 * np.pi, int(360 * self.chordal_tolerance))

        if self.cut_pipe_diameter < self.mount_pipe_diameter:
            offset = (self.mount_pipe_diameter - self.cut_pipe_diameter) / 2
        else:
            offset = 0

        x = cut_pipe_circumference * angles / (2 * np.pi)
        y = offset + self.cut_pipe_diameter / 2 * np.sin(angle_in_radians / 2) * (1 + np.cos(angles))
        return x, y


if __name__ == "__main__":
    
    # Initialize the PipeCutter instance with appropriate parameters
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

    # cutter.copy_gcode_to_clipboard()  # Uncomment to copy G-code to clipboard
    # cutter.save_plot_as_svg(filename="cut.svg")
    # cutter.plot_cutting_path()  # Uncomment to plot the cutting path

