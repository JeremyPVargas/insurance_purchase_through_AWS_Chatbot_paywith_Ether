#libraries and dependencies
from pathlib import Path
import sys
import streamlit as st
from PIL import Image
import pandas as pd
import base64
from bs4 import BeautifulSoup
from pycoingecko import CoinGeckoAPI
from streamlit_extras.colored_header import colored_header
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
from streamlitpayapp import Bronze_price, Silver_price, Gold_price, Platinum_price, table
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from ether_wallet import generate_account, get_balance, send_transaction
from operator import floordiv

#page configuration
st.set_page_config(layout="centered")

# --- PATH SETTINGS ---
THIS_DIR = Path("./pages/Pay_with_ETHEREUM.py").parent if "ether_wallet.py" in locals() else Path.cwd()
ASSETS_DIR = "./assets"
STYLES_DIR = "./styles"
CSS_FILE = "./styles/main.css"


def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css_file(CSS_FILE)

st.title('Pay for your medical coverage with Ethereum')
colored_header(
    label= "This page provides the current price of ETHEREUM (ETH) and will convert it the price of your selected medical plan in USD.",
    description="We are able to offer lower premiums because we use technology to save you money",
    color_name="green-60",
    )

# --- SIDE BAR INFORMATION -----------------------------------------------------------------

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


#---------------------------------#
# ETHEREUM PRICE SECTION

left_col, right_col = st.columns((1,2))
with left_col:
    st.subheader("Ethereum price converted to USD")
    cg = CoinGeckoAPI()
    eth = cg.get_price(ids='ethereum',
                    vs_currencies='usd',
                    include_market_cap='true',
                    include_24hr_vol='true',
                    include_24hr_change='true',
                    include_last_updated_at='true')
    eth = pd.DataFrame(eth)
    usd = (eth['ethereum'].loc[eth.index[1]])
    print(usd)
    plans_eth = table['prices'].div(usd)
    plans_eth=pd.DataFrame(plans_eth)
    table = pd.concat([table, plans_eth], axis=1)
    table.columns = [*table.columns[:-1], 'plans_in_eth']
    print(table)

    st.write ("Currently, the price for 1 ETHER is: $ {:.2f}".format(usd))

# ---- ETH PRICE OF PLANS CONVERTED --------------------------------------------------------------
    eth_bronze =(table['plans_in_eth'].loc[table.index[0]])
    eth_bronze = float('{:0.2f}'.format(eth_bronze))
    print(eth_bronze)
    eth_silver =(table['plans_in_eth'].loc[table.index[1]])
    print(eth_silver)
    eth_gold =(table['plans_in_eth'].loc[table.index[2]])
    print(eth_gold)
    eth_platinum =(table['plans_in_eth'].loc[table.index[3]])
    print(eth_platinum)


# ---- COSMETIC Space - Column for Picture--------------------------------------------------------------

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


# ---- HEALTH PLAN SELECTED  #---------------------------------#

st.write("---")

if "final_selection" not in st.session_state:
        st.session_state["final_selection"] ="plan_selected"
plan_selected = st.session_state["final_selection"]

price_of_plan_selected = st.write (plan_selected, key = "plan_selected")


if plan_selected == 'BRONZE':
    st.header("You selected: Puget Sound BRONZE")
    st.header("$ {:.2f} per month".format(Bronze_price))
    st.header("The price in ETH: ")
    st.write(eth_bronze)
elif plan_selected == 'SILVER':
    st.header("The health plan you selected is Puget Sound SILVER")
    st.header("$ {:.2f} per month".format(Silver_price))
    st.header("The price in ETH: ")
    st.write(eth_silver)
elif plan_selected == 'GOLD':
    st.header("The health plan you selected is Puget Sound GOLD")
    st.header("$ {:.2f} per month".format(Gold_price))
    st.header("The price in ETH: ")
    st.write(eth_gold)
else:
    st.header("You selected: Mount Rainer PLATINUM")
    st.header("$ {:.2f} per month".format(Platinum_price))
    st.header("The price in ETH: ")
    st.write(eth_platinum)


eth_price_of_plan_selected = st.write(price_of_plan_selected, key = 'eth_price_of_plan_selected')

if plan_selected == 'BRONZE':
    eth_price_of_plan_selected = eth_bronze
elif plan_selected == 'SILVER':
    eth_price_of_plan_selected = eth_silver
elif plan_selected == 'GOLD':
    eth_price_of_plan_selected = eth_gold
else:
    eth_price_of_plan_selected = eth_platinum
    


# ENTER ETHER WALLET NUMBER -----------------------------------------------------------------

st.write("---")
st.subheader(":rocket: To complete your purchase you will need to enter your ETHER wallet number here")

if 'my_account' not in st.session_state:
    st.session_state['my_account'] = ""

my_account = st.text_input("Please enter you ETHER account number here", st.session_state["my_account"])
submit =st.button("Submit")
if submit:
    st.session_state["my_account"]= my_account
    st.write("Your ETHER wallet number is: ",my_account)


# COMPLETE PURCHASE #-----------------------------------------------------------------

from ether_wallet import generate_account, get_balance, send_transaction

@dataclass
class Transaction (object):
    charge: float
    price_of_plan_selected: float
    usd: float
    eth_price_of_plan_selected: float

st.write("---")

# FOR LIFE ACCOUNT INFORMATION (dummy account from practice) 
Forlifeaccount = "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0"
# User WALLET ACCOUNT 
my_account = generate_account()
# charge = price_of_plan_selected / usd
ether = get_balance(w3, my_account.address)

st.subheader("Complete your purchase")
if st.button("Purchase Plan with Ether"):
    
    transaction_hash = send_transaction(w3, my_account, Forlifeaccount, eth_price_of_plan_selected)
    
st.markdown("#### Validated Transaction Hash")
 
st.write("---")

transaction_hash = send_transaction(w3, my_account, Forlifeaccount, eth_price_of_plan_selected)
st.write(transaction_hash)


st.write("---")
# --- ABOUT ------------------------------------------------------------------------------------------------------#

expander_bar = st.expander("Source")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinGecko](https://www.coingecko.com/.
* **Credit:** 1.Web scraper concept adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")