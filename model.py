import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the crop data from CSV file
df = pd.read_csv('crop_data.csv')

# Define feature columns (X) - all columns except 'crop_name'
X = df.drop('crop_name', axis=1)

# Define target variable (y) - the 'crop_name' column
y = df['crop_name']

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model to file
joblib.dump(model, 'crop_model.joblib')

print("Model trained and saved successfully!")
print(f"Features used: {list(X.columns)}")
print(f"Number of samples: {len(df)}")
print(f"Number of unique crops: {len(y.unique())}")