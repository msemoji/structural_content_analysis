#!/usr/bin/env python

# This Python 3.6 was written in August 2020 by mswartz2@gmu.edu
# This code will import text string, extract any emojis as list if present, and then
# analyze the structure and return the list of content types in order
# This code is based on analysis of structure of tweets

# Dependencies
# extractEmojis.py and Unicode_emojis_list.py
import extractEmojis

import regex, re, ast


# FUNCTION TO GET THE SPANS OF A TWEET AND LABEL THE CONTENT TYPE
#import ast
# the emoji list or unique emoji list

def tokenizeStructure(text_string):
    # inputs: 'RT @person @person2 ❤️all hearts ❤❤❤️!! http://www.url.com', ['❤️']
    # code: sections_list = split_tweet_text_into_sections_list_of_tuples_w_emoji_unique_list(text, text_emoji_unique_list)
    # output = [('RT','RT'),(' ','space'),('@person','at_mention'),(' ','space'),('@person2','at_mention'),(' ','space'),('❤️','emoji'),('all','word'),(' ','space'),('hearts','word'),(' ','space'),('❤️','emoji'),('❤️','emoji'),('❤️','emoji'),('!','punctuation'),('!','punctuation'),(' ','space'),('http://www.url.com','url')]
    
    # uses the regex library to split on multiple delims and keep them using the ()    
    if text_string == '' or type(text_string) != str:
        return []
    else:
        cleaned_text = extractEmojis.repairEmojisInText(text_string)
        emoji_list = extractEmojis.getEmojisFromText(cleaned_text)
        unique_emojis_list = sorted(list(set(emoji_list)))
        # to make processing easier
        sorted_emoji_list_by_len = sort_list_by_length_descending(unique_emojis_list)
        try:
            # if emoji list present then do this
            if len(unique_emojis_list) > 0:
                # this approach with paranthesis to preserve capture groups from regex match
                emoji_combined = "(" + ")|(".join(sorted_emoji_list_by_len) + ")"
                patterns = re.compile(emoji_combined + '|(\.\s)|([!?\s])')  # add in the punctuation
            else:
                patterns = re.compile('(\.\s)|([!?\s])')  # add in the punctuation
            text_split_plus_nones = re.split(patterns, cleaned_text)
            text_split = [seq for seq in text_split_plus_nones if seq != None and seq != '']
        except: 
            # this to manually split with str for problem emoji like keycap astericks
            punc_list = ['!','?','. ']
            if len(text_emoji_unique_list) > 0:
                splitter_list = sorted_emoji_list_by_len + punc_list
            else:
                splitter_list = punc_list
            text_split = split_text_str_by_list_of_strings_keep_splitter(cleaned_text,splitter_list)
        
        # Check the contents in structure
        section_list = []
        sec_type_list = []
        token_tuple_list = []
        span_list = []
        sec_type_old = 'none'
        sec_type = 'none'
        span = ''
        section_cnt = len(text_split)
        section_num = 0
        for section in text_split:
            if section == None or section == '' or section == 'none':
                sec_type = 'none'
            elif section == 'RT':
                sec_type = 'RT'
            elif section == ' ':
                sec_type = 'space'
            elif section in unique_emojis_list:
                sec_type = 'emoji'
            elif 'http' in section:
                sec_type = 'url'
            elif '@' in section[0]:
                sec_type = 'at_mention'
            elif '#' in section[0]:
                sec_type = 'hashtag'
            elif section in ['!','?','. ']:
                sec_type = 'punctuation'
            else:
                sec_type = 'word'
            token_tuple_list.append((section,sec_type))
        return token_tuple_list 



# combines words and spaces next to each other into a single span
# and combines emojis next to each other into a single span 
# a span is a single content type and the sequential content of the same type 
# e.g. three at_mentions in a tweet in a row would be a single span of type "at_mention"
# e.g. four emojis in a row would be a single emoji content type span
def getFullDocumentStructureWithContent(token_tuple_list):
    # input: [('RT','RT'),(' ','space'),('@person','at_mention'),(' ','space'),('@person2','at_mention'),(' ','space'),('❤️','emoji'),('all','word'),(' ','space'),('hearts','word'),(' ','space'),('❤️','emoji'),('❤️','emoji'),('❤️','emoji'),('!','punctuation'),('!','punctuation'),(' ','space'),('http://www.url.com','url')]
    # code: span_list = get_spans_from_sections(sections_list)
    # output: [('RT', 1, ['RT']),('at_mention', 2, ['@person','@person2']), ('emoji', 1, ['❤️']),('text', 4, ['all️',' ','hearts',' ']) ,('emoji', 3, ['❤️','❤️','❤️']),('punctuation',2,['!','!']),('url',1,['http://www.url.com'])]
    if token_tuple_list == [] or type(token_tuple_list) != list:
        return []    
    else:
        span_type_list = []
        span_content_list = []
        span_tuple_list = []
        prev_sec_type = 'none'
        join=False
        #for sec_num in range(len(sections_list)-1,-1,-1):
        sec_num = 0
        len_sec_list = len(token_tuple_list)
        span_parts_list = []
        span = ''
        span_type = ''
        for i in range(len(token_tuple_list)):
            sec_tuple = token_tuple_list[i]
            sec_type = sec_tuple[1]
            sec = sec_tuple[0]
            # clean up the at mention from a RT
            if sec_type == 'at_mention':
                if ':' in sec:
                    sec = sec.replace(':','')
            if sec_type == 'word':
                sec_type = 'text'
                     
            # merge the content containing spaces or that is the same
            if (sec_type == 'space' and prev_sec_type == 'text') or (sec_type == prev_sec_type):
                    # add space but not the type
                    span = span + sec
                    span_parts_list.append(sec)
            # drop spaces between spans e.g. url space url will become url
            elif (sec_type == 'space' and prev_sec_type != 'text') and i != len(token_tuple_list)-1:
                #print('skip')
                continue 
            else:
                if sec_type != prev_sec_type and sec_type != 'space':
                    if sec_num>0 :
                        # append old span
                        span_content_list.append(span_parts_list)
                        span_type_list.append(span_type)
                        span_tuple_list.append((span_type,len(span_parts_list),span_parts_list))
                    # create a new span
                    span = sec
                    span_parts_list = [sec]
                    span_type = sec_type
                    prev_sec_type = sec_type
            sec_num +=1
            #append last span
            if i == len(token_tuple_list)-1:
                span_content_list.append(span_parts_list)
                span_type_list.append(span_type)
                span_tuple_list.append((span_type,len(span_parts_list),span_parts_list))
        full_document_structure_with_content = span_tuple_list
        return full_document_structure_with_content


# function to get document structure which is list of tuples of content type and count tokens (e.g. count of at_mentions in an at_mention span)
def getDocumentStructure(full_document_structure_with_content):
    if type(full_document_structure_with_content) == list and len(full_document_structure_with_content)>0:
        return [(tup[0],tup[1]) for tup in full_document_structure_with_content]
    else:
        return []
    # input: span_list = [('RT', 1, ['RT']),('at_mention', 2, ['@person','@person2']), ('emoji', 1, ['❤️']),('text', 4, ['all️',' ','hearts',' ']) ,('emoji', 3, ['❤️','❤️','❤️']),('punctuation',2,['!','!']),('url',1,['http://www.url.com'])]
    # code: structure_list = get_structure_of_content(span_list)
    # output: ['RT','at_mention','emoji','text','emoji','punctuation','url']


# function to get list of content structures of a document
def getContentStructure(full_document_structure_with_content):
    if type(full_document_structure_with_content) == list and len(full_document_structure_with_content)>0:
        return [tup[0] for tup in full_document_structure_with_content]
    else:
        return []
    # input: span_list = [('RT', 1, ['RT']),('at_mention', 2, ['@person','@person2']), ('emoji', 1, ['❤️']),('text', 4, ['all️',' ','hearts',' ']) ,('emoji', 3, ['❤️','❤️','❤️']),('punctuation',2,['!','!']),('url',1,['http://www.url.com'])]
    # code: structure_list = get_structure_of_content(span_list)
    # output: ['RT','at_mention','emoji','text','emoji','punctuation','url']








## HELPER FUNCTIONS
### 
# helper functions to get spans by splitting text and preserving emoji and fixing compound
# emoji characters that regex breaks or doesn't recogize

def sort_list_by_length_descending(list_to_sort):
    # this doesn't work any other way so don't change it
    list_to_sort.sort(key=len, reverse=True)
    return list_to_sort

"""

def findall_in_string_no_re(textstr, search_for_str_pattern):
    index_list_of_find_str_in_textstr = []
    i = textstr.find(search_for_str_pattern)
    if i != -1:
        index_list_of_find_str_in_textstr.append(i)
    # continue until you don't have anymore
    while i != -1:
        i = textstr.find(search_for_str_pattern, i+1)
        if i != -1:
            index_list_of_find_str_in_textstr.append(i)
    return index_list_of_find_str_in_textstr


def split_text_str_by_list_of_strings_keep_splitter(text_to_process, list_of_str_splitter):  
    sorted_desc_list_of_str_splitter = sort_list_by_length_descending(list_of_str_splitter)
    split_index_spans = []
    # note does not preserve compound emoji but fixes later
    for kc in sorted_desc_list_of_str_splitter:
        kc_res = findall_in_string_no_re(text_to_process, kc)
        kc_spans = [(i,i+len(kc)) for i in kc_res]
        split_index_spans = split_index_spans + kc_spans
    split_index_spans = sorted(split_index_spans)
    if split_index_spans[-1][1] != len(text_to_process):
        split_index_spans.append((split_index_spans[-1][1],len(text_to_process)))
    first = split_index_spans[0][0]
    split_index_spans.insert(0,(0,first))
    # fill in new spans
    new_index_spans = []
    end = 0 
    for i in range(0,len(split_index_spans)):
        span_tuple = split_index_spans[i]
        st = span_tuple[0]
        if st == end:
            end = span_tuple[1]
            new_index_spans.append((st,end))
        else:
            #fill the gap by reverse start and end
            if st > end:
                new_index_spans.append((end,st))
                # then proceed
                end = span_tuple[1]
                new_index_spans.append((st,end))
                
    text_split_by_emoji_list = [text_to_process[tup[0]:tup[1]] for tup in new_index_spans]
    # process the spaces and split on them
    text_split_on_space = []
    space_span = [sorted_desc_list_of_str_splitter]
    span = ''
    for span in text_split_by_emoji_list:
        if ' ' in span:
            space_span = re.split('(\s+)', span)            
            for little_span in space_span:
                text_split_on_space.append(little_span)
        else:
            text_split_on_space.append(span)
    clean_text_split_spaces = [text_split for text_split in text_split_on_space if text_split != '']
    # fix compound emojis
    compound_emoji_list =  []
    for cemoji in sorted_desc_list_of_str_splitter:
        if '\u200d' in cemoji:
            compound_emoji_list.append(cemoji)
    compound_emoji_list_sorted_by_len = sort_list_by_length_descending(compound_emoji_list) 
    # find all pieces that are just the joiner
    index_of_joiners = [p for p in range(len(clean_text_split_spaces)) if clean_text_split_spaces[p] == '\u200d']
    index_of_joiners_reversed = sorted(index_of_joiners, reverse=True)
    for p in index_of_joiners_reversed:
        nextone = clean_text_split_spaces[p+1]
        thisone = clean_text_split_spaces[p]
        pastone = clean_text_split_spaces[p-1]
        fix = pastone + thisone + nextone
        clean_text_split_spaces[p+1] = fix
        del clean_text_split_spaces[p]
        del clean_text_split_spaces[p-1]
    index_of_joiners = [p for p in range(len(clean_text_split_spaces)) if clean_text_split_spaces[p].endswith('\u200d')]
    index_of_joiners_reversed = sorted(index_of_joiners, reverse=True) 
    for p in index_of_joiners_reversed:
        nextone = clean_text_split_spaces[p+1]
        thisone = clean_text_split_spaces[p]
        combined_sections_w_cemoji = thisone + nextone
        clean_text_split_spaces[p] = combined_sections_w_cemoji
        del clean_text_split_spaces[p+1]
        try_next_cemoji = True
    # find pieces start with joiner grab the next one
    index_of_joiners = [p for p in range(len(clean_text_split_spaces)) if clean_text_split_spaces[p].startswith('\u200d')]
    skintone_list = ['🏻','🏼','🏽','🏾','🏿']
    index_of_skintone = [p for p in range(len(clean_text_split_spaces)) for skintone in skintone_list if clean_text_split_spaces[p].startswith(skintone)]
    index_of_joiners_reversed = sorted(index_of_joiners+ index_of_skintone, reverse=True) 
    for p in index_of_joiners_reversed:
        prevone = clean_text_split_spaces[p-1]
        thisone = clean_text_split_spaces[p]
        combined_sections_w_cemoji = prevone + thisone
        for cemoji in compound_emoji_list_sorted_by_len:
            if cemoji in combined_sections_w_cemoji:
                clean_text_split_spaces[p-1] = cemoji
                sec_split = combined_sections_w_cemoji.split(cemoji)
                clean_text_split_spaces[p] = sec_split[1]
                break
    clean_text_split_spaces_no_nones = [text_piece for text_piece in clean_text_split_spaces if text_piece != '' ]
    return clean_text_split_spaces_no_nones
# end of helper functions

"""