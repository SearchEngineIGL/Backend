import re
import spacy

import fitz 

def remove_header_footer(page):
     header_long=20
     footer_long=30
     blocks = page.get_text("blocks")
     header_block=blocks[0]
     footer_block=blocks[len(blocks)-1]
    #  print(header_block)
    #  print("___________________________________________________")
     
    
     
     if(len(footer_block[4])>20):
         footer_block=( blocks[len(blocks)-2])
         
     if header_block[3]-header_block[1]<= header_long:
        # print(header_block[3]-header_block[1])
        blocks.remove(header_block)
         
     if footer_block[3]-footer_block[1]<= footer_long:
       
        blocks.remove(footer_block) 
     return blocks
def extract_title(blocks):
    num = 0
    title_not_found = True
    title_position = 50

    while title_not_found:
        
        title_block = blocks[num]
        print(type(title_block[4]))
        if title_block[3] - title_block[1] <= title_position and '<image:' not in str(title_block[4]):
            print("Title found")
            title_not_found = False
        else:
            num += 1

    return title_block
def blocks_to_text(blocks):
    text = ""
    for block in blocks:
        # Check if the block is a text block (not an image)
        if type(block[4]) == str:
            text += block[4] + " "  # Append the text and add a space between blocks
    return text.strip()  # Remove leading and trailing whitespaces

pdf_path = 'article_02.pdf'

with fitz.open(pdf_path) as pdf_document:
    text = ""
    num_pages = pdf_document.page_count
    for page_num in range(num_pages):
        page = pdf_document[page_num]
        page.wrap_contents()
        blocks = remove_header_footer(page)
        if page_num == 0:
            title = extract_title(blocks)
            print(title)
       
        #    print(blocks)
        text += blocks_to_text(blocks)
        print("this is page number", page_num)
def extract_from_position_to_abstract(text, start_position):
    # Convert search terms and text to lowercase
    lower_text = text.lower()
    start_position = max(0, min(len(text), start_position))

    # Find the position of "abstract" and "keywords" after the given start_position
    abstract_position = lower_text.find("abstract", start_position)
    keywords_position = lower_text.find("keywords", start_position)

    if abstract_position < 0 and keywords_position < 0:
        # Neither "abstract" nor "keywords" found, return the text from start_position to the end
        extracted_text = text[start_position:]
    else:
        # Find the closest occurrence of "abstract" or "keywords" after start_position
        position = min(pos for pos in [abstract_position, keywords_position] if pos >= 0)

        # Extract the substring from start_position until "abstract" or "keywords" or end of the text
        extracted_text = text[start_position:position]

    return extracted_text.strip()


def recognize_authors_with_spacy(text):
    nlp = spacy.load("en_core_web_lg")
    # Use spaCy to recognize persons (authors)
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if len(persons)==0:
         nlp = spacy.load("en_core_web_md")
         # Use spaCy to recognize persons (authors)
         doc = nlp(text)
         persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] 
    if len(persons)==0:
         nlp = spacy.load("en_core_web_sm")
         # Use spaCy to recognize persons (authors)
         doc = nlp(text)
         persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] 
    return persons
def remove_names_and_emails(text, persons):
    # Split the text into lines
    lines = text.split('\n')

    # Remove lines containing email addresses
    lines = [line for line in lines if '@' not in line]
    # print(lines)
    # Remove lines containing names from the persons list
    for person in persons:
        # for line in lines:
        #     if (person not in line):
        #         lines=lines.remove(line)
        
        lines = [line for line in lines if person not in line]

    # Join the remaining lines back into a single text
    cleaned_text = '\n'.join(lines)

    return cleaned_text.strip()




def extract_sections(text):
    # Define patterns for each section
    # title_pattern = re.compile(r"Title: (.+)")
    authors_pattern = re.compile(r"Authors: (.+)")
    
    abstract_pattern = re.compile(r"ABSTRACT[\n: ]+(.+?)(?:KEYWORDS|$)", re.DOTALL)
    keywords_pattern = re.compile(r"KEYWORDS[\n: ]+(.+?)(?:ACM Reference Format:|$)", re.DOTALL)
    content_pattern = re.compile(r"INTRODUCTION[\n: ]+(.+?)(?:REFERENCES|$)", re.DOTALL)
    references_pattern = re.compile(r"REFERENCES\n(.+)", re.DOTALL)

    # Extract information using regular expressions
    # title_match = title_pattern.search(text)
    # authors_match = authors_pattern.search(text)
    abstract_match = abstract_pattern.search(text)
    keywords_match = keywords_pattern.search(text)
    content_match = content_pattern.search(text)
    references_match = references_pattern.search(text)

    # Get matched groups
    # title = title_match.group(1) if title_match else None
    # authors = authors_match.group(1) if authors_match else None
    abstract = abstract_match.group(1).strip() if abstract_match else None
    keywords = keywords_match.group(1).strip() if keywords_match else None
    content = content_match.group(1).strip() if content_match else None
    references = references_match.group(1).strip() if references_match else None

    # Find the position of the title in the text
    title_position = text.find(title[4]) if title else -1
    # print(title_position)
    # Modify authors extraction based on title position
    if title_position != -1:
         start_position = title_position + len(title[4])

         authors_section = extract_from_position_to_abstract(text, start_position)
        #  print(authors_section)
         authors=recognize_authors_with_spacy(authors_section)
        #  print(authors)
         institutions = remove_names_and_emails(authors_section,authors)
        #  print("------------------------------------------")
        #  print(institutions)

    return title[4], institutions , authors, abstract, keywords, content, references
# 
# Example usage
article_text = text
# print(text)
title, institutions , authors, abstract, keywords, content, references = extract_sections(article_text)

# # Print the information
print(f"Title__________________: {title}")
print(f"Institution-------------------------: {institutions}")
print(f"Authors________________________: {authors}")
print(f"Abstract------------------------: {abstract}")
print(f"Keywords__________________________: {keywords}")
print(f"References---------------------: {references}")
print(f"Content_________________________: {content}")