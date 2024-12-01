import streamlit as st
import google.generativeai as genai
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("AI-Powered Proposal Builder Bot")
st.write("""
    This app allows you to generate detailed proposals with personalized content 
    and competitive insights using Gemini's generative AI model.
""")

# Section for user to upload CSV file containing client data
st.subheader("Upload Client Information CSV File:")

csv_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Function to send email
def send_email(proposal_content, client_email, subject="Generated Proposal"):
    try:
        # Set up the SMTP server (example for Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]
        
        # Prepare the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = client_email
        message["Subject"] = subject
        
        # Add proposal content as the email body
        message.attach(MIMEText(proposal_content, "plain"))
        
        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client_email, message.as_string())
        
        st.success(f"Proposal sent to {client_email}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Process the uploaded CSV file
if csv_file is not None:
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Ensure the CSV has the necessary columns: Client Name, Project Name, Services, Budget Range, Deadline, Email
    required_columns = ["Client Name", "Project Name", "Services", "Budget Range", "Deadline", "Email"]
    if all(col in df.columns for col in required_columns):
        
        # Loop through the clients and generate proposals
        for index, row in df.iterrows():
            client_name = row["Client Name"]
            project_name = row["Project Name"]
            services = row["Services"]
            budget_range = row["Budget Range"]
            deadline = row["Deadline"]
            client_email = row["Email"]

            # Create the prompt
            prompt = f"""
                Generate a proposal for a client named {client_name}, for a project named {project_name}. 
                The services provided include {services}. The project budget is {budget_range}, 
                and the deadline for the project is {deadline}. Provide personalized content 
                based on this information and include competitive insights.
            """

            # Button to generate proposal for each client, with a unique key based on client index
            if st.button(f"Generate Proposal for {client_name}", key=f"generate_{index}"):
                try:
                    # Load and configure the Gemini model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Generate response from the model using the generated prompt
                    response = model.generate_content(prompt)
                    
                    # Display the generated proposal in Streamlit
                    st.write(f"Generated Proposal for {client_name}:")
                    st.write(response.text)
                    
                    # Send the proposal via email
                    send_email(response.text, client_email)

                except Exception as e:
                    st.error(f"Error generating proposal for {client_name}: {e}")
    else:
        st.error(f"The uploaded CSV file is missing one or more required columns: {', '.join(required_columns)}")
else:
    st.write("Please upload a CSV file to proceed.")
