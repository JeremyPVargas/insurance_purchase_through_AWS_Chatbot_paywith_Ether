from pathlib import Path
import os
import streamlit as st
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib
import streamlit as st  
from dotenv import load_dotenv
from PIL import Image
from streamlit_extras.colored_header import colored_header
from ether_wallet import generate_account, get_balance, send_transaction
from boto3 import client

# --- READ JSON FILE FROM S3 Bucket in AWS

load_dotenv()
BUCKET = 'insurance4life'
FILE_TO_READ = 'sample.json'
client = client('s3',
                 aws_access_key_id='MY_AWS_KEY_ID',
                 aws_secret_access_key='MY_AWS_SECRET_ACCESS_KEY'
                )
result = client.get_object(Bucket=BUCKET, Key=FILE_TO_READ) 
text = result["Body"].read().decode()
print(text['Details']) # Use your desired JSON Key for your value 



# >> Something

# --- PAGE CONFIG ---
st.set_page_config(
    page_title= "COMPANY_NAME",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- SESSION STATE ----



# --- PATH SETTINGS ---
THIS_DIR = Path("./streamlitapp.py").parent if "streamlitapp.py" in locals() else Path.cwd()
ASSETS_DIR = THIS_DIR /'assets'
STYLES_DIR = "./styles"
CSS_FILE = "./styles/main.css"
PRICE_DIR ="./pricetojson.json" 

def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css_file(CSS_FILE)

st.markdown("# FOR LIFE - HEALTH INSURANCE")
colored_header(
    label= "Medical Insurance created to keep you healthy",
    description="We are able to offer lower premiums because we use technology to save you money",
    color_name="green-60",
    )
#st.write("")
st.write("---")

# --- GENERAL SETTINGS ---
COMPANY_NAME = "FOR LIFE - HEALTH INSURANCE"
MISSION = "Our mission is to keep you healhty so you can live your best life"
VALUE_PROP = "Our health insurance products are priced exclusively to bring the most value for you"
GREETING = "Thank you for completing the health and habits questionarie" 
PAYPAL_CHECKOUT = "https://www.paypal.com/paypalme/ResonantSolutions"
CONTACT_EMAIL = "jeremyvargas@resonantsolutions.org"
PRODUCT_DESCRIPTION = """
MyToolBelt saves every smart office worker time and effort when it comes to analysis with a unique set of tools you won’t find anywhere else:
- Generate flawless Python code based on your cell selection
- … and many more powerful features
**This is your new superpower; why go to work without it?**
"""


# --- MAIN SECTION ---
#st.header(MISSION)
left_col, right_col = st.columns((2,1))
with left_col:
    st.text("")
    st.text("")
    st.text("")
    st.header(MISSION)
with right_col:
    pic1 = Image.open("./assets/pic1.png")
    st.image(pic1, width=350)
st.write("---")
st.subheader(VALUE_PROP)

#st.sidebar.session_state
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.header("")
st.sidebar.text("")
st.sidebar.header("Based on your responses we found 4 medical insurance products to keep you healthy.")
st.sidebar.header("Each plan is priced according to your needs and health goals")
st.sidebar.text("")
st.sidebar.header("See details on the your :point_right:")
st.sidebar.text("")
st.sidebar.text("--------------------------------------------")
st.sidebar.title("          BRONZE")
st.sidebar.text("Bronze price goes here")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("          SILVER")
st.sidebar.text("Silver price goes here")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("          GOLD")
st.sidebar.text("Gold price goes here")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("          PLATINUM")
st.sidebar.text("Platinum price goes here")

# --- FEATURES ---
st.write("")
st.write("---")
st.subheader(":muscle: Your Health Plans")
st.write("---")
plan_desc = {
    "bronze.png": [
        "Puget Sound BRONZE",
        "-	Visits to PCP: 		$50",
    	"-  Generic RX:		    $35",
    	"-  Deductible:		    $6,000",
    	"-  Max-out of pocket:	$10,000",
    	"- Preferred Network: 	FQHCs",
    	"- Out of Network		PA Required",
    	"- ER deductible:		$500 first visit",
    	
    ],
    "silver.png": [
        "Puget Sound SILVER",
        "-	Visits to PCP: 		$30",
        "-	Generic RX:		    $20",
        "-	Deductible:		    $3,000",
        "-	Max-out pocket:	    $8,000",
        "-	Preferred Network: 	FQHCs",
        "-	Out of Network		PA Required",
        "-	ER deductible:		$500 first visit",

    ],

    "gold.png": [
        "Puget Sound GOLD",
        "-	Visits to PCP: 		$15",
        "-	Generic RX:		    $10",
        "-	Deductible:		    $1,000",
        "-	Max-out pocket:	    $6,000",
        "-	Preferred Network: 	FQHC and Select providers",
        "-	Out of Network		PA Required",
        "-	ER deductible:		$300 first visit",
    ],
    "platinum.png": [
        "MT Rainier PLATINUM",
        "-	Visits to PCP: 		$10",
        "-	Generic RX:		    $8",
        "-	Deductible:		    $600",
        "-	Max-out pocket:	    $7,000",
        "-	Preferred Network: 	FQHC and Select providers",
        "-	Out of Network		PA Required",
        "-	ER deductible:		$300 first visit",

    ],
}



for image, description in plan_desc.items():
    image = Image.open(ASSETS_DIR / image)    
    st.write("")
    left_col, right_col = st.columns(2)
    left_col.image(image, use_column_width=True)
    right_col.write(f"***{description[0]}***")
    right_col.write(description[1])
    right_col.write(description[2])
    right_col.write(description[3])
    right_col.write(description[4])
    right_col.write(description[5])
    right_col.write(description[6])
    right_col.write(description[7])



# Plans
@dataclass
class Record:
    account: str
    plan: str
    amount: float


# Plan Selection
st.write("---")
st.subheader(":ballot_box_with_check: SELECT YOUR PLAN") 
col1, buff, col2 =st.columns([1,0.5,3])
plans = ['BRONZE', 'SILVER','GOLD', 'PLATINUM']

next = st.button("Next option")

if 'final_selection' not in st.session_state:
    st.session_state['final_selection'] = ""

if next:
    if st.session_state["plan_selected"] == 'BRONZE':
        st.session_state.plan_selected = 'SILVER'
    elif st.session_state["plan_selected"] == 'SILVER':
        st.session_state.plan_selected = 'GOLD'
    elif st.session_state["plan_selected"] == 'GOLD':
        st.session_state.plan_selected = 'PLATINUM'
    else: 
        st.session_state.plan_selected = 'BRONZE'

option = col1.radio("Click on the button to select your plan", plans, key="plan_selected")
#option = col1.radio("Click on the button to select your plan", plans)

st.session_state["final_selection"] = option

if option == 'BRONZE':
    col2.write("You selected 'BRONZE'")
elif option == 'SILVER':
    col2.write("You selected 'SILVER'")
elif option == 'GOLD':
    col2.write("You selected 'GOLD'")
else:
    col2.write("You selected 'PLATINUM'")

# Payment Selection
st.write("---")
st.subheader(":ballot_box_with_check: SELECT PURCHASE METHOD") 
left_col, right_col = st.columns((2, 1))
with left_col:
    Pay_with_ETHEREUM= "http://localhost:8502/Pay_with_ETHEREUM"
    st.markdown(
    f'<a href={Pay_with_ETHEREUM} class="button1">👉 Pay with ETHER</a>',
    unsafe_allow_html=True,
    )
with right_col:
    Pay_with_PAYPAL = "https://www.paypal.com/paypalme/ResonantSolutions"
    st.markdown(
    f'<a href={Pay_with_PAYPAL} class="button">👉 Pay with PAYPAL</a>',
    unsafe_allow_html=True,
    )

# --- FAQ ---
st.write("")
st.write("---")
st.subheader(":raising_hand: FAQ")
faq = {
    "When does my coverage start?": "Your coverage starts the first day of the next month.",
    "Will my previous policy be canceled atomatically?": "Yes, once you are signed up, our system will cancel your current insurance plan if you have one.",
    "How can I pay": "you can pay by ETHER (Cryptocurrency), Credit Card, or by PayPal",
    "What do you mean pay with ETHER?": "ETHER is a Cryptocurrency on the Ethereum Blockchain. you will need to enter your Adress-Key to complete the payment. This is very simple and we have all the information you need",
    "What is Annual Deductible": "The annual deductible is the amount of money you pay for medical and prescription drugs before your health plan starts to pay. Some plans have a separate deductible for prescription drugs. In this case, you must pay for prescription drugs up to this amount before the plan pays for prescription drugs.",
    "What is Out-of-Pocket Max": "he out-of-pocket maximum is the most you will have to pay for covered services in a year. Once you spend this amount, your plan pays the total amount for your care.",
    "What is Generic Drugs" : "The amount you will pay for a generic prescription drug.",
    "Primary Care Visit" : "The amount you will pay for a primary care visit to treat an injury or illness.",
    "Quality Rating": "Plans receive a 1 to 5 star quality rating. Ratings include data from surveys and carriers.",
    "In-Network and Out-of-Network":"In-Network refers to weather a particular medical provider, or health services organization is contracted with For Life Health Insurance to deliver services to our customers.Please visit the list of In-Network providers"
}
for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)

# --- CONTACT FORM ---
st.write("")
st.write("---")
left_col, right_col = st.columns((2, 1))
with left_col:
    st.subheader(":mailbox: Contact Us.  We will reply within 12 hours!")
    contact_form = f"""
    <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
     <input type="hidden" name="_captcha" value="true">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="text" name="phone" placeholder="Your phone number" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
    </form>
     <button type="submit" class="button">Send ✉</button>
    """
st.markdown(contact_form, unsafe_allow_html=True)


#emojis
#https://www.webfx.com/tools/emoji-cheat-sheet/
#CoinGecko
#https://github.com/man-c/pycoingecko
#AI Image generator
#https://www.aiimagegenerator.org/
 