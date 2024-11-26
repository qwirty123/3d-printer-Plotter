import subprocess
import json
import re

INPUT_SVG = "car_bp.svg"
Z_HOP_THRESH = 2
SETTINGS_FILE = "svg2gcode_settings_noprime.json"


# # Check if width and height are correct
# # This is specifically for my ender 3, your size might be different
# with open(INPUT_SVG) as svg_file:
#     text = svg_file.read()
#     if ('width="230mm"' not in text) or ('height="230mm"' not in text):
#         raise ValueError("The svg should be 230mmx230mm")


subprocess.run(["svg2gcode.exe", "--settings", SETTINGS_FILE, "--out", "output_temp.gcode", INPUT_SVG])

settings = json.load(open(SETTINGS_FILE))


def get_number_after_letter(line: str, letter: str):
    # Examples:
    # get_number_after_letter("G0 X49 Y61", "X") == 49
    # get_number_after_letter("G0 X49 Y61", "Y") == 61

    pattern = rf"{letter}(-?\d+(\.\d*)?)"   # Don't ask me, chatgpt wrote this
    match = re.search(pattern, line)

    if match:
        return float(match.group(1))  # Convert to float and return
    return None  # Return None if the letter is not found


with open("output_temp.gcode", 'r') as file:
    lines = file.readlines()  # Reads all lines into a list
    lines = [x.strip() for x in lines]

    for line_num, line in enumerate(lines):
        if line == settings["machine"]["tool_off_sequence"]:
            try:
                prev_line = lines[line_num-1]   # Location before z-hop
                next_line = lines[line_num+1]   # Location after z-hop
                next_next_line = lines[line_num+2]  # Tool on sequence
            except IndexError:
                # Last or first lines
                continue

            if not prev_line.startswith("G1"): continue
            if not next_line.startswith("G0"): continue
            if not next_next_line == settings["machine"]["tool_on_sequence"]: continue

            before_x = get_number_after_letter(prev_line, "X")
            before_y = get_number_after_letter(prev_line, "Y")
            after_x = get_number_after_letter(next_line, "X")
            after_y = get_number_after_letter(next_line, "Y")

            distance = ((before_x-after_x)**2 + (before_y-after_y)**2)**0.5     # distance from before z-hop to after

            if distance < Z_HOP_THRESH:
                # remove z-hop
                lines[line_num] = ""
                lines[line_num+2] = ""

    out_filename = INPUT_SVG.removesuffix(".svg") + ".gcode"
    with open(out_filename, 'w') as file2:
        for line2 in lines:
            file2.write(line2 + '\n')





