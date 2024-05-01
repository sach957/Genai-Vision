from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro-vision")

def get_response(input,image,prompt):
     response = model.generate_content([input,image[0],prompt])
     return response.text

def input_image_setup(upload_image):
    if upload_image is not None:
        bytes_data = upload_image.getvalue()
        image_parts = [
            {
                "mime_type" : upload_image.type,
                "data" : bytes_data
            }
        ]
    
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt: ",key="input")

uploaded_file = st.file_uploader("Choose an image... ", type=["jpg","jpeg","png"])
                                 
if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image, caption="uploaded Image.", use_column_width=True)

submit = st.button("Tell me about invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image

"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response = get_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)