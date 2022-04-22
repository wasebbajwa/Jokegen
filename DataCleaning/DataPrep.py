import pandas as pd 
import os 
from sklearn.model_selection import train_test_split
from pathlib import Path

# Change the path variable to wherever your data folder is 
path='C:/Users/wbajw/MSDS 458/MSDS 460 Project/VsCode/data'
# Read in the CSV
data=pd.read_csv(f'{path}/train.csv')
# Some comments/posts are deleted or removed, so we get rid of them
data = data[data.Post != '[deleted]']
data = data[data.Post != '[removed]']
# Only keep the uni-code characters and drop the rest
data.Title.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
data.Title.replace({r'\W +' :' '},regex=True,inplace=True)
data.Post.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
data.Post.replace({r'\W +' :' '},regex=True,inplace=True)
# Add a token to let us know that the joke is over
data['Post']=data['Post']+'<eop>'
# Concat the two columns to make one full joke as the Title usually contains the hook while the post contains the punchline
data=data[data['Total No. of Comments']<=10]
data['text']=data['Title']+' '+data['Post']
data=data['text'].to_frame()
# Drop null rows
data=data.dropna()
print(data.shape[0])

# Split the data into a train and test set for later
train, test = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)


# determine the path where to save the train and test file
train_path = Path(path,'train_cleaned.csv')
test_path = Path(path, 'test_cleaned.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train.to_csv(train_path, sep=',', index=False)
test.to_csv(test_path, sep=',', index=False)