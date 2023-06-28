import base64
import streamlit as st
import requests
import PIL.Image
import io
import pickle
import pandas as pd
import numpy as np
import bz2file as bz2

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

global df,combined_features,FASTAPI_URL

#FASTAPI_URL = "https://my-product-recommender.azurewebsites.net"

FASTAPI_URL = "http://localhost:8000"

df = pd.read_pickle("embedded.pkl")
#df = decompress_pickle('sentencetransformer2.pbz2')

brand_counts = df['brand_name'].value_counts().sort_values(ascending=False)
brand_options = brand_counts.index.tolist()

product_id_options=['B000NZW3J8','B000ULN4NO','B00008JP7C','B001KU60XA','B0000ANHST','B004IPRWRC','B0037TPECK','B0068VM5T4','B0085A43W8']

st.set_page_config(page_title='Product Recommender',page_icon='🛒', layout='wide')

page_bg_img = f"""
<style>
[data-testid="stVerticalBlock"]{{
max-width: 100rem;
border-radius: 8px;
padding:15px 15px 15px 15px;
background: rgb(0 0 0 / 0.9%);
}}
[data-testid="stHeader"]{{
background: rgb(227 227 227 / 57%);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Product Recommender")

st.subheader("Search by Product ID")
col1, col2, col3 = st.columns(3)
product_id = col1.text_input("**Enter a product id**") 

product_id2 = col2.selectbox('**Or Select a Product ID**', [''] + product_id_options)

k = col3.slider('Select Number of Products to be recommended', 5, 20, 5, key="slider1")

default_image_url = "https://via.placeholder.com/200x200?text=No+Image"

if product_id or product_id2:
    if product_id2:
        product_id = product_id2
    response = requests.get(f"{FASTAPI_URL}/{product_id}/{k}")
    data = response.json()
    
    with st.container():
        if "Error" in data:
            st.error(data["Error"])
        else:
            st.write(f"**Recommendations for** _:orange[{product_id}]_:")
            for item in data:
                # Check if the product_img_url field is present and valid
                if "imgurl" in item and item["imgurl"]:
                    try:
                        # Get the image data from the product_img_url field
                        img_data = requests.get(item["imgurl"]).content
                        # Convert the image data to a bytes object
                        img_bytes = io.BytesIO(img_data)
                        # Open the image from the bytes object
                        img = PIL.Image.open(img_bytes)
                    except Exception as e:
                        # If there is an exception, use the default or placeholder image instead
                        img_data = requests.get(default_image_url).content
                        img_bytes = io.BytesIO(img_data)
                        img = PIL.Image.open(img_bytes)
                else:
                    # If there is no valid product_img_url field, use the default or placeholder image instead
                    img_data = requests.get(default_image_url).content
                    img_bytes = io.BytesIO(img_data)
                    img = PIL.Image.open(img_bytes)
                # Display the image, title, and similarity score in a column layout
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img, width=150, use_column_width ="auto")
                with col2:
                    st.markdown(f"- Product ID - {item['product_id']}")
                    st.markdown(f"- Title - {item['product_title']}")
                    st.markdown(f"- Brand - {item['brand_name']}")
                    st.markdown(f"- Rating - {item['rating']}")
                    st.markdown(f"- Category - {item['category']}") 
                    st.markdown(f"- Review - {item['review_text'].replace('$', 'USD')}")
                    st.markdown(f"- Similarity - {item['similarity']}")          
            st.success('**Successful Recommendation!**', icon="✅")
        
st.subheader("Search by Brand & Category")            
col3, col4, col5 = st.columns(3)
# Get the product title and category from the user

brand_name = col3.selectbox('**Select a Brand**', [''] + brand_options)

prod_category_options = list(set(df.loc[df['brand_name'] == brand_name]['category'].tolist()))

category = col4.selectbox("**Select a category**", [''] + prod_category_options)

k2 = col5.slider('Select Number of Products to be recommended', 5, 20, 5, key="slider2")

# Define a variable that holds the URL of the default or placeholder image
default_image_url = "https://via.placeholder.com/200x200?text=No+Image"

if brand_name and category:

    # Send a POST request to the FastAPI endpoint with the user input as JSON data
    response = requests.post(f"{FASTAPI_URL}/{brand_name}/{category}/{k2}", json={"brand_name": brand_name, "category": category})
    data = response.json()

    with st.container():
        if "Error" in data:
            st.error(data["Error"])
        else:
            st.write(f"**Recommendations for Brand- _:orange[{brand_name}]_ and Category - {category}:**")
            for item in data:
                # Check if the product_img_url field is present and valid
                if "imgurl" in item and item["imgurl"]:
                    try:
                        # Get the image data from the product_img_url field
                        img_data = requests.get(item["imgurl"]).content
                        # Convert the image data to a bytes object
                        img_bytes = io.BytesIO(img_data)
                        # Open the image from the bytes object
                        img = PIL.Image.open(img_bytes)
                    except Exception as e:
                        # If there is an exception, use the default or placeholder image instead
                        img_data = requests.get(default_image_url).content
                        img_bytes = io.BytesIO(img_data)
                        img = PIL.Image.open(img_bytes)
                else:
                    # If there is no valid product_img_url field, use the default or placeholder image instead
                    img_data = requests.get(default_image_url).content
                    img_bytes = io.BytesIO(img_data)
                    img = PIL.Image.open(img_bytes)
                # Display the image, title, and similarity score in a column layout
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img, width=150, use_column_width ="auto")
                with col2:
                    st.markdown(f"- Product ID - {item['product_id']}")
                    st.markdown(f"- Title - {item['product_title']}")
                    st.markdown(f"- Brand - {item['brand_name']}")
                    st.markdown(f"- Rating - {item['rating']}")
                    st.markdown(f"- Category - {item['category']}") 
                    st.markdown(f"- Review - {item['review_text'].replace('$', 'USD')}")
                    st.markdown(f"- Similarity - {item['similarity']}")          
            st.success('**Successful Recommendation!**', icon="✅")
else:
    if not brand_name and category or brand_name and not category:
        st.warning("Please Choose a value from Brand & Category")              
