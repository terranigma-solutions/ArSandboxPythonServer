from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import base64
import os
import numpy as np


app = Flask(__name__)

@app.route('/testImage', methods=['GET'])
def process_image():
    ### Get the data from the request
    # Parse the JSON body
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400

    width = data.get('width')
    height = data.get('height')
    pixel_data = data.get('data')

    print("Width: ", width)
    print("Height: ", height)
    # Load the image from the hard drive
    image_path = 'C:\\Users\\svirg\\Downloads\\testRescaled.png'

    # Check if the image path exists
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image path does not exist'}), 404
        print("Image path does not exist")

    image = plt.imread(image_path)

    # Convert the image to a format that can be sent in the response
    buffer = io.BytesIO()
    plt.imsave(buffer, image, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return jsonify({'image': img_str})


def apply_false_color(image):
    # Check the shape of the image data
    if len(image.shape) == 3 and image.shape[2] == 1:
        # Squeeze the single channel dimension
        image = image.squeeze(axis=2)
    elif len(image.shape) != 2:
        raise TypeError(f"Invalid shape {image.shape} for image data")

    # Create a colormap
    viridis = plt.get_cmap('viridis')

    # Normalize the data to the range min-max
    norm = mcolors.Normalize(vmin=image.min(), vmax=image.max())

    # Apply the colormap to values between min and max
    colored_image = viridis(norm(image))

    # Set values <= min to black
    colored_image[image <= image.min()] = [0, 0, 0, 1]

    # Set values >= max to white
    colored_image[image >= image.max()] = [1, 1, 1, 1]

    # Print the dimensions of the colored image
    print("Colored image dimensions:", colored_image.shape)

    # Verify the shape of colored_image before plotting
    if len(colored_image.shape) != 3 or colored_image.shape[2] != 4:
        raise TypeError(f"Invalid shape {colored_image.shape} for colored image data")

    # Plot the colored image for debugging


    return colored_image


@app.route('/sandbox', methods=['POST'])
def sandbox():
    # Get width and height from query parameters
    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)
    minDepth = request.args.get('minDepth', type=float)
    maxDepth = request.args.get('maxDepth', type=float)

    print("minDepth: ", minDepth)
    print("maxDepth: ", maxDepth)

    if width is None or height is None:
        return jsonify({'error': 'Missing width or height'}), 400

    # Get the pixel data from the request body
    try:
        pixel_data = np.frombuffer(request.data, dtype=np.float32)
        depthImage = pixel_data.reshape((height, width))
        depthImage = np.flipud(depthImage)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

### Do something with the image data here


    false_color_image = apply_false_color(depthImage)


### Return the image data as a response to display in the sandbox

    # Convert the false color image to a format that can be sent in the response
    buffer = io.BytesIO()
    plt.imsave(buffer, false_color_image, format='png')
    plt.show()
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the image. the image can have any size. The sandbox will resize it to fit the display
    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)