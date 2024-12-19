# SCREENPLAY - Fountain Script Data Manager

![alt text](img/icon.png)

## Overview

This Python script provides a command-line tool for processing and searching Fountain screenplay script files. It allows you to:
- Add episodes from Fountain script files to a JSON database
- Look up details about artists and locations across your scripts

## Features

- Process Fountain screenplay files and extract:
  - Scene details (setting, location, time of day)
  - Artist information (artist name, costume, props)
- Store parsed data in a JSON file
- Search for artists or locations across multiple episodes
- Prevent duplicate episode processing

## Requirements

- Python 3.7+
- Standard library modules: `re`, `json`, `os`, `sys`, `argparse`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EiadurRahman/screenplay.git
cd screenplay
```

2. Ensure you have Python installed:
```bash
python --version
```

## Usage

### Adding an Episode

To add a new episode from a Fountain script file:
```bash
python script.py addEpisode path/to/your/screenplay.fountain
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

### Scene Headings
Scene headings should follow this format:
```
EXT./INT. Location - Time of Day #SceneNumber#
```

### Artist/Costume/Props
Artist details should be enclosed in square brackets:
```
[Artist Name, Costume Description, Props]
```

## Example

### Adding an Episode
```bash
python script.py addEpisode episode_1.fountain
```

### Searching
```bash
python script.py lookup --artist "Sarah"
python script.py lookup --location "Office"
```

## Output

- Parsed data is saved in `data.json`
- Search results display scene number, setting, location, and artist details



## Contact

md. Eiadur Rahman - eiadurrahman07@gmail.com

Project Link: [https://github.com/EiadurRahman/screenplay](https://github.com/EiadurRahman/screenplay)
