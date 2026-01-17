import threading
import time
import tkinter as tk
from tkinter import messagebox

import pyautogui


class MacroStep:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    def label(self):
        if self.kind == "click_center":
            return "Click center of screen"
        if self.kind == "wait":
            return f"Wait {self.value} seconds"
        return "Unknown"


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Macro")
        self.steps = []
        self.running = False
        self.stop_event = threading.Event()
        self.worker = None

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(frame, height=10, width=40)
        self.listbox.grid(row=0, column=0, columnspan=3, sticky="nsew")

        btn_click = tk.Button(frame, text="Add Click Center", command=self.add_click)
        btn_click.grid(row=1, column=0, pady=6, sticky="ew")

        wait_frame = tk.Frame(frame)
        wait_frame.grid(row=1, column=1, pady=6, sticky="ew")
        tk.Label(wait_frame, text="Wait (s):").pack(side=tk.LEFT)
        self.wait_entry = tk.Entry(wait_frame, width=6)
        self.wait_entry.insert(0, "1")
        self.wait_entry.pack(side=tk.LEFT)
        btn_wait = tk.Button(frame, text="Add Wait", command=self.add_wait)
        btn_wait.grid(row=1, column=2, pady=6, sticky="ew")

        btn_remove = tk.Button(frame, text="Remove Selected", command=self.remove_selected)
        btn_remove.grid(row=2, column=0, pady=6, sticky="ew")

        self.run_btn = tk.Button(frame, text="Run Forever", command=self.start)
        self.run_btn.grid(row=2, column=1, pady=6, sticky="ew")

        self.stop_btn = tk.Button(frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.grid(row=2, column=2, pady=6, sticky="ew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

    def add_click(self):
        step = MacroStep("click_center")
        self.steps.append(step)
        self.listbox.insert(tk.END, step.label())

    def add_wait(self):
        raw = self.wait_entry.get().strip()
        try:
            seconds = float(raw)
            if seconds < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Wait seconds must be a non-negative number.")
            return
        step = MacroStep("wait", seconds)
        self.steps.append(step)
        self.listbox.insert(tk.END, step.label())

    def remove_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        index = sel[0]
        self.listbox.delete(index)
        del self.steps[index]

    def start(self):
        if not self.steps:
            messagebox.showwarning("No steps", "Add at least one step.")
            return
        if self.running:
            return
        self.running = True
        self.stop_event.clear()
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.worker = threading.Thread(target=self.run_loop, daemon=True)
        self.worker.start()

    def stop(self):
        if not self.running:
            return
        self.stop_event.set()
        self.running = False
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def run_loop(self):
        screen_w, screen_h = pyautogui.size()
        center_x = screen_w // 2
        center_y = screen_h // 2

        while not self.stop_event.is_set():
            for step in list(self.steps):
                if self.stop_event.is_set():
                    break
                if step.kind == "click_center":
                    pyautogui.click(center_x, center_y)
                elif step.kind == "wait":
                    time.sleep(step.value)

        self.root.after(0, self._mark_stopped)

    def _mark_stopped(self):
        self.running = False
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
