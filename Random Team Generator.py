import tkinter as tk
from tkinter import messagebox
import random
import re


class RandomTeamGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Team Generator")
        self.root.geometry("1050x750")
        self.root.minsize(800, 600)

        self.colors = {
            "background": "#101827",
            "panel": "#1b2738",
            "card": "#253449",
            "primary": "#8b5cf6",
            "primary_hover": "#7c3aed",
            "text": "#f1f5f9",
            "muted": "#94a3b8",
            "success": "#34d399",
            "border": "#34445a"
        }

        self.last_teams = []

        self.root.configure(bg=self.colors["background"])

        self.create_interface()

    def create_interface(self):
        header = tk.Frame(
            self.root,
            bg=self.colors["background"],
            padx=30,
            pady=25
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="Random Team Generator",
            font=("Arial", 25, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Shuffle names. Create balanced teams. Start playing!",
            font=("Arial", 11),
            fg=self.colors["muted"],
            bg=self.colors["background"]
        ).pack(anchor="w", pady=(6, 0))

        main = tk.Frame(
            self.root,
            bg=self.colors["background"],
            padx=25,
            pady=10
        )
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=1, uniform="column")
        main.grid_columnconfigure(1, weight=1, uniform="column")
        main.grid_rowconfigure(0, weight=1)

        self.create_input_panel(main)
        self.create_results_panel(main)

        footer = tk.Frame(
            self.root,
            bg=self.colors["background"],
            padx=30,
            pady=12
        )
        footer.pack(fill="x")

        self.status_label = tk.Label(
            footer,
            text="Ready to create your teams!",
            font=("Arial", 10),
            fg=self.colors["muted"],
            bg=self.colors["background"]
        )
        self.status_label.pack(anchor="w")

    def create_input_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg=self.colors["panel"],
            padx=20,
            pady=20,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        tk.Label(
            panel,
            text="Enter Participants",
            font=("Arial", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["panel"]
        ).pack(anchor="w")

        tk.Label(
            panel,
            text="Enter one name per line. Commas also work.",
            font=("Arial", 10),
            fg=self.colors["muted"],
            bg=self.colors["panel"],
            wraplength=350
        ).pack(anchor="w", pady=(6, 15))

        text_frame = tk.Frame(
            panel,
            bg=self.colors["panel"]
        )
        text_frame.pack(fill="both", expand=True)

        self.names_text = tk.Text(
            text_frame,
            height=15,
            font=("Arial", 11),
            bg="#111d2c",
            fg=self.colors["text"],
            insertbackground="white",
            relief="flat",
            padx=12,
            pady=12,
            wrap="word",
            undo=True
        )
        self.names_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            text_frame,
            command=self.names_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.names_text.configure(
            yscrollcommand=scrollbar.set
        )

        self.names_text.bind(
            "<KeyRelease>",
            self.update_name_count
        )

        self.name_count_label = tk.Label(
            panel,
            text="0 participants",
            font=("Arial", 10),
            fg=self.colors["muted"],
            bg=self.colors["panel"]
        )
        self.name_count_label.pack(
            anchor="w",
            pady=(10, 20)
        )

        tk.Label(
            panel,
            text="Number of Teams",
            font=("Arial", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["panel"]
        ).pack(anchor="w", pady=(0, 8))

        self.team_count_var = tk.StringVar(value="2")

        self.team_spinbox = tk.Spinbox(
            panel,
            from_=1,
            to=30,
            textvariable=self.team_count_var,
            font=("Arial", 12),
            bg="#111d2c",
            fg=self.colors["text"],
            buttonbackground=self.colors["card"],
            insertbackground="white",
            relief="flat",
            width=8,
            justify="center"
        )
        self.team_spinbox.pack(anchor="w", pady=(0, 20))

        generate_button = tk.Button(
            panel,
            text="Generate Random Teams",
            command=self.generate_teams,
            font=("Arial", 12, "bold"),
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=12
        )
        generate_button.pack(fill="x", pady=(0, 10))

        generate_button.bind(
            "<Enter>",
            lambda event: generate_button.config(
                bg=self.colors["primary_hover"]
            )
        )
        generate_button.bind(
            "<Leave>",
            lambda event: generate_button.config(
                bg=self.colors["primary"]
            )
        )

        button_frame = tk.Frame(
            panel,
            bg=self.colors["panel"]
        )
        button_frame.pack(fill="x")

        tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            font=("Arial", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=9
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        tk.Button(
            button_frame,
            text="Shuffle Again",
            command=self.generate_teams,
            font=("Arial", 10, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=9
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def create_results_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg=self.colors["panel"],
            padx=20,
            pady=20,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        heading = tk.Frame(
            panel,
            bg=self.colors["panel"]
        )
        heading.pack(fill="x", pady=(0, 15))

        tk.Label(
            heading,
            text="Your Teams",
            font=("Arial", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["panel"]
        ).pack(side="left")

        self.results_canvas = tk.Canvas(
            panel,
            bg=self.colors["panel"],
            highlightthickness=0
        )
        self.results_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            panel,
            orient="vertical",
            command=self.results_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.results_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.results_frame = tk.Frame(
            self.results_canvas,
            bg=self.colors["panel"]
        )

        self.canvas_window = self.results_canvas.create_window(
            (0, 0),
            window=self.results_frame,
            anchor="nw"
        )

        self.results_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.results_canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        self.show_empty_message()

        copy_button = tk.Button(
            panel,
            text="Copy Team Results",
            command=self.copy_results,
            font=("Arial", 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=10
        )
        copy_button.pack(fill="x", pady=(12, 0))

    def update_scroll_region(self, event=None):
        self.results_canvas.configure(
            scrollregion=self.results_canvas.bbox("all")
        )

    def update_canvas_width(self, event):
        self.results_canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def parse_names(self):
        raw_names = self.names_text.get(
            "1.0",
            "end-1c"
        )

        names = re.split(r"[\n,;]+", raw_names)

        return [
            name.strip()
            for name in names
            if name.strip()
        ]

    def update_name_count(self, event=None):
        names = self.parse_names()
        count = len(names)

        label = "participant" if count == 1 else "participants"

        self.name_count_label.config(
            text=f"{count} {label}"
        )

    def generate_teams(self):
        names = self.parse_names()

        if not names:
            messagebox.showwarning(
                "No Participants",
                "Please enter at least one participant name."
            )
            return

        try:
            team_count = int(self.team_count_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Team Count",
                "Please enter a valid number of teams."
            )
            return

        if team_count < 1:
            messagebox.showerror(
                "Invalid Team Count",
                "The number of teams must be at least 1."
            )
            return

        if team_count > len(names):
            messagebox.showerror(
                "Too Many Teams",
                "The number of teams cannot exceed the number of participants."
            )
            return

        random.shuffle(names)

        teams = [[] for _ in range(team_count)]

        for index, name in enumerate(names):
            teams[index % team_count].append(name)

        self.last_teams = teams

        self.display_teams()

        self.status_label.config(
            text=f"Successfully generated {team_count} random teams "
                 f"from {len(names)} participants!",
            fg=self.colors["success"]
        )

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def show_empty_message(self):
        self.clear_results()

        tk.Label(
            self.results_frame,
            text="Your teams will appear here.",
            font=("Arial", 12),
            fg=self.colors["muted"],
            bg=self.colors["panel"],
            pady=40
        ).pack(fill="x")

    def display_teams(self):
        self.clear_results()

        for index, members in enumerate(self.last_teams):
            self.create_team_card(index + 1, members)

        self.root.update_idletasks()
        self.results_canvas.yview_moveto(0)

    def create_team_card(self, team_number, members):
        card = tk.Frame(
            self.results_frame,
            bg=self.colors["card"],
            padx=16,
            pady=15,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        card.pack(fill="x", pady=6)

        header = tk.Frame(
            card,
            bg=self.colors["card"]
        )
        header.pack(fill="x", pady=(0, 10))

        tk.Label(
            header,
            text=f"TEAM {team_number}",
            font=("Arial", 12, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["card"]
        ).pack(side="left")

        tk.Label(
            header,
            text=f"{len(members)} members",
            font=("Arial", 9),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        ).pack(side="right")

        for member_number, member in enumerate(members, start=1):
            member_frame = tk.Frame(
                card,
                bg=self.colors["card"]
            )
            member_frame.pack(fill="x", pady=3)

            tk.Label(
                member_frame,
                text=f"{member_number}.",
                font=("Arial", 10, "bold"),
                fg=self.colors["success"],
                bg=self.colors["card"],
                width=3,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                member_frame,
                text=member,
                font=("Arial", 11),
                fg=self.colors["text"],
                bg=self.colors["card"],
                anchor="w",
                wraplength=300
            ).pack(side="left", fill="x", expand=True)

    def copy_results(self):
        if not self.last_teams:
            messagebox.showinfo(
                "No Results",
                "Generate teams before copying the results."
            )
            return

        output = []

        for index, members in enumerate(self.last_teams, start=1):
            output.append(f"TEAM {index}")

            for member in members:
                output.append(f"  - {member}")

            output.append("")

        result_text = "\n".join(output)

        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()

        self.status_label.config(
            text="Team results copied to clipboard!",
            fg=self.colors["success"]
        )

    def clear_all(self):
        self.names_text.delete("1.0", "end")
        self.team_count_var.set("2")
        self.last_teams = []

        self.update_name_count()
        self.show_empty_message()

        self.status_label.config(
            text="All entries and results have been cleared.",
            fg=self.colors["muted"]
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTeamGenerator(root)
    root.mainloop()