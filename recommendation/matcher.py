# recommendation/matcher.py
# Recommendation system for matching company profiles to tenders

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle
import os
import logging

logger = logging.getLogger(__name__)

# Constants
DATA_DIR = "data"
VECTORIZER_FILE = os.path.join(DATA_DIR, "vectorizer.pkl")

def train_vectorizer(tenders_df):
    """
    Train a TF-IDF vectorizer on tender descriptions
    """
    logger.info("Training TF-IDF vectorizer...")
    
    # Combine title and description for better context
    texts = tenders_df["title"] + " " + tenders_df["description"].fillna("")
    
    # Create and fit vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    vectorizer.fit(texts)
    
    # Save vectorizer for later use
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VECTORIZER_FILE, "wb") as f:
        pickle.dump(vectorizer, f)
    
    return vectorizer

def get_tender_vectors(tenders_df, vectorizer):
    """
    Convert tender descriptions to TF-IDF vectors
    """
    texts = tenders_df["title"] + " " + tenders_df["description"].fillna("")
    return vectorizer.transform(texts)

def match_profile_to_tenders(profile_text, tenders_df, vectorizer):
    """
    Match a company profile against available tenders
    Returns tenders with similarity scores
    """
    logger.info("Matching profile to tenders...")
    
    # Get tender vectors
    tender_vectors = get_tender_vectors(tenders_df, vectorizer)
    
    # Convert profile to vector
    profile_vector = vectorizer.transform([profile_text])
    
    # Calculate similarity scores
    sim_scores = cosine_similarity(profile_vector, tender_vectors).flatten()
    
    # Add scores to tenders dataframe
    result_df = tenders_df.copy()
    result_df["match_score"] = sim_scores
    
    # Sort by match score (descending)
    result_df = result_df.sort_values("match_score", ascending=False)
    
    return result_df

def advanced_matching(profile_text, tenders_df, vectorizer, weights=None):
    """
    Advanced matching with weighted features
    """
    if weights is None:
        weights = {
            "title_match": 0.4,
            "description_match": 0.4,
            "organization_match": 0.2
        }
    
    # Get basic match scores
    basic_matches = match_profile_to_tenders(profile_text, tenders_df, vectorizer)
    
    # Extract key terms from profile (simplified)
    profile_terms = set(profile_text.lower().split())
    
    # Calculate additional feature scores
    result_df = basic_matches.copy()
    
    # Apply weights to get final score
    result_df["weighted_score"] = result_df["match_score"]
    
    # Sort by weighted score
    result_df = result_df.sort_values("weighted_score", ascending=False)
    
    return result_df