#libraries and dependencies
from pathlib import Path
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
from pycoingecko import CoinGeckoAPI
from streamlit_extras.colored_header import colored_header
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
from ether_wallet import generate_account, get_balance, send_transaction 



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

st.title('Pay for your medical coverage with Ethereum (ETH)')
colored_header(
    label= "This page provides the current price of ETHEREUM (ETH) and will convert it the price of your selected medical plan in USD.",
    description="We are able to offer lower premiums because we use technology to save you money",
    color_name="green-60",
    )


#---------------------------------#
# CONVERSION RATE SECTION

left_col, right_col = st.columns((1,2))
with left_col:
    #st.text("")
    #st.write("")
    st.subheader("Ethereum price converted to USD")
    cg = CoinGeckoAPI()
    eth = cg.get_price(ids='ethereum',
                    vs_currencies='usd',
                    include_market_cap='true',
                    include_24hr_vol='true',
                    include_24hr_change='true',
                    include_last_updated_at='true')
    eth
    st.text('Currently, the price for one (1) ETHER is: ')
 
with right_col:
    st.write("")
    st.text("")
    st.write("")
    st.text("")
    st.write("")
    st.text("")
    st.write("")
    st.text("")
    image = Image.open("./assets/eth.png")
    st.image(image, width = 500)

#---------------------------------#
# HEALTH PLAN SELECTED

st.write("---")
st.subheader("The Health Plan you selected is")

if "final_selection" not in st.session_state:
        st.session_state["final_selection"] =""
plan_selected = st.session_state["final_selection"]

st.write("You have selected: ",plan_selected)

  #, st.session_state["plan_selected"],plan_selected)

#plans = st.session_state("plan_selected",st.session_state["plan_selected"])

#plans = st.text_input("The plan you selected is", st.session_state['plans'])

#st.markdown(
    #f'<a href={PLAN} class="list">👉 Your Plan Level</a>',
    #unsafe_allow_html=True,
#)
#---------------------------------#
# ENTER ETHER WALLET NUMBER

st.write("---")
st.session_state
st.subheader(":rocket: To complete your purchase you will need to enter your ETHER wallet number here")

if 'my_account' not in st.session_state:
    st.session_state['my_account'] = ""

my_account = st.text_input("Please enter you ETHER account number here", st.session_state["my_account"])
submit =st.button("Submit")
if submit:
    st.session_state["my_account"]= my_account
    st.write("Your ETHER wallet number is: ",my_account)

#---------------------------------#
# COMPLETE PURCHASE

st.write("---")
st.subheader("Complete your purchase")
EXECUTE = "send_transaction"
st.markdown(
    f'<a href={EXECUTE} class="button1"> Complete Purchase</a>',
    unsafe_allow_html=True,
)
#---------------------------------#
# CONFIRMATION HASH

st.write("---")
st.subheader("Confirmation")
transaction_hash = send_transaction(w3, account, candidate_address, wage)
st.write(transaction_hash)

# FOR LIFE ACCOUNT INFORMATION
forlifeaccount = "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0"

def get_account(w3):
    """For Life Insurance Ether Account."""
    db_list = list(candidate_database.values())

    for number in range(len(people)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("FinTech Finder Rating: ", db_list[number][2])
        st.write("Hourly Rate per Ether: ", db_list[number][3], "eth")
        st.text(" \n")
#---------------------------------#
account = generate_account()
ether = get_balance(w3, account.address)
forlifeaccount = "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0"

#---------------------------------#
st.write("---")
# About
expander_bar = st.expander("Source")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinGecko](https://www.coingecko.com/.
* **Credit:** 1.Web scraper concept adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")