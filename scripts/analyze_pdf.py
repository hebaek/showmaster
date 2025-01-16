import fitz  # PyMuPDF
import json

# List of actors (provided in advance)
ROLES = {
    'DARRYL': ['DARRYL'],
    'ALEXANDRA': ['ALEXANDRA', 'ALEX'],
    'JANE': ['JANE'],
    'SUKIE': ['SUKIE'],
    'FELICIA': ['FELICIA'],
    'JENNIFER': ['JENNIFER'],
    'MICHAEL': ['MICHAEL'],
    'CLYDE': ['CLYDE'],
    'FIDEL': ['FIDEL'],
    'GINA': ['GINA'],
    'BRENDA': ['BRENDA'],
    'GRETA': ['GRETA'],
    'MARGE': ['MARGE'],
    'JOE': ['JOE', 'JO'],
    'RAYMOND': ['RAYMOND'],
    'TOBY': ['TOBY'],
    'ED': ['ED'],
    'FRANK': ['FRANK'],
    'REBECCA': ['REBECCA', 'REBECKA'],
    'LITEN PIKE': ['LITEN PIKE', 'DEN LILLE JENTA'],
    'MAVIS': ['MAVIS'],
    'MABEL': ['MABEL'],
    'MARCY': ['MARCY'],
    'FRANNY': ['FRANNY'],
    'EUDORA': ['EUDORA'],
    'CURTIS': ['CURTIS'],
    'HOMER': ['HOMER'],
    'DOKTOR PAT': ['DOKTOR PAT'],

    'ENSEMBLE': ['ALLE', 'ALLE TRE', 'GRUPPE 1', 'GRUPPE 2', 'GRUPPE 3', 'GRUPPE 4', 'HEKSENE', 'MENN', 'LOKALBEFOLKNINGEN I EASTWICK', 'BYFOLKET', 'BEGGE', 'KVINNER', 'BYFOLK', 'KJÆRESTE VENNER', 'ENSEMBLET'],
}





def normalize_coordinates(x0, y0, page_width, page_height):
    """
    Normalize coordinates:
    - x-coordinate: between 0 and 1 relative to the page width.
    - y-coordinate: between 0 and 1 relative to the page height.
    """
    x_normalized = x0 / page_width  # Normalize x-coordinate
    y_normalized = y0 / page_height  # Normalize y-coordinate
    return round(x_normalized, 3), round(y_normalized, 3)  # Ensure three decimal places


def annotate_pdf_and_generate_json(pdf_path, output_pdf_path, output_json_path):
    """
    Annotates a theatrical manuscript PDF by marking roles, scenes, and songs.
    Outputs results in JSON format for easy integration into other programs.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the annotated PDF.
        output_json_path (str): Path to save the JSON output.
    """
    # Open the PDF
    doc = fitz.open(pdf_path)

    # Storage for roles, scenes, and songs
    data = {
        "roles": [],
        "scenes": [],
        "songs": []
    }

    # Iterate through each page in the PDF
    for page_number in range(len(doc)):
        page = doc[page_number]
        page_width, page_height = page.rect.width, page.rect.height  # Get page dimensions

        # Use "dict" mode to extract fine-grained text spans
        text_data = page.get_text("dict")  # Extract text as a dictionary
        blocks = text_data["blocks"]  # Get text blocks

        # Process each block of text
        for block in blocks:
            for line in block.get("lines", []):  # Process individual lines
                for span in line.get("spans", []):  # Process individual spans (smaller pieces of text)
                    text = span["text"].strip()  # Extract and clean the text
                    bbox = span["bbox"]  # Get the bounding box (x0, y0, x1, y1)
                    x0, y0, x1, y1 = bbox

                    # Detect songs
                    if text.lower().startswith("sang: "):
                        # Extract song title
                        song_title = text.replace("Sang:", "").strip()

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                        # Store the song information
                        data["songs"].append({
                            "page": page_number + 1,  # Page number (1-based index)
                            "x": x_normalized,
                            "y": y_normalized,
                            "title": song_title
                        })

                        # Annotate the song in the PDF
                        song_text = f"Sang: {song_title}"
                        text_color = (0, 0, 1)  # Blue color in RGB
                        page.insert_text(
                            (x0, y0),
                            song_text,
                            fontsize=12,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs

                    # Detect scenes
                    if text.startswith("SCENE "):
                        parts = text.split(":")
                        if len(parts) == 2:
                            scene_id = parts[0].replace("SCENE ", "").strip()
                            scene_name = parts[1].strip()

                            # Normalize coordinates for scene location
                            x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                            # Store the scene information
                            data["scenes"].append({
                                "page": page_number + 1,
                                "x": x_normalized,
                                "y": y_normalized,
                                "scene_id": scene_id,
                                "scene_name": scene_name
                            })

                            # Annotate the scene in the PDF
                            scene_text = f"SCENE {scene_id}: {scene_name}"
                            text_color = (0, 0.5, 0)  # Green color in RGB
                            page.insert_text(
                                (x0, y0),
                                scene_text,
                                fontsize=12,
                                color=text_color,
                                fontname="Helvetica-Bold"
                            )
                        continue  # Skip further processing for scenes

                    # Detect roles
                    font_name = span.get("font", "").lower()  # Get the font name
                    is_bold = "bold" in font_name  # Check if "bold" is in the font name

                    if is_bold:
                        # Split the text by ",", "OG", "/", or "+" to handle multiple roles
                        possible_roles = [role.strip() for role in text.replace("OG", ",").replace("/", ",").split(",")]

                        # Match the text to roles and their synonyms
                        matched_roles = []
                        for role_text in possible_roles:
                            for role, synonyms in ROLES.items():
                                if any(synonym in role_text for synonym in synonyms):
                                    matched_roles.append(role)
                                    break

                        # Skip empty role lists (no matches found)
                        if not matched_roles:
                            continue

                        # Remove duplicates and preserve order
                        matched_roles = list(dict.fromkeys(matched_roles))

                        # Normalize coordinates for role location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                        # Store the role information
                        data["roles"].append({
                            "page": page_number + 1,  # Page number (1-based index)
                            "x": x_normalized,
                            "y": y_normalized,
                            "roles": matched_roles
                        })

                        # Annotate the role list in the PDF
                        text_x = x0 - 5  # Position text slightly left of the bounding box
                        line_spacing = 12  # Vertical spacing between lines
                        alignment_offset = 8  # Move the roles 8 pixels lower
                        for i, role_name in enumerate(matched_roles):
                            role_y = y0 + alignment_offset + (i * line_spacing)
                            text_width = fitz.get_text_length(role_name, fontsize=10, fontname="Helvetica-Bold")
                            role_text_x = text_x - text_width  # Right-align the text
                            page.insert_text(
                                (role_text_x, role_y),
                                role_name,
                                fontsize=10,
                                color=(0, 0, 1),  # Blue color in RGB
                                fontname="Helvetica-Bold"
                            )

    # Save the annotated PDF
    doc.save(output_pdf_path)
    print(f"Annotated PDF saved to: {output_pdf_path}")

    # Save the JSON data to a file
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"JSON output saved to: {output_json_path}")


if __name__ == "__main__":
    # Path to the input PDF manuscript
    pdf_path = "manuscript.pdf"  # Replace with your PDF file path

    # Path to the output annotated PDF
    output_pdf_path = "annotated_manuscript.pdf"

    # Path to the output JSON file
    output_json_path = "output_data.json"

    # Annotate the PDF and generate JSON
    annotate_pdf_and_generate_json(pdf_path, output_pdf_path, output_json_path)