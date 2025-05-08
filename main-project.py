'''
Agent 1 (Leijie) is responsible for analyzing each image inputed by the user into strings to be stored in a txt file
called "compiled_closet". The AI will sort the items by **tops, bottoms, shoes and accessories** as well as style
and weather compatibility.

Agent 2 (Elisa) will take as input certain styles that the user likes and sort through the closet to find 
and output clothing that fit that description as "style_clothing". This data will be treated by Agent 3.

Agent 3 (Angeline) is responsible for taking both outputs from Agent 2 and 4 into CONSIDERATION and outputs 3
combinations of clothing that would suit both the event and the style the user is looking for. The user will have 
the option of saving any of the combinations they like as "saved_outfit_x".   
    If none of the combinations are to the user's taste, the AI will prompt the user for what could have been
    missing in the combinations. The output will then be sent to Agent 4 to check if the closet has anything similar
    in store and rerun the program with the added outfit taken into consideration.


Agent 4 (Chanelle) will take as input a description of an event the user wants to go to. Using this description, it
will search through "complied_closet" and find and output clothing that would fit the event. The output will be saved
as "event_clothing". The data will be treated by Agent 3.

    The bot would also accept input from Agent 3 if the user suggests an item of clothing that they wouldve thought
    fit the combinations better. However, this involves sorting through the closet and making sure that the item of
    clothing is in the closet in the first place

And if you're wondering why Annamaria's name isn't attached to any Agent, well, guess who gets to compile all
of this. 
'''
#%%
#imports
import base64 #used to encode the images
import openai 
from langchain.chat_models import ChatOpenAI

#initializing AI for llm
llm = ChatOpenAI(
    openai_api_key="[API KEY]"
,
    model_name="gpt-4.1",      
    temperature=0              
)

#initializing for openai
openai.api_key = "[API KEY]"


#stores the outfit paths
imagePathlst = [
   r"outfits/outfit1.jpg",
   r"outfits/outfit2.jpg",
   r"outfits/outfit3.jpg",
]
clothTypeTagsLst = ["Top", "Bottom", "Dress", "One-Piece", "Outerwear", "Footwear", "Accessorie"]
clothEventTagsLst = ["Work", "Formal", "Lounge", "Outdoor Activities", "Fitness", "Beach", "Party", "School", "Business"]
clothWeatherTagsLst = [ "Rainy Weather", "Cold Weather", "Hot Weather"]

binaryFileNameLst = []
analyzedclotheLst = []

def image_encoded():
    fileCount = 0
    
    for imgPath in imagePathlst: #for each image path in imagePathlst
        fileCount += 1
        try:
            with open(imgPath, "rb") as img_file: #read file at the end of path in binary
                encoded_string = base64.b64encode(img_file.read()).decode("utf-8") #encode file in utf-8 and saves it to variable
                
        except FileNotFoundError:
            print("Please verify your image path.") #if there isnt a file at the end of path, print..

        binaryFileName = f"clothe {fileCount}.b64.txt" #references the current outfit with index and appends to binaryFileNameLst
        binaryFileNameLst.append(binaryFileName)
        try:
            with open(binaryFileName, "w", encoding="utf-8") as output_file: #opens file using write mode and writes the encoded text
                output_file.write(encoded_string)
                print(f"Image {fileCount} is added to virtual closet file")
        except FileNotFoundError:
            print("Binary file doesn't exist.") 
        print(f"encoding code")
        
image_encoded()

def ai_ageant_cloth_analyse():
    index = 0
    for binaryPath in binaryFileNameLst: #for each file
        index += 1
        with open(binaryPath, "r", encoding="utf-8") as analyse_file: #reads encoded file using utf-8
            content = analyse_file.read()

        print(f"analyzing image {index} from {binaryPath}... \n")

        response = openai.chat.completions.create( #chatmodels/generate model reply/based off of this prompt
            model="gpt-4.1",
            temperature= 0.5,
            messages=[
                {
                    "role": "user", #person talking to model
                    "content": [ #type of content the model will be taking as input, there are two: text and image_url
                        {
                            "type": "text",
                            "text": f"""
                                You are a fashion expert. Analyze EACH clothing piece and accessory in the image using the following criteria
                                PLEASE BE CAREFUL! the image may be an outfit multiple different piece, plz annalyze the pieces indenpendently from
                                each other when giving the tags. Each item must have its own tags:
        
                                - use ONE event tag to identifies item using following categories: {clothEventTagsLst}
                                - Assign the item to ONE of those type of tags: {clothTypeTagsLst}
                                - Identify the ONE main color
                                - Assign the item to ONE of those weather types: {clothWeatherTagsLst}

                                Format your reply like:
                                item description,color,eventtag,weather tag,item type tag
                                
                                no need to numerote it 
                                and don't do greeting just the data
                                no space between the data outputs
                                """
                        },
                        {
                            "type": "image_url", #also input encoded image as content for the bot
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{content}"
                            }
                        }
                    ]
                }
            ],
        )
        result = response.choices[0].message.content #gives chatGPTs response

        analyzedclotheName = f"analyzed clothe{index}.txt" #gives name to file according to index so they match and append it to the list
        analyzedclotheLst.append(analyzedclotheName)
        with open(analyzedclotheName,"w") as virtualCloset: #create file for each analyzed outfit and write data in it
            virtualCloset.write(result)

ai_ageant_cloth_analyse()

def clothe_data_management():  
    virtualClosetDict = {}  
    for analyzedcloth in analyzedclotheLst:
        with open(analyzedcloth, "r" ) as infile: 
            analyzedclothesLines = infile.readlines() #read the analysis from the bot

            for line in analyzedclothesLines: #formating to delete unecessary characters
                piececlothinglst = line.strip(" "+"\n").split(",")
                pieceName = piececlothinglst[0] #sets name of clothing (1 value in the key tags) as key
                criterionlst = piececlothinglst[1:] #and list of tags starting as the second tags and value
                virtualClosetDict.update({pieceName: criterionlst})

    with open("vituralClosetDict.txt","w") as textfile:
        textfile.write(str(virtualClosetDict).strip("'"))
    return virtualClosetDict

clothe_data_management()

virtualClosetDict = clothe_data_management()
#==========================================================

#-----------------------

    #AGENT 4 [CHANI]


# This one works
#input for weather_giver()
situation = input('Where will this event take place? Give the country, the city and the area. Ex: Canada, montreal, kirkland')
date = input('What is the date of your event? Give the year, month and day of the event.')
time = input(f'''At what time is this event happening? Give the time interval of your event in the 24 hours clock system,no minutes needed. Ex: 12 to 18''')


#SOME OF THE DETAILS HERE ARE HARDCODED VVV
def weather_giver():
    #location = 'Canada,montreal,kirkland' #
    #date = '2025,december,23' #
    #time = '12 to 16' #
    
    prompt = f""" You are a weather expert and you analyse the {situation}, the {time} and the {date}
    that the user inputs. The date will be a time interval using the 24 hours system. You must output the tag from the list that best matches your analysis of
    the user's input.
    list: {clothWeatherTagsLst}
    your reply: a tag without greeting or numeroting just a simple string and no spaces before and after the string.
    """
    response = llm.invoke(prompt).content
    return(response)


weather_giver()

def weather_clothes():
    closet = virtualClosetDict
    clot = []
    for i in closet:
        tagslst = closet[i]
        if tagslst[2].strip() == weather_giver():
            clot.append(i)
    return clot
weather_clothes()


def style_giver():
    prompt = f""" You are an expert stylist and you will analyse the {situation} that the user inputs. You must then
    find the tag in the list that matches the most the situation.
    list: {clothEventTagsLst}
    your reply: one tag without greeting or numeroting just a simple string and no spaces before and after the string.
    """
    response = llm.invoke(prompt).content
    return(response)
style_giver()

def style_clothes():
    closetS = virtualClosetDict
    clotS = []
    for i in closetS:
        tagslst = closetS[i]
        if tagslst[1].strip() == style_giver():
            clotS.append(i)
    return clotS
style_clothes()

def event_output():
    lst_style = style_clothes()
    lst_unique = weather_clothes()
    for i in lst_style:
        if i not in lst_unique:
            lst_unique.append(i)
    return lst_unique


#-----------------------
    #AGENT 2 [ELISA]

file_contents = event_output()


def style_reccommender(file_contents, user_Style_input):
    chatbot_prompt2 = f""" O Great Stylist! You are now in charge of filtering the user's closet based on their aesthetic(s) named in.
    You will have to read through all the different pieces found in "file_contents" and filter out pieces that do not match with the user's aesthetic and keep the ones that do. Take in account color when matching the pieces with a style
    For example, if the user has the "decora" style in their "selected_styles, keep colorful items like a peachy orange cardigan, but filter out bland and monotone items like black baumwolle pants. Look online to get inspiration for the the pieces of clothing matching with "selected_styles" list
    Do NOT invent words that are not from either "file_contents" or "selected_styles".
    items of clothing: {file_contents}
    list of aesthetics or fashion styles to respect: {user_Style_input}
    Your reply should be (the pieces of clothings that MATCH with the user's aesthetic are appended to the stylized_closet list) : stylized_closet = ["item1","item2","item3",...]
    you must output a minimum of 1 item"""
    response = llm.invoke(chatbot_prompt2).content
    return response

#For stocking the preferences of the user
selected_styles = []
last_style = None



while True:
    user_Style_input = input("give the style that you want to try?")
    user_option_input = input("write proceed if you are satisfied with your choices \n"
                             "write continue if you want to add one more style")
    if user_option_input.lower().strip() == "proceed":
#since we can't print a fct to get our wanted results, but we can't use return: 
        filtered = style_reccommender(file_contents, user_Style_input)
#This is a list, for Angeline's code
        print(filtered)
        break

#These following checks are to make sure can't break
    if user_option_input.lower().strip() == "continue":
        if last_style:
            if last_style in user_Style_input:
                print("Chatbot: You've already added this aesthetic.")
            else:
                selected_styles.append(last_style)
                print(f"Chatbot: Added “{last_style}” to your chosen styles:", selected_styles)
                print(f"""Chatbot: You can always type "proceed" to filter out your closet if you are satisfied with your style selection!""")
            last_style = None
#Remember, continue runs the code from while Trueyes

#following helps to not accidentally add an aesthetic you said "no" to
        response = "Chatbot: Good Choice"
        continue

    #response = style_first(user_input)
    print("Chatbot: ", response)


#-----------------------


#-----------------------

#   AGENT 3 [ANGELINE

# reads files from 3 other agents !guys can you make sure that each of your agents ouputs a file that mine can read?
closet = clothe_data_management()
style = selected_styles
event = situation
reason = None


# gives the agent its role. it takes the closet, style and event from the 3 other agents as inputs
def Agent_3(closet, style, event, reason):
    prompt =  f"""Hello, You are an expert of compromise, creativity, comparison and comparison, and use your skills in the domain of fashion to suggest outfits
    to your client based on their situation. You have access to the closet which has been analyzed for you by Agent 1. Agent 2 will provide
    you with the stylistic preferences of your client, and Agent 4 will provide you with keywords describing the client's needs. With your
    incredible artistic and problem-solving talent, you must scan the closet for the pieces which best correspond to the information given
    to you by Agent 2 and Agent 4. As a fashion designer, you must then make combinations with them; combine tops, bottoms, and other pieces
    in a way that is logical and fashionable. Finally, you will give these combinations as suggestions to the client. Give the client at least
    3 different combinations, with the respective names of 'combination one', 'combination two', and 'combination three'. Specify to the client 'combination one' as the one which matched the requirements the most closely as "most recommended".
    Be concise, and avoid finishing with unnecessary comments.
    closet: {closet}
    stylistic preferences: {style}
    keywords describing needs: {event}
    PS: you will reflect with {reason} in mind if ever the client is not satisfied. If there is no client complaint skip this step.
    Your combinations:
    """
    response = llm.invoke(prompt).content
    print(response)
    return response

Agent_3(closet, style, event, reason)


# the following code will save the outfit if the client liked it, or try again if the client did not.
clientopinion = input('Do you like the proposed outfit? respond with either: Yes or No')

# i imagine there being a file for saved outfits. i think this would be useful for the style agent (to be informed of what the user likes)
# this code saves the outfit in a file named 'saved_outfits.txt' under a name the user chooses 

if clientopinion == 'Yes':
    while clientopinion == 'Yes':
        accepted_answers = ['One','Two', 'Three']
        newoutfit = input('which combination would you like to save? Please type either: One, Two, or Three')
# error handling if user does not type One, Two, or Three
        if newoutfit not in accepted_answers:
            while newoutfit not in accepted_answers:
                newoutfit = input('Sorry, that combination does not exist. Please type either: One, Two, or Three')
# this code splits the file of the outfits into a list of 3 outfits. this is so the chosen outfit to save can be accessed.
        chosenoutfit = ""
        with open("new_outfits.txt", "r") as file: 
            newoutfits = file.read()
            newoutfits = newoutfits.split('Combination')
            for i in newoutfits:
                if newoutfit in i:
                    chosenoutfit = i

# this code will save the chosen outfit under a name the client chooses in the file 'saved outfits'
        newoutfitname = input('what would you like to name your saved outfit?')
        f = open('saved_outfits.txt','a')
        f.write(f'{newoutfitname} : {chosenoutfit}' )
        f.close()    
        print(f'Your new stunning outfit has been successfully saved as {newoutfitname}')
# this code allows the user the option to save an additional outfit
        clientopinion = input('Would you like to save another outfit? Please respond with either : Yes or No')
    if clientopinion == 'No':
        print('Okay, have a wonderful day you fashion icon. See you next time!')
        

# this code takes the client's feedback into consideration by sending it to the Event agent so it gets added as new needs in the event file, then restarts the program. 
elif clientopinion == 'No': 
        reason = input('My apologies, I will try to do better next time. What do you want in your outfit that was missing?')
        print('Got it. I\'ll try again with that in mind.')
        Agent_3(closet,style,event,reason)


# error handling if the user does not type yes or no
else: 
    print('Sorry, it seems like something went wrong. Please try again by typing one of the 2 proposed answers.')
# %%
