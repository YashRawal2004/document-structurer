
# **AI-Powered Document Structurer**

An AI-backed solution designed to transform **unstructured PDF documents** (resumes, invoices, forms, reports, etc.) into **granular, structured Excel outputs**.
It leverages **OpenAI (GPT-4o)** for intelligent parsing and **Streamlit** for an interactive UI.

---

## 🚀 **Features**



* **Context Retention**
  Stores narrative text, side notes, and additional insights in a dedicated **Comments** field.

* **100% Data Capture**
  No information is skipped, summarized, or ignored — everything is preserved.

* **Formatted Excel Export**
  Generates a `.xlsx` file with auto-adjusted columns, wrapped text, clean formatting, and styled headers.

---

## 📂 **Project Structure**

```text
DOCUMENT_CAPTURER/
├── .venv/               # Virtual environment managed by uv
├── app.py               # Main Streamlit application
├── pyproject.toml       # Project metadata & dependencies (uv)
├── uv.lock              # Lockfile for dependency versions
├── .python-version      # Python version pin
├── requirements.txt     # Packages
└── README.md            # Project documentation
```

---

## 🛠️ **Installation & Setup**

This project uses **uv** for fast dependency management and environment setup.

### **Prerequisites**

* Python **3.10+**
* **uv** package manager
  Install via pip:

  ```bash
  pip install uv
  ```
* An **OpenAI API Key**

---

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/your-username/document-capturer.git
cd document-capturer
```

---

### **Step 2: Install Dependencies**

`uv` will automatically create `.venv` and install dependencies from `uv.lock`.

```bash
uv sync
```

---

### **Step 3: Run the Application**

Use `uv run` to ensure the virtual environment and dependencies load correctly:

```bash
uv run streamlit run app.py
```

The app starts at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 📖 **Usage Guide**

1. **Enter OpenAI API Key**
   Add your API key in the Streamlit sidebar.
   *(Keys are NOT stored anywhere.)*

2. **Upload PDF Document**
   Drag and drop your file (e.g., `Data Input.pdf`).

3. **Process the File**
   Click **🚀 Process Document** to extract structured data.

4. **Review & Export**
   Preview the table and click **📥 Download Formatted Excel** to export the structured `.xlsx` report.

---

## 🧩 **Tech Stack**

| Component       | Technology                |
| --------------- | ------------------------- |
| Frontend        | Streamlit                 |
| AI Processing   | LangChain + OpenAI GPT-4o |
| PDF Parsing     | pypdf                     |
| Data Formatting | Pandas + XlsxWriter       |
| Package Manager | uv                        |


