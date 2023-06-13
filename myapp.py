import streamlit as st
import requests
import PIL.Image
import io


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
prod_title_options=["Carhartt Men's Heavyweight Crewneck Sweatshirt",
 "Bay Island Sportswear Men's Bring Me The Horizon &quot;Smooli&quot; Slim Fit T-Shirt",
 "The Walking Dead Warning Sign Men's T-Shirt",
 'Lego Star Wars -- Dark Pieces T-Shirt, X-Large',
 'Authentic Pigment Unisex-Adult 5.6 Oz. Pigment-Dyed &amp; Direct-Dyed Ringspun Pocket T-Shirt',
 "Russell Athletic Men's Basic Cotton Tee",
 'Clever Girl -- Jurassic Park Adult T-Shirt',
 'Dragon Ball Z Goku Top:Small (Small)',
 '24 Stainless Steel Metal Collar Stays for Dress Shirts',
 'GUESS Campus Shirt']
prod_category_options=['clothing carhartt sweatshirts',
 't shirts',
 'clothing men t shirts',
 't shirts men',
 't shirts',
 'clothing active shirts tees big tall',
 'novelty t shirts men',
 't shirts men',
 'accessories dress shirts',
 'casual button down shirts guess']




st.set_page_config(page_title='Product Recommender', page_icon=':smiley:', layout='wide')
st.title("Product Recommender")

st.subheader("Search by Product ID")
col1, col2 = st.columns(2)
product_id = col1.text_input("Enter a product id") 

product_id2 = col2.selectbox('Or Select a Product ID', [''] + product_id_options)
if product_id or product_id2:
    if product_id2:
        product_id = product_id2
    response = requests.get(f"https://product-recommender.azurewebsites.net/{product_id}")
    data = response.json()
    if "Error" in data:
        st.error(data["Error"])
    else:
        st.write(f"Recommendations for {product_id}:")
        for item in data:
            st.markdown(f"- {item['product_title']} ({item['similarity']})")


st.subheader("Search by Product Title & Category")            
col3, col4 = st.columns(2)
# Get the product title and category from the user

product_title = col3.selectbox('Select a Product Title', [''] + prod_title_options)
category = col4.selectbox("Select a category", [''] + prod_category_options)

# Define a variable that holds the URL of the default or placeholder image
default_image_url = "https://via.placeholder.com/200x200?text=No+Image"

if product_title and category:

    # Send a POST request to the FastAPI endpoint with the user input as JSON data
    response = requests.post(f"https://product-recommender.azurewebsites.net/{product_title}/{category}", json={"product_title": product_title, "category": category})
    data = response.json()
    if "Error" in data:
        st.error(data["Error"])
    else:
        st.write(f"Recommendations for {product_title} - {category}:")
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
                st.image(img, width=200)
            with col2:
                st.markdown(f"- {item['product_title']} ({item['similarity']})")
