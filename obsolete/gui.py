import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import re
import sys

class ScriptManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Manager")
        self.root.geometry("800x500")
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TNotebook.Tab", padding=[12, 4])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root, style="Custom.TNotebook")
        
        # Create tabs
        self.add_episode_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.add_episode_tab, text="Add Episode")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Setup both tabs
        self._setup_add_episode_tab()
        self._setup_search_tab()
        
        # JSON file path
        self.json_file = "data.json"
        
        # Store search results
        self.current_results = []
        self.current_search_term = ""

    def _setup_add_episode_tab(self):
        # File selection frame
        file_frame = ttk.LabelFrame(self.add_episode_tab, text="Select Fountain File", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        # File path entry and browse button
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side="left", padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self._browse_file)
        browse_btn.pack(side="left", padx=5)
        
        # Process button
        process_btn = ttk.Button(self.add_episode_tab, text="Process File", command=self._process_file)
        process_btn.pack(pady=10)
        
        # Status text
        self.status_text = tk.Text(self.add_episode_tab, height=10, wrap=tk.WORD)
        self.status_text.pack(fill="both", expand=True, padx=10, pady=5)

    def _setup_search_tab(self):
        # Search type selection
        search_frame = ttk.LabelFrame(self.search_tab, text="Search Options", padding=10)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search type radio buttons
        self.search_type = tk.StringVar(value="artist")
        ttk.Radiobutton(search_frame, text="Search by Artist", 
                       variable=self.search_type, value="artist").pack(side="left", padx=5)
        ttk.Radiobutton(search_frame, text="Search by Location", 
                       variable=self.search_type, value="location").pack(side="left", padx=5)
        
        # Search entry
        search_entry_frame = ttk.Frame(self.search_tab)
        search_entry_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(search_entry_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_entry_frame, width=50)
        self.search_entry.pack(side="left", padx=5)
        
        # Search button
        search_btn = ttk.Button(search_entry_frame, text="Search", command=self._perform_search)
        search_btn.pack(side="left", padx=5)
        
        # Download button (initially disabled)
        self.download_btn = ttk.Button(search_entry_frame, text="Download", 
                                     command=self._download_results, state="disabled")
        self.download_btn.pack(side="left", padx=5)
        
        # Results text
        self.results_text = tk.Text(self.search_tab, height=20, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=5)

    def _browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Fountain File",
            filetypes=[("Fountain files", "*.fountain"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def _download_results(self):
        if not self.current_results:
            return
            
        # Create filename based on search type and term
        filename = f"{self.current_search_term}.txt"
        
        try:
            # Ask user where to save the file
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=filename,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.current_results))
                messagebox.showinfo("Success", f"Results saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def process_fountain_file(self, input_file: str) -> None:
        """Processes a Fountain script file and adds its data to the JSON file."""
        # Constants
        SCENE_PATTERN = r"^(EXT\.|INT\.|EXT/INT\.|INT/EXT\.)\s.+$"
        CONTENT_PATTERN = r"\["

        # Initialize data structure
        file_name = os.path.basename(input_file).split('.')[0]
        new_data = {
            "episode": file_name,
            "scenes": []
        }

        # Load existing data
        if os.path.exists(self.json_file):
            with open(self.json_file, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Check if file already processed
        if any(entry["episode"] == file_name for entry in existing_data):
            self.status_text.insert(tk.END, f"File '{file_name}' is already in the JSON file. Skipping.\n")
            return

        def parse_scene_heading(line: str) -> dict:
            pattern = r"^(EXT\.|INT\.|EXT/INT\.|INT/EXT\.)\s(.+?)\s-\s(.+?)\s(#\d+#)$"
            match = re.match(pattern, line)
            if match:
                return {
                    "setting": match.group(1),
                    "location": match.group(2),
                    "TOD": match.group(3),
                    "identifier": match.group(4),
                }
            return None

        def parse_content_line(line: str) -> list:
            line = line.replace('[', '').replace(']', '')
            result = line.split(',')
            return result if result else None

        # Read and parse the Fountain file
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read().splitlines()

        current_scene = None
        scene_count = 0

        for line in content:
            # Match scene headings
            if re.match(SCENE_PATTERN, line):
                scene_count += 1
                scene_data = parse_scene_heading(line)
                if scene_data:
                    current_scene = {
                        "scene_number": scene_count,
                        "scene_heading": line,
                        "setting": scene_data["setting"],
                        "location": scene_data["location"],
                        "TOD": scene_data["TOD"],
                        "artists": []
                    }
                    new_data["scenes"].append(current_scene)

            # Match content lines
            elif re.match(CONTENT_PATTERN, line) and current_scene:
                result = parse_content_line(line)
                if result:
                    artist = result[0].strip()
                    costume = result[1].strip()
                    props = result[2].strip() if len(result) > 2 else ""
                    current_scene["artists"].append({
                        "artist": artist,
                        "costume": costume,
                        "props": props
                    })

        # Append new data and save
        existing_data.append(new_data)
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        self.status_text.insert(tk.END, f"Data from '{file_name}' successfully added to '{self.json_file}'.\n")

    def lookup(self, search_type: str, search_value: str) -> None:
        """Performs the search and displays results."""
        with open(self.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        search_value = search_value.lower()
        results = []

        if search_type == "artist":
            results.append(f"Search Results for Artist: {search_value}\n")
            for entry in data:
                for scene in entry["scenes"]:
                    searched_artist = None
                    other_artists = []
                    
                    for artist in scene["artists"]:
                        if search_value in artist["artist"].lower():
                            searched_artist = artist
                        else:
                            other_artists.append(artist)
                    
                    if searched_artist:
                        results.append(f"  |_scene {scene['scene_number']} : {scene['setting']}, {scene['TOD']}")
                        results.append(f"    |_location : {scene['location']}")
                        results.append(f"        |_artist_name : {searched_artist['artist']}")
                        results.append(f"            |_costume : {searched_artist['costume']}")
                        results.append(f"            |_props : {searched_artist['props']}")
                        results.append("     ")
                        
                        for idx, artist in enumerate(other_artists, 1):
                            results.append(f"        |_other_artist_{idx} : {artist['artist']}")
                            results.append(f"            |_costume : {artist['costume']}")
                            results.append(f"            |_props : {artist['props']}")
                            if idx < len(other_artists):
                                results.append("     ")
                        results.append("")

        elif search_type == "location":
            results.append(f"Search Results for Location: {search_value}\n")
            for entry in data:
                for scene in entry["scenes"]:
                    if search_value in scene["location"].lower():
                        results.append(f"  |_scene {scene['scene_number']} : {scene['setting']}, {scene['TOD']}")
                        for idx, artist in enumerate(scene["artists"], 1):
                            results.append(f"        |_artist_{idx} : {artist['artist']}")
                            results.append(f"            |_costume : {artist['costume']}")
                            results.append(f"            |_props : {artist['props']}")
                            if idx < len(scene["artists"]):
                                results.append("     ")
                        results.append("")

        # Store results and search term
        self.current_results = results
        self.current_search_term = search_value

        # Display results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n".join(results))
        
        # Enable/disable download button based on results
        if results and len(results) > 1:  # More than just the header
            self.download_btn.configure(state="normal")
        else:
            self.download_btn.configure(state="disabled")

    def _process_file(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
            
        try:
            self.status_text.delete(1.0, tk.END)
            self.process_fountain_file(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {str(e)}")

    def _perform_search(self):
        search_value = self.search_entry.get()
        if not search_value:
            messagebox.showerror("Error", "Please enter a search term")
            return
            
        try:
            self.lookup(self.search_type.get(), search_value)
        except Exception as e:
            messagebox.showerror("Error", f"Error performing search: {str(e)}")

def main():
    root = tk.Tk()
    app = ScriptManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()