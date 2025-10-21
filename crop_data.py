# ---- crop_data.py ----

# UPDATED: Image paths now correctly include the 'client/' prefix
CROP_IMAGES = {
    'apple': 'images/apple.jpg',
    'banana': 'images/banana.jpg',
    'blackgram': 'images/blackgram.jpg',
    'chickpea': 'images/chickpea.jpg',
    'coconut': 'images/coconut.jpg',
    'coffee': 'images/coffee.jpg',
    'cotton': 'images/cotton.jpg',
    'grapes': 'images/grapes.jpg',
    'jute': 'images/jute.jpg',
    'kidneybeans': 'images/kidneybeans.jpg',
    'lentil': 'images/lentil.jpg',
    'maize': 'images/maize.jpg',
    'mango': 'images/mango.jpg',
    'mothbeans': 'images/mothbeans.jpg',
    'mungbean': 'images/mungbean.jpg',
    'muskmelon': 'images/muskmelon.jpg',
    'orange': 'images/orange.jpg',
    'papaya': 'images/papaya.jpg',
    'pigeonpeas': 'images/pigeonpeas.jpg',
    'pomegranate': 'images/pomegranate.jpg',
    'rice': 'images/rice.jpg',
    'watermelon': 'images/watermelon.jpg',
    'default': 'images/default.jpg'
}

CROP_DETAILS = {
    'apple': {'description': 'A temperate fruit that requires a cold winter period.', 'water': 'Moderate', 'yield': '10-20 tons/ha'},
    'banana': {'description': 'A tropical fruit that requires high humidity and rich soil.', 'water': 'High', 'yield': '30-50 tons/ha'},
    'blackgram': {'description': 'A warm-season bean that thrives in clayey loam soils.', 'water': 'Low', 'yield': '0.6-1 tons/ha'},
    'chickpea': {'description': 'A cool-season legume that grows best in well-drained soils.', 'water': 'Low', 'yield': '1-2.5 tons/ha'},
    'coconut': {'description': 'A tropical tree valued for its fruit, oil, and fiber.', 'water': 'High', 'yield': '10-15 tons/ha'},
    'coffee': {'description': 'A tropical plant that requires specific altitude and soil.', 'water': 'High', 'yield': '0.7-1.5 tons/ha'},
    'cotton': {'description': 'A key textile crop needing a long, frost-free period.', 'water': 'Moderate', 'yield': '2-3 tons/ha'},
    'grapes': {'description': 'A vine fruit grown in temperate climates worldwide.', 'water': 'Moderate', 'yield': '15-25 tons/ha'},
    'jute': {'description': 'A fiber crop requiring a warm, humid climate.', 'water': 'Very High', 'yield': '2-2.5 tons/ha'},
    'kidneybeans': {'description': 'A common bean variety that prefers warm climates.', 'water': 'Moderate', 'yield': '1.5-2.5 tons/ha'},
    'lentil': {'description': 'A cool-season pulse crop that can tolerate drought.', 'water': 'Low', 'yield': '1-1.5 tons/ha'},
    'maize': {'description': 'A versatile crop used for food and feed.', 'water': 'Moderate', 'yield': '4-6 tons/ha'},
    'mango': {'description': 'A tropical tree needing a distinct dry season to fruit.', 'water': 'Moderate', 'yield': '8-15 tons/ha'},
    'mothbeans': {'description': 'A drought-resistant legume common in arid regions.', 'water': 'Very Low', 'yield': '0.4-0.8 tons/ha'},
    'mungbean': {'description': 'A fast-growing, drought-tolerant bean grown in warm climates.', 'water': 'Low', 'yield': '0.5-1.2 tons/ha'},
    'muskmelon': {'description': 'A sweet vine fruit that loves hot, dry climates.', 'water': 'Moderate', 'yield': '15-20 tons/ha'},
    'orange': {'description': 'A citrus fruit known for its Vitamin C.', 'water': 'High', 'yield': '20-40 tons/ha'},
    'papaya': {'description': 'A tropical fruit tree that requires warmth and well-drained soil.', 'water': 'High', 'yield': '40-60 tons/ha'},
    'pigeonpeas': {'description': 'A hardy, drought-tolerant legume that grows in many soils.', 'water': 'Low', 'yield': '0.7-1.5 tons/ha'},
    'pomegranate': {'description': 'A drought-tolerant shrub preferring a semi-arid climate.', 'water': 'Moderate', 'yield': '10-15 tons/ha'},
    'rice': {'description': 'A staple food crop that thrives in high rainfall areas.', 'water': 'Very High', 'yield': '4-5 tons/ha'},
    'watermelon': {'description': 'A hydrating fruit needing a long, warm growing season.', 'water': 'High', 'yield': '25-40 tons/ha'},
    'default': {'description': 'General information not available for this crop.', 'water': 'N/A', 'yield': 'N/A'}
}

CROP_FILTER_DATA = {
    'seasons': { 'Kharif (Monsoon)': ['Rice', 'Maize', 'Jute', 'Cotton', 'Mungbean', 'Blackgram', 'Pigeonpeas', 'Mothbeans'], 'Rabi (Winter)': ['Wheat', 'Chickpea', 'Lentil', 'Kidneybeans'], 'Zaid (Summer)': ['Watermelon', 'Muskmelon', 'Papaya'], 'Any Season / Perennial': ['Grapes', 'Mango', 'Banana', 'Pomegranate', 'Orange', 'Coconut', 'Coffee', 'Apple']},
    'types': { 'Cereal': ['Rice', 'Maize', 'Wheat'], 'Fruit': ['Apple', 'Banana', 'Grapes', 'Mango', 'Muskmelon', 'Orange', 'Papaya', 'Pomegranate', 'Watermelon'], 'Legume/Pulse': ['Blackgram', 'Chickpea', 'Kidneybeans', 'Lentil', 'Mothbeans', 'Mungbean', 'Pigeonpeas'], 'Fiber': ['Cotton', 'Jute'], 'Plantation': ['Coconut', 'Coffee']}
}

