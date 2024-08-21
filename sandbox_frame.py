from flask import jsonify
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

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