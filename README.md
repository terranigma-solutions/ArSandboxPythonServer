# CG3 AR Sandbox Server

This project is a simple example for a Server for the [CG3 AR Sandbox](https://github.com/terranigma-solutions/cg3-ar-sandbox). It is intended as a starting point to easily implement more sophisticated applications into an ar sandbox without handling any of the complicated stuff like depth acquisition, threading or calibration. 
## What it currently does

- Extracts parameters and pixel data from the request.
- Applies false color mapping to the depth image.
- Returns the processed image as a base64-encoded string in a JSON response.
- Handles errors gracefully and returns appropriate error messages.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/SimonVirgo/depth-image-processing-api.git
    cd depth-image-processing-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Run the Sandbox application
3. Go to the Server Module and fill out ip, port and endpoint.
4. hit Start


## File Structure

- `app.py`: Main Flask application file.
- `sandbox_frame.py`: Contains the `SandboxFrame` class for processing depth images.
- `requirements.txt`: Lists the dependencies required for the project.

## API Endpoints

### POST /sandbox

**Description**: Processes the depth image data and returns the false color image.

**Parameters**:
- `width` (int): The width of the depth image.
- `height` (int): The height of the depth image.
- `minDepth` (float): The minimum depth value in the image.
- `maxDepth` (float): The maximum depth value in the image.

**Request Body**: Raw binary data of the depth image.

**Response**:
- `200 OK`: Returns a JSON object with the base64-encoded false color image.
- `400 Bad Request`: Returns a JSON object with an error message if there is an issue with the request.

