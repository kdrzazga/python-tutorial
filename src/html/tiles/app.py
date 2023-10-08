from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Define the size of each tile
tile_width = 100
tile_height = 100

# Load the image from the static folder
image_path = os.path.join(app.config['STATIC_FOLDER'], 'images', 'your_image.png')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reveal_tile', methods=['POST'])
def reveal_tile():
    # Get the tile coordinates from the request
    x = int(request.form['x'])
    y = int(request.form['y'])
    
    # Calculate the tile position in the image
    tile_x = x * tile_width
    tile_y = y * tile_height
    
    # Define the size of the revealed area (e.g., 50x50 pixels)
    revealed_width = 50
    revealed_height = 50
    
    # Create a JSON response to reveal the tile
    response = {
        'x': tile_x,
        'y': tile_y,
        'width': revealed_width,
        'height': revealed_height
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
