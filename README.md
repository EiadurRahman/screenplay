# SCREENPLAY - Fountain Script Data Manager

![alt text](img/icon.png)

## Overview

This project offers a tool for managing Fountain screenplay script data with both command-line and GUI options. It enables you to:
- Add episodes from Fountain script files to a JSON database
- Look up details about artists and locations across your scripts
- Use a user-friendly GUI to interact with the tool
- Format and export screenplay data into Markdown files
- Save search results in both text and Markdown formats

## Features

- **Command-line mode**:
  - Process Fountain screenplay files and extract:
    - Synopsis  
    - Scene details (setting, location, time of day)
    - Artist information (artist name, costume, props)
  - Store parsed data in a JSON file
  - Search for artists or locations across multiple episodes
  - Save search results in text and Markdown files
  - Format and export screenplay data into a `.md` file
  - Prevent duplicate episode processing
- **GUI mode**:
  - Perform all actions available in the command-line version through a graphical interface
  - Easy access for non-technical users
  - Compiled GUI version available for direct use (in dist/ directory)

## Requirements

- **Command-line version**:
  - Python 3.7+
  - Standard library modules: `re`, `json`, `os`, `sys`, `argparse`
- **GUI version**:
  - Python 3.7+
  - Requires `tkinter` (included with most Python distributions)
  - **Compiled version**: No additional dependencies needed (available in the `dist/` directory)

## Installation

### Command-line Version
1. Clone the repository:
    ```bash
    git clone https://github.com/EiadurRahman/screenplay.git
    cd screenplay
    ```

2. Ensure you have Python installed:
    ```bash
    python --version 
    ```

### GUI Version
1. **Running the Python GUI**:
    - Open the `gui_version.py` file using Python:
      ```bash
      python gui_version.py # try to use latest version (in root directory)
      ```

2. **Using the Compiled GUI**:
    - Locate the executable in the `dist/` directory:
      - Windows: `dist/ScriptManager_version.exe`
    - Run the executable directly (no Python required).

## Usage

### Command-line Version

#### Adding an Episode
To add a new episode from a Fountain script file:
```bash
python main.py addEpisode path/to/your/screenplay.fountain
```
### Searching for Artists

To search for an artist across all episodes:
```bash
python main.py lookup --artist "John Doe"
```

### Searching for Locations

To search for a specific location:
```bash
python main.py lookup --location "Downtown"
```

## Fountain Script Format Requirements

The script expects Fountain scripts with specific formatting:

### Synopsis 
Synopsis should follow this format:
```
= this is a synopsis
```

### Scene Headings
Scene headings should follow this format:
```
EXT. or INT. or EXT/INT. Location - Time of Day #SceneNumber#
```

### Artist/Costume/Props
Artist details should be enclosed in square brackets:
```
[Artist Name, Costume Description, Props]
```

## Example work flow (CLI)

### Adding an Episode
```bash
python main.py addEpisode episode_1.fountain
```

### Searching
```bash
python main.py lookup --artist "Sarah"
python main.py lookup --location "Office"
```

## Output

- Parsed data is saved in `data.json`
- Search results display Synopsis, scene number, setting, location, and artist details

### Note: Previous versions of the code are stored in the `obsolete/` directory. These are not recommended for use.

## Contact

md. Eiadur Rahman - eiadurrahman07@gmail.com

Project Link: [https://github.com/EiadurRahman/screenplay](https://github.com/EiadurRahman/screenplay)
