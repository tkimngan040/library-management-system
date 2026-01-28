import tkinter as tk

class HistoryView(tk.Frame):

    def __init__(self, master, controller, borrows):
        super().__init__(master)
        self.controller = controller  # HistoryController

        headers = ["Book", "Borrow Date", "Return Date", "Fine", "Action"]
        for i, h in enumerate(headers):
            tk.Label(
                self,
                text=h,
                font=("Arial", 10, "bold")
            ).grid(row=0, column=i, padx=8, pady=5)

        # ===== LOAD DATA =====
        for r, b in enumerate(borrows, start=1):
            tk.Label(self, text=b[1]).grid(row=r, column=0)
            tk.Label(self, text=b[2]).grid(row=r, column=1)
            tk.Label(self, text=b[3] if b[3] else "-").grid(row=r, column=2)
            tk.Label(self, text=b[4]).grid(row=r, column=3)

            if b[3] is None:
                # Chưa trả → cho phép RETURN
                tk.Button(
                    self,
                    text="RETURN",
                    command=lambda bid=b[0]: self.controller.app.book.handle_return(bid)
                ).grid(row=r, column=4)
            else:
                tk.Label(self, text="Done").grid(row=r, column=4)
