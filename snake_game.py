import tkinter as tk  # tkinter is a GUI (graphical user interface) used in python (tk top level width)
import random


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")  # game title

        self.title_label = tk.Label(self.root, text="Snake Game", font=("Helvetica", 24))
        self.title_label.pack(pady=20)  # Title move to center

        # Score label
        self.score = 0  # starting score
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 18))
        self.score_label.pack(pady=10)  # size of the score and make it to the center

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Helvetica", 16))
        self.start_button.pack(pady=20)  # Start game button

        self.root.geometry("660x660")  # size of the pop up white screen

        # Load background image
        self.background_image = tk.PhotoImage(file="ground.png")  # Ensure you have a "background.png"

        self.canvas = tk.Canvas(self.root, width=650, height=450)  # size of the game background window
        self.canvas.pack()

        self.snake_block = 20  # size of the snake and food
        self.snake_speed = 200  # milliseconds speed of snake
        self.snake = []
        self.direction = "Right"  # make our on decision
        self.food_position = None

    def start_game(self):
        self.score = 0  # score when game start
        self.score_label.config(text=f"Score: {self.score}")
        self.snake = [(300, 200), (300, 200)]  # size of the snake
        self.direction = "Right"
        self.food_position = self.create_food()
        self.start_button.pack_forget()  # Hide the start button
        self.run_game()

    def create_food(self):
        x = random.randint(0, (600 - self.snake_block) // self.snake_block) * self.snake_block  #WIDTH
        y = random.randint(0, (400 - self.snake_block) // self.snake_block) * self.snake_block  #HEIGHT
        return (x, y)

    def change_direction(self, event):  # snake moment using button
        if event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"

    def run_game(self):
        new_head = self.snake[0]

        if self.direction == "Left":
            new_head = (new_head[0] - self.snake_block, new_head[1])
        elif self.direction == "Right":
            new_head = (new_head[0] + self.snake_block, new_head[1])
        elif self.direction == "Up":
            new_head = (new_head[0], new_head[1] - self.snake_block)
        elif self.direction == "Down":
            new_head = (new_head[0], new_head[1] + self.snake_block)

        # Check for boundary collision
        if (new_head[0] < 0 or new_head[0] >= 650 or  # width
                new_head[1] < 0 or new_head[1] >= 450 or  # height
                new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Check for food collision
        if new_head == self.food_position:
            self.food_position = self.create_food()
            self.score += 1  # Increase the score
            self.score_label.config(text=f"Score: {self.score}")  # Update the score display
        else:
            self.snake.pop()

        self.update_canvas()
        self.root.after(self.snake_speed, self.run_game)

    def update_canvas(self):
        self.canvas.delete("all")  # Clear the canvas

        # Display the background image
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Draw food
        self.canvas.create_oval(self.food_position[0], self.food_position[1],  # Food shape to oval
                                self.food_position[0] + self.snake_block,
                                self.food_position[1] + self.snake_block,
                                fill="red")

        # Draw snake
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1],
                                         segment[0] + self.snake_block,
                                         segment[1] + self.snake_block,
                                         fill="blue")

    def game_over(self):
        self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Arial", 24))
        self.root.update()
        self.start_button.pack(pady=20)  # Show the start button again


# Main application window
root = tk.Tk()    # creates the main application window
game = SnakeGame(root) # initalizes the game by creating an instance of the SnakeGame clz, which sets up GUI and game logic.
root.bind("<KeyPress>", game.change_direction) # Bind key press event (to method that handles direction changes for the snake.)
root.mainloop() #starts the tkinter event loop(window open and game response acc; to user input)