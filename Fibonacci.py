# Author: Youssef Aitbouddroub
# 1/25/2025
# Visualization for the famous Fibonacci sequence

from manim import *
from math import *

class FibonacciSpiral(MovingCameraScene):
    def construct(self):
        # Display introductory text
        intro_text_1 = Text("Fibonacci sequence visualization", font_size=36)
        intro_text_2 = Text("Implemented by Youssef Aitbouddroub", font_size=24).next_to(intro_text_1, DOWN)

        # Group the texts together into a VGroup
        intro_group = VGroup(intro_text_1, intro_text_2)

        # Animate the group
        self.play(Write(intro_group))
        self.wait(2)
        self.play(FadeOut(intro_group))

        # Fibonacci function to generate sequence
        def fibonacci_function(n):
            fib = [1, 1]
            for _ in range(2, n):
                fib.append(fib[-1] + fib[-2])
            return fib

        # Generate the Fibonacci sequence
        fib_vect = fibonacci_function(18)  # Note: some values may result in out of range errors

        # Initialize starting position (top-left corner of the first square)
        x, y = 0, 0

        # Initialize the current direction: 0=right, 1=down, 2=left, 3=up
        direction = 0

        # Initialize bounds for the entire sequence
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0

        # Keep track of the current corner for spiral arcs
        arc_start = np.array([0, -1, 0])

        # Draw squares
        for i, size in enumerate(fib_vect):
            # Create the square
            square = Square(side_length=size, color=BLUE, fill_opacity=0.3, stroke_width=int(size/2)+1)
            square.move_to(np.array([x + size / 2, y - size / 2, 0])) 

            # Add Fibonacci number text inside the square
            fib_text = Text(str(fib_vect[i])).scale(int(size/2)+1)
            fib_text.move_to(square.get_center())  

            # Update bounds based on the current square
            min_x = min(min_x, x)
            max_x = max(max_x, x + size)
            min_y = min(min_y, y - size)
            max_y = max(max_y, y)

            # Animate the square and the text
            self.play(DrawBorderThenFill(square), Write(fib_text))

            # Add a spiral arc for this square
            arc_radius = size
            arc = Arc(
                radius=arc_radius,
                start_angle=PI / 2 * direction,
                angle=PI / 2,
                color=RED,
                stroke_width=int(size/2)+1,
            )

            # Update position for the next square
            if direction == 0:  # Moving right
                if i > 0:
                    arc_start = np.array([x, y - fib_vect[i], 0])
                    x += fib_vect[i]
                else:
                    x += size
            elif direction == 1:  # Moving down
                if i > 0:
                    arc_start = np.array([x + fib_vect[i], y - fib_vect[i], 0])
                    y -= fib_vect[i]
                    x -= fib_vect[i - 1]
                else:
                    y -= size
            elif direction == 2:  # Moving left
                if i > 0:
                    arc_start = np.array([x + fib_vect[i], y, 0])
                    x -= fib_vect[i + 1]
                    y += fib_vect[i - 1]
            elif direction == 3:  # Moving up
                if i > 0:
                    arc_start = np.array([x, y, 0])
                    y += fib_vect[i + 1]

            # Move the arc center to the updated position and flip it
            arc.move_arc_center_to(arc_start)
            arc.flip(axis=DOWN)
            self.play(Create(arc))

            # Update direction (cycle through 0, 1, 2, 3)
            direction = (direction + 1) % 4

            # Dynamically adjust camera to fit the bounding box
            frame_width = max_x - min_x
            frame_height = max_y - min_y
            max_dimension = max(frame_width, frame_height) * 3  # Add some padding
            # Animate the camera zoom and position
            self.play(
                self.camera.frame.animate.set_width(max_dimension).move_to(
                    np.array([(min_x + max_x) / 2, (min_y + max_y) / 2, 0])
                )
            )
            
        # Add a final wait time to view the result
        self.wait()
