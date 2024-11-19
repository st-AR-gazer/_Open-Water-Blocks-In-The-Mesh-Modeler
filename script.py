import os
import json
import logging

def extract_block_name(path):
    """
    Extracts the block name from a given path.
    Ignores paths that end with a '/' as they are considered directories.
    """
    if path.endswith('/'):
        return None
    return os.path.basename(path)

def setup_logging(log_file='process_log.txt'):
    """
    Sets up logging to output to both the console and a log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode='w')
        ]
    )

def find_water_blocks_with_matching_lengths(json_file_path, output_file='water_block_matches.json'):
    """
    Reads a JSON file containing a list of paths, identifies blocks with 'water' in their names,
    finds other blocks with the same name length, sorts them alphabetically, and writes the results
    to an output JSON file and logs. Also, finds additional 'water' matches within the contents
    of matched lists but excludes them from main length matches.
    
    :param json_file_path: Path to the input JSON file containing the list of paths.
    :param output_file: Name of the output JSON file to save the results.
    """
    root_dir = os.getcwd()
    block_names = []

    try:
        with open(json_file_path, 'r') as f:
            paths = json.load(f)
        logging.info(f"Successfully loaded JSON data from '{json_file_path}'.")
    except FileNotFoundError:
        logging.error(f"The file '{json_file_path}' was not found.")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return

    for path in paths:
        block_name = extract_block_name(path)
        if block_name:
            block_names.append(block_name)

    total_blocks = len(block_names)
    logging.info(f"Total blocks extracted: {total_blocks}")
    if total_blocks == 0:
        logging.warning("No block names were extracted from the provided JSON data.")
        return

    water_blocks = [name for name in block_names if 'water' in name.lower()]
    total_water_blocks = len(water_blocks)
    logging.info(f"Total 'water' blocks found: {total_water_blocks}")

    matches = {}
    if total_water_blocks == 0:
        logging.warning("No blocks containing 'water' were found in the provided data.")
    else:
        water_blocks_sorted = sorted(water_blocks, key=lambda x: x.lower())
        
        total_matched_blocks = 0
        total_unmatched_blocks = 0

        for water_block in water_blocks_sorted:
            target_length = len(water_block)
            same_length_blocks = [
                other for other in block_names 
                if len(other) == target_length and 'water' not in other.lower()
            ]
            
            same_length_blocks_sorted = sorted(same_length_blocks, key=lambda x: x.lower())
            
            additional_water_matches = [
                block for block in same_length_blocks_sorted if 'water' in block.lower()
            ]

            if same_length_blocks_sorted:
                matches[water_block] = {
                    "length_matches": same_length_blocks_sorted,
                    "additional_water_matches": additional_water_matches if additional_water_matches else "No Additional Water Matches"
                }
                total_matched_blocks += 1
            else:
                matches[water_block] = {
                    "length_matches": "No Match",
                    "additional_water_matches": "No Additional Water Matches"
                }
                total_unmatched_blocks += 1

        logging.info(f"Total 'water' blocks with matches: {total_matched_blocks}")
        logging.info(f"Total 'water' blocks with no matches: {total_unmatched_blocks}")

    output_file_path = os.path.join(root_dir, output_file)

    try:
        with open(output_file_path, 'w') as f:
            json.dump(matches, f, indent=4)
        logging.info(f"Results successfully saved to '{output_file_path}'.")
    except Exception as e:
        logging.error(f"Error saving results to '{output_file_path}': {e}")
        return

    if matches:
        logging.info("\nMatch Results (Sorted):")
        for block, details in matches.items():
            length_matches = details["length_matches"]
            additional_water_matches = details["additional_water_matches"]
            logging.info(f"{block}:")
            logging.info(f"  Length Matches: {', '.join(length_matches) if isinstance(length_matches, list) else length_matches}")
            logging.info(f"  Additional Water Matches: {', '.join(additional_water_matches) if isinstance(additional_water_matches, list) else additional_water_matches}")
    else:
        logging.info("No 'water' blocks were processed, so no matches to display.")

if __name__ == "__main__":
    setup_logging(log_file='process_log.txt')

    json_file = 'InventoryStructure.json'
    find_water_blocks_with_matching_lengths(json_file)
