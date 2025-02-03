import fitz  # PyMuPDF
import json

from ordered_set import OrderedSet



# List of actors (provided in advance)
ROLELIST = {
    'DARRYL': ['DARRYL'],
    'ALEXANDRA': ['ALEXANDRA', 'ALEX'],
    'JANE': ['JANE'],
    'SUKIE': ['SUKIE'],
    'FELICIA': ['FELICIA'],
    'JENNIFER': ['JENNIFER'],
    'MICHAEL': ['MICHAEL'],
    'CLYDE': ['CLYDE'],
    'FIDEL': ['FIDEL'],
    'GINA': ['GINA','FRANNY'],
    'BRENDA': ['BRENDA'],
    'GRETA': ['GRETA','EUDORA'],
    'MARGE': ['MARGE'],
    'JOE': ['JOE', 'JO'],
    'RAYMOND': ['RAYMOND'],
    'TOBY': ['TOBY','DOKTOR PAT','DR PAT'],
    'ED': ['ED'],
    'FRANK': ['FRANK'],
    'DEN LILLE JENTA': ['LITEN PIKE', 'DEN LILLE JENTA'],
    'MAVIS': ['MAVIS'],
    'MABEL': ['MABEL'],
    'MARCY': ['MARCY','REBECCA', 'REBECKA'],
    'CURTIS': ['CURTIS'],
    'HOMER': ['HOMER'],
}
ENSEMBLELIST = {
    'ALLE UNNTATT HEKSENE': ['ALLE UNNTATT HEKSENE'],
    'ALLE FEM': ['ALLE FEM'],
    'ALLE TRE': ['ALLE TRE'],
    'ALLE': ['ALLE'],
    'GRUPPE 1': ['GRUPPE 1'],
    'GRUPPE 2': ['GRUPPE 2'],
    'GRUPPE 3': ['GRUPPE 3'],
    'GRUPPE 4': ['GRUPPE 4'],
    'HEKSENE': ['HEKSENE'],
    'MENN': ['MENN'],
    'BYFOLKET': ['BYFOLKET','BYFOLK','LOKALBEFOLKNINGEN I EASTWICK'],
    'BEGGE': ['BEGGE'],
    'KVINNER': ['KVINNER'],
    'KJÆRESTE VENNER': ['KJÆRESTE VENNER'],
    'ENSEMBLET': ['ENSEMBLET'],
}

ALLROLES = {}
for role in ROLELIST:     ALLROLES[role] = ROLELIST[role]
for role in ENSEMBLELIST: ALLROLES[role] = ENSEMBLELIST[role]

role_list = [role for role in ROLELIST.keys()]
ensemble_list = [role for role in ENSEMBLELIST.keys()]



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
        "last_page": len(doc),
        "lines": [],
        "scenes": [],
        "music": [],
        "acts": [],
    }

    lines_raw = []

    # Iterate through each page in the PDF
    for page_number in range(len(doc)):
        page = doc[page_number]
        page_width, page_height = page.rect.width, page.rect.height  # Get page dimensions

        # Use "dict" mode to extract fine-grained text spans
        text_data = page.get_text("dict", sort=True)  # Extract text as a dictionary
        blocks = text_data["blocks"]  # Get text blocks



        # Process each block of text
        for block in blocks:
            for line in block.get("lines", []):  # Process individual lines
                for span in line.get("spans", []):  # Process individual spans (smaller pieces of text)
                    size = span["size"]
                    text = span["text"].strip()  # Extract and clean the text
                    bbox = span["bbox"]  # Get the bounding box (x0, y0, x1, y1)
                    x0, y0, x1, y1 = bbox




                    # Detect songs
                    if text.startswith("MIN AKT: "):
                        parts = text.split(":")
                        if len(parts) == 3:
                            act_id = parts[1].strip()
                            act_name = parts[2].strip()

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                        # Store the song information
                        data["acts"].append({
                            "id": act_id,
                            "name": act_name,
                            "start": {
                                "page": page_number + 1,  # Page number (1-based index)
                                "y": y_normalized
                            },
                            "end": None
                        })

                        # Annotate the song in the PDF
                        act_text = f"AKT {act_id}: {act_name}"
                        text_color = (0, 0, 1)  # Blue color in RGB
                        page.insert_textbox(
                            (2, y0, page_width - 4, y0 + 22),
                            act_text,
                            fontsize=12,
                            align=1,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs

                    # Detect song end
                    if text.startswith("AKT SLUTT"):

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)
                        y_normalized += 0.021

                        # Store the song information
                        data["acts"][-1]['end'] = {
                            "page": page_number + 1,  # Page number (1-based index)
                            "y": y_normalized + 0.021
                        }

                        # Annotate the song in the PDF
                        act_text = "AKT SLUTT"
                        text_color = (0, 0, 1)  # Blue color in RGB
                        page.insert_textbox(
                            (2, y0, page_width - 4, y0 + 22),
                            act_text,
                            fontsize=12,
                            align=1,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs




                    # Detect songs
                    if text.startswith("MIN MUSIKK: "):
                        parts = text.split(":")
                        if len(parts) == 3:
                            song_type = "song"
                            song_id = parts[1].strip()
                            song_name = parts[2].strip()
                        if len(parts) == 4:
                            song_type = parts[1].strip()
                            song_id   = parts[2].strip()
                            song_name = parts[3].strip()

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                        # Store the song information
                        data["music"].append({
                            "id": song_id,
                            "name": song_name,
                            "type": song_type,
                            "start": {
                                "page": page_number + 1,  # Page number (1-based index)
                                "y": y_normalized
                            },
                            "end": None
                        })

                        # Annotate the song in the PDF
                        song_text = f"MUSIKK {song_id}: {song_name}"
                        text_color = (0, 0, 1)  # Blue color in RGB
                        page.insert_textbox(
                            (2, y0, page_width - 4, y0 + 22),
                            song_text,
                            fontsize=12,
                            align=2,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs



                    # Detect song end
                    if text.startswith("MUSIKK SLUTT"):

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)
                        y_normalized += 0.021

                        # Store the song information
                        data["music"][-1]['end'] = {
                            "page": page_number + 1,  # Page number (1-based index)
                            "y": y_normalized
                        }

                        # Annotate the song in the PDF
                        song_text = "MUSIKK SLUTT"
                        text_color = (0, 0, 1)  # Blue color in RGB
                        page.insert_textbox(
                            (2, y0, page_width - 4, y0 + 22),
                            song_text,
                            fontsize=12,
                            align=2,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs




                    # Detect scenes
                    if text.startswith("MIN SCENE: "):
                        parts = text.split(":")
                        if len(parts) == 3:
                            scene_id = parts[1].strip()
                            scene_name = parts[2].strip()

                            # Normalize coordinates for scene location
                            x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)

                            # Store the scene information
                            data["scenes"].append({
                                "id": scene_id,
                                "name": scene_name,
                                "start": {
                                    "page": page_number + 1,
                                    "y": y_normalized
                                },
                                "end": None,
                            })

                            # Annotate the scene in the PDF
                            scene_text = f"SCENE {scene_id}: {scene_name}"
                            text_color = (0, 0.5, 0)  # Green color in RGB
                            page.insert_textbox(
                                (2, y0, page_width - 4, y0 + 22),
                                scene_text,
                                fontsize=12,
                                align=0,
                                color=text_color,
                                fontname="Helvetica-Bold"
                            )
                        continue  # Skip further processing for scenes

                    # Detect scene end
                    if text.startswith("SCENE SLUTT"):

                        # Normalize coordinates for song location
                        x_normalized, y_normalized = normalize_coordinates(x0, y0, page_width, page_height)
                        y_normalized += 0.021

                        # Store the song information
                        data["scenes"][-1]['end'] = {
                            "page": page_number + 1,  # Page number (1-based index)
                            "y": y_normalized
                        }

                        # Annotate the song in the PDF
                        scene_text = "SCENE SLUTT"
                        text_color = (0, 0.5, 0)  # Blue color in RGB
                        page.insert_textbox(
                            (2, y0, page_width - 4, y0 + 22),
                            scene_text,
                            fontsize=12,
                            align=0,
                            color=text_color,
                            fontname="Helvetica-Bold"
                        )
                        continue  # Skip further processing for songs





                    # Detect roles
                    font_name = span.get("font", "").lower()  # Get the font name
                    is_bold = "bold" in font_name  # Check if "bold" is in the font name

                    if is_bold and size > 10.5 and size < 11.5:
                        # Split the text by ",", "OG", "/", or "+" to handle multiple roles
                        possible_roles = [role.strip() for role in text.replace("OG", ",").replace("/", ",").split(",")]

                        # Match the text to roles and their synonyms
                        matched_roles = []
                        for role_text in possible_roles:
                            for role, synonyms in ALLROLES.items():
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
                        roles = []
                        ensembles = []

                        for role in matched_roles:
                            if role in role_list: roles.append(role)
                            if role in ensemble_list: ensembles.append(role)

                        lines_raw.append({
                            "page": page_number + 1,  # Page number (1-based index)
                            "y": round(y_normalized + 0.005, 3),
                            "roles": roles,
                            "ensembles": ensembles,
                        })

                        # Annotate the role list in the PDF
                        text_x = x0 - 5  # Position text slightly left of the bounding box
                        line_spacing = 12  # Vertical spacing between lines
                        alignment_offset = 11  # Move the roles 8 pixels lower
                        for i, role_name in enumerate(roles):
                            role_y = y0 + alignment_offset + (i * line_spacing)
                            text_width = fitz.get_text_length(role_name, fontsize=10, fontname="Helvetica-Bold")
                            role_text_x = text_x - text_width  # Right-align the text
                            page.insert_text(
                                (role_text_x, role_y),
                                role_name,
                                fontsize=10,
                                color=(0, 0.5, 0),  # Blue color in RGB
                                fontname="Helvetica-Bold"
                            )
                        for i, role_name in enumerate(ensembles):
                            role_y = y0 + alignment_offset + (i * line_spacing)
                            text_width = fitz.get_text_length(role_name, fontsize=10, fontname="Helvetica-Bold")
                            role_text_x = text_x - text_width  # Right-align the text
                            page.insert_text(
                                (role_text_x, role_y),
                                role_name,
                                fontsize=10,
                                color=(0.5, 0.5, 0),  # Blue color in RGB
                                fontname="Helvetica-Bold"
                            )


    def get_location(line):
        return line["page"] + line["y"]

    lines_raw.sort(key=get_location)



    prev_loc = 0.0
    for line in lines_raw:
        if (get_location(line) - prev_loc) < 0.01:
            roleset     = OrderedSet(data["lines"][-1]["roles"] + line["roles"])
            ensembleset = OrderedSet(data["lines"][-1]["ensembles"] + line["ensembles"])
            data["lines"][-1]["roles"]     = list(roleset)
            data["lines"][-1]["ensembles"] = list(ensembleset)

        else:
            data["lines"].append(line)

        prev_loc = get_location(line)




    # Save the annotated PDF
    doc.save(output_pdf_path)
    print(f"Annotated PDF saved to: {output_pdf_path}")

    # Save the JSON data to a file
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"JSON output saved to: {output_json_path}")


if __name__ == "__main__":
    # Path to the input PDF manuscript
    pdf_path = "data/originals/manus-nytt.pdf"  # Replace with your PDF file path

    # Path to the output annotated PDF
    output_pdf_path = "data/compiled/manus/manus-analyzed.pdf"

    # Path to the output JSON file
    output_json_path = "data/sources/manus.json"

    # Annotate the PDF and generate JSON
    annotate_pdf_and_generate_json(pdf_path, output_pdf_path, output_json_path)
