class TubeBender:
    def __init__(self, tube_diameter, line_length):
        self.tube_diameter = tube_diameter
        self.line_length = line_length  # Length of the line to be drawn in mm
        self.bends = []  # List to store bend information

    def add_bend(self, inches_in, angle):
        """
        Add a bend to the list.
        :param inches_in: Distance from the starting notch to where the bend line starts, in inches.
        :param angle: The angle around the cylinder where the bend line should be drawn, in degrees.
        """
        self.bends.append({'inches_in': inches_in, 'angle': angle})

    def plot_bends(self):
        """
        Generate a visual representation of the bends on the tube.
        """
        import matplotlib.pyplot as plt
        import numpy as np

        # Assuming the tube is "unwrapped" into a 2D plane for visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Draw each bend
        for bend in self.bends:
            # Convert inches to mm for plotting (assuming 25.4 mm per inch)
            distance_mm = bend['inches_in'] * 25.4
            angle_rad = np.radians(bend['angle'])
            
            # Calculate start and end points of the line
            start_x = distance_mm
            end_x = start_x + self.line_length * np.cos(angle_rad)
            start_y = self.tube_diameter / 2 * np.sin(angle_rad)
            end_y = start_y + self.line_length * np.sin(angle_rad)
            
            # Draw the line
            ax.plot([start_x, end_x], [start_y, end_y], 'k-', lw=2)  # 'k-' for black line

        ax.set_title('Tube Bending Lines')
        ax.set_xlabel('Distance along the tube (mm)')
        ax.set_ylabel('Circumferential position (mm)')
        plt.grid(True)
        plt.show()

# Example usage:
tube_diameter = 100  # Diameter of the tube in mm
line_length = 50  # Length of the line to be drawn in mm

bender = TubeBender(tube_diameter, line_length)
bender.add_bend(inches_in=24, angle=0)  # Add a bend 24 inches in, at 0 degrees
bender.add_bend(inches_in=24, angle=45)  # Add another bend 24 inches in, at 45 degrees
bender.plot_bends()  # Visualize the bends
