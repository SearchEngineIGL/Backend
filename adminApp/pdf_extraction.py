import re
import spacy
import fitz 
"""__Function to remove header/footer
     from the pdf file__
    """
def remove_header_footer(page):
     header_long=20
     footer_long=30
     blocks = page.get_text("blocks")
     header_block=blocks[0]
     footer_block=blocks[len(blocks)-1] 
     if(len(footer_block[4])>20):
         footer_block=( blocks[len(blocks)-2])      
     if header_block[3]-header_block[1]<= header_long:
        blocks.remove(header_block)
     if footer_block[3]-footer_block[1]<= footer_long:
        blocks.remove(footer_block) 
     return blocks
"""__Function to extract title
     from the pdf file__
    """
def extract_title(blocks):
    num = 0
    title_not_found = True
    title_position = 50

    while title_not_found:
        title_block = blocks[num]
       
        if title_block[3] - title_block[1] <= title_position and '<image:' not in str(title_block[4]):
           
            title_not_found = False
        else:
            num += 1
    return title_block

"""__Function to transform a block to text(String)
     from the pdf file__
    """
def blocks_to_text(blocks):
    text = ""
    for block in blocks:
        if type(block[4]) == str:
            text += block[4] + " "  # Append the text and add a space between blocks
    return text.strip()  # Remove leading and trailing whitespaces
"""__Function to extract authors section (authors + institutions)
     from the pdf file__
 """
def extract_authors_section(text, start_position):
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

"""__Function to recongnize authors names using the model of spacy
     in the authors section 
     from the pdf file__
 """
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
"""__Function to extract  institutions from the authors section
     from the pdf file__
 """
def extract_institutions(text, persons):
    # Split the text into lines
    lines = text.split('\n')

    # Remove lines containing email addresses
    lines = [line for line in lines if '@' not in line]
    # print(lines)
    # Remove lines containing names from the persons list
    for person in persons:
        
        lines = [line for line in lines if person not in line]

    # Join the remaining lines back into a single text
    cleaned_text = '\n'.join(lines)

    return cleaned_text.strip()
"""__Function to extract  all the other sections from the text 
     of the pdf file__
 """
def extract_sections(text,title):
    # Define patterns for each section    
    abstract_pattern = re.compile(r"ABSTRACT[\n: ]+(.+?)(?:KEYWORDS|$)", re.DOTALL)
    keywords_pattern = re.compile(r"KEYWORDS[\n: ]+(.+?)(?:ACM Reference Format:|$)", re.DOTALL)
    content_pattern = re.compile(r"INTRODUCTION[\n: ]+(.+?)(?:REFERENCES|$)", re.DOTALL)
    references_pattern = re.compile(r"REFERENCES\n(.+)", re.DOTALL)

    # Extract information using regular expressions
    abstract_match = abstract_pattern.search(text)
    keywords_match = keywords_pattern.search(text)
    content_match = content_pattern.search(text)
    references_match = references_pattern.search(text)

    # Get matched groups
    abstract = abstract_match.group(1).strip() if abstract_match else None
    keywords = keywords_match.group(1).strip() if keywords_match else None
    content = content_match.group(1).strip() if content_match else None
    references = references_match.group(1).strip() if references_match else None

    # Find the position of the title in the text
    title_position = text.find(title) if title else -1
    # print(title_position)
    # Modify authors extraction based on title position
    if title_position != -1:
         start_position = title_position + len(title)

         authors_section = extract_authors_section(text, start_position)
        #  print(authors_section)
         authors=recognize_authors_with_spacy(authors_section)
        #  print(authors)
         institutions = extract_institutions(authors_section,authors)
        #  print("------------------------------------------")
        #  print(institutions)

    return  institutions , authors, abstract, keywords, content, references




"""__Function to read the pdf file and extract all th information needed
     __
 """
def extract_article_pdf(pdf_path):
     with fitz.open(pdf_path) as pdf_document:
      text = ""
      num_pages = pdf_document.page_count
      for page_num in range(num_pages):
        page = pdf_document[page_num]
        page.wrap_contents()
        blocks = remove_header_footer(page)
        if page_num == 0:
            title = extract_title(blocks)
          
       
        #    print(blocks)
        text += blocks_to_text(blocks)
       

     institutions , authors, abstract, keywords, content, references = extract_sections(text,title[4])
      # Create a dictionary
     article_data = {
        "title":title[4],
        "institutions": institutions,
        "authors": authors,
        "abstract": abstract,
        "keywords": keywords,
        "content": content,
        "references": references
     }
     # Return the dictionary
     return article_data
     


# # Example usage
# pdf_path = 'article_02.pdf'
# article_data = extract_article_pdf(pdf_path)

# for key, value in article_data.items():
#     print(f"{key}: {value}")
