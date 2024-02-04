import subprocess
import cv2

def get_camera_index(serial_number):
    try:
        # Run lsusb command to list USB devices
        result = subprocess.run(['lsusb'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')

        # Iterate through lines in the lsusb output
        for line in output.split('\n'):
            if 'your_camera_name' in line:  # Replace 'your_camera_name' with a unique identifier
                # Extract the serial number and index
                parts = line.split(' ')
                current_serial_number = parts[5]
                current_index = int(parts[3][:-1])  # Remove the trailing colon and convert to integer

                # Check if the current serial number matches
                if current_serial_number == serial_number:
                    return current_index

        # If serial number is not found, return None
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_camera_index(serial_number, camera_index):
    try:
        with open('camera_config.txt', 'a') as file:
            file.write(f"{serial_number}:{camera_index}\n")
    except Exception as e:
        print(f"Error saving camera index: {e}")

def load_camera_index(serial_number):
    try:
        with open('camera_config.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(':')
                if parts[0] == serial_number:
                    return int(parts[1])
    except Exception as e:
        print(f"Error loading camera index: {e}")
    return None

# Replace 'your_serial_number' with the actual serial number of your camera
desired_serial_number = 'your_serial_number'

# Load or get the camera index based on the serial number
camera_index = load_camera_index(desired_serial_number)

if camera_index is None:
    # If not found in the file, get it using lsusb and save it
    camera_index = get_camera_index(desired_serial_number)
    if camera_index is not None:
        save_camera_index(desired_serial_number, camera_index)

# Check if the camera index is found
if camera_index is not None:
    print(f"Camera with serial number {desired_serial_number} found at index {camera_index}")
    
    # Create a VideoCapture object for the found camera
    cap = cv2.VideoCapture(camera_index)

    # Continue with your processing or capturing logic here

    # Release the VideoCapture object when done
    cap.release()
else:
    print(f"Camera with serial number {desired_serial_number} not found.")
