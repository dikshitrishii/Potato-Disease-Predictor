import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Streamlit UI
st.title("Image Classification App")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Predict function
def predict(image):
    # Define FastAPI backend URL
    FASTAPI_URL = "http://localhost:8000"  # Update this with your FastAPI server URL
    
    try:
        # Convert image to bytes-like object
        img_byte_array = BytesIO()
        image.save(img_byte_array, format=image.format)
        img_byte_array = img_byte_array.getvalue()
        
        # Make request to FastAPI server
        response = requests.post(f"{FASTAPI_URL}/predict", files={"file": img_byte_array})
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            predicted_class = data["class"]
            confidence = data["confidence"]
            st.write(f"Predicted class: {predicted_class}")
            st.write(f"Confidence: {confidence}")
            
            # Display the uploaded image at one-fourth of its original size
            st.image(image, caption='Uploaded Image', width=image.width // 4, use_column_width=True)
            
        else:
            st.error("Error occurred while fetching prediction.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

# Predict button
if st.button("Predict"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        predict(image)
    else:
        st.error("Please upload an image for classification.")
