import pygame
import math
import numpy as np

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
BACKGROUND_COLOR = (0, 255, 0)
FRICTION = 0.3
clock = pygame.time.Clock() 
dt = clock.tick(60) / 1000.0 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball and Stick Game")


def draw_trees():
    # Draw better trees in the background
    tree_foliage_color = (0, 128, 0)  # Dark green color for foliage
    tree_trunk_color = (139, 69, 19)  # Brown color for tree trunk

    # Example tree positions and sizes
    tree_positions = [
        (50, 525, 15, 60),  # Small tree
        (60, 525, 20, 80),  # Slightly larger tree
        (80, 525, 15, 60),  # Small tree
        (100, 525, 20, 80),  # Slightly larger tree
        (250, 525, 15, 60),  # Small tree
        (450, 525, 20, 80),  # Slightly larger tree
        (460, 525, 15, 60),  # Small tree
        (470, 525, 20, 80),  # Slightly larger tree
        (480, 525, 15, 60),  # Small tree
        (500, 525, 20, 80)   # Slightly larger tree
    ]

    for tree_pos in tree_positions:
        x, y, width, height = tree_pos

        # Draw the tree trunk directly below the foliage
        trunk_width = width // 4
        trunk_height = height - (height // 3)  # Adjust the trunk height as needed
        trunk_x = x - trunk_width // 2
        trunk_y = y - height
        pygame.draw.rect(screen, tree_trunk_color, (trunk_x, trunk_y, trunk_width, trunk_height))

        # Draw the tree foliage (a simple triangle)
        foliage_height = height - trunk_height
        pygame.draw.polygon(screen, tree_foliage_color, [(x - width // 2, y - height), (x + width // 2, y - height), (x, y - height - foliage_height)])


def get_gravity():
    try:
        gravity = float(input("Enter the gravity value (m/s^2): "))
        return gravity
    except ValueError:
        print("Invalid input. Please enter a valid numerical value.")
        return get_gravity()

def main():
    # Initialize game variables
    swing_speed = 100
    swing_angle = np.pi / 4
    ball = Ball(50, 50, swing_speed, swing_angle)
    stick = Stick()
    # GRAVITY = get_gravity()
     # Create a clock object
    time_passed = 0.0  # Initialize time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input for swinging stick
        # ...

        # Calculate time passed since the last frame and update it
         # 60 FPS, converted to seconds
        time_passed += dt
        # Update game objects
        ball.update(time_passed)  # Pass the time to update function
        stick.update(swing_speed, swing_angle)

        # handle_collisions(ball, stick)

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the game objects
        ball.draw()
        stick.draw()
        draw_trees()
        pygame.display.update()

    pygame.quit()

class Ball:
    def __init__(self, x, y, speed, theta):
        self.x = x
        self.y = y
        self.x_0 = x
        self.y_0 = y
        self.speed = speed  # Initial speed of the ball
        self.theta = math.radians(theta)  # Initial angle of launch in radians
        self.velocity_x_0 = self.speed * math.cos(self.theta)  # Initial velocity in the x-direction
        self.velocity_y_0 = self.speed * math.sin(self.theta)  # Initial velocity in the y-direction
        self.velocity_y = self.velocity_y_0
        self.velocity_x = self.velocity_x_0
        self.radius = 10
        self.time = 0.0  # Time elapsed for this ball
        self.time_of_collison_y = 0.0
        self.time_of_collison_x = 0.0
        self.gravity = get_gravity()
        
    def update(self, time_passed):
        # Update ball position and velocity based on physics
        if (np.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2) < 1e-4):
            return
        self.time = time_passed
        new_x = self.x + self.velocity_x * (dt)
        new_y = self.y_0 + self.velocity_y_0 * (self.time - self.time_of_collison_y) + 0.5 * self.gravity * ((self.time - self.time_of_collison_y) ** 2)
        
        if new_y - self.radius < 0:
            new_y = self.radius  # Place the ball just above the ground
            self.y_0 = new_y
            self.velocity_y *= -0.8  # Reverse the vertical velocity with some loss
            self.velocity_y_0 = -0.8 * self.velocity_y
            self.time_of_collison_y = self.time
        # Checking for collisions
        if new_y + self.radius > SCREEN_HEIGHT:
            self.time_of_collison_y = self.time
            self.velocity_y_0 = -0.8 * self.velocity_y
            self.velocity_y *= -0.8
            new_y = SCREEN_HEIGHT - self.radius
            self.y_0 = new_y
        # Check for collisions with the screen boundaries
        if new_x - self.radius < 0 or new_x + self.radius > SCREEN_WIDTH:
            if new_x < self.radius:
                new_x = self.radius
            else:
                new_x = SCREEN_WIDTH - self.radius
            self.velocity_x *= -0.8  # Reverse the horizontal velocity with some loss
            self.x_0 = new_x
            self.time_of_collison_x = self.time
        # Update position and velocity after handling collisions
        self.x = new_x
        self.y = new_y
        self.velocity_y = self.velocity_y_0 + self.gravity * (self.time - self.time_of_collison_y)  # Apply gravity
        # If ball is on the ground, apply friction coefficient to reduce x velocity
        if self.y == SCREEN_HEIGHT - self.radius:
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - FRICTION * dt)
            else:
                self.velocity_x = min(0, self.velocity_x + FRICTION * dt)
    def draw(self):
        print(f"speed x = {self.velocity_x}, dt = {dt}")
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)

class Stick:
    def __init__(self):
        self.angle = 0  # Stick angle
        self.length = 100 # Stick length
        self.width = 5
        self.tip_x = 0
        self.tip_y = 0
        self.base_x = 0
        self.base_y = 100

    def update(self, swing_speed, swing_angle_degrees):
        # Convert the swing angle from degrees to radians
        swing_angle_radians = math.radians(swing_angle_degrees)

        # Calculate the new angle of the stick
        self.angle += swing_angle_radians

        # Limit the swing speed to a maximum of 100 km/hr (approximately 27.8 m/s)
        if swing_speed > 27.8:
            swing_speed = 27.8

        # Calculate the horizontal and vertical components of the swing velocity
        swing_velocity_x = swing_speed * math.cos(self.angle)
        swing_velocity_y = swing_speed * math.sin(self.angle)

        # Calculate the new tip coordinates
        self.tip_x = self.base_x + swing_velocity_x
        self.tip_y = self.base_y - swing_velocity_y

    def draw(self):
        pygame.draw.line(screen, (0, 0, 0), (0, 0), (int(self.tip_x), int(self.tip_y)), 5)

def handle_collisions(ball, stick):
    # Check if the ball has collided with the ground
    if ball.y - ball.radius < 0:
        ball.y = ball.radius  # Place the ball just above the ground
        ball.velocity_y *= -0.8  # Reverse the vertical velocity with some loss

    # Check if the ball has collided with the stick
    stick_vector = pygame.Vector2(stick.tip_x - stick.base_x, stick.tip_y - stick.base_y)
    ball_vector = pygame.Vector2(ball.x - stick.base_x, ball.y - stick.base_y)
    angle_between = stick_vector.angle_to(ball_vector)

    if 0 < angle_between < 90 and ball_vector.length() < stick.length:
        # Calculate the velocity change for the ball due to the stick collision
        ball_velocity = pygame.Vector2(ball.velocity_x, ball.velocity_y)
        ball_velocity.reflect_ip(stick_vector)

        # Apply a speed reduction of 20% upon collision
        ball.velocity_x = ball_velocity.x * 0.8
        ball.velocity_y = ball_velocity.y * 0.8

    # Check if the ball has collided with the screen boundaries
    if ball.x - ball.radius < 0 or ball.x + ball.radius > SCREEN_WIDTH:
        ball.velocity_x *= -0.8  # Reverse the horizontal velocity with some loss

    # Ensure the ball stays within the screen bounds
    ball.x = max(ball.radius, min(ball.x, SCREEN_WIDTH - ball.radius))

if __name__ == "__main__":
    main()
