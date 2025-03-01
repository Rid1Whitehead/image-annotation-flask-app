# Flask Image Annotation App

## Description

This Flask-based web application allows users to annotate images in a specified directory. Users can select a directory containing images, categorize images using custom labels, and navigate through the images while saving their annotations.

## Features

- Upload and annotate images from a selected directory
- Define custom categories for annotations
- Save annotation data in a CSV file (`annotations.csv`)
- Track and navigate through annotated images
- Reset annotation progress

## Requirements

- Python 3.x
- Flask

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install dependencies using:
   ```bash
   pip install flask
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```

## Usage

1. Open a web browser and go to `http://127.0.0.1:5000/`.
2. Select a directory containing images.
3. Enter categories for annotation (comma-separated).
4. Annotate each image by selecting relevant categories.
5. Navigate through images and save annotations.
6. Reset annotations when needed.

## File Structure

- `app.py`: Main Flask application.
- `templates/`: HTML templates for the web interface.
- `static/`: Static files such as CSS, JS, and images.
- `annotations.csv`: Stores image annotations.

## Endpoints

- `/` - Home page for directory selection.
- `/select_directory` - Processes directory selection and category input.
- `/annotate` - Displays images for annotation.
- `/navigate` - Saves annotations and navigates to the next image.
- `/reset` - Clears session and annotations.
- `/image/<filename>` - Serves images from the selected directory.

## Configuration

- Modify `app.config['ALLOWED_EXTENSIONS']` in `app.py` to allow specific image formats.
- Change `app.secret_key` for security.

## Notes

- Ensure the selected directory contains valid image files.
- Annotations are saved persistently in `annotations.csv`.

## License

This project is open-source and can be modified as needed.

##

