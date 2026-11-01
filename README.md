# AI-Coding-and-Debugging-Agent
# 🐞 AI Coding and Debugging Agent

### An AI-powered Python Code Analysis and Debugging Assistant

## 📌 Project Overview

**AI Coding and Debugging Agent (CodeFix AI)** is an intelligent Python-based application designed to help developers analyze Python code, identify syntax errors, detect potential bugs, and receive AI-powered debugging suggestions.

The application combines Python's built-in Abstract Syntax Tree (AST) analysis with Google's Gemini AI to provide code analysis, error explanations, corrected code, and testing suggestions.

## ✨ Features

- 🔍 **Syntax Checking:** Detects Python syntax errors using AST analysis.
- 🤖 **AI-Powered Debugging:** Uses Google Gemini AI to analyze submitted code.
- 🐛 **Bug Detection:** Identifies potential coding errors and explains problems.
- 💻 **Corrected Code:** Provides suggested corrected Python code.
- 📊 **Code Analysis:** Displays lines of code, functions, classes, and warnings.
- 🧪 **Test Case Suggestions:** Suggests test cases and expected results.
- 📂 **Python File Upload:** Upload Python `.py` files for analysis.
- 📥 **Download Reports:** Download debugging reports and corrected code.
- 🎨 **Interactive Dashboard:** Simple and user-friendly Streamlit interface.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Google Gen AI SDK
- Python AST Module
- Regular Expressions
- Python-dotenv

## 📂 Project Structure

```text
AI-Coding-and-Debugging-Agent/
│
├── app.py
│   └── Main Streamlit Application
│
├── requirements.txt
│   └── Required Python Libraries
│
├── .gitignore
│   └── Files excluded from GitHub
│
├── README.md
│   └── Project Documentation
│
└── .env
    └── API Key (Local File Only)
```

## ⚙️ Installation and Setup

Follow these steps to run the project on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kshitija20022006/AI-Coding-and-Debugging-Agent.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Coding-and-Debugging-Agent
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### Step 4: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 5: Configure Gemini API Key

1. Get your Gemini API key from Google AI Studio.
2. Create a file named `.env` in the project folder.
3. Add the following line:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your actual API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🚀 How to Use

1. Open the CodeFix AI application.
2. Upload a Python `.py` file or paste Python code into the code editor.
3. Click the **Analyze & Fix** button.
4. The application performs local Python syntax and code analysis.
5. Gemini AI analyzes the submitted code and provides a debugging report.
6. Review the errors, explanations, and suggested corrected code.
7. Explore suggested test cases and improvements.
8. Download the generated report or corrected code.

## 🧠 How It Works

The application uses two analysis methods:

### 1. Local Python Code Analysis

- Uses Python AST to parse submitted code.
- Checks for syntax errors.
- Counts lines, functions, and classes.
- Identifies selected coding warnings.

### 2. Gemini AI-Based Debugging

- Sends the submitted code and local analysis results to Gemini.
- Analyzes possible bugs.
- Explains errors in simple language.
- Suggests corrected code.
- Provides test cases and improvement recommendations.

## 🔐 API Configuration

This project requires a valid Google Gemini API key for AI-powered debugging.

Get your API key here:

https://aistudio.google.com/apikey

Keep your API key private and configure it using environment variables.

## 🎯 Project Objectives

- Make Python debugging easier and faster.
- Help developers understand coding errors.
- Provide intelligent code correction suggestions.
- Improve code quality and developer productivity.
- Demonstrate the use of Generative AI in software development.

## 🔮 Future Enhancements

- Support for multiple programming languages.
- Advanced bug detection.
- Automated code execution in a secure environment.
- Integration with GitHub repositories.
- Real-time code suggestions.
- Advanced code quality analysis.

## ⚠️ Disclaimer

The AI-generated debugging suggestions may not always be correct. Always review and test generated code before using it in production.

## 👩‍💻 Author

**Kshitija**

GitHub: https://github.com/Kshitija20022006

## ⭐ Support

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ using Python, Streamlit, and Google Gemini AI.**
