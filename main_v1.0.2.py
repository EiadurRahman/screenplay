import re
import json
import os
import sys
import argparse

'''
hey dev here. this was the initial version of the script. as you can see, it's a bit messy and not very user-friendly. but it works! and fully functional.
but most of the futhur improvements are made in the next versions (GUI VERSIONS). but all the core functionalities are same in all versions. 
'''

# Configure output encoding
sys.stdout.reconfigure(encoding='utf-8')

def process_fountain_file(input_file: str, json_file: str = "data.json") -> None:
    """
    Parses a Fountain script file and appends its data to a JSON file.
    Now includes synopsis tracking for scenes.
    """
    # Constants
    SCENE_PATTERN = r"^(EXT\.|INT\.|EXT/INT\.|INT/EXT\.)\s.+$"
    CONTENT_PATTERN = r"\["
    SYNOPSIS_PATTERN = r"^=\s+(.+)$"

    # Initialize data structure
    file_name = os.path.basename(input_file).split('.')[0]
    new_data = {
        "episode": file_name,
        "scenes": []
    }

    # Load existing data
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Check if file already processed
    if any(entry["episode"] == file_name for entry in existing_data):
        print(f"File '{file_name}' is already in the JSON file. Skipping.")
        return

    def parse_scene_heading(line: str) -> dict | None:
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

    def parse_content_line(line: str) -> list | None:
        line = line.replace('[', '').replace(']', '')
        result = line.split(',')
        return result if result else None

    # Read and parse the Fountain file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read().splitlines()

    current_scene = None
    scene_count = 0
    current_synopsis = ""

    for line in content:
        # Check for synopsis
        synopsis_match = re.match(SYNOPSIS_PATTERN, line)
        if synopsis_match:
            current_synopsis = synopsis_match.group(1).strip()
            continue

        # Match scene headings
        if re.match(SCENE_PATTERN, line):
            scene_count += 1
            scene_data = parse_scene_heading(line)
            if scene_data:
                current_scene = {
                    "scene_number": scene_count,
                    "scene_heading": line,
                    "synopsis": current_synopsis,  # Add synopsis to scene data
                    "setting": scene_data["setting"],
                    "location": scene_data["location"],
                    "TOD": scene_data["TOD"],
                    "artists": []
                }
                new_data["scenes"].append(current_scene)
                current_synopsis = ""  # Reset synopsis for next scene

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

    # Append new data
    existing_data.append(new_data)

    # Save updated data
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Data from '{file_name}' successfully added to '{json_file}'.")

def lookup(json_file: str, search_type: str, search_value: str) -> None:
    """
    Enhanced search function that includes episode grouping and synopsis display.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    search_value = search_value.lower()
    print("-" * 75)
    print(f"Search Results for {search_type.title()}: {search_value}")

    if search_type == "artist":
        # Group results by episode
        for entry in data:
            episode_printed = False
            for scene in entry["scenes"]:
                # Check if the searched artist is in this scene
                searched_artist = None
                other_artists = []
                
                for artist in scene["artists"]:
                    if search_value in artist["artist"].lower():
                        searched_artist = artist
                    else:
                        other_artists.append(artist)
                
                if searched_artist:
                    if not episode_printed:
                        print(f"|_ep{entry['episode']}")
                        episode_printed = True
                    
                    # Print synopsis if available
                    print(f"    |_synopsis : {scene.get('synopsis', '')}")
                    print(f"    |_scene {scene['scene_number']} : {scene['setting']}, {scene['TOD']}")
                    print(f"        |_location : {scene['location']}")
                    print(f"            |_artist_name : {searched_artist['artist']}")
                    print(f"                |_costume : {searched_artist['costume']}")
                    print(f"                |_props : {searched_artist['props']}")
                    
                    # Print other artists
                    for idx, artist in enumerate(other_artists, 1):
                        print(f"     ")
                        print(f"            |_other_artist_{idx} : {artist['artist']}")
                        print(f"                |_costume : {artist['costume']}")
                        print(f"                |_props : {artist['props']}")
                    print()

    elif search_type == "location":
        # Group results by episode
        for entry in data:
            episode_printed = False
            for scene in entry["scenes"]:
                if search_value in scene["location"].lower():
                    if not episode_printed:
                        print(f"|_ep{entry['episode']}")
                        episode_printed = True
                    
                    # Print synopsis if available
                    print(f"    |_synopsis : {scene.get('synopsis', '')}")
                    print(f"    |_scene {scene['scene_number']} : {scene['setting']}, {scene['TOD']}")
                    for idx, artist in enumerate(scene["artists"], 1):
                        print(f"            |_artist_{idx} : {artist['artist']}")
                        print(f"                |_costume : {artist['costume']}")
                        print(f"                |_props : {artist['props']}")
                        if idx < len(scene["artists"]):
                            print("     ")
                    print()
    
    print("-" * 75)

def add_episode_from_file(input_file: str, json_file: str = "data.json") -> None:
    process_fountain_file(input_file, json_file)

def search_episode_data(json_file: str, search_type: str, search_value: str) -> None:
    lookup(json_file, search_type, search_value)

def main():
    parser = argparse.ArgumentParser(description="Script for managing Fountain script data.")
    subparsers = parser.add_subparsers(dest='command')

    # Add episode subcommand
    add_episode_parser = subparsers.add_parser('addEpisode', help="Add an episode from a Fountain file.")
    add_episode_parser.add_argument('filepath', type=str, help="Path to the Fountain file to add.")

    # Lookup subcommand
    lookup_parser = subparsers.add_parser('lookup', help="Search for artist or location.")
    lookup_parser.add_argument('--location', type=str, help="Location name to search.")
    lookup_parser.add_argument('--artist', type=str, help="Artist name to search.")

    args = parser.parse_args()

    if args.command == 'addEpisode':
        add_episode_from_file(args.filepath)
    elif args.command == 'lookup':
        if args.location:
            search_episode_data("data.json", "location", args.location)
        elif args.artist:
            search_episode_data("data.json", "artist", args.artist)
        else:
            print("Please specify either --location or --artist for lookup.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()