import fitz
import re
import pandas as pd
from tqdm import tqdm
# import camelot



def read_pdf(file_path, paper_type):
    text = ""
    # Open the PDF document
    try:
        doc = fitz.open(file_path)
        # print(file_path)
        doc.delete_page(0)
        if paper_type == "ms":
            doc.delete_page(0)
        # Access a specific page
        for page in doc:
            text += page.get_text()
    except fitz.FileNotFoundError:
        return False

    return text


#     doc.save(output_file_path)

def remove_text(text, paper_type):
    # text = extract_text(output_file_path)
    if paper_type == "qp":
        text = re.sub(r"\.{2,}", "", text)
        text = re.sub(r"\s+BLANK PAGE\s+", "", text)

        text = re.sub(r"\[Turn over", "", text)

        pattern = r'\d{2}_\d{4}_\d{2}_\d{4}_\d+(\.\d+)?(?:[^\d]*\d*)?\n© UCLES \d+\n\d+'
        # Use re.sub with re.DOTALL to replace matched patterns with an empty string
        text = re.sub(pattern, '', text, flags=re.DOTALL)
        

        pattern = re.compile(r'^\d+$\n^\d+/\d+/[A-Z]/[A-Z]/\d+$\n^© UCLES \d{4}$', re.MULTILINE)
        # Use re.sub() to replace the matched pattern with an empty string
        text = re.sub(pattern, '', text)

    if paper_type == "ms":
        pattern = re.compile(r'Question\s*Answer\s*Marks\s*', re.MULTILINE)
        # Use re.sub to remove the matched pattern
        text = re.sub(pattern, '', text)

        # Define the pattern to match the text
        pattern = re.compile(r'\d{4}/\d+\s*Cambridge IGCSE – Mark Scheme\s*PUBLISHED\s*March \d{4}')
        # Use re.sub() to replace the matched pattern with an empty string
        text = re.sub(pattern, '', text)

        pattern = re.compile(r'© UCLES \d+\s*Page \d+ of \d+')

        # Use re.sub() to replace the matched pattern with an empty string
        text = re.sub(pattern, '', text)
    text = '\n'.join(line for line in text.splitlines() if line.strip())
    return text

def divide_questions(text, paper_type):

    if paper_type == "qp":
        # Use regular expression to split text based on the pattern "[number]"
        split_text = re.split(r'(\[\d+\])', text)
        result = [item for item in split_text if item]
    elif paper_type == "ms":
        pattern = re.compile(r'\d+ \n')
        result = re.split(pattern, text)
        result = [line.strip() for line in result if line.strip()]

    # Filter out empty strings and keep square brackets at the end


    return result

def define_question_no(questions):
    # Define a pattern to match letters inside brackets
    pattern = re.compile(r'\((?:[a-d]|(?:i{1,3}|iv))\)')

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

def extract_qp() -> None:
    df = pd.DataFrame({"Paper_No": "", "Question Number": "", "Question": "", "Marks": []})
    for year in tqdm([19, 20, 21, 22, 23]):
        for code in [11, 12, 13]:
            for time in ['s', 'm', 'w']:
                #CS Paper
                paper_no = f"0478_{time}{year}_qp_{code}"
                input_file_path = f"cs/qp/p1/{paper_no}.pdf"

                #ICT Paper
                paper_no = f"0417_{time}{year}_qp_{code}"
                input_file_path = f"ict/qp/{paper_no}.pdf"

                if qp := read_pdf(input_file_path, "qp"):
                    qp = remove_text(qp, "qp")
                    qp = divide_questions(qp, "qp")
                    if len(qp) % 2 == 1:
                        qp = qp[:-1]
                    try:    
                        df = pd.concat([df, new_df(qp, paper_no)])
                    except ValueError:
                        print(f"{paper_no} not able to add to dataframe")
    df.to_excel('output_cs.xlsx', index=False)
    df.to_json('output.json', orient="records")

def extract_ms() -> None:
    # for year in tqdm([19, 20, 21, 22, 23]):
    #     for code in [11, 12, 13]:
    #         for time in ['s', 'm', 'w']:
                #CS Paper
                # paper_no = f"0478_{time}{year}_ms_{code}"
                # input_file_path = f"cs/ms/p1/{paper_no}.pdf"

                # #ICT Paper
                # paper_no = f"0417_{time}{year}_ms_{code}"
                # input_file_path = f"ict/ms/{paper_no}.pdf"

                # if ms := read_pdf(input_file_path, "ms"):
                #     ms = remove_text(ms, "ms")
                #     ms = 

    input_file_path = f"ict/ms/0417_m21_ms_12.pdf"
    ms = read_pdf(input_file_path, "ms")
    ms = remove_text(ms, "ms")
    ms = divide_questions(ms, "ms")
    for i in ms:
        print("===")
        print(i)

# extract_qp()
extract_ms()
