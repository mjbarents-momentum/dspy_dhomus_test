from pdf2image import convert_from_path
from io import BytesIO, StringIO
import pandas as pd
import base64
import requests
import os

# Convert pdf to base64 image
def pdf_to_base64_image(pdf_path, first_page=1, last_page=1, image_format='JPEG', quality=100):
    # Convert the specified PDF pages to images
    images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page)
    
    # Convert the first image to base64
    buffer = BytesIO()  # Create an in-memory buffer
    images[0].save(buffer, format=image_format, quality=quality)  # Save the image to the buffer
    buffer.seek(0)  # Reset buffer position to the start
    
    return base64.b64encode(buffer.read()).decode('utf-8')  # Encode to base64 and return

# Call gpt to parse base64 image
def get_csv_tabel(contract_base64):
  api_key = api_key=os.environ.get("OPENAI_API_KEY")
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Parse the image and extract the table. Specify the column names and return each row as a new line, with columns separated by a semicolon (';'). Only return the table without any additional text or explanation."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{contract_base64}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  text = response.json()['choices'][0]['message']['content']
  text = text.lstrip('```\n')
  csv_data = StringIO(text)
  df = pd.read_csv(csv_data, delimiter=';')

  return df
