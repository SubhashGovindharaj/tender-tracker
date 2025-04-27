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

## Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **BeautifulSoup4**: Web scraping
- **PDFPlumber**: PDF text extraction
- **Scikit-learn**: TF-IDF vectorization and similarity scoring
- **Pandas**: Data manipulation and analysis

## Future Enhancements

- Integration with additional state procurement portals
- Advanced NLP for better tender-profile matching
- Mobile app notifications
- Document generation for tender responses

## License

MIT License

## Author

Subhash Govindharaj