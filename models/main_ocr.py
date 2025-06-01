import google.generativeai as genai
from werkzeug.utils import secure_filename

# Configure generative AI
genai.configure(api_key='AIzaSyD5UWzyTDVlOtU9tNbCAEscvXxQvk7MVOg')
gemini_model = genai.GenerativeModel('models/gemini-1.5-flash-002')

def process_image(filepath):
    try:
        # Upload the file to generative AI
        sample_file = genai.upload_file(path=filepath)
        text = "OCR this image"
        response = gemini_model.generate_content([text, sample_file])
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"
