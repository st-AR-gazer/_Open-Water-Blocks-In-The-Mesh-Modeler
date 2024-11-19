import json

def find_matching_keys_in_top(json_file_path, input_string):
    input_length = len(input_string)

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for top_key, value in data.items():
        if 'length_matches' in value:
            length_matches = value['length_matches']
            for item in length_matches:
                if len(item) == input_length:
                    print(f"Top Key: {top_key}, Match: {item}")

input_string = "PlatformWaterBase"
json_file_path = "water_block_matches.json"

find_matching_keys_in_top(json_file_path, input_string)
