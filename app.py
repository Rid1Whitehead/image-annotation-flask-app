from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import csv
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['ANNOTATIONS_FILE'] = 'annotations.csv'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_images(image_folder):
    try:
        images = [img for img in os.listdir(image_folder) if allowed_file(img)]
    except FileNotFoundError:
        return []
    
    random.shuffle(images)
    return images

def save_annotations(image, categories):
    with open(app.config['ANNOTATIONS_FILE'], mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image, *categories])

@app.route('/')
def index():
    return render_template('select_directory.html')

@app.route('/select_directory', methods=['POST'])
def select_directory():
    selected_directory = request.form.get('directory')
    categories_input = request.form.get('categories')

    if os.path.isdir(selected_directory):
        session['image_folder'] = selected_directory
        session['categories'] = [cat.strip() for cat in categories_input.split(',')] if categories_input else []
        
        images = load_images(selected_directory)
        if images:
            session['images'] = images
            session['annotated_images'] = []  # Track annotated images
            session['current_index'] = 0
            return redirect(url_for('annotate'))
        else:
            flash('No valid images found in the selected directory.')
    else:
        flash('Invalid directory.')
    return redirect(url_for('index'))

@app.route('/annotate')
def annotate():
    images = session.get('images', [])
    annotated_images = session.get('annotated_images', [])
    categories = session.get('categories', [])
    selected_categories = []  # Default selected categories

    if not images:
        return "No images available", 404

    # Check if all images have been annotated
    if len(annotated_images) >= len(images):
        return render_template('index.html', image_filename=None, image_count=len(images),
                               categories=categories, all_annotated=True)

    # Get the current image
    current_index = session.get('current_index', 0)
    current_image = images[current_index]

    return render_template('index.html', image_filename=current_image, image_count=current_index + 1,
                           categories=categories, selected_categories=selected_categories,
                           image_folder=session['image_folder'], all_annotated=False)

@app.route('/navigate', methods=['POST'])
def navigate():
    current_index = session.get('current_index', 0)
    images = session.get('images', [])
    annotated_images = session.get('annotated_images', [])
    selected_categories = request.form.get('selected_categories').split(',') if request.form.get('selected_categories') else []

    # Save annotations for the current image
    current_image = images[current_index]
    if current_image not in annotated_images:
        save_annotations(current_image, selected_categories)
        annotated_images.append(current_image)
        session['annotated_images'] = annotated_images

    # Move to the next image
    session['current_index'] = current_index + 1 if current_index < len(images) - 1 else current_index

    return redirect(url_for('annotate'))

@app.route('/reset')
def reset():
    session.clear()
    open(app.config['ANNOTATIONS_FILE'], 'w').close()
    return redirect(url_for('index'))

@app.route('/image/<filename>')
def image(filename):
    image_folder = session.get('image_folder', '')
    return send_from_directory(image_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)