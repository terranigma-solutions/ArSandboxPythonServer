from flask import Flask, request
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sandbox_frame import SandboxFrame

app = Flask(__name__)

def apply_false_color(image):
    viridis = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=image.min(), vmax=image.max())
    colored_image = viridis(norm(image))
    colored_image[image <= image.min()] = [0, 0, 0, 1]
    colored_image[image >= image.max()] = [1, 1, 1, 1]
    return colored_image

@app.route('/sandbox', methods=['POST'])
def sandbox():
    frame = SandboxFrame(request)
    if frame.error:
        return frame.handle_error()

    false_color_image = apply_false_color(frame.depthImage)
    return frame.convert_image_to_response(false_color_image)

if __name__ == '__main__':
    app.run(debug=True)