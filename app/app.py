
# Main application file for Government Tender Tracker & Bid-Match Recommender

import streamlit as st
import pandas as pd
import base64
import os
import sys
import logging
import pickle

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules from different folders
from data_collection.scraper import scrape_cppp_tenders, scrape_gem_tenders, get_all_tenders
from data_processing.processor import extract_text_from_pdf, extract_key_details
from recommendation.matcher import train_vectorizer, get_tender_vectors, match_profile_to_tenders
from notification.notifier import send_email_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data"
PROFILE_DIR = os.path.join(DATA_DIR, "profiles")
TENDERS_FILE = os.path.join(DATA_DIR, "tenders.pkl")
VECTORIZER_FILE = os.path.join(DATA_DIR, "vectorizer.pkl")

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)

# --------------------------------
# Streamlit UI Functions
# --------------------------------

def load_data():
    """Load tenders data or create if not exists"""
    if os.path.exists(TENDERS_FILE):
        return pd.read_pickle(TENDERS_FILE)
    else:
        return get_all_tenders()

def load_vectorizer():
    """Load TF-IDF vectorizer or create if not exists"""
    if os.path.exists(VECTORIZER_FILE):
        with open(VECTORIZER_FILE, "rb") as f:
            return pickle.load(f)
    else:
        tenders_df = load_data()
        return train_vectorizer(tenders_df)

def save_uploaded_file(uploaded_file):
    """Save an uploaded file to disk"""
    file_path = os.path.join(PROFILE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def get_file_download_link(df, filename, text):
    """Generate a link to download a dataframe as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# --------------------------------
# Main Streamlit App
# --------------------------------

def main():
    # Page title and description
    st.set_page_config(page_title="Government Tender Tracker", page_icon="📊", layout="wide")
    
    st.title("Government Tender Tracker & Bid-Match Recommender")
    st.markdown("""
    Find the perfect government tenders for your business! This application helps you:
    * Track tenders from various government portals
    * Match tenders to your company profile
    * Get instant recommendations based on your capabilities
    """)
    
    # Initialize session state variables if not exists
    if "tenders_df" not in st.session_state:
        st.session_state.tenders_df = load_data()
    
    if "vectorizer" not in st.session_state:
        st.session_state.vectorizer = load_vectorizer()
    
    if "profile_text" not in st.session_state:
        st.session_state.profile_text = ""
    
    if "match_results" not in st.session_state:
        st.session_state.match_results = None
    
    if "notification_email" not in st.session_state:
        st.session_state.notification_email = ""
    
    if "match_threshold" not in st.session_state:
        st.session_state.match_threshold = 0.3
    
    # Create sidebar
    with st.sidebar:
        st.header("Options")
        
        # Refresh data button
        if st.button("Refresh Tender Data"):
            with st.spinner("Fetching latest tenders..."):
                st.session_state.tenders_df = get_all_tenders()
                st.session_state.vectorizer = train_vectorizer(st.session_state.tenders_df)
            st.success(f"Loaded {len(st.session_state.tenders_df)} tenders!")
        
        st.divider()
        
        # Company profile upload/input
        st.subheader("Company Profile")
        profile_option = st.radio("Select profile input method:", ["Text Input", "Upload Document"])
        
        if profile_option == "Text Input":
            st.session_state.profile_text = st.text_area(
                "Enter your company profile and capabilities:", 
                st.session_state.profile_text,
                height=200
            )
        else:
            uploaded_file = st.file_uploader("Upload company profile (PDF, DOC, TXT)", type=["pdf", "docx", "txt"])
            if uploaded_file:
                with st.spinner("Processing uploaded profile..."):
                    file_path = save_uploaded_file(uploaded_file)
                    if uploaded_file.type == "application/pdf":
                        st.session_state.profile_text = extract_text_from_pdf(file_path)
                    elif uploaded_file.type == "text/plain":
                        st.session_state.profile_text = uploaded_file.getvalue().decode("utf-8")
                    else:
                        st.warning("Document format not fully supported. Only text content will be extracted.")
                        # In a real app, you'd add DOCX handling here with python-docx
                        st.session_state.profile_text = "Sample profile text for demonstration"
                    
                    st.success("Profile uploaded successfully!")
        
        st.divider()
        
        # Matching options
        st.subheader("Matching Options")
        st.session_state.match_threshold = st.slider(
            "Match threshold score:", 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.match_threshold,
            step=0.05
        )
        
        # Notification options
        st.subheader("Notifications")
        st.session_state.notification_email = st.text_input(
            "Email for notifications:", 
            st.session_state.notification_email
        )
    
    # Main content area - tabs
    tab1, tab2, tab3 = st.tabs(["All Tenders", "Recommended Tenders", "Dashboard"])
    
    # Tab 1: All Tenders
    with tab1:
        st.header("Available Tenders")
        
        # Search and filter options
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("Search tenders:", "")
        with col2:
            source_filter = st.multiselect(
                "Filter by source:",
                options=st.session_state.tenders_df["source"].unique(),
                default=st.session_state.tenders_df["source"].unique()
            )
        
        # Apply filters
        filtered_df = st.session_state.tenders_df
        if search_term:
            mask = (
                filtered_df["title"].str.contains(search_term, case=False, na=False) | 
                filtered_df["description"].str.contains(search_term, case=False, na=False) |
                filtered_df["organization"].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        if source_filter:
            filtered_df = filtered_df[filtered_df["source"].isin(source_filter)]
        
        # Display tenders
        st.dataframe(
            filtered_df[["tender_id", "title", "organization", "deadline", "emd_amount", "source"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Download option
        st.markdown(
            get_file_download_link(filtered_df, "tenders.csv", "Download tenders as CSV"),
            unsafe_allow_html=True
        )
    
    # Tab 2: Recommended Tenders
    with tab2:
        st.header("Tender Recommendations")
        
        if not st.session_state.profile_text:
            st.warning("Please add your company profile in the sidebar to get recommendations.")
        else:
            # Match button
            if st.button("Match Tenders to Profile"):
                with st.spinner("Analyzing and matching tenders..."):
                    st.session_state.match_results = match_profile_to_tenders(
                        st.session_state.profile_text,
                        st.session_state.tenders_df,
                        st.session_state.vectorizer
                    )
            
            # Display match results
            if st.session_state.match_results is not None:
                # Filter by threshold
                matches_df = st.session_state.match_results[
                    st.session_state.match_results["match_score"] >= st.session_state.match_threshold
                ]
                
                if len(matches_df) > 0:
                    st.success(f"Found {len(matches_df)} matching tenders!")
                    
                    # Display matches
                    st.dataframe(
                        matches_df[["tender_id", "title", "organization", "deadline", "emd_amount", "match_score"]],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download option
                    st.markdown(
                        get_file_download_link(matches_df, "matched_tenders.csv", "Download matches as CSV"),
                        unsafe_allow_html=True
                    )
                    
                    # Send notifications option
                    if st.session_state.notification_email and st.button("Send Email Notifications"):
                        with st.spinner("Sending notifications..."):
                            sent_count = 0
                            for _, tender in matches_df.iterrows():
                                if send_email_notification(st.session_state.notification_email, tender):
                                    sent_count += 1
                            
                            st.success(f"Sent {sent_count} notification emails!")
                else:
                    st.info("No matching tenders found above the threshold score. Try lowering the threshold.")
    
    # Tab 3: Dashboard
    with tab3:
        st.header("Tender Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tenders by Source")
            source_counts = st.session_state.tenders_df["source"].value_counts()
            st.bar_chart(source_counts)
        
        with col2:
            st.subheader("Upcoming Deadlines")
            # Convert deadline to datetime
            df_copy = st.session_state.tenders_df.copy()
            df_copy["deadline"] = pd.to_datetime(df_copy["deadline"], errors="coerce")
            df_copy = df_copy.sort_values("deadline")
            
            # Only include rows with valid deadlines
            valid_deadlines = df_copy.dropna(subset=["deadline"])
            if not valid_deadlines.empty:
                deadline_counts = valid_deadlines.groupby(valid_deadlines["deadline"].dt.strftime("%Y-%m")).size()
                st.line_chart(deadline_counts)
            else:
                st.info("No valid deadline data available")
        
        # Top organizations
        st.subheader("Top Organizations by Tender Count")
        org_counts = st.session_state.tenders_df["organization"].value_counts().head(10)
        st.bar_chart(org_counts)

if __name__ == "__main__":
    main()