from pathlib import Path
import os
import json
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
import boto3

# --- PAGE CONFIG #-----------------------------------------------------------------
st.set_page_config(
    page_title= "COMPANY_NAME",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="expanded"
)

#--- READ JSON FILE FROM S3 Bucket in AWS  #-----------------------------------------------------------------

load_dotenv()
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY') 

for bucket in s3.buckets.all():
    print(bucket.name)

for obj in s3.Bucket('insurance4life').objects.all():
    print(obj)

content_object = s3.Object('insurance4life', 'sample.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)

prices = pd.DataFrame(json_content)
prices = pd.DataFrame(prices)

# ---PLANS ---#-----------------------------------------------------------------

plans = {'plans' : ["BRONZE", "silver", "gold", "platinum"]}
plans = pd.DataFrame(plans)


# ---TABLE WITH PLANS AND PRICES ---#-----------------------------------------------------------------
table =pd.concat([plans, prices], axis=1)
print(table.convert_dtypes().dtypes)

# ---PRICES of PLANS #-----------------------------------------------------------------
Bronze_price = (table['prices'].loc[table.index[0]])
Silver_price = (table['prices'].loc[table.index[1]])
Gold_price = (table['prices'].loc[table.index[2]])
Platinum_price = (table['prices'].loc[table.index[3]])

print("Bronze price is {:.2f}".format(Bronze_price))
print ("Silver price is {:.2f}".format(Silver_price))
print ("Gold price is {:.2f}".format(Gold_price))
print ("Platinum price is {:.2f}".format(Platinum_price))


# --- PATH SETTINGS --------------------------------------------------------------------
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
st.write("---")

# --- GENERAL SETTINGS --------------------------------------------------------------------
COMPANY_NAME = "FOR LIFE - HEALTH INSURANCE"
MISSION = "Our mission is to keep you healhty so you can live your best life"
VALUE_PROP = "Our health insurance products are priced exclusively to bring the most value for you"
GREETING = "Thank you for completing the health and habits questionarie" 
PAYPAL_CHECKOUT = "https://www.paypal.com/paypalme/ResonantSolutions"
CONTACT_EMAIL = "jeremyvargas@resonantsolutions.org"
# PRODUCT_DESCRIPTION = """
# """

# --- MAIN SECTION --------------------------------------------------------------------

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

# --- SIDE BAR INFORMATION -----------------------------------------------------------------

st.sidebar.text("--------------------------------------------")
st.sidebar.header("Based on your responses we found 4 medical insurance products to keep you healthy.")
st.sidebar.header("Each plan is priced according to your needs and health goals")
st.sidebar.text("--------------------------------------------")
st.sidebar.header("See details on the your :point_right:")
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
st.sidebar.header("See details on the your :point_right:")


# --- PLAN FEATURES AND DETAILS -----------------------------------------------------------------
st.write("")
st.write("---")
st.subheader(":muscle: Your Health Plans")
st.write("---")
plan_desc = {
    "bronze.png": [
        "Puget Sound BRONZE: $ {:.2f} per month".format(Bronze_price),
        "- Visits to PCP: 		$50",
    	"- Generic RX:		    $35",
    	"- Deductible:		    $6,000",
    	"- Max-out of pocket:	$10,000",
    	"- Preferred Network: 	FQHCs",
    	"- Out of Network		PA Required",
    	"- ER deductible:		$500 first visit",
    ],
    "silver.png": [
        "Puget Sound SILVER: $ {:.2f} per month".format(Silver_price),
        "-	Visits to PCP: 		$30",
        "-	Generic RX:		    $20",
        "-	Deductible:		    $3,000",
        "-	Max-out pocket:	    $8,000",
        "-	Preferred Network: 	FQHCs",
        "-	Out of Network		PA Required",
        "-	ER deductible:		$500 first visit",
    ],

    "gold.png": [
        "Puget Sound GOLD: $ {:.2f} per month".format(Gold_price),
        "-	Visits to PCP: 		$15",
        "-	Generic RX:		    $10",
        "-	Deductible:		    $1,000",
        "-	Max-out pocket:	    $6,000",
        "-	Preferred Network: 	FQHC and Select providers",
        "-	Out of Network		PA Required",
        "-	ER deductible:		$300 first visit",
    ],
    "platinum.png": [
        "MT Rainier PLATINUM $ {:.2f} per month".format(Platinum_price),
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
    right_col.write(f"**{description[0]}**")
    right_col.write(description[1])
    right_col.write(description[2])
    right_col.write(description[3])
    right_col.write(description[4])
    right_col.write(description[5])
    right_col.write(description[6])
    right_col.write(description[7])

# Plans DATACLASS #-----------------------------------------------------------------
@dataclass
class Record:
    account: str
    plan: str
    amount: float

# Plan Selection #-----------------------------------------------------------------
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

st.session_state["final_selection"] = option

if option == 'BRONZE':
    col2.header("")
    col2.header("You selected BRONZE")
    col2.header("$ {:.2f} per month".format(Bronze_price))
elif option == 'SILVER':
    col2.header("You selected SILVER")
    col2.header("$ {:.2f} per month".format(Silver_price))
elif option == 'GOLD':
    col2.header("You selected GOLD")
    col2.header("$ {:.2f} per month".format(Gold_price))
else:
    col2.header("You selected PLATINUM")
    col2.header("$ {:.2f} per month".format(Platinum_price))

# Payment Selection #-----------------------------------------------------------------
st.write("---")
st.subheader(":ballot_box_with_check: SELECT PURCHASE METHOD") 
left_col, right_col = st.columns((2, 1))
with left_col:
    Pay_with_ETHEREUM= "http://localhost:8501/Pay_with_ETHEREUM"
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

# --- FAQ --------------------------------------------------------------------
st.write("")
st.write("---")
st.subheader(":raising_hand: FAQ")
faq = {
    "When does my coverage start?": "Your coverage starts the first day of the next month.",
    "Will my previous policy be canceled atomatically?": "Yes, once you are signed up, our system will cancel your current insurance plan if you have one.",
    "How can I pay": "You can pay with the crytocurrency ETHER or by PayPal",
    "What do you mean pay with ETHER?": "ETHER is a Cryptocurrency on the Ethereum Blockchain. you will need to enter your Adress-Key to complete the payment. This is very simple and we have all the information you need",
    "What is Annual Deductible": "The annual deductible is the amount of money you pay for medical and prescription drugs before your health plan starts to pay. Some plans have a separate deductible for prescription drugs. In this case, you must pay for prescription drugs up to this amount before the plan pays for prescription drugs.",
    "What is Out-of-Pocket Max": "The out-of-pocket maximum is the most you will have to pay for covered services in a year. Once you spend this amount, your plan pays the total amount for your care.",
    "What is Generic Drugs" : "The amount you will pay for a generic prescription drug.",
    "Primary Care Visit" : "The amount you will pay for a primary care visit to treat an injury or illness.",
    "Quality Rating": "Plans receive a 1 to 5 star quality rating. Ratings include data from surveys and carriers.",
    "In-Network and Out-of-Network":"In-Network refers to weather a particular medical provider, or health services organization is contracted with For Life Health Insurance to deliver services to our customers.Please visit the list of In-Network providers"
}
for question, answer in faq.items():
    with st.expander(question):
        st.subheader(answer)

# --- CONTACT FORM -------------------------------------------------------------------
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


#emojis
#https://www.webfx.com/tools/emoji-cheat-sheet/
#CoinGecko
#https://github.com/man-c/pycoingecko
#AI Image generator
#https://www.aiimagegenerator.org/
#purchae form sample code
#https://github.com/Sven-Bo/sell-digitial-products-using-streamlit-stripe/blob/master/streamlit_app.py