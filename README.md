# Government Tender Tracker & Bid-Match Recommender

A web-based application that automatically aggregates tender notices from government e-procurement portals and recommends relevant tenders based on company capability profiles.

## Features

- **Real-Time Tender Aggregation**: Automated ingestion of tender metadata and documents from multiple procurement portals
- **Automated Requirement Scanner**: Extraction of EMD amounts, bid deadlines, and scope details
- **Company Profile Matching**: TF-IDF based similarity scoring to flag high-potential tenders
- **Interactive Dashboard**: Search, filter, and view tender recommendations
- **Notification System**: Email alerts for matching tenders

## Project Structure

```
tender-tracker/
├── app/              # Main Streamlit application
├── data/             # Data storage directory
│   └── profiles/     # Company profiles storage
├── data_collection/  # Web scraping modules
├── data_processing/  # PDF and text processing modules
├── recommendation/   # TF-IDF recommendation system
├── notification/     # Email/SMS notification functionality
└── README.md         # Project documentation
```

## Installation & Setup

1. Clone the repository:
```
git clone https://github.com/SubhashGovindharaj/tender-tracker.git
cd tender-tracker
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
streamlit run app/app.py
```

## Usage

1. **View Tenders**: Browse and search through automatically aggregated tenders from multiple sources
2. **Add Company Profile**: Upload your company capabilities document or enter them as text
3. **Get Recommendations**: Match your profile against available tenders
4. **Setup Notifications**: Configure email notifications for high-matching tenders

## Data Sources

The application currently scrapes tender information from:
- Central Public Procurement Portal (CPPP) - https://etenders.gov.in/eprocure/app
- Government e-Marketplace (GeM) - https://gem.gov.in/ & https://bidplus.gem.gov.in/all-bids

Future Enhancements 🚀
	•	Add login/signup functionality for companies.
	•	Allow companies to edit/update their capability profiles dynamically.
	•	Implement advanced matching using AI/ML models (e.g., BERT embeddings).
	•	Add support for scraping more State-level procurement portals.
	•	Enable SMS and Email real-time alerts through Twilio and Gmail integration.
	•	Schedule scrapers to run automatically using cron jobs or cloud functions.

Tech Stack 🛠️
	•	Backend Scraping: Python, Requests, BeautifulSoup
	•	Data Processing: Pandas, PDFPlumber (for extracting PDFs)
	•	Matching Algorithms: TF-IDF, Cosine Similarity
	•	Frontend Dashboard: Streamlit
	•	Notifications: SMTP (Gmail), Twilio SMS (optional)
	•	Deployment (future): AWS / Azure / Railway.app (Streamlit sharing)

 <p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python Badge">
  <img src="https://img.shields.io/badge/Streamlit-%230E1117.svg?style=flat&logo=streamlit" alt="Streamlit Badge">
  <img src="https://img.shields.io/badge/BeautifulSoup-DataScraping-green" alt="BeautifulSoup Badge">
  <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License Badge">
</p>


## License

MIT License

## Author

Subhash Govindharaj
