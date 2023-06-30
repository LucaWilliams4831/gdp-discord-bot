import discord
import asyncio
from discord.ext import tasks
import requests
import httpx
from bs4 import BeautifulSoup
import datetime
from datetime import date
import math
# Your Discord token here
TOKEN = ''

# Your channel ID here
CHANNEL_ID = 1124045974982115348

intents = discord.Intents.default()  # Create a new instance of `Intents` class.

# Specify the intent(s) that your bot needs.
intents.members = True  # Enable member-related events.

client = discord.Client(intents=intents) 

# Event triggered when the bot connects to Discord
@client.event
async def on_ready():
    print('Bot connected to Discord successfully')
    # Start the loop after the bot has connected
    await send_hello_message.start()

# Function to send the "hello" message
def updateDebtClock():
    CAGR = 0.0794
    initialDebt = 30928910000000
    perSecondGrowthRate = math.pow(1 + CAGR, 1 / (365 * 24 * 60 * 60)) - 1
    currentTime = datetime.datetime.now()
    startOf2023 = datetime.datetime(2023, 1, 1, 0, 0, 0)
    secondsSince2023 = (currentTime - startOf2023).total_seconds()
    currentDebt = initialDebt * math.pow(1 + perSecondGrowthRate, secondsSince2023)
    # set the timezone you want to display

    return currentDebt
async def send_hello():

    channel = client.get_channel(CHANNEL_ID)
    url = "https://tradingeconomics.com/matrix"
    china_text = ""

    headers = {"User-Agent": "Mozilla/5.0"}
    response = httpx.get(url, headers=headers)
    usdebt = format(updateDebtClock()/10e11, ',.1f')

    send_text = ""
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the HTML response content
       soup = BeautifulSoup(response.text, "html.parser")
    
        # Find the table tag
       table = soup.find("table")
        
        # Create an empty array to store table data
       table_data = []
        
        # Find all the rows (tr tags) within the table
       rows = table.find_all("tr")
        
        # Iterate over each row and extract the data
       for row in rows:
            # Extract the text content inside each row (td tags)
           row_data = [cell.get_text(strip=True) for cell in row.find_all("td")]
           if len(row_data) > 1:
              if row_data[0] == "United States":
                 send_text += "US National Debt: \t\t" + usdebt + "T\n"
                 send_text += "US GDP:\t\t\t\t\t\t" + format((float(row_data[1])/1e3), ',.2f') + "T\n"
                 send_text += "US Interest Rate:  \t\t" + row_data[4] + "%\n"
                 send_text += "US Inflation Rate: \t\t" + row_data[5] + "%\n"
                 send_text += "\nDebt/GDP\n"
                 send_text += "USA:     \t\t\t\t\t\t" + row_data[8] + "%\n"

              if row_data[0] == "Japan":
                 send_text += "Japan: \t\t\t\t\t\t" + row_data[8] + "%\n"
              if row_data[0] == "United Kingdom":
                 send_text += "UK:\t\t\t\t\t\t\t\t" + row_data[8] + "%\n"
              if row_data[0] == "China":
                 china_text += "China:      \t\t\t\t\t\t" + row_data[8] + "%\n"      # Add the row data to the table_data array
           
           table_data.append(row_data)
        
        # Print the table data
       print(send_text)
       send_text += china_text
    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)

    if channel is not None:
        await channel.send(send_text)
    else:
        print("Channel not found")
# Background task to send the "hello" message every hour
@tasks.loop(hours=1)
async def send_hello_message():
    await send_hello()

# Run the Discord bot
client.run(TOKEN)
