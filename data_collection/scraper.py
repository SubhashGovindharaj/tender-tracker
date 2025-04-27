# data_collection/scraper.py
# Web scraping module for government tender portals

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import pickle

logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data"
TENDERS_FILE = os.path.join(DATA_DIR, "tenders.pkl")

def scrape_cppp_tenders():
    """
    Scrape tenders from Central Public Procurement Portal (CPPP)
    Returns a dataframe with tender details
    """
    logger.info("Scraping CPPP tenders...")
    
    url = "https://etenders.gov.in/eprocure/app"
    try:
        # In a real implementation, you might need to navigate through multiple pages
        # This is a simplified version for demonstration
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Extract tender info (this will need to be customized based on actual website structure)
        tenders = []
        
        # Demo data since actual scraping depends on site structure
        # In a real implementation, you'd parse the HTML to extract this info
        demo_tenders = [
            {
                "tender_id": "CPPP-2025-001",
                "title": "Supply of IT Equipment for Government Offices",
                "organization": "Ministry of Electronics and IT",
                "deadline": "2025-05-15",
                "emd_amount": "₹150,000",
                "description": "Supply and installation of computers, printers and networking equipment",
                "source": "CPPP",
                "url": "https://etenders.gov.in/eprocure/app?tender_id=CPPP-2025-001"
            },
            {
                "tender_id": "CPPP-2025-002",
                "title": "Development of MIS System for Public Distribution",
                "organization": "Food Corporation of India",
                "deadline": "2025-05-20",
                "emd_amount": "₹200,000",
                "description": "Design and development of management information system for tracking public distribution operations",
                "source": "CPPP",
                "url": "https://etenders.gov.in/eprocure/app?tender_id=CPPP-2025-002"
            }
        ]
        
        tenders.extend(demo_tenders)
        return pd.DataFrame(tenders)
    
    except Exception as e:
        logger.error(f"Error scraping CPPP: {str(e)}")
        return pd.DataFrame()

def scrape_gem_tenders():
    """
    Scrape tenders from Government e-Marketplace (GeM)
    Returns a dataframe with tender details
    """
    logger.info("Scraping GeM tenders...")
    
    url = "https://bidplus.gem.gov.in/all-bids"
    try:
        # In a real implementation, you'd need to navigate through pages
        # This is a simplified version for demonstration
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Demo data since actual scraping depends on site structure
        demo_tenders = [
            {
                "tender_id": "GEM-2025-B-001",
                "title": "Annual Maintenance Contract for Data Center",
                "organization": "National Informatics Centre",
                "deadline": "2025-05-10",
                "emd_amount": "₹300,000",
                "description": "Comprehensive maintenance of servers, storage and network infrastructure",
                "source": "GeM",
                "url": "https://bidplus.gem.gov.in/bid/GEM-2025-B-001"
            },
            {
                "tender_id": "GEM-2025-B-002",
                "title": "Smart City IoT Infrastructure Development",
                "organization": "Smart Cities Mission",
                "deadline": "2025-05-25",
                "emd_amount": "₹500,000",
                "description": "Development of IoT sensors and analytics platform for traffic management, waste management and public safety",
                "source": "GeM",
                "url": "https://bidplus.gem.gov.in/bid/GEM-2025-B-002"
            },
            {
                "tender_id": "GEM-2025-B-003",
                "title": "Cloud Migration Services for Government Applications",
                "organization": "Ministry of Railways",
                "deadline": "2025-06-05",
                "emd_amount": "₹250,000",
                "description": "Migration of legacy applications to cloud infrastructure with data security and performance optimization",
                "source": "GeM",
                "url": "https://bidplus.gem.gov.in/bid/GEM-2025-B-003"
            }
        ]
        
        return pd.DataFrame(demo_tenders)
    
    except Exception as e:
        logger.error(f"Error scraping GeM: {str(e)}")
        return pd.DataFrame()

def get_all_tenders():
    """
    Aggregate tenders from all sources and save to pickle file
    """
    logger.info("Aggregating tenders from all sources...")
    
    # Get tenders from different sources
    cppp_tenders = scrape_cppp_tenders()
    gem_tenders = scrape_gem_tenders()
    
    # Combine all tenders
    all_tenders = pd.concat([cppp_tenders, gem_tenders], ignore_index=True)
    
    # Save tenders to pickle file
    os.makedirs(DATA_DIR, exist_ok=True)
    all_tenders.to_pickle(TENDERS_FILE)
    
    return all_tenders