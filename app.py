import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
from pypdf import PdfReader
import io

# --- 1. Data Schema Configuration ---
class DataPoint(BaseModel):
    """
    Represents a single row in the final Excel sheet.
    Captures the Key, Value, and any contextual comments.
    """
    key: str = Field(description="The specific label, header, or question found in the document text.")
    value: str = Field(description="The exact answer, data, or text detail associated with the key. Must use original wording.")
    comments: Optional[str] = Field(description="Any extra context, side notes, or formatting details relevant to this data point.")

class ExtractedData(BaseModel):
    """The collection of all extracted data points."""
    entries: List[DataPoint]

# --- 2. Helper Functions ---

def get_pdf_text(uploaded_file):
    """Extracts raw text from the uploaded PDF file."""
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def process_document(api_key, text_content):
    """
    Uses OpenAI to parse unstructured text into structured JSON 
    based on the DataPoint schema.
    """
    # Initialize the LLM
    # 'temperature=0' ensures deterministic/consistent outputs
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",  # Using a capable model for complex layout understanding
        openai_api_key=api_key
    )

    # Define the prompt to strictly follow assignment constraints
    system_prompt = """
    You are a specialized data extraction AI. Your goal is to transform unstructured PDF text into a structured Excel-ready format.
    
    **STRICT ASSIGNMENT RULES:**
    1. **100% Data Capture:** You must capture EVERY piece of information. Do not omit anything.
    2. **Original Language:** Retain the exact wording for the 'Value' field. Do not paraphrase or summarize unless absolutely necessary for format.
    3. **Key:Value Logic:** Identify logical pairings. If a text is a heading followed by a paragraph, the heading is the Key.
    4. **Context:** If there is surrounding text that provides important nuance but isn't the direct value, place it in the 'Comments' field.
    
    Analyze the input text and output a JSON object containing a list of these Key-Value-Comment entries.
    """


    # Bind the schema for structured output (forces JSON format)
    structured_llm = llm.with_structured_output(ExtractedData)

    # Create the LangChain pipeline
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Here is the document content:\n\n{text}")
    ])
    
    chain = prompt | structured_llm

    # Execute the chain
    return chain.invoke({"text": text_content})

def create_formatted_excel(dataframe):
    """
    Generates a neatly formatted Excel file using XlsxWriter.
    Includes text wrapping, bold headers, and column sizing.
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write raw data
        dataframe.to_excel(writer, index=False, sheet_name='Extracted Data')
        
        # Get workbook/worksheet objects for formatting
        workbook = writer.book
        worksheet = writer.sheets['Extracted Data']
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4F81BD',  # Professional Blue
            'font_color': 'white',
            'border': 1
        })
        
        body_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1
        })
        
        # Apply formatting to headers
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set column widths (A=Key, B=Value, C=Comments)
        worksheet.set_column('A:A', 30, body_format)
        worksheet.set_column('B:B', 50, body_format)
        worksheet.set_column('C:C', 40, body_format)
        
    return output.getvalue()

# --- 3. Streamlit UI Layout ---

st.set_page_config(page_title="AI Document Structurer", layout="wide")

st.title("🤖 AI-Powered Document Structuring")
st.markdown("""
This tool transforms unstructured PDFs into structured Excel files.
* **Extracts Key:Value pairs**
* **Captures 100% of data**
* **Preserves original wording**
""")

st.divider()

# Sidebar: Configuration
with st.sidebar:
    st.header("🔒 Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Required to run the extraction model.")
    
    st.info("Your key is used only for this session and not stored.")
    st.markdown("---")
    st.markdown("**Instructions:**\n1. Enter API Key.\n2. Upload PDF.\n3. Download Excel.")

# Main Area: File Upload
uploaded_file = st.file_uploader("Upload your 'Data Input.pdf'", type=["pdf"])

if uploaded_file:
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to proceed.")
    else:
        if st.button("🚀 Process Document", type="primary"):
            with st.spinner("Reading PDF and extracting data (this may take a moment)..."):
                try:
                    # Step 1: Get Text
                    raw_text = get_pdf_text(uploaded_file)
                    
                    # Step 2: AI Processing
                    result = process_document(api_key, raw_text)
                    
                    # Step 3: Convert to DataFrame
                    data_dicts = [item.dict() for item in result.entries]
                    df = pd.DataFrame(data_dicts)
                    
                    # Step 4: Success Feedback & Preview
                    st.success("Processing Complete!")
                    
                    st.subheader("Data Preview")
                    st.dataframe(df, use_container_width=True)
                    
                    # Step 5: Excel Generation & Download
                    excel_data = create_formatted_excel(df)
                    
                    st.download_button(
                        label="📥 Download Formatted Excel",
                        data=excel_data,
                        file_name="Structured_Output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")