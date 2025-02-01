import tkinter as tk
import random

class SpaceShooter:
    def __init__(self, root):
        self.root = root
        self.root.title("Galactic Defender")
        self.main_menu()
    
    def main_menu(self):
        self.clear_screen()
        self.menu_frame = tk.Frame(self.root, bg="black")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(self.menu_frame, text="GALACTIC DEFENDER", fg="white", bg="black", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        start_button = tk.Button(self.menu_frame, text="Start Game", command=self.start_game, font=("Arial", 16))
        start_button.pack(pady=10)
        
        options_button = tk.Button(self.menu_frame, text="Options", command=self.options_menu, font=("Arial", 16))
        options_button.pack(pady=10)
        
        quit_button = tk.Button(self.menu_frame, text="Quit", command=self.root.quit, font=("Arial", 16))
        quit_button.pack(pady=10)
    
    def options_menu(self):
        self.clear_screen()
        self.options_frame = tk.Frame(self.root, bg="black")
        self.options_frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(self.options_frame, text="OPTIONS", fg="white", bg="black", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        
        back_button = tk.Button(self.options_frame, text="Back", command=self.main_menu, font=("Arial", 16))
        back_button.pack(pady=10)
    
    def start_game(self):
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=500, height=700, bg="black")
        self.canvas.pack()
        
        self.player = self.canvas.create_rectangle(230, 650, 270, 690, fill="cyan")
        self.projectiles = []
        self.aliens = []
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)
        
        self.running = True
        self.spawn_alien()
        self.update_game()
    
    def move_left(self, event):
        if self.canvas.coords(self.player)[0] > 10:
            self.canvas.move(self.player, -20, 0)
    
    def move_right(self, event):
        if self.canvas.coords(self.player)[2] < 490:
            self.canvas.move(self.player, 20, 0)
    
    def shoot(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        projectile = self.canvas.create_rectangle(x1+15, y1-10, x2-15, y1, fill="white")
        self.projectiles.append(projectile)
    
    def spawn_alien(self):
        x_pos = random.randint(20, 480)
        alien = self.canvas.create_rectangle(x_pos, 50, x_pos+40, 90, fill="red")
        self.aliens.append(alien)
        if self.running:
            self.root.after(1500, self.spawn_alien)
    
    def update_game(self):
        for proj in self.projectiles:
            self.canvas.move(proj, 0, -10)
        
        for alien in self.aliens:
            self.canvas.move(alien, 0, 5)
        
        self.projectiles = [proj for proj in self.projectiles if self.canvas.coords(proj)[1] > 0]
        self.aliens = [alien for alien in self.aliens if self.canvas.coords(alien)[3] < 700]
        
        if self.running:
            self.root.after(50, self.update_game)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceShooter(root)
    root.mainloop()
