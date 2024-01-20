from PyPDF2 import PdfReader, PdfWriter
from fitz import fitz
import pdfminer
from pdfminer.high_level import extract_text
import re
import os
import pandas as pd
from tqdm import tqdm




def read_pdf(file_path):
    text = ""
    # Open the PDF document
    try:
        doc = fitz.open(file_path)
        # print(file_path)
        doc.delete_page(0)
        
        # Access a specific page
        for page in doc:
            text += page.get_text()
            # page.set_cropbox(crop_box)
    except fitz.FileNotFoundError:
        return False

    return text


#     doc.save(output_file_path)

def remove_text(text):
    # text = extract_text(output_file_path)

    text = re.sub(r"\.{2,}", "", text)
    text = re.sub(r"\s+BLANK PAGE\s+", "", text)

    text = re.sub(r"\[Turn over", "", text)

    pattern = r'\d{2}_\d{4}_\d{2}_\d{4}_\d+(\.\d+)?(?:[^\d]*\d*)?\n© UCLES \d+\n\d+'
    # Use re.sub with re.DOTALL to replace matched patterns with an empty string
    text = re.sub(pattern, '', text, flags=re.DOTALL)

    text = '\n'.join(line for line in text.splitlines() if line.strip())

    return text

def divide_questions(text):

    # Use regular expression to split text based on the pattern "[number]"
    split_text = re.split(r'(\[\d+\])', text)

    # Filter out empty strings and keep square brackets at the end
    result = [item for item in split_text if item]

    return result

def define_question_no(questions):
    # Define a pattern to match letters inside brackets
    pattern = re.compile(r'\(([a-zA-Z])\)')
    question_no = [1]
    for i, question in enumerate(questions):
        # Find all matches in the input string
        match = pattern.search(question)

        # If there are matches, rearrange the string
        if match:
            match = match.group(0)
            # print(match)
            # Move the letters to the beginning of the string
            question = question.replace(f'{match}', '')
            question = f'{match} {question}'
            questions[i] = question

            print(i)
            if i != 0:
                if match != "(a)":
                    question_no.append(question_no[i - 1])
                else:
                    question_no.append(question_no[i - 1] + 1)
        elif i != 0:
            question_no.append(question_no[i - 1] + 1)

    return questions, question_no

def new_df(array, paper_no):

    questions = [value for i, value in enumerate(array) if i % 2 == 0]
    
    questions, question_no = define_question_no(questions)

    df = pd.DataFrame({"Paper_No": paper_no, "Question Number": question_no, "Question": questions, "Marks": [value for i, value in enumerate(array) if i % 2 == 1]})
    return df

# a = divide(read_pdf(delete_page1_header_footer()))[:-1]
df = pd.DataFrame({"Paper_No": "", "Question Number": "", "Question": "", "Marks": []})
for year in tqdm([19, 20, 21, 22, 23]):
    for code in [11, 12, 13]:
        for time in ['m', 's', 'w']:
            # Define input and output file paths
            # input_file_path = "pp/0417_m21_qp_12.pdf"
            # output_file_path = "pp/0417_m21_qp_12_new.pdf"
            paper_no = f"0417_{time}{year}_qp_{code}"
            input_file_path = f"pp/{paper_no}.pdf"
            if a := read_pdf(input_file_path):
                # a = read_pdf(input_file_path) 
                a = remove_text(a)
                a = divide_questions(a)[:-1]
                df = pd.concat([df, new_df(a, paper_no)])
# df.to_excel('output.xlsx', index=False)
