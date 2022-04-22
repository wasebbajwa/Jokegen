import os
import praw 
import pandas as pd 
import re


with open('c:/Users/wbajw/MSDS 458/MSDS 460 Project/VsCode/RedditBot/SecretsNstuff.txt','r') as f:
    lines=f.read()
    secrets=[]
    flines=lines.split('\n')
    flines=[i.split('=', 1)[1] for i in flines]
    
reddit = praw.Reddit(client_id=flines[0],         
                               client_secret=flines[1],      
                               user_agent=flines[2],
                               username=flines[3],
                               password=flines[4])  

jokes=pd.read_csv('C:/Users/wbajw/MSDS 458/MSDS 460 Project/VsCode/GeneratedJokes/Jokes.csv')
hook=jokes.iat[1,1]
punchlines=jokes['Joke'].tolist()

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Get the top 5 values from our subreddit
subreddit = reddit.subreddit('jokes')
for submission in subreddit.hot(limit=1000):
    #print(submission.title)

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        
        if re.search(f'{hook}',submission.title, re.IGNORECASE):
            # Reply to the post
            for i in range(len(punchlines)):
                submission.reply(f'Another punchline is {punchlines[i]}')
                print("Bot replying to : ", submission.title)

            # Store the current id into our list
                posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

