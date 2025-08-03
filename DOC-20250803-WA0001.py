import tkinter as tk
from tkinter import simpledialog, messagebox

class UserData:
    def __init__(self, file_path="user_data.txt"):
        self.file_path = file_path
        self.users = self.load_user_data()

    def load_user_data(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()
                users = {}
                for line in lines:
                    username, password, score = line.strip().split(",")
                    users[username] = {"password": password, "score": int(score)}
                return users
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open(self.file_path, "w") as file:
            for username, data in self.users.items():
                file.write(f"{username},{data['password']},{data['score']}\n")

    def add_user(self, username, password):
        if username not in self.users:
            self.users[username] = {"password": password, "score": 0}
            self.save_user_data()
            return True
        else:
            return False

    def authenticate_user(self, username, password):
        return self.users.get(username, {}).get("password") == password

    def get_score(self, username):
        return self.users.get(username, {}).get("score", 0)

    def increment_score(self, username):
        if username in self.users:
            self.users[username]["score"] += 1
            self.save_user_data()

class NQueensSolver:
    def __init__(self, N, canvas):
        self.N = N
        self.canvas = canvas
        self.board = [[0]*N for _ in range(N)]
        self.remaining_queens = N

    def is_attack(self, i, j):
        # Check for any queen placed at (i, k) or (k, j)
        for k in range(0, self.N):
            if self.board[i][k] == 1 or self.board[k][j] == 1:
                return True
        # Check for any queen placed diagonally
        for k in range(0, self.N):
            for l in range(0, self.N):
                if (k + l == i + j) or (k - l == i - j):
                    if self.board[k][l] == 1:
                        return True
        return False

    def place_queen(self, row, col):
        # Place a queen at the specified position
        if not self.is_attack(row, col):
            self.board[row][col] = 1
            self.remaining_queens -= 1
            self.update_board()
            if self.remaining_queens == 0:
                messagebox.showinfo("You Win!", "Congratulations! You solved the N-Queens puzzle.")
                return True
        else:
            messagebox.showerror("Invalid Position", "A queen cannot be placed in the selected position. Try again.")
        return False

    def reset_board(self):
        self.board = [[0]*self.N for _ in range(self.N)]
        self.remaining_queens = self.N
        self.update_board()
        self.destroy()

    def update_board(self):
        self.canvas.delete("all")
        for i in range(self.N):
            for j in range(self.N):
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(j*50, i*50, j*50+50, i*50+50, fill=color)

                if self.board[i][j] == 1:
                    self.canvas.create_text(j*50 + 25, i*50 + 25, text="Q", font=("Arial", 16), fill="red")

class HomePage:
    
    def __init__(self, user_data, root):
        self.user_data = user_data
        self.current_user = None
        self.root = root
        self.root.title("N-Queens Game")
        self.root.configure(bg='yellow')

        self.login_frame = tk.Frame(self.root, bg='yellow')
        self.login_frame.pack()

        self.sign_up_frame = tk.Frame(self.root, bg='yellow')
        self.sign_up_frame.pack()

        self.portal_frame = tk.Frame(self.root, bg='yellow')

        self.load_queens_image()  # Load queens image
        
        self.frame = tk.Frame(self.root , width=50, height=10)
        self.frame.pack(side='left')
        self.sign_up_page()
        self.login_page()
        self.add_text_to_frame("instructions.txt",self.frame)
        self.frame.place(x=0, y=0, relwidth=0.3, relheight=0.5)
    
    def add_text_to_frame(self,file_path, frame):
        self.frame=frame
        with open(file_path, 'r') as file:
            self.text = file.read()
            self.text_widget = tk.Text(frame, wrap='word')
            self.text_widget.insert('1.0', self.text)
            self.text_widget.pack(side='left')

    def load_queens_image(self):
        # Load queens image (replace 'queens.png' with your image file)
        try:
            self.queens_image = tk.PhotoImage(file='queens.png')
            self.queens_label = tk.Label(self.root, image=self.queens_image, bg='yellow')
            self.queens_label.photo = self.queens_image
            self.queens_label.pack()
        except tk.TclError:
            print("Failed to load queens image. Make sure the file path is correct.")

    def sign_up_page(self):
        username_label = tk.Label(self.sign_up_frame, text="Username:", bg='yellow')
        username_label.pack()

        username_entry = tk.Entry(self.sign_up_frame)
        username_entry.pack()

        password_label = tk.Label(self.sign_up_frame, text="Password:", bg='yellow')
        password_label.pack()

        password_entry = tk.Entry(self.sign_up_frame, show="*")
        password_entry.pack()

        sign_up_button = tk.Button(self.sign_up_frame, text="Sign Up", command=lambda: self.sign_up(username_entry.get(), password_entry.get()))
        sign_up_button.pack()

    def sign_up(self, username, password):
        if self.user_data.add_user(username, password):
            messagebox.showinfo("Sign Up Successful", "Account created successfully!")
        else:
            self.show_error_dialog("Sign Up Failed", "Username already exists. Please choose a different username.")

    def login_page(self):
        username_label = tk.Label(self.login_frame, text="Username:", bg='yellow')
        username_label.pack()

        username_entry = tk.Entry(self.login_frame)
        username_entry.pack()

        password_label = tk.Label(self.login_frame, text="Password:", bg='yellow')
        password_label.pack()

        password_entry = tk.Entry(self.login_frame, show="*")
        password_entry.pack()

        login_button = tk.Button(self.login_frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack()

    def login(self, username, password):
        if self.user_data.authenticate_user(username, password):
            self.current_user = username
            self.show_portal(username)
        else:
            self.show_error_dialog("Login Failed", "Invalid username or password")

    def show_portal(self, username):
        self.login_frame.pack_forget()
        self.sign_up_frame.pack_forget()

        self.portal_frame.pack()

        portal_label = tk.Label(self.portal_frame, text=f"Welcome, {username}", bg='yellow')
        portal_label.pack()

        play_button = tk.Button(self.portal_frame, text="Start Game", command=self.start_game_page)
        play_button.pack()

        scoreboard_button = tk.Button(self.portal_frame, text="Scoreboard", command=self.show_scoreboard_page)
        scoreboard_button.pack()

    def start_game_page(self):
        if self.current_user:
            N = simpledialog.askinteger("Board Size", "Enter the number of queens:")
            canvas = tk.Canvas(self.root, width=N*50, height=N*50, bg='yellow')
            canvas.pack()
            solver = NQueensSolver(N, canvas)
            solver.update_board()
            canvas.bind("<Button-1>", lambda event: self.on_cell_click(event, solver))

    def on_cell_click(self, event, solver):
        col = event.x // 50
        row = event.y // 50
        if solver.place_queen(row, col):
            self.user_data.increment_score(self.current_user)
            self.show_scoreboard_page()

    def show_scoreboard_page(self):
        score = self.user_data.get_score(self.current_user)
        messagebox.showinfo("Scoreboard", f"Your current score: {score}")

    def show_error_dialog(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    user_data = UserData()
    root = tk.Tk()
    homepage = HomePage(user_data, root)
    root.mainloop()
