import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool
import os

# Set API keys
os.environ["GOOGLE_API_KEY"] = "AIzaSyA0S7F21ExbBnR06YXkEi7aj94nWP5kJho"
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key="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"
)

class MyCustomTool(BaseTool):
    name: str = "ConversationTool"
    description: str = """Welcome to Bob, your personal shopping assistant! 🎉
Hello and thank you for visiting! I'm Bob, your friendly guide to finding the perfect products just for you. 😊

I can help you:
- Explore top-quality products across various categories.
- Provide details about the best deals and benefits.
- Share links to shop directly for the items you love. 🛒

Whether you're here for a friendly chat or ready to shop, I've got you covered! Feel free to ask about any product, and I’ll guide you with tailored suggestions.

For example:
- Ask "What are the best laptops under $1000?" 
- Say "I need running shoes for men."
- Or even, "Find me a good smartphone for photography."

Once you're ready, I'll even provide a button to shop directly! Thank you for stopping by—let's explore together! 🌟"""
    
    def _run(self, query: str) -> str:
        # Craft a friendly and engaging response based on the user query
        return f"Thank you for your query! 😊 You asked about: {query}. Let me find the best options for you right away!"

def button_tool(product: str) -> str:
    base_url = "https://www.amazon.com/s?k="
    product_url = f"{base_url}{product.replace(' ', '+')}"
    return f"""
    <div style="text-align: center; margin-top: 20px;">
        <a href="{product_url}" target="_blank">
            <button style="padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Buy {product} Now
            </button>
        </a>
    </div>
    """

# Initialize Tools
convo_tool = MyCustomTool()
button_tool_instance = Tool(
    name="ButtonTool",
    description="""Provide a clickable button linking users to a shopping page based on their input.
For example, if a user searches for a laptop, generate a button linking to Amazon's laptop search page.""",
    func=button_tool
)

# Initialize Agent
agent = initialize_agent(
    llm=llm,
    tools=[convo_tool, button_tool_instance],
    verbose=True,
    handle_parsing_errors=True
)

# Initialize session state for chat history and button visibility
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app layout
st.set_page_config(page_title="Bob - Your Shopping Assistant", page_icon="🛍️")
st.title("🛍️ Chat With Bob")
st.caption("🎉 Your Personal Shopping Assistant")

# Display a beautiful greeting message
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #007bff;">Hello there! 🌟</h2>
        <p>I'm Bob, your friendly shopping assistant. How can I help you today? Whether you're here to explore or to make a purchase, I'm here to make your experience delightful. 😊</p>
    </div>
    """,
    unsafe_allow_html=True
)

# User input
text = st.chat_input("Ask Bob anything about products or shopping...")

# Handle user input and generate response
if text:
    with st.spinner("Bob is thinking..."):
        try:
            response = agent.run(text)
            st.session_state.chat_history.append({"question": text, "response": response})

            # Check if the query is about a product
            if "buy" in text.lower() or "product" in text.lower():
                product_name = text.replace("buy", "").replace("product", "").strip()
                st.markdown(button_tool(product_name), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Sorry, something went wrong: {e}")

# Display conversation history
for chat in st.session_state.chat_history:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
            <div style="background-color: ; padding: 10px; border-radius: 5px; max-width: 70%;">
                {chat['question']} 🤓
            </div>
        </div>
        <div style="display: flex; justify-content: flex-start; margin-top: -10px; margin-bottom: 20px;">
            <div style="background-color: ; padding: 10px; border-radius: 5px; max-width: 70%;">
                🛒 Bob: {chat['response']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display the button if applicable
# if st.session_state.show_button:
#     st.markdown(button_tool(text), unsafe_allow_html=True)
