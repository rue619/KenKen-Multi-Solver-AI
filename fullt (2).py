import random
import copy
import math
import time
import tkinter as tk
from tkinter import ttk

# ==========================================
# SECTION 1: GLOBAL SETTINGS & THEME
# ==========================================
PASTEL_COLORS = [
    "#FFD1DC", "#AED6F1", "#ABEBC6", 
    "#FDEBD0", "#D7BDE2", "#F9E79F", 
    "#A3E4D7", "#E6E6FA"
]

# ==========================================
# SECTION 2: CORE KENKEN LOGIC
# ==========================================
def cage_satisfies(vals, op, target):
    if not vals: return False
    if op == '+': return sum(vals) == target
    if op == '*': return math.prod(vals) == target
    if op == '-':
        return len(vals) == 2 and abs(vals[0] - vals[1]) == target
    if op == '/':
        return len(vals) == 2 and (max(vals) / min(vals) == target)
    if op in [None, 'None', '']: return vals[0] == target
    return False

# ==========================================
# SECTION 3: GENETIC ALGORITHM SECTION
# ==========================================
class GeneticSolver:
    def __init__(self, n, cages, pop_size=500):
        self.n, self.cages, self.pop_size = n, cages, pop_size
        self.mutation_rate = 0.25

    def random_individual(self):
        return [random.sample(range(1, self.n + 1), self.n) for _ in range(self.n)]

    def fitness(self, ind):
        col_score = sum(len(set(ind[r][c] for r in range(self.n))) / self.n for c in range(self.n)) / self.n
        cage_score = sum(1 for cage in self.cages if cage_satisfies([ind[r][c] for r, c in cage['cells']], cage['op'], cage['target'])) / len(self.cages)
        return col_score + cage_score

    def mutate(self, ind):
        for r in range(self.n):
            if random.random() < self.mutation_rate:
                c1, c2 = random.sample(range(self.n), 2)
                ind[r][c1], ind[r][c2] = ind[r][c2], ind[r][c1]
        return ind

    def crossover(self, p1, p2):
        return [copy.deepcopy(p1[r] if random.random() < 0.5 else p2[r]) for r in range(self.n)]

# ==========================================
# SECTION 4: BACKTRACKING SECTION (UPDATED)
# ==========================================
def is_valid_bt(board, row, col, num, cages, n):
    # Check row and column constraints
    for i in range(n):
        if board[row][i] == num or board[i][col] == num:
            return False

    board[row][col] = num
    valid = True
    for cage in cages:
        if (row, col) in cage['cells']:
            filled_values = [board[r][c] for r, c in cage['cells'] if board[r][c] != 0]
            # Only validate the math if the cage is fully filled
            if len(filled_values) == len(cage['cells']):
                if not cage_satisfies(filled_values, cage['op'], cage['target']):
                    valid = False
            break
    
    board[row][col] = 0 # Reset after check
    return valid

def solve_backtracking_gui(board, gui):
    for row in range(gui.n):
        for col in range(gui.n):
            if board[row][col] == 0:
                for num in range(1, gui.n + 1):
                    if is_valid_bt(board, row, col, num, gui.cages, gui.n):
                        board[row][col] = num
                        
                        # Visualization
                        gui.draw_grid()
                        gui.root.update()
                        time.sleep(0.08) # Animation speed
                        
                        if solve_backtracking_gui(board, gui):
                            return True
                        
                        # Backtrack
                        board[row][col] = 0
                        gui.draw_grid()
                        gui.root.update()
                        time.sleep(0.04)
                return False
    return True

# ==========================================
# SECTION 5: GUI & VISUALIZATION (TKINTER)
# ==========================================
class KenKenApp:
    def __init__(self, root, n, cages):
        self.root = root
        self.n, self.cages = n, cages
        self.cell_size = 80
        self.root.title("KenKen Multi-Solver AI")
        
        self.gen, self.fitness = 0, 0.0
        self.state = "MENU"
        self.board = [[0]*n for _ in range(n)]
        
        # UI Elements
        self.canvas = tk.Canvas(root, width=n*self.cell_size, height=n*self.cell_size, bg="white")
        self.canvas.pack(pady=10, padx=10)
        
        self.stats_label = tk.Label(root, text=f"Gen: {self.gen} | Fitness: {self.fitness:.4f}", 
                                    font=("Arial", 12, "bold"), fg="red")
        self.stats_label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Genetic Algorithm", bg="#329632", fg="white", font=("Arial", 10, "bold"),
                  command=self.start_ga).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Backtracking", bg="#963232", fg="white", font=("Arial", 10, "bold"),
                  command=self.start_bt).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Reset Board", bg="#646464", fg="white", font=("Arial", 10, "bold"),
                  command=self.reset_board).pack(pady=5)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for cage in self.cages:
            color = cage.get('color', "#F0F0F0")
            for r, c in cage['cells']:
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
                if (r, c) == cage['cells'][0]:
                    hint = f"{cage['target']}{cage['op'] if cage['op'] else ''}"
                    self.canvas.create_text(x1+5, y1+5, text=hint, anchor="nw", font=("Arial", 10, "bold"))

        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] != 0:
                    text_color = "red" if self.state == "SOLVING_BT" else "blue"
                    self.canvas.create_text(c*self.cell_size + self.cell_size/2, 
                                            r*self.cell_size + self.cell_size/2, 
                                            text=str(self.board[r][c]), font=("Arial", 24, "bold"), fill=text_color)

    def reset_board(self):
        self.state = "MENU"
        self.board = [[0]*self.n for _ in range(self.n)]
        self.gen, self.fitness = 0, 0.0
        self.stats_label.config(text=f"Gen: {self.gen} | Fitness: {self.fitness:.4f}")
        self.draw_grid()

    def start_bt(self):
        self.state = "SOLVING_BT"
        self.board = [[0]*self.n for _ in range(self.n)]
        if solve_backtracking_gui(self.board, self):
            self.state = "DONE"
            self.draw_grid()

    def start_ga(self):
        self.state = "SOLVING_GA"
        self.ga_engine = GeneticSolver(self.n, self.cages)
        self.pop = [self.ga_engine.random_individual() for _ in range(500)]
        self.run_ga_step()

    def run_ga_step(self):
        if self.state != "SOLVING_GA": return
        fits = [self.ga_engine.fitness(ind) for ind in self.pop]
        best_idx = fits.index(max(fits))
        self.board = self.pop[best_idx]
        self.fitness = fits[best_idx]
        self.stats_label.config(text=f"Gen: {self.gen} | Fitness: {self.fitness:.4f}")
        self.draw_grid()

        if self.fitness >= 2.0:
            self.state = "DONE"
        else:
            new_pop = [copy.deepcopy(self.pop[i]) for i in sorted(range(len(fits)), key=lambda k: -fits[k])[:50]]
            while len(new_pop) < 500:
                p1, p2 = random.sample(self.pop[:100], 2)
                new_pop.append(self.ga_engine.mutate(self.ga_engine.crossover(p1, p2)))
            self.pop, self.gen = new_pop, self.gen + 1
            self.root.after(10, self.run_ga_step)

# ==========================================
# SECTION 6: DATA & STARTUP
# ==========================================
cages_data = [
    {'cells': [(0, 0), (1, 0), (2, 0), (3, 0)], 'op': '*', 'target': 24, 'color': PASTEL_COLORS[0]},
    {'cells': [(0, 1), (1, 1), (2, 1)], 'op': '+', 'target': 9, 'color': PASTEL_COLORS[1]},
    {'cells': [(0, 2), (0, 3)], 'op': '-', 'target': 1, 'color': PASTEL_COLORS[2]},
    {'cells': [(1, 2), (1, 3)], 'op': '/', 'target': 3, 'color': PASTEL_COLORS[3]},
    {'cells': [(2, 2), (2, 3)], 'op': '+', 'target': 5, 'color': PASTEL_COLORS[4]},
    {'cells': [(3, 1), (3, 2), (3, 3)], 'op': '*', 'target': 8, 'color': PASTEL_COLORS[5]},
]

if __name__ == "__main__":
    root = tk.Tk()
    app = KenKenApp(root, 4, cages_data)
    root.mainloop()