from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import tempfile
import ssl

app = Flask(__name__)
CORS(app)

# 'EOF'SSL'EOF'
ssl._create_default_https_context = ssl._create_unverified_context

# 
LANGUAGE_MAP = {
    "zh": "Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
    "ar": "Arabic",
    "pt": "Portuguese"
}

# 
whisper_model = None
translation_models = {}

def init_whisper_model():
Whisper"""
    global whisper_model
    if whisper_model is None:
        print("Initializing Whisper model...")
        try:
            whisper_model = whisper.load_model("large-v3-turbo")
             Whisper model loaded successfully")print("
        except Exception as e:
            print( Failed to load large-v3-turbo: {e}")f"
            print("Loading medium model as fallback...")
            whisper_model = whisper.load_model("medium")
             Whisper medium model loaded")print("

def get_translator(source_lang, target_lang):
    """"""
    try:
        from transformers import pipeline
        
        model_key = f"{source_lang}_to_{target_lang}"
        
        if model_key in translation_models:
            return translation_models[model_key]
        
        print(f"Loading translator for {source_lang} -> {target_lang}...")
        
        if source_lang == "en" and target_lang == "zh":
            model = pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh")
        elif source_lang == "zh" and target_lang == "en":
            model = pipeline("translation_zh_to_en", model="Helsinki-NLP/opus-mt-zh-en")
        else:
            return None
        
        translation_models[model_key] = model
        print( Translator loaded for {source_lang} -> {target_lang}")f"
        return model
    except Exception as e:
        print(f"Translation model loading failed: {e}")
        return None

@app.route('/health', methods=['GET'])
def health():
#    """
"""
    return jsonify({"status": "ok", "message": "API service is running"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
#

    
    
    - audio:       (multipart/form-data)
    - target_language: 'EOF' ()
    """
    try:
        init_whisper_model()
        
        # Dockerfile README.md app.py date.py demo_server.py index.html requirements.txt start.sh 
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        target_language = request.form.get('target_language', None)
        
        # 
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name
        
        try:

            print(f"Processing audio: {audio_file.filename}")
            result = whisper_model.transcribe(tmp_path)
            
            detected_language = result.get("language", "unknown")
            transcribed_text = result.get("text", "").strip()
            
            response_data = {
                "transcribed_text": transcribed_text,
                "detected_language": detected_language,
                "language_name": LANGUAGE_MAP.get(detected_language, detected_language),
            }
            
#            # 'EOF''EOF'
            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$
            if target_language and detected_language != target_language:
                translator = get_translator(detected_language, target_language)
                if translator:
                    try:
                        translation_result = translator(transcribed_text)
                        translated_text = translation_result[0]['translation_text']
                        response_data["translated_text"] = translated_text
                        response_data["target_language"] = target_language
                    except Exception as e:
                        print(f"Translation failed: {e}")
                        response_data["translation_note"] = f"Translation not available for {detected_language} -> {target_language}"
                else:
                    response_data["translation_note"] = f"Translation not supported for {detected_language} -> {target_language}"
            
            print( Processing complete - detected: {detected_language}")f"
            return jsonify(response_data), 200
            
        finally:
            # 
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        print(f"Error in transcribe: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/languages', methods=['GET'])
def get_languages():
"""
    return jsonify(LANGUAGE_MAP), 200

@app.route('/', methods=['GET'])
def root():
#            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$EC";             }API
"""
    return jsonify({
        "message": "Whisper Speech Recognition & Translation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /transcribe": "Transcribe audio with language detection and optional translation",
            "GET /languages": "List supported languages",
            "GET /health": "Health check"
        }
    }), 200

if __name__ == '__main__':
    print("=" * 50)
    print("=" * 50)    print("
    init_whisper_model()
    print("\ Ready to accept requests on 0.0.0.0:5000")n
    app.run(host='0.0.0.0', port=5000, debug=False)
