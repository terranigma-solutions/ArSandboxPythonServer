from flask import jsonify
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

class SandboxFrame:
    """
    A class to represent a frame of depth image data and handle its processing.

    Attributes:
    ----------
    request : flask.Request
        The Flask request object containing the image data and parameters.
    width : int
        The width of the depth image.
    height : int
        The height of the depth image.
    minDepth : float
        The minimum depth value of the sandbox.
    maxDepth : float
        The maximum depth value of the sandbox.
    depthImage : numpy.ndarray
        The processed depth image data.
    error : str
        The error message if an exception occurs during processing.
    """

    def __init__(self, request):
        """
        Constructs all the necessary attributes for the SandboxFrame object.

        Parameters:
        ----------
        request : flask.Request
            The Flask request object containing the image data and parameters.
        """
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
        """
        Extracts the parameters from the request object and sets the width, height, minDepth, and maxDepth attributes.

        Raises:
        ------
        ValueError
            If width or height is missing from the request parameters.
        """
        self.width = self.request.args.get('width', type=int)
        self.height = self.request.args.get('height', type=int)
        self.minDepth = self.request.args.get('minDepth', type=float)
        self.maxDepth = self.request.args.get('maxDepth', type=float)

        if self.width is None or self.height is None:
            raise ValueError('Missing width or height')

    def extract_pixel_data(self):
        """
        Extracts and processes the pixel data from the request object and sets the depthImage attribute.

        Raises:
        ------
        ValueError
            If there is an error in processing the pixel data.
        TypeError
            If the shape of the depth image data is invalid.
        """
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
        """
        Converts the false color image to a base64-encoded string and returns it as a JSON response.

        Parameters:
        ----------
        false_color_image : numpy.ndarray
            The false color image to be converted.

        Returns:
        -------
        flask.Response
            A JSON response containing the base64-encoded image string.
        """
        buffer = io.BytesIO()
        plt.imsave(buffer, false_color_image, format='png')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return jsonify({'image': img_str})

    def handle_error(self):
        """
        Returns a JSON response containing the error message.

        Returns:
        -------
        flask.Response
            A JSON response containing the error message.
        """
        return jsonify({'error': self.error}), 400