import openai
import os
import config
import pandas as pd
from utils import extract_text_from_pdf

# Set up OpenAI API
openai.api_key = config.CHATGPT_API_KEY

def process_pdfs():
    q_path = os.path.join(config.UPLOAD_FOLDER, "question_paper.pdf")
    a_path = os.path.join(config.UPLOAD_FOLDER, "answer_sheet.pdf")

    # Extract text
    questions = extract_text_from_pdf(q_path)
    answers = extract_text_from_pdf(a_path)

    # Generate Excel file
    excel_path = os.path.join(config.OUTPUT_FOLDER, "extracted_data.xlsx")

    data = {
        "Question No.": list(range(1, len(questions) + 1)),
        "Question": questions,
        "Answer": answers
    }

    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

    return excel_path
