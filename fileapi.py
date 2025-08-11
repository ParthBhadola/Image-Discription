from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import google.generativeai as genai
import time
import io
import base64
from PIL import Image
# Configure your Gemini API key
genai.configure(api_key="")  
# Initialize the Gemini chat model
model_name = "gemini-2.5-flash-preview-05-20"
chat_session = genai.GenerativeModel(model_name).start_chat()
app = FastAPI()
@app.post("/describe-image")
async def describe_image(file: UploadFile = File(...)):
    try:
        # Read the image file
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        # Convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        # Send the base64 image string to the chat model for description
        response = chat_session.send_message(f"Describe this image: data:image/jpeg;base64,{img_str}")
        return {"description": response.text}
    except Exception as e:
        if "429" in str(e):
            time.sleep(46)  
            return {"error": "Quota exceeded. Please try again later."}
        raise HTTPException(status_code=500, detail=str(e))

