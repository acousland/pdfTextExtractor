import streamlit as st
import PyPDF2
import io
from collections import Counter

def extract_text_from_pdf(file_data):
    with io.BytesIO(file_data) as file:
        reader = PyPDF2.PdfReader(file)
        all_lines = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                page_lines = page_text.split('\n')
                all_lines.extend(page_lines)
        
        # Count the frequency of each line
        line_freq = Counter(all_lines)

        # Identify lines that occur on more than one page (likely headers/footers)
        repetitive_lines = {line for line, count in line_freq.items() if count > 1}

        # Reassemble text without repetitive lines
        filtered_text = '\n'.join(line for line in all_lines if line not in repetitive_lines)

        return filtered_text

st.title('PDF Text Extractor')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file.getvalue())
    st.write("Extracted Text:")
    st.text_area("Text", text, height=300)