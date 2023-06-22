import base64
import streamlit as st
import requests
import PIL.Image
import io

import pickle
import pandas as pd
import numpy as np
    
global df2
df2 = pd.read_pickle("my_data2.pkl")

prod_title_options = df2['product_title'].unique().tolist()

product_id_options=['B0009U69UG',
 'B00FQN7LXK',
 'B008TZWRBI',
 'B006XW8A56',
 'B0009G8BNS',
 'B00075ZYRW',
 'B009FNMDXA',
 'B0057QR3MK',
 'B001YK4GNC',
 'B005YP21XU']
prod_title=["Carhartt Men's Heavyweight Crewneck Sweatshirt",
 "Bay Island Sportswear Men's Bring Me The Horizon &quot;Smooli&quot; Slim Fit T-Shirt",
 "The Walking Dead Warning Sign Men's T-Shirt",
 'Lego Star Wars -- Dark Pieces T-Shirt, X-Large',
 'Authentic Pigment Unisex-Adult 5.6 Oz. Pigment-Dyed &amp; Direct-Dyed Ringspun Pocket T-Shirt',
 "Russell Athletic Men's Basic Cotton Tee",
 'Clever Girl -- Jurassic Park Adult T-Shirt',
 'Dragon Ball Z Goku Top:Small (Small)',
 '24 Stainless Steel Metal Collar Stays for Dress Shirts',
 'GUESS Campus Shirt']
prod_category=['clothing carhartt sweatshirts',
 't shirts',
 'clothing men t shirts',
 't shirts men',
 't shirts',
 'clothing active shirts tees big tall',
 'novelty t shirts men',
 't shirts men',
 'accessories dress shirts',
 'casual button down shirts guess']

st.set_page_config(page_title='Product Recommender', page_icon=':moon:', layout='wide')
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img1 = get_img_as_base64("mygif.gif")
img2 = get_img_as_base64("mygif3.gif")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img1}");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
opacity:0.5
color:black;
}}

[data-testid="stVerticalBlock"]{{
max-width: 100rem;
border-radius: 8px;
padding:15px 15px 15px 15px;
background: rgb(222 222 217 / 55%);
color: rgb(0 0 0);
}}

[data-testid="stHeader"]{{
position: fixed;
top: 0px;
left: 0px;
right: 0px;
height: 2.875rem;
background: rgb(77 76 63 / 48%);
outline: none;
z-index: 999990;
display: block;
}}

[data-testid="stSidebar"] {{
background-image: url("data:image/png;base64,{img2}");
background-size: cover;
background-position: center; 
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Product Recommender")

# Using object notation
with st.sidebar.container():
    st.header("About")
    st.subheader("“Our product recommender system uses machine learning algorithms to predict and suggest items that users would be interested in purchasing. Powered by Azure, our system is designed to help users find the products they want quickly and easily.”")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")

    st.subheader('Contact Information')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<a href="mailto:ayushkumar.ae@gmail.com"><img src="https://img.icons8.com/material-outlined/40/000000/new-post.png"/></a>', unsafe_allow_html=True)

    with col2:
        st.markdown('<a href="https://github.com/ayushkr03"><img src="https://img.icons8.com/material-outlined/40/000000/github.png"/></a>', unsafe_allow_html=True)

    with col3:
        st.markdown('<a href="https://www.linkedin.com/in/ayushkumar03/"><img src="https://img.icons8.com/material-outlined/40/000000/linkedin.png"/></a>', unsafe_allow_html=True)

st.subheader("Search by Product ID")
col1, col2 = st.columns(2)
product_id = col1.text_input("**Enter a product id**") 

product_id2 = col2.selectbox('**Or Select a Product ID**', [''] + product_id_options)
if product_id or product_id2:
    if product_id2:
        product_id = product_id2
    response = requests.get(f"https://product-recommender.azurewebsites.net/{product_id}")
    data = response.json()
    if "Error" in data:
        st.error(data["Error"])
    else:
        st.write(f"**Recommendations for** _:orange[{product_id}]_:")
        for item in data:
            st.markdown(f"- {item['product_title']} ( {item['similarity']} )")


st.subheader("Search by Product Title & Category")            
col3, col4 = st.columns(2)
# Get the product title and category from the user

product_title = col3.selectbox('**Select a Product Title**', [''] + prod_title_options)

prod_category_options = list(set(df2.loc[df2['product_title'] == product_title]['category'].tolist()))

category = col4.selectbox("**Select a category**", prod_category_options)

# Define a variable that holds the URL of the default or placeholder image
default_image_url = "https://via.placeholder.com/200x200?text=No+Image"

if product_title and category:

    # Send a POST request to the FastAPI endpoint with the user input as JSON data
    response = requests.post(f"https://product-recommender.azurewebsites.net/{product_title}/{category}", json={"product_title": product_title, "category": category})
    data = response.json()

    with st.container():
        if "Error" in data:
            st.error(data["Error"])
        else:
            st.write(f"**Recommendations for _:orange[{product_title}]_ - {category}:**")
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
                        #st.warning(f"Failed to load or display image:")
                        img_data = requests.get(default_image_url).content
                        img_bytes = io.BytesIO(img_data)
                        img = PIL.Image.open(img_bytes)
                else:
                    # If there is no valid product_img_url field, use the default or placeholder image instead
                    st.error(f"No valid image URL found for {item['product_title']}")
                    img_data = requests.get(default_image_url).content
                    img_bytes = io.BytesIO(img_data)
                    img = PIL.Image.open(img_bytes)
                # Display the image, title, and similarity score in a column layout
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img, width=150)
                with col2:
                    st.markdown(f"- Title - {item['product_title']}")
                    st.markdown(f"- Rating - {item['rating']}")
                    st.markdown(f"- Similarity - {item['similarity']}")           
            st.success('**Successful Recommendation! Have a Nice Day**', icon="✅")
               
