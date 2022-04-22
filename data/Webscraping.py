from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import argparse,sys,os
from time import sleep
import pandas as pd 

#Webscraing the names of comedies
parser = argparse.ArgumentParser(description='Webscraping ScrapsFromTheLost to get access to comedy transcripts')
parser.add_argument('--website', default="https://scrapsfromtheloft.com/stand-up-comedy-scripts/",
                    help="The website that contains links to all of the individual transcripts")
parser.add_argument('--tag', default="a",
                    help="Tag of whichever part of the site you want to webscrape")

args = parser.parse_args()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(args.website)
Comedies= driver.find_elements(By.TAG_NAME,args.tag)
comedies_list = []
for link in Comedies:
    comedies_list.append(link.get_attribute('href'))
websites = list(comedies_list[20:])
driver.quit()


### Creating dataframe
column_names = ["Comedy Title","Transcript"]
df = pd.DataFrame(columns = column_names)

### Webscraping for the actual transcripts
TranscriptCorpus=[]
RunCount=0
for website in websites:
    if RunCount==0:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        RunCount+=1
    driver.get(website)
    Transcripts= driver.find_elements(By.TAG_NAME,"p")
    Transcript = []
    
    for i in range(len(Transcripts)):
        Transcript.append(Transcripts[i].text)
    
        if i==len(Transcripts)-1:
            JoinedScript=' '.join(Transcript)
            TranscriptCorpus.append(JoinedScript)
            print('waiting')
            sleep(15)
    
data_tuples_zipped=list(zip(websites,TranscriptCorpus))
pd.DataFrame(data_tuples_zipped,columns=['Title','Transcript']).to_csv('Transcripts.csv')


    
