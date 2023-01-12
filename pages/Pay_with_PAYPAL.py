from pathlib import Path
import os
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib
import streamlit as st  
from PIL import Image
from streamlit_extras.colored_header import colored_header


#page configuration
st.set_page_config(layout="centered")


# --- PATH SETTINGS ---
THIS_DIR = Path("./streamlitapp.py").parent if "streamlitapp.py" in locals() else Path.cwd()
ASSETS_DIR = "./assets"
STYLES_DIR = "./styles"
CSS_FILE = "./styles/main.css"


def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css_file(CSS_FILE)

st.title("Use PayPal to purchase your Medical Insurance")
colored_header(
    label= "Medical Insurance created to keep you healthy",
    description="We are able to offer lower premiums because we use technology to save you money",
    color_name="green-60",
    )


# --- GENERAL SETTINGS ---
COMPANY_NAME = "FOR LIFE - HEALTH INSURANCE"
MISSION = "Our mission is to keep you healhty so you can live your best life"
VALUE_PROP = "Our health insurance products are priced exclusively to bring the most value for you"
PAYPAL_CHECKOUT = "https://www.paypal.com/paypalme/ResonantSolutions"
CONTACT_EMAIL = "jeremyvargas@resonantsolutions.org"
PRODUCT_NAME = "Our health insurance plan products are priced exclusively to bring the most value for you. So you can live your best life"
st.markdown("#")
PRODUCT_DESCRIPTION = """
MyToolBelt saves every smart office worker time and effort when it comes to analysis with a unique set of tools you won’t find anywhere else:
- Generate flawless Python code based on your cell selection
- Call Python scripts from Excel without having to lift a finger
- Create Jupyter Notebooks from Excel
- Add tickmarks to cells and highlight key areas
- Create an informative table of contents with ease
- … and many more powerful features
**This is your new superpower; why go to work without it?**
"""
# HEALTH PLAN SELECTED

st.subheader("The Health Plan you selected is")
if "plan_selected" not in st.session_state:
        st.session_state["plan_selected"] =""
plan_selected = st.session_state["plan_selected"]

st.write("You have selected: ",plan_selected)
st.write("---")

# PLAN PRICE 
st.write("")
st.subheader("The Price in USD is")
st.write("---")
st.markdown(
        f'<a href={PAYPAL_CHECKOUT} class="button">👉 Pay with Paypal</a>',
        unsafe_allow_html=True,
    )
# --- MAIN SECTION ---
#st.header(PRODUCT_NAME)
left_col, right_col = st.columns((2, 1))
with left_col:
    st.text("")
    st.header(PRODUCT_NAME)
    
with right_col:
    pic1 = Image.open("./assets/pic2.png")
    st.image(pic1, width=500)



st.write("")
st.write("---")
    # About
expander_bar = st.expander("Source")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinGecko](https://www.coingecko.com/.
* **Credit:** 1.Web scraper concept adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")