import pandas as pd
import requests #Pushshift accesses Reddit via an url so this is needed
import json #JSON manipulation
import csv #To Convert final table into a csv file to save to your machine
import datetime
import dateutil.parser
import os
import argparse
parser = argparse.ArgumentParser(description='Webscraping Reddit To Get Posts and Comments')


parser.add_argument('--sub', default="Jokes",
                    help="Only include the actual subreddit name, no need to include /r/")

parser.add_argument('--before',default='18/10/2020',
                    help='Only grab posts before this date DD/MM/YY Format')
parser.add_argument('--after',default='18/10/2014',
                    help='Only grab posts after this date DD/MM/YY Format')

parser.add_argument('--file',default='train.csv',
                    help='This is the name of the file containing our posts we have scraped')
        
args = parser.parse_args()

#This function builds an Pushshift URL, accesses the webpage and stores JSON data in a nested list
def getPushshiftData(after, before, sub):
    #Build URL
    url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='+str(args.sub)+'&size=400&after='+str(after)+'&before='+str(before)
    #Print URL to show user
    #Request URL
    r = requests.get(url)
    #Load JSON data from webpage into data variable
    data = json.loads(r.text)
    #return the data element which contains all the submissions data
    return data['data']

#This function will be used to extract the key data points from each JSON result
def collectSubData(subm):
    #subData was created at the start to hold all the data which is then added to our global subStats dictionary.
    subData = list() #list to store data points
    title = subm['title']
    try:
        punchline = subm['selftext']
    except KeyError:
        punchline = "NaN"
    url = subm['url']
    #flairs are not always present so we wrap in try/except    
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']

    #Put all data points into a tuple and append to subData
    subData.append((sub_id,title,punchline,url,author,score,created,numComms,permalink))
    #Create a dictionary entry of current submission data and store all data related to it
    subStats[sub_id] = subData

sub = args.sub #Which Subreddit to search in
subCount = 0
subStats = {}
after = args.after
after = int(dateutil.parser.parse(after, dayfirst=True).timestamp())
before= args.before
before = int(dateutil.parser.parse(before, dayfirst=True).timestamp())


data = getPushshiftData(after, before,sub)
# We need to run this function outside the loop first to get the updated after variable
#data = getPushshiftData(after, before, sub)
# Will run until all posts have been gathered i.e. When the length of data variable = 0
# from the 'after' date up until before date
while len(data) > 0: #The length of data is the number submissions (data[0], data[1] etc), once it hits zero (after and before vars are the same) end
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    #update after variable to last created date of submission
    after = data[-1]['created_utc']
    #data has changed due to the new after variable provided by above code
    try:
        data = getPushshiftData(after, before, args.sub)
    except:
        after = data[-2]['created_utc']

### Create a folder with the name data
path='data'
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)
    
    
def updateSubs_file():
    upload_count = 0
    #location = "\\Reddit Data\\" >> If you're running this outside of a notebook you'll need this to direct to a specific location

    file = args.file
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Post","Url","Author","Score","Publish Date","Total No. of Comments","Permalink"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
    print(f'Downloaded {upload_count} posts!')
            
updateSubs_file()
