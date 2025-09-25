# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Starting the model training process...")

# --- Step 1: Load the Dataset ---
# Load the dataset from a CSV file. Make sure 'Crop_recommendation.csv' is in the same folder.
try:
    df = pd.read_csv('Crop_recommendation.csv')
    print("Dataset loaded successfully.")
    print("Dataset preview:")
    print(df.head())
except FileNotFoundError:
    print("Error: 'Crop_recommendation.csv' not found. Please download it and place it in the same directory.")
    exit()

# --- Step 2: Prepare the Data ---
# Features (X) are all columns except 'label'
# Target (y) is the 'label' column (which contains the crop names)
X = df.drop('label', axis=1)
y = df['label']

print("\nFeatures (X) and Target (y) have been separated.")

# --- Step 3: Split the Data for Training and Testing ---
# We split the data into 80% for training and 20% for testing.
# random_state ensures that we get the same split every time we run the script.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Data split into training set ({len(X_train)} rows) and testing set ({len(X_test)} rows).")

# --- Step 4: Choose and Train the Model ---
# We will use the RandomForestClassifier, a powerful and reliable model for this type of task.
model = RandomForestClassifier(n_estimators=100, random_state=42)

print("\nTraining the Random Forest model...")
# The 'fit' method trains the model on our training data
model.fit(X_train, y_train)
print("Model training complete.")

# --- Step 5: Evaluate the Model ---
# We make predictions on the test data to see how well our model performs.
y_pred = model.predict(X_test)

# We calculate the accuracy by comparing the predicted labels with the true labels.
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Evaluation:")
print(f"The model's accuracy on the test data is: {accuracy * 100:.2f}%")

# --- Step 6: Save the Trained Model ---
# We save the trained model to a file so our FastAPI application can use it.
model_filename = 'crop_model.joblib'
joblib.dump(model, model_filename)

print(f"\nModel successfully trained and saved as '{model_filename}'.")
print("You can now place this file in your main application directory.")