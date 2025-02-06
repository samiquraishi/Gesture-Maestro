# Gestue Maestro - A hand gesture controller

This project allows you to control certain computer actions (left arrow, right arrow, spacebar) using hand gestures recognized by your webcam.  It uses computer vision techniques with the Mediapipe library to track hand landmarks and interpret gestures based on the distance between specific fingertips.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Gestures](#gestures)
-   [Dependencies](#dependencies)
-   [Contributing](#contributing)

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/hand-gesture-controller.git](https://www.google.com/search?q=https://github.com/your-username/hand-gesture-controller.git)  # Replace with your repository URL
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv        # Create the virtual environment
    source venv/bin/activate   # Activate (Linux/macOS)
    venv\Scripts\activate      # Activate (Windows)
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Script:**
    ```bash
    python hand.py 
    ```

2.  **Gesture Recognition:** The script will capture video from your webcam.  Perform the following gestures to trigger actions:

## Gestures

*   **Left Arrow:** Hold your hand with your index and thumb relatively close together (within a certain distance threshold). The closer they are, the longer the key will be pressed.
*   **Spacebar:** Hold your hand with your index and thumb at a medium distance.
*   **Right Arrow:** Hold your hand with your index and thumb further apart (beyond another distance threshold). The further they are, the longer the key will be pressed.

## Dependencies

the dependencies are listed in the `requirements.txt` file for easy installation.

## Contributing

Contributions are welcome!  Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
