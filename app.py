
import os
import ast
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==================================================
# 1. PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="CodeFix AI",
    page_icon="🐞",
    layout="wide"
)

load_dotenv(override=True)

# ==================================================
# 2. DASHBOARD DESIGN
# ==================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #111c35);
    color: #f8fafc;
}
.block-container {
    max-width: 1450px;
    padding-top: 25px;
}
.hero {
    background: linear-gradient(120deg, #172554, #4338ca, #6d28d9);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 22px;
}
.hero h1 {
    color: white;
    font-size: 36px;
}
.hero p {
    color: #e0e7ff;
    font-size: 16px;
}
div[data-testid="stMetric"] {
    background: #182338;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
}
div.stButton > button {
    min-height: 45px;
    border-radius: 10px;
    font-weight: bold;
}
section[data-testid="stSidebar"] {
    background: #101827;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. SIDEBAR
# ==================================================

with st.sidebar:
    st.title("🐞 CodeFix AI")
    st.caption("Your Python debugging assistant")
    st.divider()

    st.subheader("🛠️ Features")
    st.markdown("""
    - 🔍 Syntax checking
    - 🤖 AI code analysis
    - 🐛 Bug explanations
    - 💻 Corrected code
    - 🧪 Test case suggestions
    - 📥 Download reports
    """)

    st.divider()
    st.caption("Always review generated code before running it.")

# ==================================================
# 4. LOCAL PYTHON CHECKER
# ==================================================

def analyze_python_code(code):
    result = {
        "syntax": "Not checked",
        "errors": [],
        "warnings": [],
        "lines": len(code.splitlines()),
        "functions": 0,
        "classes": 0
    }

    if not code.strip():
        result["syntax"] = "Empty input"
        result["errors"].append("Please enter some Python code.")
        return result

    try:
        tree = ast.parse(code)
        result["syntax"] = "Valid Python syntax"

    except SyntaxError as exc:
        result["syntax"] = "Syntax error"
        result["errors"].append(
            f"Line {exc.lineno or '?'}: {exc.msg}"
        )
        return result

    result["functions"] = sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        for node in ast.walk(tree)
    )

    result["classes"] = sum(
        isinstance(node, ast.ClassDef)
        for node in ast.walk(tree)
    )

    for node in ast.walk(tree):

        if isinstance(node, ast.ExceptHandler) and node.type is None:
            result["warnings"].append(
                f"Line {node.lineno}: Bare except may hide errors."
            )

        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                result["warnings"].append(
                    f"Line {node.lineno}: '{node.name}' contains only pass."
                )

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                result["warnings"].append(
                    f"Line {node.lineno}: Review the use of {node.func.id}()."
                )

    result["warnings"] = list(dict.fromkeys(result["warnings"]))
    return result

# ==================================================
# 5. GEMINI AI DEBUGGING
# ==================================================

def debug_with_ai(code, local_result):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    prompt = f"""
You are an expert Python debugging assistant.

Analyze the submitted Python code.

LOCAL CHECK RESULTS:
{local_result}

SUBMITTED CODE:
```python
{code}
```

Write a complete report using these headings:

## 1. Summary
Explain what the code does.

## 2. Errors and Bugs
Identify actual bugs and explain them simply.
Include line numbers when possible.
Do not invent errors.

## 3. Corrected Code
Provide the full corrected Python code in a Python code block.
Preserve the purpose of the original program.

## 4. Changes Made
Explain each change.

## 5. Test Cases
Suggest at least three test cases and expected results when possible.
Do not claim that you ran the code.

## 6. Improvements
Suggest useful improvements.

Be accurate. If the code is already correct, say so.
Never claim you executed the code.
"""

    client = genai.Client(api_key=api_key)

    try:
        # Uses the standard Gemini generate_content API.
        # Model name is based on the recommendation in the user's API error.
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        answer = response.text

        if not answer or not answer.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return answer.strip()

    finally:
        client.close()

# ==================================================
# 6. HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🐞 CodeFix AI</h1>
    <p>Find bugs, understand errors, and improve your Python code with AI.</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 7. SESSION STATE
# ==================================================

if "source_code" not in st.session_state:
    st.session_state.source_code = '''def calculate_total(price, quantity):
    total = price * quantity
    return total

print(calculate_total(100, "2"))
'''

if "local_result" not in st.session_state:
    st.session_state.local_result = None

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

# ==================================================
# 8. CODE EDITOR
# ==================================================

left, right = st.columns([1.6, 1])

with left:
    st.subheader("📝 Python Code Editor")

    uploaded = st.file_uploader(
        "Upload a Python file",
        type=["py"]
    )

    if uploaded is not None:
        try:
            uploaded_code = uploaded.getvalue().decode("utf-8")

            if uploaded_code != st.session_state.source_code:
                st.session_state.source_code = uploaded_code
                st.session_state.local_result = None
                st.session_state.ai_result = None

        except UnicodeDecodeError:
            st.error("Could not read this file as UTF-8.")

    code = st.text_area(
        "Your code",
        key="source_code",
        height=370,
        label_visibility="collapsed",
        placeholder="Paste your Python code here..."
    )

    col1, col2 = st.columns(2)

    with col1:
        analyze_clicked = st.button(
            "🔍 Analyze & Fix",
            type="primary",
            use_container_width=True
        )

    with col2:
        clear_clicked = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state.source_code = ""
        st.session_state.local_result = None
        st.session_state.ai_result = None
        st.rerun()

with right:
    st.subheader("✨ Your AI Assistant")

    st.markdown("""
    **🔍 Syntax checking**  
    Find basic Python syntax errors.

    **🤖 AI debugging**  
    Get explanations of code problems.

    **💻 Corrected code**  
    Receive a proposed complete solution.

    **🧪 Test suggestions**  
    Learn how to test your program.

    **📥 Download**  
    Save your corrected code and report.
    """)

    st.info(
        "Local checks work independently. AI analysis requires "
        "a valid API key and an accessible Gemini model."
    )

# ==================================================
# 9. ANALYZE CODE
# ==================================================

if analyze_clicked:
    if not code.strip():
        st.warning("Please enter or upload Python code.")

    else:
        st.session_state.ai_result = None

        local_result = analyze_python_code(code)
        st.session_state.local_result = local_result

        try:
            with st.spinner("Gemini is analyzing your code..."):
                answer = debug_with_ai(code, local_result)

            st.session_state.ai_result = answer
            st.success("✅ Analysis completed successfully.")

        except Exception as exc:
            st.error("AI analysis failed.")

            with st.expander("View exact error", expanded=True):
                st.code(f"{type(exc).__name__}: {exc}")

            error_text = str(exc).lower()

            if "404" in error_text or "not found" in error_text:
                st.warning(
                    "The Gemini model may not be available for your API key. "
                    "Check the model name and availability in Google AI Studio."
                )
            elif "429" in error_text or "quota" in error_text:
                st.warning(
                    "The API quota or rate limit may have been reached."
                )
            elif "401" in error_text or "403" in error_text or "api key" in error_text:
                st.warning(
                    "Check that your Gemini API key is valid."
                )
            elif "connection" in error_text or "timeout" in error_text:
                st.warning("Check your internet connection.")

# ==================================================
# 10. LOCAL ANALYSIS RESULTS
# ==================================================

local_result = st.session_state.local_result

if local_result:
    st.divider()
    st.subheader("🧪 Local Code Analysis")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Lines of Code", local_result["lines"])
    m2.metric("Functions", local_result["functions"])
    m3.metric("Classes", local_result["classes"])
    m4.metric("Warnings", len(local_result["warnings"]))

    if local_result["syntax"] == "Valid Python syntax":
        st.success("✅ Python syntax is valid.")
    elif local_result["syntax"] == "Syntax error":
        st.error("❌ Python syntax error detected.")
    else:
        st.warning(local_result["syntax"])

    for error in local_result["errors"]:
        st.error(error)

    for warning in local_result["warnings"]:
        st.warning(warning)

# ==================================================
# 11. DISPLAY AI REPORT
# ==================================================

ai_result = st.session_state.ai_result

if ai_result:
    st.divider()
    st.subheader("🤖 AI Debugging Report")

    tab1, tab2, tab3 = st.tabs([
        "📋 Full Report",
        "💻 Corrected Code",
        "📥 Download"
    ])

    with tab1:
        st.markdown(ai_result)

    with tab2:
        match = re.search(
            r"##\s*3\.\s*Corrected Code\s*(.*?)(?=\n##\s*4\.|\Z)",
            ai_result,
            flags=re.DOTALL | re.IGNORECASE
        )

        if match:
            section = match.group(1)

            code_match = re.search(
                r"```(?:python)?[ \t]*\n(.*?)```",
                section,
                flags=re.DOTALL | re.IGNORECASE
            )

            if code_match:
                corrected_code = code_match.group(1).strip()

                st.code(corrected_code, language="python")

                st.download_button(
                    "⬇️ Download Corrected Python File",
                    data=corrected_code + "\n",
                    file_name="corrected_code.py",
                    mime="text/x-python",
                    use_container_width=True
                )
            else:
                st.markdown(section)
        else:
            st.info("See the full report for the corrected code.")

    with tab3:
        st.download_button(
            "⬇️ Download Analysis Report",
            data=ai_result,
            file_name="codefix_report.md",
            mime="text/markdown",
            use_container_width=True
        )

# ==================================================
# 12. FOOTER
# ==================================================

st.divider()
st.caption("CodeFix AI | Python Analysis and AI-Assisted Debugging")


