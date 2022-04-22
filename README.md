# JokeCreator


## Overview
The goal of this project was to test the limits of modern day transformer architectures on the task of generating jokes. I chose to work on this as humor is one of the most subjective aspects of human interaction. What one person finds funny, another person can find bland and annoying. The base model used for pre-training was GPT-2 as the model was trained locally; however, in the future, I plan to train a more complex model in the cloud in order to compare the results. 

<img width="610" alt="transformer architecture" src="https://user-images.githubusercontent.com/70357685/164815718-c560859f-a025-43cc-a7a2-fac90f715d53.PNG">


## Data Overview
Reddit is an American social news aggregation, web content rating, and discussionwebsite. Registered members submit content to the site such as links, text posts, images, and videos, which are then voted up or down by other members. Members submit their content tospecific pages within Reddit, called subreddits. In order to collect the large number of jokes needed to train a transformer network, the subreddit “Dadjokes” was web scraped via the Requests package. 100 posts every day were collected between the 30th of October, 2014 to the 30th of October, 2020. In total, over 300,000 jokes were collected. The data was uploaded to a CSV file containing the title of the post, the content of the body, and the amount of upvotes the joke received. The title of the post contains the hook of the joke, while the content of the body
contains the punchline. After using a variety of pre-processing and text cleaning techniques, there was about 150,000 jokes left for training.


## Testing
The model results were evaluated by means of a crowd-sourced Turing test. Using an original text-producing bot based on the models, the models’ outputs were uploaded to the social media website Reddit. The bot would read a joke prompt from Reddit, typically in the form of a question, and generate an answer and upload the answer as a comment on the original joke. Then, users gave the generated jokes an “upvote” (+1) if they found them funny and a “downvote” (-1) otherwise. The net score was the metric used to evaluate overall joke quality. 

## Results
Overall , the performance of the transformer based method was mediocre; however, there were several bottlenecks that decreased the performance of the generator. One major bottleneck was the performance of the initial pre-trained model. GPT-2 Medium only has about 250 million parameters while modern day methods have over 6 billion. Another issue was that the batch sizes had to be relatively large in order to preserve memory during the tokenization and training process. One way to address this in the future without relying on substantially greater computational power is to leverage architectures such as the reformer model. It greatly increases efficiency by replacing dot-production attention with locality-sensitive hashing(Kaiser, 2020).

## Next Steps
These experiments, while disappointing, nevertheless are indicative of some progress in the space of joke generation. The transformer model was capable of generating a few jokes that were human-quality, even if these were a small drop in the bucket. It is probable that continued investigation into these techniques may lead to better results in the future. In order to improve the performance of the transformer, one technique could be to continuously ingest data into the model and have it train on live incoming data rather than one specific dataset. This would allow the bot to learn jokes revolving around current events. Another method to increase theperformance of the model could be to introduce greater penalties for jokes that received downvotes. Together, this would allow the bot to mimic human humor better as it would start to learn more about jokes revolving around current events. Another way to improve the model would be to address the computing bottleneck. Instead of training locally, services such as AWS or Azure could be used to deploy a model trained on billions of parameters instead of only hundreds of millions



