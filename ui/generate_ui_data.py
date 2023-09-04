import base64
import json
import os

# Define the directory where the profiles are stored
profiles_dir = "../profiles"

# List all the profile IDs (directories) under the profiles directory
profile_ids = os.listdir(profiles_dir)

# Initialize an empty dictionary to store all profile data
all_profiles = {}

# Loop through all profile IDs to read their respective data
for profile_id in profile_ids:
    profile_data = {}

    # Construct directory path for each profile
    profile_dir = os.path.join(profiles_dir, profile_id)

    # Read profile.json
    with open(os.path.join(profile_dir, "profile.json")) as f:
        profile_data["profile"] = json.load(f)

    # Read matches.json
    with open(os.path.join(profile_dir, "matches.json")) as f:
        profile_data["matches"] = json.load(f)

    # Check if profile.png exists and if so, read it as a base64 encoded string
    profile_image_path = os.path.join(profile_dir, "profile.png")
    if os.path.exists(profile_image_path):
        with open(profile_image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
            profile_data["image"] = base64_image

    # Add profile data to all_profiles dictionary
    all_profiles[profile_id] = profile_data

# Convert the dictionary to a JSON-formatted string
all_profiles_json_str = json.dumps(all_profiles)

# Create a JavaScript file that contains the profiles data
js_content = f"export const profiles = {all_profiles_json_str};"

# Save this JavaScript content to a .js file
js_file_path = "./src/all_profiles.js"
with open(js_file_path, "w") as f:
    f.write(js_content)
