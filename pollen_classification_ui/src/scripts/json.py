import os
import simplejson as json

def extract_pollen_info(directory_path):
    # List to store pollen information
    pollens = []

    # Iterate over the items in the directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Split the folder name into cins_name and epitet_name
            if "_" in item:
                cins_name, epitet_name = item.split("_", 1)
            else:
                cins_name = item
                epitet_name = ""

            # Add shape and location (dummy values for now)
            shape = "Unknown"
            location = "Unknown"

            # Create a dictionary for the pollen
            pollen_info = {
                "cins_name": cins_name,
                "epitet_name": epitet_name,
                "location": location,
                "shape": shape
            }

            # Append the pollen information to the list
            pollens.append(pollen_info)
    
    return pollens

# Specify the directory path
directory_path = 'D:/Projects/pollen_multi_class_ai/pollen_classification_ui/referans_polen'

# Extract pollen information from folder names
pollen_info_list = extract_pollen_info(directory_path)

# Create a dictionary to store the pollen information
pollen_data = {"pollens": pollen_info_list}

# Specify the output JSON file path
output_json_path = 'D:/Projects/pollen_multi_class_ai/pollen_classification_ui/pollen_info.json'

# Save the pollen information to a JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(pollen_data, json_file, indent=4)

print(f'Pollen information saved to {output_json_path}')