from flask import Flask
from waitress import serve
import os
import logging
import random
from google import genai
from google.genai import types
import base64

app = Flask(__name__)
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

from google import genai
from google.genai import types
import base64

def generate():
  client = genai.Client(
      vertexai=True,
      location="us-central1",
  )

  model = "gemini-2.0-flash-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text="""Return a random fact about rackspace.""")
      ]
    )
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    system_instruction=[types.Part.from_text(text="""I am an arrogant chatbot. I know everything.""")],
  )

  returnstring=""
  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    returnstring = returnstring + chunk.text
    #print(chunk.text, end="")
  return returnstring

@app.route("/")
def randomfact():
  randomfact=generate()
  return randomfact + "\n"

@app.route("/version")
def version():
  return "ROI ML App Demo 1.1\n"

if __name__ == "__main__":
  serve(app,host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))
