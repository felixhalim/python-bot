import update_reg_user as reg_user
import update_request_bucket as req_bucket
from telegram.ext import Updater, CommandHandler
import os

# Read token from separate file
with open('telegram-bot-token', 'r') as file:
    TOKEN = file.read().replace('\n', '')

NAME = "project-goodall" # Heroku app name
PORT = int(os.environ.get('PORT', '8443')) # Port is given by Heroku

# Local dictionary of registered user
# Local list of request bucket
Local_reg_user = {}
Local_req_bucket_username = []
Local_req_bucket_matric = []

# Function to check if user is registered
def register(update, context, greet=1):
    userData = update.message.from_user
    if(userData.username in Local_reg_user):
        if(greet):
            update.message.reply_text('Your account has been registered, {}'.format(userData.first_name))
        return 1
    else:
        update.message.reply_text('Sorry, your account is not registered. Please sign up on https://forms.gle/B1biAkCSfTRy6BVj8, {}'.format(userData.first_name))
        return 0

# Function to get the matric number
def profile(update, context):
    userData = update.message.from_user
    if(register(update,context,0)):
        uname = userData.username
        counter_help = Local_reg_user[uname][2]
        update.message.reply_text('Hi {}, you have saved {} soul this semester'.format(userData.first_name, counter_help))
     

# Function to get the matric number
def get(update, context):
    if(register(update,context,0)):
        if(len(Local_req_bucket_matric)>1):
            matric = Local_req_bucket_matric.pop() # pop local list
            Local_req_bucket_username.pop() # pop local list
            req_bucket.popMatric() # pop spreadsheet
            update.message.reply_text('Enjoy your food, {}'.format(matric))
        else:
            update.message.reply_text('Sorry, there is no matric currently')
        
# Function to check if user has donated that period
def hasDonated(username):
    if(Local_reg_user[username][3] == "0"): # 3 is the donate bool
        reg_user.setData(username,"bool_donate","1") # change spreadsheet
        Local_reg_user[username][3] = "1" # change local dict
        
        counter_help = Local_reg_user[username][2]
        reg_user.setData(username,"counter_help",str(int(counter_help)+1)) # change spreadsheet
        Local_reg_user[username][2] = str(int(counter_help)+1) # change local dict
        
        return 0
    else:
        return 1

# Function to add user matric to request bucket
def give(update, context):
    userData = update.message.from_user
    if(register(update,context,0)): # user is registered
        if(not hasDonated(userData.username)):
            update.message.reply_text('Thank you for your donation, {}'.format(userData.first_name))
            uname = userData.username
            matric = Local_reg_user[uname][0] # 0 is the matric list
            
            Local_req_bucket_username.append(uname) # add local list
            Local_req_bucket_matric.append(matric) # add local list
            req_bucket.addMatric(uname,matric) # add spreadsheet
        else:
            update.message.reply_text('You have donated today')
    else: # user is not registered
        update.message.reply_text('You have not created an account, {}'.format(userData.first_name))

# Function to sync data from Google Spreadsheet
def sync(update,context):
    update.message.reply_text('Sync Done')
    Local_reg_user.update(reg_user.getLatestData())
    global Local_req_bucket_matric, Local_req_bucket_username 
    Local_req_bucket_matric = req_bucket.getLatestMatric()
    Local_req_bucket_username = req_bucket.getLatestUsername()

def main():    
    Local_reg_user.update(reg_user.getLatestData())
    global Local_req_bucket_matric, Local_req_bucket_username
    Local_req_bucket_matric = req_bucket.getLatestMatric()
    Local_req_bucket_username = req_bucket.getLatestUsername()

    updater = Updater(TOKEN, use_context=True) #Put token

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('register', register))
    dp.add_handler(CommandHandler('get', get))
    dp.add_handler(CommandHandler('give', give))
    dp.add_handler(CommandHandler('sync',sync))
    dp.add_handler(CommandHandler('profile',profile))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()

if __name__ == '__main__':
    main()