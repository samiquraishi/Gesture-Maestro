# Import necessary libraries and setup
import time
import copy
import math
import numpy as np
import argparse
import cv2 as cv
import mediapipe as mp
import pyautogui as pg
from collections import deque

# Define constants for hand gesture sections and corresponding keys
DISTANCE_SECTION_1 = 12
DISTANCE_SECTION_2 = 55
DISTANCE_SECTION_3 = 75

KEY_LEFT = "left"
KEY_SPACE = "space"
KEY_RIGHT = "right"

# Function to obtain command-line arguments with rephrased comments
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, default=0, help="Specify the video capture device index.")
    parser.add_argument("--width", type=int, default=960, help="Set the width of the video frame.")
    parser.add_argument("--height", type=int, default=540, help="Set the height of the video frame.")
    parser.add_argument('--use_static_image_mode', action='store_true', help="Enable static image mode.")
    parser.add_argument("--min_detection_confidence", type=float, default=0.7, help="Set the minimum detection confidence.")
    parser.add_argument("--min_tracking_confidence", type=int, default=0.5, help="Set the minimum tracking confidence.")
    args, unknown = parser.parse_known_args()
    return args

# Main function for hand gesture recognition and control with rephrased comments
def execute_gesture_recognition():
    # Parse command-line arguments
    input_args = parse_command_line_arguments()

    video_device = input_args.device
    frame_width = input_args.width
    frame_height = input_args.height
    static_image_mode = input_args.use_static_image_mode
    min_detection_confidence = input_args.min_detection_confidence
    min_tracking_confidence = input_args.min_tracking_confidence

    # Set up video capture
    capture = cv.VideoCapture(video_device)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, frame_width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Initialize Mediapipe Hands module
    hands_module = mp.solutions.hands
    hands_detector = hands_module.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # Initialize variables for gesture history
    history_length = 16
    point_history = deque(maxlen=history_length)

    # Set the initial mode
    current_mode = 0

    while True:
        pressed_key = cv.waitKey(10)
        if pressed_key == 27:  # If the ESC key is pressed, exit the loop
            break
        number, current_mode = update_gesture_mode(pressed_key, current_mode)

        # Read a frame from the video capture
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)  # Flip the image horizontally
        debug_frame = copy.deepcopy(frame)

        # Process the image using Mediapipe Hands
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = hands_detector.process(frame)
        frame.flags.writeable = True

        # Perform hand gesture recognition
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                landmark_positions = calculate_landmark_positions(debug_frame, hand_landmarks)
                x1, y1 = landmark_positions[4]
                x2, y2 = landmark_positions[8]
                hand_distance = math.dist((x1, y1), (x2, y2))

                print(round(hand_distance, 2))

                # Perform corresponding actions based on hand gesture distance
                if DISTANCE_SECTION_2 >= hand_distance >= DISTANCE_SECTION_1:
                    pg.keyDown(KEY_LEFT)
                    time.sleep(round(abs((DISTANCE_SECTION_2 - hand_distance) * 0.026)))
                    pg.keyUp(KEY_LEFT)
                elif DISTANCE_SECTION_2 < hand_distance <= DISTANCE_SECTION_3:
                    pg.keyDown(KEY_SPACE)
                    time.sleep(0.01)
                    pg.keyUp(KEY_SPACE)
                elif hand_distance > DISTANCE_SECTION_3:
                    pg.keyDown(KEY_RIGHT)
                    time.sleep(round(abs((DISTANCE_SECTION_3 - hand_distance) * 0.026)))
                    pg.keyUp(KEY_RIGHT)
        else:
            point_history.append([0, 0])

    # Release video capture and close windows
    capture.release()
    cv.destroyAllWindows()

# Function to update the gesture recognition mode
def update_gesture_mode(pressed_key, current_mode):
    number = -1
    if 48 <= pressed_key <= 57:
        number = pressed_key - 48
    if pressed_key == 110:
        current_mode = 0
    if pressed_key == 107:
        current_mode = 1
    if pressed_key == 104:
        current_mode = 2
    return number, current_mode

# Function to calculate hand landmark points
def calculate_landmark_positions(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_positions = []
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_positions.append([landmark_x, landmark_y])
    return landmark_positions

# Run the main function if the script is executed
if __name__ == '__main__':
    execute_gesture_recognition()
