#!/usr/bin/env python
# coding: utf-8

# # Demo of how to identify the structure of a tweet

# In[1]:


# This code demonstrates how to perform structural content analysis on data, e.g. tweets
# this enables comparison of structure of content such as order of content types rather than specific text


# In[2]:


import identifyStructure


# In[3]:


# TEST to show the results and how to get the document structure and content structure

print('Original input:')
test = 'RT @here @there @everywhere #hashtag #emojitest is all 4️⃣ ❤️ more 🇦🇺 👨🏾‍👩🏾‍👧🏾‍👦🏾txt and more!!! https://www.url.com 🧵👨🏾‍👩🏾‍👧🏾‍👦🏾👩🏾‍💻👪🏿 🗳️🗳 😃 🟠https://www.url.com'
print(test)
print()


print('Step 1: Processed structure tokens')
# This step analyzes the contents of the input text and and labels each segment based on content type
list_of_token_tuples = identifyStructure.tokenizeStructure(test)
print(list_of_token_tuples)
print()


print('Step 2: Full document structure with count tokens and contents')
# This step creates spans by combining sequential content of same type together into a structure span
# The output is for each span in order, the type of content, number of tokens, and a list of the content in that span
full_document_structure_w_content = identifyStructure.getFullDocumentStructureWithContent(list_of_token_tuples)
print(full_document_structure_w_content)
print()


print('Document structure (list of content type and count of tokens)')
# This lists the order of content and the number of tokens that make up that span
# e.g. three emojis in a row would be [('emoji',3)]
document_structure = identifyStructure.getDocumentStructure(full_document_structure_w_content)
print(document_structure)
print()


print('Content structure is a list of the content types in order')
# just the order of content types
content_structure = identifyStructure.getContentStructure(full_document_structure_w_content)
print(content_structure)


# In[4]:


# Apply document structure to your data

import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


# In[5]:


# load in sample data
df = pd.read_csv('./sample_data/sample_csv_data_w_emojis_utf8.csv')
df.head(5)


# In[6]:


# IF YOU HAVE A LOT OF DATA THIS STEP CAN TAKE A WHILE (e.g. an hour for over a 30 million rows)
df['full_document_structure'] =   df['text'].apply(lambda x: identifyStructure.getFullDocumentStructureWithContent(identifyStructure.tokenizeStructure(x)))
df.head(7)


# In[7]:


df['document_structure'] = df['full_document_structure'].apply(identifyStructure.getDocumentStructure)
df['content_structure'] = df['full_document_structure'].apply(identifyStructure.getContentStructure)

df.head(7)


# In[8]:


# see top 7 most common document structures across the sample
# document structure is the list of content types and count of tokens of the same type

# to view data elements that are of a list data type use the pandas .astype(str)
df['document_structure'].astype(str).value_counts()[:7]


# In[9]:


# see the top 10 most common content structures across the sample
df['content_structure'].astype(str).value_counts()[:10]


# In[10]:


# save the top 10 content structures to a dataframe
top10_content_structures_df = df['content_structure'].astype(str).value_counts()[:10].reset_index()
top10_content_structures_df.columns=['content_structure','count_rows']
top10_content_structures_df


# In[11]:


# get the count of users per each of the top 10 content structures
content_structure_count_of_users = []
list_of_top_10_content_structures = top10_content_structures_df['content_structure'].tolist()

for content_struct in list_of_top_10_content_structures:
    content_structure_count_of_users.append(df[df['content_structure'].astype(str)==content_struct]['userid'].nunique())
top10_content_structures_df['author_count'] = content_structure_count_of_users
top10_content_structures_df


# In[12]:


# get content spans of a specific type
# e.g. get at_mention spans
df['at_mention_spans'] = df['full_document_structure'].apply(lambda x: [tuple(tup[2]) for tup in x if tup[0]=='at_mention'])
df['emoji_spans'] = df['full_document_structure'].apply(lambda x: [tuple(tup[2]) for tup in x if tup[0]=='emoji'])
df['url_spans'] = df['full_document_structure'].apply(lambda x: [tuple(tup[2]) for tup in x if tup[0]=='url'])
df['emoji_spans_as_lists'] = df['full_document_structure'].apply(lambda x: [tup[2] for tup in x if tup[0]=='emoji'])

df


# In[13]:


# top 5 most used at_mention spans in common with count of rows
print(df['at_mention_spans'].astype(str).value_counts()[:5])

# top 5 most used at_mention spans in common with count of rows
print(df['emoji_spans'].astype(str).value_counts()[:5])

# top 5 most used at_mention spans in common with count of rows
print(df['url_spans'].astype(str).value_counts()[:5])


# In[14]:


# using extractEmojis get list of emojis and unique emojis
df['emoji_list'] = df['text'].apply(identifyStructure.extractEmojis.getEmojisFromText)
df['emoji_unique_list'] = df['emoji_list'].apply(identifyStructure.extractEmojis.getUniqueEmojisFromEmojiList)
df


# In[15]:


df.to_csv('processed_output_of_structural_content_of_sample_data.csv', index=False, encoding='utf8')
df.to_excel('processed_output_of_structural_content_of_sample_data.xlsx', index=False, encoding='utf8')


# In[ ]:




