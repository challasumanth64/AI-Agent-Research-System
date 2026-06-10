import streamlit as st
import os
import io
import markdown
from xhtml2pdf import pisa
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from agents import get_research_agent

load_dotenv()

st.set_page_config(page_title="Multi-Agent Research", layout="wide", page_icon="🔬")

st.title("🔬 Multi-Agent Research System")
st.caption("Powered by LangGraph (v1.x), Mistral AI, and Tavily Search")

# ==========================================
# PDF GENERATION FUNCTION
# ==========================================
def generate_pdf_from_markdown(md_text):
    """Converts Markdown text to a beautifully styled PDF byte stream."""
    # 1. Convert Markdown to HTML
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # 2. Wrap in a full HTML document with professional CSS styling
    html_content = f"""
    <html>
    <head>
        <style>
            @page {{
                size: a4;
                margin: 2cm;
            }}
            body {{
                font-family: Helvetica, Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333333;
            }}
            h1 {{
                color: #2c3e50;
                font-size: 22pt;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 5px;
                margin-top: 20px;
            }}
            h2 {{
                color: #2980b9;
                font-size: 16pt;
                margin-top: 15px;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 3px;
            }}
            h3 {{
                color: #2980b9;
                font-size: 13pt;
                margin-top: 10px;
            }}
            p {{
                margin-bottom: 10px;
                text-align: justify;
            }}
            ul, ol {{
                margin-bottom: 10px;
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            strong {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    # 3. Create a memory buffer to hold the PDF data
    pdf_buffer = io.BytesIO()
    
    # 4. Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    
    if pisa_status.err:
        raise Exception(f"Failed to create PDF: {pisa_status.err}")
        
    # 5. Extract the bytes and clean up
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_bytes

# ==========================================
# STREAMLIT UI
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    mistral_key = st.text_input("Mistral API Key", value=os.getenv("MISTRAL_API_KEY", ""), type="password")
    tavily_key = st.text_input("Tavily API Key", value=os.getenv("TAVILY_API_KEY", ""), type="password")
    
    if mistral_key:
        os.environ["MISTRAL_API_KEY"] = mistral_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        
    st.markdown("---")
    st.info("1. Enter API keys.\n2. Type a research question.\n3. Watch the LangGraph agent work!")

query = st.text_input(
    "📝 Enter your research question:", 
    placeholder="e.g., How is Artificial Intelligence transforming modern education?",
)

if st.button("🚀 Start LangGraph Research", type="primary"):
    if not os.getenv("MISTRAL_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("⚠️ Please provide both Mistral and Tavily API keys.")
    elif not query.strip():
        st.warning("⚠️ Please enter a research question.")
    else:
        with st.spinner("🤖 LangGraph Agent is researching, scraping, and writing..."):
            try:
                # 1. Initialize the agent
                agent = get_research_agent()
                
                # 2. Define the system instructions
                system_prompt = """You are an expert academic research assistant. 
                Your goal is to answer the user's research question comprehensively.
                
                Instructions:
                1. First, use the search tool to find relevant information and URLs.
                2. If the search results contain promising URLs, use the scrape_url tool to get deeper details from up to 2 of those URLs.
                3. Synthesize all gathered information into a final, well-structured report.
                
                Your final output MUST be formatted in Markdown with these exact sections:
                1. **Executive Summary**
                2. **Key Findings** (Use bullet points)
                3. **Detailed Analysis**
                4. **Conclusion & Future Outlook**
                
                Do not output your internal thought process in the final answer, only the formatted report."""
                
                # 3. Format messages for LangGraph
                inputs = {
                    "messages": [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=query)
                    ]
                }
                
                # 4. Invoke the agent
                result = agent.invoke(inputs)
                
                # 5. Extract the final answer (the last message in the list)
                final_report = result["messages"][-1].content
                
                st.success("✅ Research report generated successfully!")
                
                # Display the report on the screen
                st.markdown("---")
                st.markdown("### 📄 Final Research Report")
                st.markdown(final_report)
                
                # 6. Generate the PDF
                with st.spinner("📄 Generating PDF document..."):
                    pdf_bytes = generate_pdf_from_markdown(final_report)
                
                # 7. Download Button for PDF
                safe_filename = "".join(x for x in query if x.isalnum() or x in (" ", "_", "-")).rstrip()[:30]
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_bytes,
                    file_name=f"research_report_{safe_filename}.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                with st.expander("View Technical Error Details"):
                    st.exception(e)