import whisper

model = whisper.load_model("base")
result = model.transcribe(r"D:\Python_Project\Whisper_AI_Model\Aakash_Maddheshiya.m4a", fp16=False,language="en", task="transcribe")
print(result["text"])

# import os
# from dotenv import load_dotenv
# from groq import Groq

# # Load variables from the .env file next to this script
# load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# client = Groq(api_key=api_key)

# filename = os.path.join(os.path.dirname(__file__), "Aakash_Maddheshiya.m4a")

# with open(filename, "rb") as file:
#     transcription = client.audio.transcriptions.create(
#         file=(os.path.basename(filename), file.read()),
#         language="en",
#         model="whisper-large-v3",
#         temperature=0,
#         response_format="verbose_json",
#     )
# print(transcription.text)