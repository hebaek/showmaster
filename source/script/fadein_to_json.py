import xml.etree.ElementTree as ET
import json
import re



# Helper functions
def name_case(text):
    """Convert text to name case (capitalize each word)."""
    return text.title().strip()

def sentence_case(text):
    """Convert text to lowercase with the first letter capitalized."""
    return text[:1].upper() + text[1:].lower().strip() if text else ""



def tag_characters_in_text(text, character_names):
    # Sort character names by length (longest first)
    sorted_names = sorted(character_names, key=len, reverse=True)

    # Replace character names with unique markers
    marker_map = {}
    for i, name in enumerate(sorted_names):
        marker = f"{{{{CHARACTER_{i}}}}}"  # e.g., "{{CHARACTER_0}}"
        marker_map[marker] = name
        # Use a regex to match the character name (case-insensitive, with boundary checks)
        text = re.sub(rf'\b{name}\b', marker, text, flags=re.IGNORECASE)

    # Split the text at the markers
    parts = re.split(r'({{CHARACTER_\d+}})', text)

    # Construct the structured data
    result = []
    for part in parts:
        if part in marker_map:  # It's a marker
            name = marker_map[part]
            result.append({"type": "character", "name": name, "text": name})
        elif part.strip():  # Non-marker text (ignore pure whitespace)
            result.append({"type": "text", "text": part})

    return result



def parse_xml_to_json(source_file, target_file):
    def create_text_object(text, is_song=False):
        obj_type = "song" if is_song else "text"
        return {"type": obj_type, "text": text}



    def extract_scene_details(scene_text, character_names):
        """
        Extract the scene details (id, name, and type) based on the scene text.
        - If the scene name starts with 'SCENE <ID> -', extract the ID and the part after the dash.
        - Otherwise, set type = "other", id = None, and use the full text as the name.
        """
        match = re.match(r"SCENE\s+(\S+)\s+-\s+(.*)", scene_text, re.IGNORECASE)
        if match:
            # Extract the scene ID and the part after the dash
            id = match.group(1).strip()
            name = normalize_song_capitalization(match.group(2).strip(), character_names)  # Apply sentence case to scene title
            scene_type = "scene"
        else:
            # Use the full text as the name, set type to "other", and leave id as None
            id = None
            name = normalize_song_capitalization(scene_text.strip(), character_names)  # Apply sentence case to non-standard scene title
            scene_type = "other"
        return id, name, scene_type



    def normalize_song_capitalization(text, character_names):
        """
        Normalize capitalization for a song:
        - Capitalize the first letter of each sentence.
        - Ensure proper capitalization for given names in the character list.
        """
        # Split text into sentences while keeping punctuation
        sentences = re.split(r'([.!?])', text)  # Keep punctuation as separate parts
        normalized_sentences = []

        for i in range(0, len(sentences), 2):  # Process sentence and punctuation pairs
            sentence = sentences[i].strip()
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""

            # Capitalize the first letter of the sentence
            normalized_sentence = sentence.capitalize()

            # Ensure names are properly capitalized
            for name in character_names:
                normalized_sentence = re.sub(
                    rf'\b{name.upper()}\b',  # Match the name in ALL CAPS
                    name_case(name),       # Replace with proper capitalization
                    normalized_sentence
                )

            # Recombine sentence with punctuation (no extra space)
            normalized_sentences.append(normalized_sentence + punctuation)

        return "".join(normalized_sentences).strip()  # Combine into a single string



    def split_blocks_and_lines(text):
        """
        Split text into blocks (on double line breaks) and lines (on single line breaks within blocks).
        """
        # Split into blocks using double line breaks
        blocks = text.split("\n\n")

        # For each block, split into lines using single line breaks
        block_content = []
        for block in blocks:
            lines = block.split("\n")
            block_content.append(lines)

        return block_content



    def create_dialogue_block(character_name, dialogue_lines, character_names):
        """
        Create a dialogue block, joining split dialogue and handling new blocks for double line breaks.
        """
        # Join all dialogue lines into a single string
        full_text = "\n".join(dialogue_lines)

        # Split into blocks and lines
        blocks = split_blocks_and_lines(full_text)

        # Create blocks and lines
        json_blocks = []
        for block in blocks:
            block_json = {
                "type": "block",
                "content": []
            }

            for line in block:
                # Check if the line is a song (ALL CAPS and longer than a threshold)
                is_song = line.isupper() and len(line.strip()) > 5

                if is_song:
                    # Normalize capitalization for songs
                    line = normalize_song_capitalization(line, character_names)

                # Add the line to the block
                block_json["content"].append({
                    "type": "line",
                    "content": [create_text_object(line, is_song=is_song)]
                })

            # Add the block to the JSON block list
            json_blocks.append(block_json)

        return json_blocks



    def create_parenthetical_block(text, character_names):
        """
        Create a block for a parenthetical object by parsing the text into characters and text.
        The entire content is wrapped in parentheses.
        """
        # Parse the text into characters and text
        parsed_content = tag_characters_in_text(text, character_names)

        # Wrap the parsed content in parentheses
        wrapped_content = [{"type": "text", "text": "("}] + parsed_content + [{"type": "text", "text": ")"}]

        return {
            "type": "block",
            "content": [
                {
                    "type": "parenthetical",
                    "content": [
                        {"type": "line", "content": wrapped_content}
                    ]
                }
            ]
        }



    def extract_characters(root):
        """Extract all character names from the <lists><characters> section."""
        character_elements = root.findall('.//lists/characters/character')
        character_names = set()
        for char in character_elements:
            name = char.get("name", "").strip()
            if name:
                character_names.add(name_case(name))
        return character_names



    def process_scenes(root, character_names):
        """Process scenes, including actions, dialogue, and parentheticals, into structured JSON."""
        scenes = []
        current_scene = None
        paragraphs = root.findall(".//paragraphs/para")

        i = 0
        while i < len(paragraphs):
            para = paragraphs[i]
            style = para.find(".//style").get("basestyle", "")
            text = para.find(".//text").text or ""

            if style == "Scene Heading":
                # Extract scene details (ID, name, type)
                id, name, scene_type = extract_scene_details(text, character_names)

                # Save the current scene if one is being processed
                if current_scene:
                    scenes.append(current_scene)

                # Start a new scene
                current_scene = {
                    "type": scene_type,
                    "id": id,  # Use the extracted scene ID
                    "name": name,   # Use the extracted scene name
                    "content": []
                }

            elif current_scene and style == "Character":
                # Handle dialogue
                character_name = name_case(text)
                dialogue_lines = []
                dialogue_blocks = []  # Blocks for dialogue
                i += 1  # Move to the next paragraph

                while i < len(paragraphs):
                    sibling = paragraphs[i]
                    sibling_style = sibling.find(".//style").get("basestyle", "")
                    sibling_text = sibling.find(".//text").text or ""

                    if sibling_style == "Dialogue":
                        # Check if the dialogue is entirely wrapped in parentheses
                        if sibling_text.strip().startswith("(") and sibling_text.strip().endswith(")"):
                            # Treat it as a parenthetical
                            dialogue_blocks.append(create_parenthetical_block(sibling_text.strip()[1:-1], character_names))
                        else:
                            # Regular dialogue line
                            dialogue_lines.append(sibling_text.strip())
                        i += 1
                    elif sibling_style == "Parenthetical":
                        # Convert dialogue lines to blocks and add them
                        if dialogue_lines:
                            dialogue_blocks.extend(create_dialogue_block(character_name, dialogue_lines, character_names))
                            dialogue_lines = []

                        # Add the parenthetical block
                        dialogue_blocks.append(create_parenthetical_block(sibling_text.strip(), character_names))
                        i += 1
                    else:
                        break  # Stop if we encounter a different style

                # Add any remaining dialogue lines
                if dialogue_lines:
                    dialogue_blocks.extend(create_dialogue_block(character_name, dialogue_lines, character_names))

                # Add the dialogue content to the scene
                current_scene["content"].append({
                    "type": "dialogue",
                    "content": [
                        {"type": "characters", "content": [{"type": "line", "content": [{"type": "character", "name": character_name, "text": character_name}]}]},
                        {"type": "lines", "content": dialogue_blocks}
                    ]
                })
                continue  # Skip incrementing i as it's already updated in the loop

            elif current_scene and style == "Action":
                # Handle action text
                parsed_action = tag_characters_in_text(text, character_names)
                current_scene["content"].append({
                    "type": "action",
                    "content": [{"type": "block", "content": [{"type": "line", "content": parsed_action}]}]
                })

            i += 1  # Move to the next paragraph

        # Add the last scene
        if current_scene:
            scenes.append(current_scene)

        return scenes



    def remove_empty_elements(obj):
        """
        Recursively removes elements from a JSON-like structure if:
        - The 'content' list is empty.
        - Any other fields (e.g., 'id', 'name') are empty or None.

        Retains elements with meaningful data in 'content' or other fields.
        """
        if isinstance(obj, dict):
            # Recursively process child elements
            cleaned_dict = {k: remove_empty_elements(v) for k, v in obj.items()}

            # Check if the dictionary should be removed
            # 'type' is required, but the element is removed if:
            # - 'content' is empty
            # - All other keys, except 'type', are empty
            if "type" in cleaned_dict:
                # Extract `content` and other keys
                content = cleaned_dict.get("content", [])
                other_keys = {k: v for k, v in cleaned_dict.items() if k != "type" and k != "content"}

                # Remove the element if `content` is empty AND all other keys are empty
                if not content and all(v in (None, "", [], {}) for v in other_keys.values()):
                    return None

            return cleaned_dict  # Keep the element if it passes the checks

        elif isinstance(obj, list):
            # Recursively process list elements
            cleaned_list = [remove_empty_elements(v) for v in obj]

            # Remove None or empty elements from the list
            return [v for v in cleaned_list if v not in (None, "", [], {})]

        # Return the object as-is for primitive types
        return obj



    # Parse the XML
    tree = ET.parse(source_file)
    root = tree.getroot()

    # Step 1: Build the character list
    character_names = extract_characters(root)

    # Step 2: Process scenes into structured JSON
    scenes = process_scenes(root, character_names)

    # Step 3: Build the final JSON structure
    json_data = {
        "title": "Svartedauden",
        "characters": [{"name": name, "variants": []} for name in sorted(character_names)],
        "content": scenes
    }

    json_data = remove_empty_elements(json_data)

    # Write the JSON to the target file
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f'Converted {source_file} to {target_file} successfully!')




if __name__ == '__main__':
    # File paths
    source_file = '../data/original/manus.xml'
    target_file = '../www/data/newmanus.json'

    # Execute the conversion
    parse_xml_to_json(source_file, target_file)
