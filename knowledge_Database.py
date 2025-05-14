import openai #9/22/2023     
import streamlit as st
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import time

### Initialize openai Credentials
openai.api_key = st.secrets['api']
pause_second = int(st.secrets['pause'])
#context = []

def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature, # this is the degree of randomness of the model's output
        )
    #   print(str(response.choices[0].message))
        st.session_state.isOpenAiAPIError = False
        return response.choices[0].message["content"]
    except:
        st.session_state.isOpenAiAPIError = True
        st.session_state.isOpenAiAPIErrorEver = True
        #11/28/2023, debugginh... ok! found the bug: openai.ChatCompletion is deprecated in openai 1.0.0
        #use openai==0.28 to get back to old version openAI API
        return 'There is rate limit for the demo system. Please wait...\n(這是展示用版本，有流量限制，請稍後按<restart>鍵。。。若使用上線用版本，則無流量限制。)'
        #return openai.error.RateLimitError()
        ##return response.choices[0].message["content"]
        
def collect_messages(prompt):
    #global context
    #prompt = inp.value_input
    #inp.value = ''
    #context.append({'role':'user', 'content':f"{prompt}"})
    ##st.session_state.messages.append({'role':'user', 'content':f"{prompt}"})    #repeat to append prompt!
    st.session_state.messages2.append({'role':'user','content':f"{prompt}"})    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):    
            #response = get_completion_from_messages(context) 
            response = get_completion_from_messages(st.session_state.messages2)
            #st.write(prompt) #for debugging...
            st.write(response) 
            #time.sleep(20)  # 每次間隔 20 秒，避免超過每分鐘 3 次。5/7/2025 modified!
            #time.sleep(pause_second)  # 每次間隔 20 秒，避免超過每分鐘 3 次。5/7/2025 modified!, 5/15/2025 comment out! I use $5 pay plan
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)            
        st.session_state.messages2.append(message)                    
    #context.append({'role':'assistant', 'content':f"{response}"})

### main_function()
### main_function()
def LoadTA(prompt):
    #global context
    #Change sheet name:
    sheet_name = 'TA'
    sheet_id = '1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc' #1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df=pd.read_csv(url)
    #df
    KB = list(df.loc[0:0,"Knowledge"])
    #st.session_state.messages2.append({'role':'system', 'content':KB[0]})  # accumulate messages 
    st.session_state.messages2 = [{'role':'system', 'content':KB[0]}] # NOT accumulate messages 
    collect_messages('')

def LoadPizzaResturant(prompt):
    sheet_name = 'Pizza' #Change sheet name:
    sheet_id = '1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc' #1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df=pd.read_csv(url)
    #df
    KB = list(df.loc[0:0,"Knowledge"])
    #st.session_state.messages2.append({'role':'system', 'content':KB[0]})  # accumulate messages 
    st.session_state.messages2 = [{'role':'system', 'content':KB[0]}] # NOT accumulate messages     
    collect_messages('')

def LoadTChineseMedicine(prompt):
    sheet_name = 'ChineseMedicine' #Change sheet name:
    sheet_id = '1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc' #1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df=pd.read_csv(url)
    #df
    KB = list(df.loc[0:0,"Knowledge"])
    #st.session_state.messages2.append({'role':'system', 'content':KB[0]})  # accumulate messages 
    st.session_state.messages2 = [{'role':'system', 'content':KB[0]}] # NOT accumulate messages     
    collect_messages('')

def LoadPCBA(prompt):
    sheet_name = 'PCBA' #Change sheet name:
    sheet_id = '1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc' #1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df=pd.read_csv(url)
    #df
    KB = list(df.loc[0:0,"Knowledge"])
    #st.session_state.messages2.append({'role':'system', 'content':KB[0]})  # accumulate messages 
    st.session_state.messages2 = [{'role':'system', 'content':KB[0]}] # NOT accumulate messages     
    collect_messages('')

def LoadAIagent(prompt):
    sheet_name = 'RPAAIagent' #Change sheet name:
    sheet_id = '1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc' #1VBtBQw8-Ch02dVp1p7xTERybGI9DCOVbqywj013Ldsc
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df=pd.read_csv(url)
    #df
    KB = list(df.loc[0:0,"Knowledge"])
    #st.session_state.messages2.append({'role':'system', 'content':KB[0]})  # accumulate messages 
    st.session_state.messages2 = [{'role':'system', 'content':KB[0]}] # NOT accumulate messages     
    collect_messages('')
### old codes
### old codes
def LoadPizzaResturant_old(prompt):
    #global context
    st.session_state.messages2.append({'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""})  # accumulate messages 
    #st.session_state.messages2 = context
    #st.session_state.messages2.append(context) 
    collect_messages('')

def LoadTradingStrategy(prompt):
    #global context
    context = [ {'role':'system', 'content':"""
The following models are trading strategies categorized as Examples-1-Models.

Model 1:
HYPOTHESIS: If a company efficiently uses its assets (equipment, patents etc.) to generate
sales, its stock may outperform the stock of its peers in the future. Denoted by the asset
turnover ratio : sales/assets
IMPLEMENTATION: If company A's asset turnover ratio is better than company B's, stock A
may outperform stock B. However, directly using the input (sales/assets) may put unusually
large long positions (buy) or short positions (sell) on outlier stocks. Rank operator removes
the vast variation of input values by ranking the input and returning float numbers equally
distributed between 0 and 1.
IMPROVEMENT: Find and simulate more fundamental ratios that are factors in determining
a company's performance and financial health.
Datafields: sales, assets
Operators: rank
Expression:
rank(sales / assets)

Model 2:
HYPOTHESIS: If the stock price of a company has increased over the last 2 days, it may
decrease in the future (time series delta of closing price today and closing price 2 days ago).
IMPLEMENTATION: If company A's stock price had increased twice as much as the stock
price of another company B, the prices of both stocks may decrease in the future. In this
reversion example, stock A may not fall double stock B, though it may fall more than stock B
(rank operator).
IMPROVEMENT: Can different neutralizations and decay settings improve this signal?
Under what neutralization would a reversion idea work best?
Datafields: close
Operators: rank, ts_delta
Expression:
rank(-ts_delta(close, 2))

Model 3:
HYPOTHESIS: If today's stock price is higher than the geometric mean price of the week
[time series product of price over 5 days raised to power (1/5)], then the stock price may fall
in the future.
IMPLEMENTATION: Directly using the input (close-ts_product(close,5)^0.2) may put
unusually large long positions (buy) or short positions (sell) on outlier stocks. Rank operator
removes the vast variation of input values by ranking the input and returning float numbers
equally distributed between 0 and 1.
IMPROVEMENT: How do you handle outlier values? Under what neutralization would a
reversion idea work best?
Datafields: close
Operators: ts_product
Expression:
ts_product(close, 5) ^ 0.2 - close
"""} ]  # accumulate messages 
    st.session_state.messages2 = context
    collect_messages('')

def LoadTChineseMedicine_old(prompt):
    #global context
    context = [ {'role':'system', 'content':"""
你是一個中醫的客服機器人，聆聽客戶的問題，並且依據所提供的中醫客服資料庫，來自動回答客戶的的問題。你首先歡迎客戶使用ABC中醫客服機器人，然後聆聽客戶的問題。你要用簡明扼要與友善的方式來回答客戶的問題。以下是所提供的中醫客服資料庫：

中醫客服資料庫包含營業時間、醫師門診時間。

營業時間：
週一	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週二	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週三	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週四	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週五	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週六	上午8:30 - 下午12:00 、下午1:30 - 下午10:00
週日	未營業

陳國揚醫師門診時間：
星期一：夜間
星期二：下午、夜間
星期三(Wednesday)：夜間
星期四：下午、夜間
星期五：夜間
星期六：上午、下午

張維量醫師門診時間：
沒有資料

林佩萱醫師門診時間：
沒有資料
"""} ]  # accumulate messages 
    st.session_state.messages2 = context
    collect_messages('')
