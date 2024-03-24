import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/detailed_reviews.csv")
df['published_at_date'] = pd.to_datetime(df['published_at_date'])

# Filter rows where 'published_at_date' is older than 2022
df_filtered = df[df['published_at_date'] >= pd.to_datetime('2022-01-01')]

# Extract 'place_name' and 'review_text' columns
result = df_filtered[['place_name', 'review_text']]

# Save the result to a new CSV file
result.to_csv("/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/recent_reviews.csv", index=False)
