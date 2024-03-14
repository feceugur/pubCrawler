import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('LDA_PubFinder/processed_data.csv')

def extract_unique_words(topics):
    unique_words = set()
    unique_words_final = []
    if isinstance(topics, str):
        topics = eval(topics)  # Convert string representation of list of dictionaries to actual list of dictionaries
        for topic_dict in topics:
            for word in topic_dict.keys():
                unique_words.add(word)
            
            unique_list = list(unique_words)
            concatenated_string = ' '.join(unique_list)
            unique_words_updated = set(concatenated_string.split())
            unique_words_final.append(list(unique_words_updated))
    return (unique_words_final.pop() if unique_words_final else [None])


# Add a new column with unique topic words
df['unique_topic_words'] = df['topic'].apply(extract_unique_words)

# Save the DataFrame to a new CSV file with the added column
df.to_csv('LDA_PubFinder/data_with_unique_topic_words.csv', index=False)
