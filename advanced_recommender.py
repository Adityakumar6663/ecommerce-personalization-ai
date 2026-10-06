import pandas as pd
import streamlit as st
from datetime import datetime

# ==============================
# Extended Product Catalog
# ==============================
products = pd.DataFrame([
    {"product_id": 1, "name": "Bluetooth Earbuds Pro", "category": "Electronics", "price": 1800, "rating": 4.5, "brand": "Noise",
     "feature_tags": ["wireless", "audio", "bluetooth", "portable", "noise-cancelling"], "quality": "good", "material": "plastic", "durability": "medium"},
    
    {"product_id": 2, "name": "Smart Watch Fitness", "category": "Electronics", "price": 2500, "rating": 4.2, "brand": "Boat",
     "feature_tags": ["fitness", "watch", "bluetooth", "health-tracking"], "quality": "good", "material": "metal", "durability": "high"},
    
    {"product_id": 3, "name": "Running Shoes Pro", "category": "Fashion", "price": 2200, "rating": 4.8, "brand": "Puma",
     "feature_tags": ["sports", "comfortable", "lightweight", "running", "durable"], "quality": "excellent", "material": "mesh", "durability": "high"},
    
    {"product_id": 4, "name": "Gaming Mouse RGB", "category": "Electronics", "price": 1200, "rating": 4.6, "brand": "Redragon",
     "feature_tags": ["gaming", "wireless", "ergonomic", "high-precision"], "quality": "good", "material": "plastic", "durability": "medium"},
    
    {"product_id": 5, "name": "Cotton T-Shirt Premium", "category": "Fashion", "price": 700, "rating": 4.1, "brand": "HRX",
     "feature_tags": ["casual", "comfortable", "cotton", "breathable"], "quality": "good", "material": "cotton", "durability": "medium"},
    
    {"product_id": 6, "name": "Portable Speaker Premium", "category": "Electronics", "price": 3200, "rating": 4.7, "brand": "JBL",
     "feature_tags": ["sound", "portable", "bluetooth", "waterproof", "bass"], "quality": "excellent", "material": "plastic", "durability": "high"},
    
    {"product_id": 7, "name": "Laptop Stand Ergonomic", "category": "Electronics", "price": 1500, "rating": 4.4, "brand": "Portronics",
     "feature_tags": ["portable", "ergonomic", "work", "adjustable"], "quality": "good", "material": "aluminum", "durability": "high"},
    
    {"product_id": 8, "name": "Yoga Mat Premium", "category": "Fitness", "price": 999, "rating": 4.3, "brand": "Decathlon",
     "feature_tags": ["fitness", "exercise", "lightweight", "non-slip"], "quality": "good", "material": "rubber", "durability": "medium"},
    
    {"product_id": 9, "name": "Wireless Charging Pad", "category": "Electronics", "price": 1100, "rating": 4.4, "brand": "Belkin",
     "feature_tags": ["wireless", "charging", "fast-charge", "portable"], "quality": "good", "material": "plastic", "durability": "medium"},
    
    {"product_id": 10, "name": "Sports Backpack", "category": "Fashion", "price": 1800, "rating": 4.6, "brand": "Puma",
     "feature_tags": ["sports", "durable", "comfortable", "lightweight", "water-resistant"], "quality": "excellent", "material": "polyester", "durability": "high"},
    
    {"product_id": 11, "name": "Noise Cancelling Headphones", "category": "Electronics", "price": 4500, "rating": 4.9, "brand": "Sony",
     "feature_tags": ["audio", "wireless", "noise-cancelling", "premium"], "quality": "excellent", "material": "plastic", "durability": "high"},
    
    {"product_id": 12, "name": "Gym Duffel Bag", "category": "Fashion", "price": 1200, "rating": 4.3, "brand": "Decathlon",
     "feature_tags": ["sports", "durable", "spacious", "lightweight"], "quality": "good", "material": "polyester", "durability": "high"},
])

# ==============================
# User Browsing History (Simulated)
# ==============================
user_browsing_history = {
    "user_id": 101,
    "name": "Aditya Kumar",
    "habit": ["Electronics", "Fashion", "Fitness"],
    "favorite_categories": ["Electronics", "Fashion", "Fitness"],
    "preferred_price_range": (800, 3500),
    "preferred_brands": ["Noise", "Boat", "Puma", "HRX", "Sony", "JBL"],
    "required_features": ["wireless", "comfortable", "lightweight", "durable"],
    "quality_preference": "good",
    "material_preference": ["mesh", "metal", "polyester", "aluminum"],
    "browsing_history": [1, 3, 4, 6, 10],  # product_ids viewed
    "purchase_history": [5, 8],  # product_ids purchased
    "avg_rating_preference": 4.3,
    "budget_sensitivity": "medium"
}

# ==============================
# Scoring Functions
# ==============================
def product_matches_query(product, query_words):
    """Check if product matches user's search query"""
    text = (product["name"] + " " + product["category"] + " " + " ".join(product["feature_tags"])).lower()
    match_count = 0
    for word in query_words:
        if word.lower() in text:
            match_count += 1
    return match_count > 0, match_count

def in_price_range(price, min_price, max_price):
    """Check if product is within user's budget"""
    return min_price <= price <= max_price

def category_match(product_category, favorite_categories):
    """Score: Category preference match"""
    return 1.0 if product_category in favorite_categories else 0.3

def brand_match(product_brand, preferred_brands):
    """Score: Brand preference match"""
    return 1.0 if product_brand in preferred_brands else 0.5

def feature_match(product_tags, required_features):
    """Score: Feature alignment with user preferences"""
    score = 0
    product_tags_text = " ".join(product_tags).lower()
    for feature in required_features:
        if feature.lower() in product_tags_text:
            score += 0.25
    return min(score, 1.0)

def quality_match(product_quality, pref_quality):
    """Score: Quality preference"""
    quality_levels = {"poor": 0, "good": 1.0, "excellent": 1.5}
    pref_level = quality_levels.get(pref_quality, 1.0)
    prod_level = quality_levels.get(product_quality, 1.0)
    return min(prod_level / pref_level, 1.5)

def material_match(product_material, material_preference):
    """Score: Material preference"""
    if product_material in material_preference:
        return 1.0
    return 0.4

def browsing_affinity(product_id, browsing_history, purchase_history):
    """Score: User's historical affinity with similar products"""
    if product_id in purchase_history:
        return 1.5
    if product_id in browsing_history:
        return 1.2
    return 0.8

def rating_score(product_rating, avg_preference):
    """Score: Product rating vs user's average preference"""
    return min(product_rating / 5.0, 1.0)

def price_penalty(price, min_price, max_price):
    """Score: Price alignment (slight boost for products in budget)"""
    if min_price <= price <= max_price:
        return 1.0
    elif price < min_price:
        return 0.8
    else:
        return 0.3

# ==============================
# Advanced Recommendation Engine
# ==============================
def recommend_products_advanced(user_profile, products, query, top_n=3):
    """
    Advanced recommendation engine that considers:
    - Query matching
    - User history
    - Price preferences
    - Quality & material preferences
    - Brand loyalty
    - Rating alignment
    """
    query_words = query.lower().split()
    recommendations = []

    for _, product in products.iterrows():
        # Step 1: Query matching
        matches, match_count = product_matches_query(product, query_words)
        if query.strip() and not matches:
            continue

        # Step 2: Calculate individual scores
        category_score = category_match(product["category"], user_profile["favorite_categories"])
        brand_score = brand_match(product["brand"], user_profile["preferred_brands"])
        feature_score = feature_match(product["feature_tags"], user_profile["required_features"])
        quality_score = quality_match(product["quality"], user_profile["quality_preference"])
        material_score = material_match(product["material"], user_profile["material_preference"])
        rating_score_val = rating_score(product["rating"], user_profile["avg_rating_preference"])
        price_score = price_penalty(product["price"], user_profile["preferred_price_range"][0], user_profile["preferred_price_range"][1])
        affinity_score = browsing_affinity(product["product_id"], user_profile["browsing_history"], user_profile["purchase_history"])

        # Step 3: Query relevance boost
        query_boost = 1.0 + (match_count * 0.15)

        # Step 4: Calculate weighted total score
        total_score = (
            0.20 * category_score +
            0.15 * brand_score +
            0.18 * feature_score +
            0.12 * quality_score +
            0.10 * material_score +
            0.10 * rating_score_val +
            0.10 * price_score +
            0.05 * affinity_score
        ) * query_boost

        # Habit-based boost
        if product["category"] in user_profile["habit"]:
            total_score *= 1.15

        recommendations.append({
            "product_id": product["product_id"],
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "brand": product["brand"],
            "rating": product["rating"],
            "features": product["feature_tags"],
            "quality": product["quality"],
            "material": product["material"],
            "score": round(total_score, 4),
            "reason_components": {
                "category": round(category_score, 2),
                "brand": round(brand_score, 2),
                "features": round(feature_score, 2),
                "quality": round(quality_score, 2),
                "material": round(material_score, 2),
                "rating": round(rating_score_val, 2),
                "price": round(price_score, 2),
                "affinity": round(affinity_score, 2)
            }
        })

    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    return recommendations[:top_n]

def generate_recommendation_reason(product, user_profile, user_query):
    """
    Generate a personalized reason why this product was recommended
    based on user's habits and query
    """
    reasons = []

    # Query-based reasons
    query_words = user_query.lower().split()
    for word in query_words:
        if word in product["name"].lower():
            reasons.append(f"matches your search for '{word}'")
        if word in " ".join(product["features"]).lower():
            reasons.append(f"includes the '{word}' feature you're looking for")

    # Habit-based reasons
    if product["category"] in user_profile["habit"]:
        reasons.append(f"aligns with your interest in {product['category']}")

    # Brand loyalty reason
    if product["brand"] in user_profile["preferred_brands"]:
        reasons.append(f"from {product['brand']}, a brand you trust")

    # Quality reason
    if product["quality"] == "excellent":
        reasons.append("highly rated for its superior quality")

    # Price reason
    if user_profile["preferred_price_range"][0] <= product["price"] <= user_profile["preferred_price_range"][1]:
        reasons.append("fits perfectly within your preferred budget")

    # Feature reason
    feature_match_count = sum(1 for f in user_profile["required_features"] if f in " ".join(product["features"]).lower())
    if feature_match_count > 0:
        reasons.append(f"offers {feature_match_count} of your preferred features")

    # Material reason
    if product["material"] in user_profile["material_preference"]:
        reasons.append(f"features your preferred {product['material']} material")

    # Rating reason
    if product["rating"] >= 4.5:
        reasons.append(f"highly rated by customers ({product['rating']}/5.0)")

    return " | ".join(reasons[:3]) if reasons else "Recommended based on your preferences"

# ==============================
# Streamlit UI
# ==============================
st.set_page_config(page_title="E-Commerce Personalization AI", layout="wide")

st.markdown("""
    <style>
    .header-text {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 10px;
    }
    .recommendation-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        background-color: #f9f9f9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .product-name {
        font-size: 1.3rem;
        color: #1f77b4;
        font-weight: bold;
    }
    .product-price {
        font-size: 1.2rem;
        color: #27ae60;
        font-weight: bold;
    }
    .reason-text {
        color: #555;
        font-style: italic;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-text">🛍️ E-Commerce Personalization AI Engine</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <p style="text-align: center; color: #666; font-size: 1.1rem;">
    Welcome! Tell us what you're looking for and our AI will recommend the perfect products 
    tailored to your preferences, habits, and budget.
    </p>
    """, unsafe_allow_html=True)

# User input
user_query = st.text_input(
    "What product are you interested in today?",
    placeholder="Example: wireless earbuds, running shoes, gaming mouse, fitness...",
    label_visibility="collapsed"
)

if user_query:
    # Get recommendations
    recommendations = recommend_products_advanced(user_browsing_history, products, user_query, top_n=3)

    if not recommendations:
        st.warning("❌ No matching products found. Try searching for: wireless, shoes, fitness, audio, sports, etc.")
    else:
        # Greeting
        st.success(f"✨ Hi {user_browsing_history['name']}! We found some amazing options for '{user_query}'. Here are our top 3 personalized recommendations:")

        # Display recommendations
        for idx, item in enumerate(recommendations, 1):
            with st.container():
                st.markdown(f'<div class="recommendation-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<span class="product-name">{idx}. {item["name"]}</span>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<span class="product-price">₹{item["price"]}</span>', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Brand", item["brand"])
                with col2:
                    st.metric("Rating", f"{item['rating']}/5.0")
                with col3:
                    st.metric("Quality", item["quality"].title())
                with col4:
                    st.metric("Match Score", f"{item['score']*100:.1f}%")

                st.markdown("**Features:**")
                st.markdown(f"🏷️ {', '.join(item['features'])}")

                reason = generate_recommendation_reason(item, user_browsing_history, user_query)
                st.markdown(f'<p class="reason-text"><strong>💡 Why we recommended this:</strong> {reason}</p>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        st.info("💳 Ready to purchase? Click 'Add to Cart' in our store to proceed with checkout!")

else:
    st.info("👉 Start by typing a product name or category you're interested in (e.g., wireless, shoes, fitness)")
    st.markdown("---")
    st.markdown("**Popular searches:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🎧 Wireless"):
            st.session_state.query = "wireless"
    with col2:
        if st.button("👟 Running Shoes"):
            st.session_state.query = "running shoes"
    with col3:
        if st.button("💪 Fitness"):
            st.session_state.query = "fitness"
    with col4:
        if st.button("🎮 Gaming"):
            st.session_state.query = "gaming"
    with col5:
        if st.button("🎵 Audio"):
            st.session_state.query = "audio"
