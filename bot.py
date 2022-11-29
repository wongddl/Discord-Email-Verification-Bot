import discord
from discord.ext import commands
from discord.ui import Button, View
from dhooks import Embed
from discord.utils import get

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import HtmlContent, Mail
from googleapiclient.discovery import build
from google.oauth2 import service_account

import random
import asyncio


SAMPLE_SPREADSHEET_ID = '1wXUYH7Wog4L0PNIAQhyVRcQXioPEbyDai-bUerTnf6c'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

DISCORD_TOKEN = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B1:B1').execute().get('values'))[3:-3]
SENDGRID_API_KEY = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B2:B2').execute().get('values',[]))[3:-3]
SENDGRID_EMAIL = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B3:B3').execute().get('values',[]))[3:-3]

id_custom_emoji = int(str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B6:B6').execute().get('values'))[3:-3])
id_channel = int(str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B7:B7').execute().get('values',[]))[3:-3])
id_msg = int(str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B8:B8').execute().get('values',[]))[3:-3])
id_guild = int(str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B9:B9').execute().get('values'))[3:-3])
id_role_verified = int(str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B10:B10').execute().get('values',[]))[3:-3])
emaildomain = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B12:B12').execute().get('values',[]))[3:-3]
server_name = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet2!B13:B13').execute().get('values',[]))[3:-3]


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=discord.Intents.all())


########### def ############
def append_user(registration_data):
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sheet1!A3', 
                    valueInputOption='USER_ENTERED', body={'values':registration_data}).execute()

def append_email(datanum,message_content):
    service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!B{datanum}', 
                    valueInputOption='USER_ENTERED', body={'values':[[message_content]]}).execute() 

def append_code(datanum,random_code):
    service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!C{datanum}', 
                    valueInputOption='USER_ENTERED', body={'values':[[random_code]]}).execute() 

def append_verified(datanum):
    verified = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!D{datanum}', 
                    valueInputOption='USER_ENTERED', body={'values':[['1']]}).execute() 

def get_author():
    data_request = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet1!A3:A100').execute().get('values',[])
    return data_request

def get_code():
    data_request_code = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet1!C3:C100').execute().get('values',[])
    return data_request_code

def get_email():
    data_request_email = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range='Sheet1!B3:B100').execute().get('values',[])
    return data_request_email

def get_verify(datanum):
    verify_request_code = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range=f'Sheet1!D{datanum}:D{datanum}').execute().get('values',[])
    return verify_request_code

def embed_welcome():
    welcome_message=discord.Embed(title=f"Welcome to {server_name}", description=f"""
    For Students of *emaildomain* only!!

    __Steps:__
    1.) Click the "<:checkmarkpng5:1047009141102743563>" reaction below.
    2.) VERIFICATION BOT will automatically respond and DM you.
    3.) Type in your valid **email address**. 
    4.) A **unique code** to be sent to your email.
    5.) Reply the given **code**.
    6.) You will receive access through <@&{id_role_verified}> role!
        """, color=0xe4ce31)
    welcome_message.set_image(url='https://media.discordapp.net/attachments/1032348940592496645/1046996671004954654/unknown.png') #WELCOME
    welcome_message.set_thumbnail(url='https://media.discordapp.net/attachments/1032348940592496645/1047008192732868628/unknown.png') #S (logo)
    welcome_message.set_footer(text="Verification process is fully automated. Contact Moderators if verification process doesn't work.")
    return welcome_message

def embed_input_email():
        embedmsg=discord.Embed(title="Type in your valid email address", description="""
Example:
`sample1@gmail.com`
    """, color=0xffffff)
        embedmsg.set_footer(text="This message will delete in 30 seconds")

        return embedmsg

def embed_input_code():
        embedmsg=discord.Embed(title="Type in your Verification Code", description="""
Example:
`987654`
    """, color=0xffffff)
        embedmsg.set_footer(text="This message will delete in 30 seconds.")

        return embedmsg

def embed_verified():
    verified_message = discord.Embed(title=f'Welcome to {server_name}', description = f'''
    You are now verified on **{server_name}** discord server.

    To get you started, head over to:
    <#1047021021846315104> and chat with other members!
    ''', color = 0xe4ce31)
    verified_message.set_image(url='https://cdn.discordapp.com/attachments/1032348940592496645/1046990279665782824/unknown.png') #VERIFIED
    verified_message.set_thumbnail(url='https://media.discordapp.net/attachments/1032348940592496645/1047008192732868628/unknown.png') #S (logo)
    verified_message.set_footer(text="Verification process is fully automated. Contact Moderators if verification process doesn't work.",)
    return verified_message

def embed_sent():
    email_message = discord.Embed(title='📨 Email Sent',description='**Verification code** has been sent to your Email Address.', color = 0xe4ce31)
    email_message.set_footer(text="Check your spam folders if the email is not at your inbox.")
    return email_message

def embed_sent_button():
    emailsent = Button(label="📧 Gmail", url='https://gmail.com', style=discord.ButtonStyle.grey)
    view = View()
    view.add_item(emailsent)
    return view

def embed_invalid_input():
    embed_invalid_input = discord.Embed(title='Invalid Input', color = 0xFF0000)
    return embed_invalid_input

def embed_invalid_code():
    embed_invalid_code = discord.Embed(title='Invalid Code', color = 0xFF0000)
    return embed_invalid_code

def emailmessage(message_content,random_code):
    emailmessage = Mail(
                    from_email=(SENDGRID_EMAIL),
                    to_emails=message_content,
                    subject='Verify your server email',
                    html_content= HtmlContent(str('Your Verification Code is: {}').format(random_code,)))
    return emailmessage

##### DISCORD ######

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    try:
        synced = await client.tree.sync()
        print(f'synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Verifying Emails~!"))
    channel = client.get_channel(id_channel)                                                                #admission channel
    msg = await channel.fetch_message(id_msg)                                                               #admission message
    emoji = client.get_emoji(id_custom_emoji)                                                               #check emoji
    await msg.clear_reactions()                                                                             #clear reactions on reset
    await msg.add_reaction(emoji)                                                                           #add reaction on reset
    print('Reaction restarted - Successfully')

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id                                                                         #get message id
    user = client.get_user(payload.user_id)                                                                 #get the user id of who pressed

    if user == client.user:
        return
    else:
      if message_id == id_msg:

        emoji = client.get_emoji(id_custom_emoji)                                                           #get emoji id
        channel = client.get_channel(id_channel)                                                            #get message's channel id
        message = await channel.fetch_message(payload.message_id)
        discord_user = str(payload.user_id)
        guild_id = str(payload.guild_id)
        member = discord.utils.find(lambda m : m.id ==payload.user_id,channel.guild.members)
        registration_data = [[discord_user,'email','code','0']]                                             #googlesheets [['A3','B3','C3','D4']]

        await channel.send('Verification Request received', delete_after = 3)
        await asyncio.sleep(1)
        await message.remove_reaction(emoji, user)
        
        
        if payload.guild_id:
            if discord_user in (item for sublist in get_author() for item in sublist):
                datanum = get_author().index([f'{str(payload.user_id)}'])+3
                if get_verify(datanum) == [['0']]:
                    await member.send('You are already on the verification process.')
                else:
                    await member.send(f'You have already verified on {server_name} Server.',delete_after=5)
            else:
                    append_user(registration_data)
                    await member.send(embed=embed_welcome())
                    await member.send(embed=embed_input_email(),delete_after=30)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_content = message.content.strip()
    print(message.author,':',message_content)

    
    guild = discord.utils.find(lambda g: g.id == id_guild, client.guilds)
    
    role = get(guild.roles, id=id_role_verified)
    author = guild.get_member(message.author.id)
    if str(message.author.id) in (item for sublist in get_author() for item in sublist):                    # - >check user if in sheets database
        datanum = get_author().index([f'{str(message.author.id)}'])+3                                       #To get Author_ID's sheet cell number (replace '3' if you have different header on ur googlesheets)
        author_user = str(service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                    range=f'Sheet1!A{datanum}:A{datanum}').execute().get('values',[]))[3:-3]
        if not message_content in (item for sublist in get_email() for item in sublist):                    # - >check user message(email or code) in db
            
            if get_verify(datanum) == [['0']]:                                                              # - >check if user is verified ('1' = verified, '0' = not verified)
                if message_content[-(int(len(emaildomain))):] == emaildomain:                               # - >check if messageconent(email) is same as email domain
                    random_code = random.randint(100000, 999999)                                            #code generation
                    append_email(datanum,message_content)
                    append_code(datanum,random_code)
                    try:
                        sg = SendGridAPIClient(SENDGRID_API_KEY)
                        response = sg.send(emailmessage(message_content,random_code))                       #send email
                        print('VERIFICATION CODE SENT')
                        await message.channel.send(embed=embed_sent(),view = embed_sent_button())
                        await message.channel.send(embed=embed_input_code(),delete_after=30)
                    except:
                        await message.channel.send(embed=discord.Embed(description='Email failed to send', color = 0xFF0000), delete_after = 5)
                elif message_content.isnumeric():
                    try:
                            datanum_code = get_code().index([f'{str(message_content)}'])+3                  #To get the CODE's sheet cell number (replace '3' if you have different header on ur googlesheets)
                            if datanum == datanum_code:
                                append_verified(datanum)
                                await message.channel.send(embed=embed_verified())
                                await author.add_roles(role)
                            else:
                                await message.channel.send(embed=embed_invalid_code(),delete_after = 5)
                    except:
                        await message.channel.send(embed=embed_invalid_code(),delete_after = 5)
                elif '@' in message_content:
                    await message.channel.send(embed=embed_invalid_input(),delete_after = 5)
        elif message_content in (item for sublist in get_email() for item in sublist):
            if str(message.author.id) == author_user:
                await message.channel.send(embed=discord.Embed(description='Email has been sent already, kindly check your inbox. Contact moderators if there is a problem.', color = 0xFF0000))
        else:
            await message.channel.send(embed=embed_invalid_input(),delete_after = 5)
    else:
        await message.channel.send(embed=discord.Embed(description='You have not received a verification process from the server yet.', color = 0xFF0000), delete_after = 5)



client.run(DISCORD_TOKEN)