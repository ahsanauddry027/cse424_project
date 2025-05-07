import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter

# Load dataset
df = pd.read_csv("clean_resume_data.csv")

# Compute resume text length
df['text_length'] = df['Feature'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
df_cleaned = df.dropna()

# Create summary
summary = f"""
Dataset Summary:
----------------
Total Records: {len(df)}
Missing Values:
{df.isnull().sum().to_string()}
Resume Text Length - Mean: {df['text_length'].mean():.2f}, Median: {df['text_length'].median()}, Mode: {df['text_length'].mode()[0]}
Top Categories:
{df['Category'].value_counts().head(5).to_string()}
"""

# Save everything to PDF
with PdfPages("eda_resume_summary_visuals.pdf") as pdf:
    # Page 1: Summary (existing)
    plt.figure(figsize=(11, 6))
    plt.axis('off')
    plt.title("EDA Summary", fontsize=16)
    plt.text(0.01, 0.98, summary, ha='left', va='top', fontsize=11, family='monospace', wrap=True)
    pdf.savefig()
    plt.close()

    # Page 2: Top Categories Plot (existing)
    plt.figure(figsize=(10, 6))
    sns.countplot(y='Category', data=df_cleaned, order=df_cleaned['Category'].value_counts().index[:10])
    plt.title("Top 10 Job Categories")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 3: Resume Length Distribution (existing)
    plt.figure(figsize=(8, 5))
    sns.histplot(df_cleaned['text_length'], bins=30, kde=True, color='teal')
    plt.title("Distribution of Resume Text Lengths")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 4: Missing Values Bar Plot (new)
   # ... (previous code remains unchanged)

    # Page 4: Missing Values Bar Plot (fixed)
    plt.figure(figsize=(10, 4))
    missing = df.isnull().sum()
    sns.barplot(
        x=missing.values, 
        y=missing.index, 
        hue=missing.index,  # Add this
        palette='viridis', 
        legend=False  # Suppress legend
    )
    plt.title('Missing Values per Column')
    plt.xlabel('Number of Missing Values')
    pdf.savefig()
    plt.close()

    # Page 5: Top 5 Categories Pie Chart (new)
    plt.figure(figsize=(8, 8))
    top5 = df['Category'].value_counts().head(5)
    plt.pie(top5, labels=top5.index, autopct='%1.1f%%', startangle=140)
    plt.title('Proportion of Top 5 Job Categories')
    pdf.savefig()
    plt.close()

    # Page 6: Text Length by Category Box Plot (fixed)
    plt.figure(figsize=(12, 6))
    top_categories = df_cleaned['Category'].value_counts().head(5).index
    filtered_df = df_cleaned[df_cleaned['Category'].isin(top_categories)]
    sns.boxplot(
        x='Category', 
        y='text_length', 
        data=filtered_df, 
        hue='Category',  # Add this
        palette='Set2', 
        legend=False  # Suppress legend
    )
    plt.title('Resume Text Length Distribution by Top Categories')
    plt.xlabel('Category')
    plt.ylabel('Word Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

  # ... (rest of the code remains the same)

    # Page 7: Top Words in Resumes (fixed)
    # First calculate top_words BEFORE plotting
    stop_words = {'the', 'and', 'to', 'of', 'in', 'a', 'for', 'with', 'on', 'at'}
    all_words = ' '.join(df_cleaned['Feature'].astype(str)).lower().split()
    filtered_words = [word for word in all_words if word not in stop_words and len(word) > 2]
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(15)  # <-- THIS MUST COME BEFORE THE PLOT
    
    # Now create the plot
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=[w[1] for w in top_words], 
        y=[w[0] for w in top_words], 
        hue=[w[0] for w in top_words], 
        palette='Blues_d', 
        legend=False
    )
    plt.title('Top 15 Most Frequent Words (Excluding Stop Words)')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.tight_layout()
    pdf.savefig()
    plt.close()