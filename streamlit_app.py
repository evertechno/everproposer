import streamlit as st
import google.generativeai as genai

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("AI-Powered Proposal Builder Bot")
st.write("""
    This app allows you to generate detailed proposals with personalized content 
    and competitive insights using Gemini's generative AI model.
""")

# Section for user to input their proposal details
st.subheader("Enter your Proposal Information:")

# Text inputs for proposal-related details
client_name = st.text_input("Client Name:", "Acme Corporation")
project_name = st.text_input("Project Name:", "Next-Gen Web Development")
services = st.text_area("Services to be Provided:", "Web design, Web development, SEO optimization")
budget_range = st.text_input("Budget Range:", "$10,000 - $15,000")
deadline = st.text_input("Project Deadline:", "March 2025")

# Prompt input field for the proposal content
prompt = f"""
    Generate a proposal for a client named {client_name}, for a project named {project_name}. 
    The services provided include {services}. The project budget is {budget_range}, 
    and the deadline for the project is {deadline}. Provide personalized content 
    based on this information and include competitive insights.
"""

# Button to generate proposal
if st.button("Generate Proposal"):
    try:
        # Load and configure the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model using the generated prompt
        response = model.generate_content(prompt)
        
        # Display the generated proposal in Streamlit
        st.write("Generated Proposal:")
        st.write(response.text)
        
        # Optionally, provide additional sections (e.g., competitive data)
        st.write("\nCompetitive Insights and Suggestions:")
        st.write("Consider highlighting your unique selling points in comparison to competitors. "
                 "Use testimonials and case studies to strengthen your proposal.")
        
    except Exception as e:
        st.error(f"Error: {e}")
