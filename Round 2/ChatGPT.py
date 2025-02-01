import tkinter as tk
import random

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Dodger")
        
        self.main_menu()
    
    def main_menu(self):
        self.clear_screen()
        self.menu_frame = tk.Frame(self.root, bg="black")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(self.menu_frame, text="BLOCK DODGER", fg="white", bg="black", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        start_button = tk.Button(self.menu_frame, text="Start Game", command=self.start_game, font=("Arial", 16))
        start_button.pack(pady=10)
        
        quit_button = tk.Button(self.menu_frame, text="Quit", command=self.root.quit, font=("Arial", 16))
        quit_button.pack(pady=10)
    
    def start_game(self):
        self.menu_frame.destroy()
        self.game_screen()
    
    def game_screen(self):
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="black")
        self.canvas.pack()
        
        self.player = self.canvas.create_oval(180, 550, 220, 590, fill="cyan")
        self.obstacles = []
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        
        self.speed = 5
        self.running = True
        self.spawn_obstacle()
        self.update_game()
    
    def move_left(self, event):
        if self.canvas.coords(self.player)[0] > 10:
            self.canvas.move(self.player, -20, 0)
    
    def move_right(self, event):
        if self.canvas.coords(self.player)[2] < 390:
            self.canvas.move(self.player, 20, 0)
    
    def spawn_obstacle(self):
        x_pos = random.randint(20, 380)
        obs = self.canvas.create_rectangle(x_pos, 0, x_pos+40, 40, fill="red")
        self.obstacles.append(obs)
        if self.running:
            self.root.after(1000, self.spawn_obstacle)
    
    def update_game(self):
        for obs in self.obstacles:
            self.canvas.move(obs, 0, self.speed)
            if self.check_collision(obs):
                self.game_over()
                return
        
        self.obstacles = [obs for obs in self.obstacles if self.canvas.coords(obs)[1] < 600]
        if self.running:
            self.root.after(50, self.update_game)
    
    def check_collision(self, obs):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        ox1, oy1, ox2, oy2 = self.canvas.coords(obs)
        return px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1
    
    def game_over(self):
        self.running = False
        self.canvas.create_text(200, 300, text="GAME OVER", fill="white", font=("Arial", 24, "bold"))
        self.root.after(2000, self.main_menu)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = GameApp(root)
    root.mainloop()
