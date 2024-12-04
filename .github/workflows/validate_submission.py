import os
import yaml
import sys

# File paths
LEADERBOARD_FILE = "leaderboard.yaml"
TASK1_FOLDER = "task1/"

# Load correct answers or any predefined validation data (if needed)
# Example: correct format and validation criteria
EXPECTED_KEYS = {"rollno", "username", "score"}

def validate_submission(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    # Load YAML file
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    # Validate keys
    if not EXPECTED_KEYS.issubset(data.keys()):
        raise ValueError(f"File {file_path} is missing required keys: {EXPECTED_KEYS - set(data.keys())}")

    # Additional validations (e.g., format checks)
    if not isinstance(data["rollno"], int) or not isinstance(data["username"], str) or not isinstance(data["score"], int):
        raise ValueError(f"Invalid data format in {file_path}. Check rollno, username, and score.")
    
    return data

def update_leaderboard(data):
    # Ensure leaderboard file exists
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as file:
            yaml.dump({"leaderboard": []}, file)

    # Load leaderboard
    with open(LEADERBOARD_FILE, "r") as file:
        leaderboard = yaml.safe_load(file)

    # Append or update entry
    entry = {"rollno": data["rollno"], "username": data["username"], "score": data["score"]}
    leaderboard["leaderboard"] = [e for e in leaderboard["leaderboard"] if e["rollno"] != data["rollno"]]
    leaderboard["leaderboard"].append(entry)

    # Save leaderboard
    with open(LEADERBOARD_FILE, "w") as file:
        yaml.dump(leaderboard, file)

def create_task_folder(data):
    # Create task folder for the user
    folder_path = os.path.join(TASK1_FOLDER, str(data["rollno"]))
    os.makedirs(folder_path, exist_ok=True)

if __name__ == "__main__":
    try:
        submission_file = sys.argv[1]  # Get submission file from command line argument
        submission_data = validate_submission(submission_file)
        create_task_folder(submission_data)
        update_leaderboard(submission_data)
        print(f"Successfully processed submission for rollno {submission_data['rollno']}.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
