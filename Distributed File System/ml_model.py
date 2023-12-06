import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import pickle
# Load data
df = pd.read_csv('file_system_data.csv')

# Convert categorical columns to numerical
label_encoders = {}
for column in ['Log Level', 'Username', 'Action Type', 'Status']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column].fillna('NA'))

# Split data into features and target
X = df.drop(['Timestamp', 'Malicious', 'Target', 'Source IP'], axis=1)  # Dropping Timestamp and the target column
y = df['Malicious']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Serialize and save the model to a .pkl file
with open('model.pkl', 'wb') as file:
    pickle.dump((model, label_encoders), file)

# Predict and evaluate the model
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
