### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests
import json
import boto3



### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except (ValueError,TypeError):
        return float("nan")
        
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except (ValueError,TypeError):
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots}
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message
        }
    }

    return response

    ## Validate data
def validate_data(age, intent_request):
    # Validate that the user is over 21 years old
    if age is not None:
        if age < 21 or age > 85:
            return build_validation_result(
                False,
                "age",
                f"You entered {age}. You should need to be 21 years old "
                " or less than 65 years old to use this service, "
                "please come back when you are 21 or enter a different age."
            )

          
    
    return build_validation_result(True, None, None)

    
# logic to parse through answers and decide what plan will be returned.  
def get_price(age, smoke, alcohol, drug):
    
    bronze = 75
    silver = 140
    gold = 200
    platinum = 275
    
    smoking = 1.13
    drinking = 1.10
    druging = 1.15
    
    age_3141 = 1.10
    age_4150 = 1.15
    age_5164 = 1.17

    
    
    if (age >= 18 and age < 31) and (smoke == "no") and (alcohol == "no") and (drug == "no"):
        bronze_price = bronze
        silver_price = silver
        gold_price = gold
        platinum_price = platinum

  
            
    elif (age >= 18 and age < 31) and (smoke == "yes") and (alcohol == "no") and (drug == "no"):
        bronze_price = bronze * smoking,
        silver_price = silver * smoking
        gold_price = gold * smoking
        platinum_price = platinum * smoking
    
    elif (age >= 18 and age < 31) and (smoke == "yes") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * smoking) * (drinking)
        silver_price = (silver * smoking) * (drinking)
        gold_price = (gold * smoking) * (drinking)
        platinum_price = (platinum * smoking) * (drinking)

        
    elif (age >= 18 and age < 31) and (smoke == "yes") and (alcohol == "no") and (drug == "yes"):
        bronze_price = (bronze * smoking) * (druging)
        silver_price = (silver * smoking) * (druging)
        gold_price = (gold * smoking) * (druging)
        platinum_price = (platinum * smoking) * (druging)
    
    elif (age >= 18 and age < 31) and (smoke == "yes") and (alcohol == "yes") and (drug == "yes"):
        bronze_price = (bronze * smoking) * (drinking) * (druging) 
        silver_price = (silver * smoking) * (drinking) * (druging)
        gold_price = (gold * smoking) * (drinking) * (druging)
        platinum_price = (platinum * smoking) * (drinking) * (druging)


    elif (age >= 18 and age < 31) and (smoke == "no") and (alcohol == "yes") and (drug == "no"):
        bronze_price = bronze * drinking
        silver_price = silver * drinking
        gold_price = gold * drinking
        platinum_price = platinum * drinking
    
   
   
    # ages 31 - 40 
    
    elif (age >= 31 and age < 41) and (smoke == "no") and (alcohol == "no") and (drug == "no"):
        bronze_price = bronze * age_3141
        silver_price = silver * age_3141
        gold_price = gold * age_3141
        platinum_price = platinum * age_3141
    
    elif (age >= 31 and age < 41) and (smoke == "yes") and (alcohol == "no") and (drug == "no"):
        bronze_price = (bronze * age_3141) * smoking
        silver_price = (silver * age_3141) * smoking
        gold_price = (gold * age_3141) * smoking
        platinum_price = (platinum * age_3141) * smoking
    
    elif (age >= 31 and age < 41) and (smoke == "yes") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_3141) *(smoking) * (drinking)
        silver_price = (silver * age_3141) * (smoking) * (drinking)
        gold_price = (gold * age_3141) * (smoking) * (drinking)
        platinum_price = (platinum * age_3141) * (smoking) * (drinking)
    elif (age >= 31 and age < 41) and (smoke == "yes") and (alcohol == "no") and (drug == "yes"):
        bronze_price = (bronze * age_3141) * (smoking) * (druging)
        silver_price = (silver * age_3141) * (smoking) * (druging)
        gold_price = (gold * age_3141) * (smoking) * (druging)
        platinum_price = (platinum * age_3141) * (smoking) * (druging)

    elif (age >= 31 and age < 41) and (smoke == "yes") and (alcohol == "yes") and (drug == "yes"):
        bronze_price = (bronze * age_3141) * (smoking) * (drinking) * (druging) 
        silver_price = (silver * age_3141) * (smoking) * (drinking) * (druging)
        gold_price = (gold * age_3141) * (smoking) * (drinking) * (druging)
        platinum_price = (platinum * age_3141) * (smoking) * (drinking) * (druging)    
    
    elif (age >= 31 and age < 41) and (smoke == "no") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_3141) * (drinking)
        silver_price = (silver * age_3141) * (drinking)
        gold_price = (gold * age_3141) * (drinking)
        platinum_price = (platinum * age_3141) * (drinking)

    # ages 41 - 50
    
    elif (age >= 41 and age < 51) and (smoke == "no") and (alcohol == "no") and (drug == "no"):
        bronze_price = bronze * age_4150
        silver_price = silver * age_4150
        gold_price = gold * age_4150
        platinum_price = platinum * age_4150
    
    elif (age >= 41 and age < 51) and (smoke == "yes") and (alcohol == "no") and (drug == "no"):
        bronze_price = (bronze * age_4150) * smoking
        silver_price = (silver * age_4150) * smoking
        gold_price = (gold * age_41501) * smoking
        platinum_price = (platinum * age_4150) * smoking
    
    elif (age >= 41 and age < 51) and (smoke == "yes") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_4150) *(smoking) * (drinking)
        silver_price = (silver * age_4150) * (smoking) * (drinking)
        gold_price = (gold * age_4150) * (smoking) * (drinking)
        platinum_price = (platinum * age_4150) * (smoking) * (drinking)
        
    elif (age >= 41 and age < 51) and (smoke == "yes") and (alcohol == "no") and (drug == "yes"):
        bronze_price = (bronze * age_4150) * (smoking) * (druging)
        silver_price = (silver * age_4150) * (smoking) * (druging)
        gold_price = (gold * age_4150) * (smoking) * (druging)
        platinum_price = (platinum * age_4150) * (smoking) * (druging)

    elif (age >= 41 and age < 51) and (smoke == "yes") and (alcohol == "yes") and (drug == "yes"):
        bronze_price = (bronze * age_4150) * (smoking) * (drinking) * (druging) 
        silver_price = (silver * age_4150) * (smoking) * (drinking) * (druging)
        gold_price = (gold * age_4150) * (smoking) * (drinking) * (druging)
        platinum_price = (platinum * age_4150) * (smoking) * (drinking) * (druging)
        
    elif (age >= 41 and age < 51) and (smoke == "no") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_4150) * (drinking)
        silver_price = (silver * age_4150) * (drinking)
        gold_price = (gold * age_4150) * (drinking)
        platinum_price = (platinum * age_4150) * (drinking)
    
        
    # ages 51 - 64
    
    elif (age >= 51 and age < 65) and (smoke == "no") and (alcohol == "no") and (drug == "no"):
        bronze_price = bronze * age_5164
        silver_price = silver * age_5164
        gold_price = gold * age_5164
        platinum_price = platinum * age_5164
    
    elif (age >= 51 and age < 65) and (smoke == "yes") and (alcohol == "no") and (drug == "no"):
        bronze_price = (bronze * age_5164) * smoking
        silver_price = (silver * age_5164) * smoking
        gold_price = (gold * age_5164) * smoking
        platinum_price = (platinum * age_5164) * smoking
    
    elif (age >= 51 and age < 65) and (smoke == "yes") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_5164) *(smoking) * (drinking)
        silver_price = (silver * age_5164) * (smoking) * (drinking)
        gold_price = (gold * age_5164) * (smoking) * (drinking)
        platinum_price = (platinum * age_5164) * (smoking) * (drinking)

    elif (age >= 51 and age < 65) and (smoke == "yes") and (alcohol == "no") and (drug == "yes"):
        bronze_price = (bronze * age_5164) * (smoking) * (druging)
        silver_price = (silver * age_5164) * (smoking) * (druging)
        gold_price = (gold * age_5164) * (smoking) * (druging)
        platinum_price = (platinum * age_5164) * (smoking) * (druging)

    elif (age >= 51 and age < 65) and (smoke == "yes") and (alcohol == "yes") and (drug == "yes"):
        bronze_price = (bronze * age_5164) * (smoking) * (drinking) * (druging) 
        silver_price = (silver * age_5164) * (smoking) * (drinking) * (druging)
        gold_price = (gold * age_5164) * (smoking) * (drinking) * (druging)
        platinum_price = (platinum * age_5164) * (smoking) * (drinking) * (druging)

    elif (age >= 51 and age < 65) and (smoke == "no") and (alcohol == "yes") and (drug == "no"):
        bronze_price = (bronze * age_5164) * (drinking)
        silver_price = (silver * age_5164) * (drinking)
        gold_price = (gold * age_5164) * (drinking)
        platinum_price = (platinum * age_5164) * (drinking)
    
    else:
        raise Exception ("did not match any if statement")
    
    
    
    
    return bronze_price,silver_price,gold_price,platinum_price





### Intents Handlers ###

def recommend_insurance(intent_request):
    """
    Performs dialog management and fulfillment for recommending an insurance.
    """
    
    first_name = get_slots(intent_request)["firstName"]
    last_name = get_slots(intent_request)["lastname"]
    smoke = get_slots(intent_request)["smoke"]   
    age = get_slots(intent_request)["age"]
    Income = get_slots(intent_request)["Income"]
    alcohol = get_slots(intent_request)["alcohol"]
    drug = get_slots(intent_request)["drug"]
    
    
    #Parse into integers
    age = parse_int(age)
    Income= parse_int(Income)
    
   
    
    
    # Gets the invocation source, for Lex dialogs "DialogCodeHook" or "invocationSource" is expected.
    source = intent_request["invocationSource"]
    
    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(age, Income,  intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
            
        # Validates user's input using the validate_data function
        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))

    # Return a message with conversion's result.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for your information here is the prices for your insurance options;
            {}
            """.format(
                get_price(age, smoke, alcohol, drug)
                
  
            
            
            
            
            ),
        },
    )



### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "Insurance_questions":
        return recommend_insurance(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")

s3 = boto3.client('s3')
    
### Main Handler ###
def lambda_handler(event, context):
     
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    
    s3 = boto3.resource('s3')
    s3object = s3.Object('insurance4life', 'sample.json')
    my_dict = {"bronzeprice": 'bronze_price',"silverprice":"silver_price","goldprice": "gold_price", "platinumprice":"platinum_price"}
    s3object.put(
    Body=(bytes(json.dumps(my_dict).encode('UTF-8')))
    )
    
    print (event)
    return dispatch(event)
    