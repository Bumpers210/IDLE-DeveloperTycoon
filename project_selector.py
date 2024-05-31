import tkinter as tk
from tkinter import ttk

class ProjectSelector:
    def __init__(self, game):
        self.game = game
        self.sort_reverse = False

    def open_project_selection(self):
        if not self.game.project_in_progress:
            project_window = tk.Toplevel(self.game.gui.root)
            project_window.title("Select Project")

            # Create a frame for the Treeview and the scrollbar
            frame = ttk.Frame(project_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            columns = ("name", "duration", "programming", "design", "marketing")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.heading("name", text="Name", command=lambda: self.sort_projects(tree, "name"))
            tree.heading("duration", text="Duration", command=lambda: self.sort_projects(tree, "duration", numeric=True))
            tree.heading("programming", text="Programming", command=lambda: self.sort_projects(tree, "programming", numeric=True))
            tree.heading("design", text="Design", command=lambda: self.sort_projects(tree, "design", numeric=True))
            tree.heading("marketing", text="Marketing", command=lambda: self.sort_projects(tree, "marketing", numeric=True))

            for project in self.game.projects:
                tree.insert("", "end", values=(project.name, project.duration, project.programming, project.design, project.marketing))

            # Create a vertical scrollbar and attach it to the treeview
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Pack the treeview into the frame
            tree.pack(fill=tk.BOTH, expand=True)

            def on_project_select(event):
                selected_item = tree.selection()[0]
                selected_project = tree.item(selected_item, "values")
                for project in self.game.projects:
                    if project.name == selected_project[0]:
                        self.game.start_selected_project(project, project_window)
                        break

            tree.bind("<Double-1>", on_project_select)

    def sort_projects(self, tree, col, numeric=False):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        if numeric:
            data.sort(key=lambda t: float(t[0]), reverse=self.sort_reverse)
        else:
            data.sort(key=lambda t: t[0], reverse=self.sort_reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)
        self.sort_reverse = not self.sort_reverse
