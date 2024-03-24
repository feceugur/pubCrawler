# **Pub Finder**


**Motivation of the Project**

The project aims to according to user inputs, the project presents the most recommended places in the Google comments for the preferred meal.

Two different methods were used and the results were compared. 

The first method used pre-trained models for sentiment analysis and topic modeling, while the second method used Vader score analysis and LDA topic modeling, which we saw in the course content. 

---

**Models Used**


*   Keypharese extraction for comments: **ml6team/keyphrase-extraction-kbir-inspec**
> This model uses KBIR as its base model and fine-tunes it on the Inspec dataset. KBIR or Keyphrase Boundary Infilling with Replacement is a pre-trained model which utilizes a multi-task learning setup for optimizing a combined loss of Masked Language Modeling (MLM), Keyphrase Boundary Infilling (KBI) and Keyphrase Replacement Classification (KRC).




*   Sentiment Analysis: **cardiffnlp/twitter-roberta-base-sentiment-latest**
> This is a RoBERTa-base model trained on ~124M tweets from January 2018 to December 2021, and finetuned for sentiment analysis with the TweetEval benchmark.

*   Keypharese extraction for user input: **davanstrien/deberta-v3-base_fine_tuned_food_ner**
> This model is a fine-tuned version of microsoft/deberta-v3-base  and DeBERTa improves the BERT and RoBERTa models using disentangled attention and enhanced mask decoder. And In DeBERTa V3, further improved the efficiency of DeBERTa using ELECTRA-Style pre-training with Gradient Disentangled Embedding Sharing.



---


**API**

Limitations:
- Google Maps API shows the 5 most useful reviews of places and no more.
- There is no other API for Google Place review
- Yelp api shows 5 reviews and not every venue
 
Solutions:
- [outscraper](https://outscraper.com/) can return 100 comments if we give place_id
- We found the ids of all placements according to the location around us from Google maps
- using these ids outscraper, we pulled the last 100 comments made in each place
- We used amazon services to deliver them and created a rest api.

For this, we used the Chalice Framework published by Amazon and deployed our API to Amazon. We stored all the information we crawled in ElasticSearch.
 

> *I have to point that my friend helped me for these API steps.*



---

### **Limitations**
* Better results could be achieved by fine-tuning the keyword extraction model in comments
* Google Maps API limits
* Sentiment analysis of sarcastic comments 
* It took too long to calculate the optimum number of topics for each comment and to do topic modeling accordingly
* Long preprocessing time and still have vulnerabilities in LDA part


**Potential Improvements of the Project**
When the user enters an input containing two food keywords, both are evaluated separately and all venues are listed accordingly. It should be developed so that the places with both keywords are listed.
