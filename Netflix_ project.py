import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

if not os.path.exists('netflix_data.csv'):
    with open('netflix_data.csv', 'w') as f:
        f.write("""date_watched,watch_time,genre,device_type
2025-07-01 20:15:00,45,Action,Smart TV
2025-07-01 22:30:00,30,Comedy,Mobile
2025-07-02 18:10:00,50,Drama,Laptop
2025-07-02 14:00:00,60,Fantasy,Smart TV
2025-07-03 19:00:00,55,Comedy,Laptop
2025-07-04 11:30:00,25,Documentary,Mobile
2025-07-04 16:45:00,35,Action,Smart TV
2025-07-05 13:00:00,70,Drama,Tablet
2025-07-05 20:00:00,90,Thriller,Laptop""")
    print(" Sample 'netflix_data.csv' created.")

df = pd.read_csv('netflix_data.csv')

print("First 5 rows of the dataset:")
print(df.head())

print("\nMissing values in each column:")
print(df.isnull().sum())

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df['date_watched'] = pd.to_datetime(df['date_watched'], errors='coerce')
df = df.dropna(subset=['date_watched'])
df['watch_time'] = pd.to_numeric(df['watch_time'], errors='coerce')
df = df.dropna(subset=['watch_time'])
df.reset_index(drop=True, inplace=True)

df['hour'] = df['date_watched'].dt.hour
df['month'] = df['date_watched'].dt.to_period('M')

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

plt.figure(figsize=(10, 5))
top_genres = df['genre'].value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, palette='coolwarm')
plt.title("Top 10 Most Watched Genres")
plt.xlabel("View Count")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(df['hour'], bins=24, kde=True, color='purple')
plt.title("Netflix Viewing by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("View Count")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

monthly_trends = df.groupby('month').size()
plt.figure(figsize=(12, 5))
monthly_trends.plot(kind='line', marker='o', color='green')
plt.title("Monthly Viewing Trends")
plt.xlabel("Month")
plt.ylabel("Total Views")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
device_counts = df['device_type'].value_counts()
sns.barplot(x=device_counts.index, y=device_counts.values, palette='Set2')
plt.title("Devices Used for Watching")
plt.ylabel("View Count")
plt.xlabel("Device Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
avg_watch_time = df.groupby('genre')['watch_time'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=avg_watch_time.values, y=avg_watch_time.index, palette='mako')
plt.title("Average Watch Time by Genre (Top 10)")
plt.xlabel("Average Watch Time (minutes)")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()

df.to_csv('netflix_cleaned_data.csv', index=False)
print("\n Cleaned data saved as 'netflix_cleaned_data.csv'")
