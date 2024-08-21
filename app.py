from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import base64
import numpy as np

app = Flask(__name__)

def apply_false_color(image):
    viridis = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=image.min(), vmax=image.max())
    colored_image = viridis(norm(image))
    colored_image[image <= image.min()] = [0, 0, 0, 1]
    colored_image[image >= image.max()] = [1, 1, 1, 1]
    return colored_image

class SandboxFrame:
    def __init__(self, request):
        self.request = request
        self.width = None
        self.height = None
        self.minDepth = None
        self.maxDepth = None
        self.depthImage = None
        try:
            self.extract_parameters()
            self.extract_pixel_data()
        except ValueError as e:
            self.error = str(e)
        else:
            self.error = None

    def extract_parameters(self):
        self.width = self.request.args.get('width', type=int)
        self.height = self.request.args.get('height', type=int)
        self.minDepth = self.request.args.get('minDepth', type=float)
        self.maxDepth = self.request.args.get('maxDepth', type=float)

        if self.width is None or self.height is None:
            raise ValueError('Missing width or height')

    def extract_pixel_data(self):
        try:
            pixel_data = np.frombuffer(self.request.data, dtype=np.float32)
            self.depthImage = pixel_data.reshape((self.height, self.width))
            self.depthImage = np.flipud(self.depthImage)

            if len(self.depthImage.shape) == 3 and self.depthImage.shape[2] == 1:
                self.depthImage = self.depthImage.squeeze(axis=2)
            elif len(self.depthImage.shape) != 2:
                raise TypeError(f"Invalid shape {self.depthImage.shape} for image data")
        except Exception as e:
            raise ValueError(str(e))

    def convert_image_to_response(self, false_color_image):
        buffer = io.BytesIO()
        plt.imsave(buffer, false_color_image, format='png')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return jsonify({'image': img_str})

    def handle_error(self):
        return jsonify({'error': self.error}), 400

@app.route('/sandbox', methods=['POST'])
def sandbox():
    frame = SandboxFrame(request)
    if frame.error:
        return frame.handle_error()

    false_color_image = apply_false_color(frame.depthImage)
    return frame.convert_image_to_response(false_color_image)

if __name__ == '__main__':
    app.run(debug=True)