import os
import json
import sys
import shutil

def load_json(json_path):
    """Load the JSON file containing water block matches."""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

def find_gbx_file(source_dir, block_name):
    """
    Find the .Block.Gbx file for a given block name.
    Assumes the file is named exactly as the block with .Block.Gbx extension.
    """
    expected_file = f"{block_name}.Block.Gbx"
    for root, dirs, files in os.walk(source_dir):
        if expected_file in files:
            file_path = os.path.join(root, expected_file)
            print(f"Found '{block_name}' in '{file_path}'.")
            return file_path
    print(f"No .Block.Gbx file found for '{block_name}'.")
    return None

def replace_block_name(content, original_name, new_name):
    """
    Replace all occurrences of original_name with new_name in the binary content.
    Ensures that the replacement name has the same length.
    Returns the modified content and the number of replacements made.
    """
    original_bytes = original_name.encode('utf-8')
    new_bytes = new_name.encode('utf-8')

    if len(original_bytes) != len(new_bytes):
        print(f"Length mismatch: '{original_name}' ({len(original_bytes)}) vs '{new_name}' ({len(new_bytes)}). Skipping replacement.")
        return content, 0

    occurrences = content.count(original_bytes)
    if occurrences == 0:
        return content, 0

    modified_content = content.replace(original_bytes, new_bytes)
    return modified_content, occurrences

def process_block_files(source_dir, target_dir, water_blocks):
    """Process block files: replace internal water block names with water block names."""
    for water_block, details in water_blocks.items():
        length_matches = details.get('length_matches', [])
        if not length_matches:
            print(f"No length matches for '{water_block}', skipping...")
            continue

        new_block = length_matches[0]
        print(f"\nProcessing water block: '{water_block}' with match: '{new_block}'.")

        source_file_path = find_gbx_file(source_dir, new_block)
        if not source_file_path:
            print(f"Source .Block.Gbx file for '{new_block}' not found. Skipping...")
            continue

        try:
            with open(source_file_path, 'rb') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading '{source_file_path}': {e}")
            continue

        modified_content, replacements = replace_block_name(content, new_block, water_block)
        if replacements == 0:
            print(f"No occurrences of '{new_block}' found in '{source_file_path}'. Skipping replacement.")
            continue
        else:
            print(f"Replaced {replacements} occurrence(s) of '{new_block}' with '{water_block}'.")

        target_block_dir = os.path.join(target_dir, water_block)
        os.makedirs(target_block_dir, exist_ok=True)
        print(f"Created directory: '{target_block_dir}'.")

        target_file_name = f"{water_block}.Block.Gbx"
        target_file_path = os.path.join(target_block_dir, target_file_name)

        try:
            with open(target_file_path, 'wb') as f_out:
                f_out.write(modified_content)
            print(f"Saved modified file to '{target_file_path}'.")
        except Exception as e:
            print(f"Error writing to '{target_file_path}': {e}")

def main():
    source_dir = r'./VanillaBlockToCustomBlock-Links'
    target_dir = r'./new_blocks'
    json_path = r'./water_block_matches.json'

    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist. Exiting.")
        sys.exit(1)

    if not os.path.exists(json_path):
        print(f"JSON file '{json_path}' not found. Please ensure it's in the correct location.")
        sys.exit(1)

    water_blocks = load_json(json_path)
    print(f"Loaded JSON data with {len(water_blocks)} water blocks.")

    process_block_files(source_dir, target_dir, water_blocks)

    print("\nHex editing automation completed.")

if __name__ == "__main__":
    main()
