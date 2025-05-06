import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

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
    # Page 1: Summary
    plt.figure(figsize=(11, 6))
    plt.axis('off')
    plt.title("EDA Summary", fontsize=16)
    plt.text(0.01, 0.98, summary, ha='left', va='top', fontsize=11, family='monospace', wrap=True)
    pdf.savefig()
    plt.close()

    # Page 2: Top Categories Plot
    plt.figure(figsize=(10, 6))
    sns.countplot(y='Category', data=df_cleaned, order=df_cleaned['Category'].value_counts().index[:10])
    plt.title("Top 10 Job Categories")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # Page 3: Resume Length Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df_cleaned['text_length'], bins=30, kde=True, color='teal')
    plt.title("Distribution of Resume Text Lengths")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")
    plt.tight_layout()
    pdf.savefig()
    plt.close()
