from pathlib import Path
import os
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import streamlit as st  
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlitpayapp import Bronze_price, Silver_price, Gold_price, Platinum_price, option


#page configuration
st.set_page_config(layout="centered")


# --- PATH SETTINGS -----------------------------------------------------------------------------
THIS_DIR = Path("./streamlitapp.py").parent if "streamlitapp.py" in locals() else Path.cwd()
ASSETS_DIR = "./assets"
STYLES_DIR = "./styles"
CSS_FILE = "./styles/main.css"


def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css_file(CSS_FILE)


# --- PAGE TITLE -----------------------------------------------------------------------------
st.title("Use PayPal to purchase your Medical Insurance")
colored_header(
    label= "Medical Insurance created to keep you healthy",
    description="We are able to offer lower premiums because we use technology to save you money",
    color_name="green-60",
    )

# --- SIDE BAR --------------------------------------------------------------------------------
st.sidebar.title("MONTHLY PREMIUMS")
st.sidebar.text("--------------------------------------------")
st.sidebar.title("BRONZE $ {:.2f} ".format(Bronze_price))
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("SILVER $ {:.2f} ".format(Silver_price))
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("GOLD $ {:.2f} ".format(Gold_price))
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("PLATINUM $ {:.2f} ".format(Platinum_price))
st.sidebar.text("--------------------------------------------")

# --- GENERAL SETTINGS ----------------------------------------------------------------------------
COMPANY_NAME = "FOR LIFE - HEALTH INSURANCE"
MISSION = "Our mission is to keep you healhty so you can live your best life"
VALUE_PROP = "Our health insurance products are priced exclusively to bring the most value for you"
PAYPAL_CHECKOUT = "https://www.paypal.com/paypalme/ResonantSolutions"
CONTACT_EMAIL = "jeremyvargas@resonantsolutions.org"
PRODUCT_NAME = "Our health insurance plan products are priced exclusively to bring the most value for you. So you can live your best life"
st.markdown("#")


# HEALTH PLAN SELECTED #-----------------------------------------------------------------


if "final_selection" not in st.session_state:
        st.session_state["final_selection"] =""

plan_selected = st.session_state["final_selection"]



# PLAN PRICE #-----------------------------------------------------------------
price_of_plan_selected = st.write (plan_selected, key = "price_of_plan_selected")

if plan_selected == 'BRONZE':
    st.header("")
    st.header("You selected: Puget Sound BRONZE")
    st.header("$ {:.2f} per month".format(Bronze_price))
elif plan_selected == 'SILVER':
    st.header("The health plan you selected is Puget Sound SILVER")
    st.header("$ {:.2f} per month".format(Silver_price))
elif plan_selected == 'GOLD':
    st.header("The health plan you selected is Puget Sound GOLD")
    st.header("$ {:.2f} per month".format(Gold_price))
else:
    st.header("You selected: Mount Rainer PLATINUM")
    st.header("$ {:.2f} per month".format(Platinum_price))




#---------------------------------#
# PAYMENT SECCION    
# --------------------------------#
    
st.write("---")
st.markdown(
        f'<a href={PAYPAL_CHECKOUT} class="button">👉 Pay with Paypal</a>',
        unsafe_allow_html=True,
    )


# --- MAIN SECTION #-----------------------------------------------------------------

left_col, right_col = st.columns((2, 1))
with left_col:
    st.text("")
    st.header(PRODUCT_NAME)
    
with right_col:
    pic1 = Image.open("./assets/pic2.png")
    st.image(pic1, width=500)

# --- CONTACT FORM #-----------------------------------------------------------------
st.write("")
st.write("---")
st.subheader(":mailbox: Contact Us.  We will reply within 12 hours!")
contact_form = f"""
<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
    <input type="hidden" name="_captcha" value="true">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="text" name="phone" placeholder="Your phone number" required>
    <input type="email" name="email" placeholder="Your email" required>
    <textarea name="message" placeholder="Your message here"></textarea>
<button type="submit" class="button">Send ✉</button>
</form>
    """
st.markdown(contact_form, unsafe_allow_html=True)

st.write("")
st.write("---")

# --- ABOUT  ---
expander_bar = st.expander("Source")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinGecko](https://www.coingecko.com/.
* **Credit:** 1.Web scraper concept adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")