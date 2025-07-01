import customtkinter as ctk
import math
import statistics
import tkinter as tk

# Môi trường đánh giá an toàn
# Cho phép sử dụng các hàm toán học cơ bản

def safe_eval(expr, extra_env=None):
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed.update({
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'round': round,
        'pow': pow,
        'factorial': math.factorial
    })
    if extra_env:
        allowed.update(extra_env)
    return eval(expr, {'__builtins__': {}}, allowed)

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Máy tính nâng cao")
        self.geometry("400x600")
        self.minsize(400, 600)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Cài font lớn cho nút và entry
        self.btn_font = ('Helvetica', 24)
        self.entry_font = ('Helvetica', 28)

        # Entry chính
        self.display = ctk.CTkEntry(self, font=self.entry_font, justify='right')
        self.display.pack(fill='x', padx=20, pady=20)

        # Tab view
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill='both', padx=20, pady=(0,20))
        for tab in ['Cơ bản', 'Khoa học', 'Thống kê', 'Ma trận', 'Đồ thị']:
            self.tabview.add(tab)

        self._build_basic_tab()
        self._build_scientific_tab()
        self._build_statistics_tab()
        self._build_matrix_tab()
        self._build_graph_tab()

    def _clear(self):
        self.display.delete(0, ctk.END)

    def _append(self, char):
        self.display.insert(ctk.END, char)

    def _evaluate(self):
        expr = self.display.get()
        try:
            result = safe_eval(expr)
            self._clear()
            self._append(str(result))
        except:
            self._clear()
            self._append("Lỗi")

    def _build_basic_tab(self):
        frame = self.tabview.tab("Cơ bản")
        buttons = [['7','8','9','/'],['4','5','6','*'],['1','2','3','-'],['0','.','(',')'],['C','=', '+']]
        for row in buttons:
            row_frame = ctk.CTkFrame(frame)
            row_frame.pack(expand=True, fill='both', pady=5)
            for char in row:
                action = self._evaluate if char=='=' else (self._clear if char=='C' else lambda x=char: self._append(x))
                btn = ctk.CTkButton(row_frame, text=char, command=action, font=self.btn_font)
                btn.pack(side='left', expand=True, fill='both', padx=5, pady=5)

    def _build_scientific_tab(self):
        frame = self.tabview.tab("Khoa học")
        for i in range(4): frame.grid_rowconfigure(i, weight=1)
        for j in range(4): frame.grid_columnconfigure(j, weight=1)
        funcs = ['sin(', 'cos(', 'tan(', 'asin(', 'acos(', 'atan(', 'log(',
                 'log10(', 'exp(', 'sqrt(', 'pow(', 'factorial(']
        for idx, fn in enumerate(funcs):
            r,c = divmod(idx,4)
            btn = ctk.CTkButton(frame, text=fn, command=lambda x=fn: self._append(x), font=self.btn_font)
            btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
        ctk.CTkButton(frame, text='Xóa', command=self._clear, font=self.btn_font).grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        ctk.CTkButton(frame, text='=', command=self._evaluate, font=self.btn_font).grid(row=3, column=2, columnspan=2, sticky='nsew', padx=5, pady=5)

    def _build_statistics_tab(self):
        frame = self.tabview.tab("Thống kê")
        ctk.CTkLabel(frame, text="Nhập dữ liệu, phân tách dấu phẩy:", font=self.btn_font).pack(pady=(10,0))
        self.stats_entry = ctk.CTkEntry(frame, placeholder_text="ví dụ:1,2,3", font=self.entry_font)
        self.stats_entry.pack(fill='x', padx=20, pady=10)
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)
        for stat in ['Trung bình','Trung vị','Độ lệch chuẩn','Tổng','Phương sai']:
            ctk.CTkButton(btn_frame, text=stat, command=lambda s=stat: self._compute_stat(s), font=self.btn_font).pack(side='left', padx=5)
        self.stats_result = ctk.CTkLabel(frame, text="Kết quả:", font=self.btn_font)
        self.stats_result.pack(pady=(20,0))

    def _compute_stat(self, stat):
        data = self.stats_entry.get().split(',')
        try:
            nums = [float(x) for x in data]
            res = {
                'Trung bình': statistics.mean(nums),
                'Trung vị': statistics.median(nums),
                'Độ lệch chuẩn': statistics.stdev(nums),
                'Tổng': sum(nums),
                'Phương sai': statistics.variance(nums)
            }[stat]
            self.stats_result.configure(text=f"Kết quả: {res}")
        except:
            self.stats_result.configure(text="Kết quả: Lỗi dữ liệu")

    def _build_matrix_tab(self):
        frame = self.tabview.tab("Ma trận")
        ctk.CTkLabel(frame, text="Các phép toán ma trận sẽ cập nhật sau...", font=self.btn_font).pack(expand=True)

    def _build_graph_tab(self):
        frame = self.tabview.tab("Đồ thị")
        ctk.CTkLabel(frame, text="Nhập hàm f(x) hoặc phương trình y=:", font=self.btn_font).pack(pady=(10,0))
        self.graph_entry = ctk.CTkEntry(frame, placeholder_text="ví dụ: y=2*x+3 hoặc sin(x)", font=self.entry_font)
        self.graph_entry.pack(fill='x', padx=20, pady=10)
        ctk.CTkButton(frame, text="Vẽ đồ thị", command=self._plot_graph, font=self.btn_font).pack(pady=10)
        self.canvas = tk.Canvas(frame, bg='white')
        self.canvas.pack(expand=True, fill='both', padx=20, pady=10)

    def _plot_graph(self):
        expr = self.graph_entry.get().strip()
        # Nếu người dùng nhập dạng y=..., loại bỏ phần y=
        if expr.lower().startswith('y='):
            expr = expr.split('=',1)[1]
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete('all')
        self.canvas.create_line(0, h/2, w, h/2)
        self.canvas.create_line(w/2, 0, w/2, h)
        try:
            points = []
            for i in range(w):
                x = (i - w/2) / (w/20)
                y = safe_eval(expr, {'x': x})
                j = h/2 - y * (h/20)
                points.append((i, j))
            for k in range(len(points)-1):
                x1,y1 = points[k]
                x2,y2 = points[k+1]
                self.canvas.create_line(x1, y1, x2, y2)
        except:
            self.canvas.create_text(w/2, h/2, text="Lỗi biểu thức", font=self.btn_font)

if __name__ == '__main__':
    app = CalculatorApp()
    app.mainloop()
