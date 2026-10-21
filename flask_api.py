import os
import uuid
import whisper

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"m4a", "mp3", "wav", "mpeg", "mpga", "webm", "mp4"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model once when the application starts
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded successfully!")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Whisper Audio Transcription API is running",
        "endpoint": "/transcribe",
        "method": "POST"
    })


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():

    # Check whether an audio file was uploaded
    if "file" not in request.files:
        return jsonify({
            "error": "No audio file provided. Use the 'file' field."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported file format",
            "allowed_formats": sorted(ALLOWED_EXTENSIONS)
        }), 400

    # Generate a unique filename to avoid collisions
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    try:
        # Save the uploaded audio file
        file.save(file_path)

        # Transcribe audio into English
        result = model.transcribe(
            file_path,
            fp16=False,
            language="en",
            task="transcribe"
        )

        return jsonify({
            "success": True,
            "filename": original_filename,
            "language": result.get("language", "en"),
            "transcription": result["text"].strip()
        }), 200

    except Exception as e:
        app.logger.exception("Audio transcription failed")

        return jsonify({
            "success": False,
            "error": "Audio transcription failed. Check the audio file and FFmpeg installation."
        }), 500

    finally:
        # Delete the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File too large. Maximum allowed size is 100 MB."
    }), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)
