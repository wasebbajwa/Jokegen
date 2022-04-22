import pandas as pd
import requests 
import json 
import csv
import time
import datetime,dateutil
import argparse,sys,os
parser = argparse.ArgumentParser(description='Webscraping Subreddits to get past dates')
parser.add_argument('--sub', default="DadJokes",
                    help="subreddit name ")
args = parser.parse_args()

#This function builds an Pushshift URL, accesses the webpage and stores JSON data in a nested list
def getPushshiftData(after, before, sub):
    #Build URL
    url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='+str(sub)+'&size=10000&after='+str(after)+'&before='+str(before)+'&sort=desc&sort_type=score'
    #Print URL to show user
    print(url)
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
    created = datetime.datetime.fromtimestamp(subm['created_utc']) 
    numComms = subm['num_comments']
    permalink = subm['permalink']

    #Put all data points into a tuple and append to subData
    subData.append((sub_id,title,punchline,url,author,score,created,numComms,permalink))
    #Create a dictionary entry of current submission data and store all data related to it
    subStats[sub_id] = subData


#Takes in a data and outputs in Unix
after = '18/10/2018'
after = int(dateutil.parser.parse(after, dayfirst=True).timestamp())
print(after)
before= '30/10/2020'
before = int(dateutil.parser.parse(before, dayfirst=True).timestamp())
print(before)
sub = "DadJokes" #Which Subreddit to search in

#subCount tracks the no. of total submissions we collect
subCount = 0
#subStats is the dictionary where we will store our data.
subStats = {}

# We need to run this function outside the loop first to get the updated after variable
data = getPushshiftData(after, before, sub)
while len(data) > 0: 
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    #update after variable to last created date of submission
    after = data[-1]['created_utc']
    #data has changed due to the new after variable provided by above code
    data = getPushshiftData(after, before, sub)


def updateSubs_file():
    upload_count = 0
    #location = "\\Reddit Data\\" >> If you're running this outside of a notebook you'll need this to direct to a specific location
    print("input filename of submission file, please add .csv")
    filename = input() #This asks the user what to name the file
    file = filename
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Punchline","Url","Author","Score","Publish Date","Total No. of Comments","Permalink"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
            
        print(str(upload_count) + " submissions have been uploaded")
updateSubs_file()
