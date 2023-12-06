import pickle
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore")

class MaliciousActivityPredictor:
    def __init__(self, model_path):
        """
        Initializes the predictor with the given model.

        Parameters:
        model_path (str): Path to the saved model pickle file.
        """
        with open(model_path, 'rb') as file:
            self.model, self.label_encoders = pickle.load(file)

    def parse_log_data(self, log_data):
        """
        Parses the log data and extracts features for the model.
        """
        log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3} - (\w+) - (.+)'
        match = re.match(log_pattern, log_data)

        if match:
            _, log_level, message = match.groups()

            username_match = re.search(r'user (\w+)', message)
            username = username_match.group(1) if username_match else 'unknown'

            action_type_match = re.search(r'(\w+) attempt', message)
            action_type = action_type_match.group(1) if action_type_match else 'other'

            status = 'failed' if 'failed' in message or log_level in ['WARNING', 'ERROR'] else 'success'

            return [log_level, username, action_type, status]

        return ['unknown', 'unknown', 'other', 'failed']  # Default values if log pattern does not match


    def predict_malicious_activity(self, log_data):
        """
        Predicts whether the activity is malicious based on the given log data.

        Parameters:
        log_data (str): A string containing the log information.

        Returns:
        bool: True if the activity is predicted to be malicious, False otherwise.
        """
        try:
            features_list = self.parse_log_data(log_data)
            if not features_list:
                print("Unable to parse log data")
                return False  # Unable to parse log data

            features = np.zeros((1, 4))

            for i, (feature, value) in enumerate(zip(['Log Level', 'Username', 'Action Type', 'Status'], features_list)):
                try:
                    features[0, i] = self.label_encoders[feature].transform([value])[0]
                except ValueError:
                    features[0, i] = -1  # Fallback for unseen labels

            prediction = self.model.predict(features)
            return prediction[0] == 1  # Assuming 1 represents malicious

        except Exception as e:
            print(f"Error in predicting malicious activity: {e}")
            return False

# Test usage:
# predictor = MaliciousActivityPredictor('model.pkl')
# data = "2023-12-04 23:49:10,003 - WARNING - Multiple failed login attempts from ('192.168.1.10', 56835)"
# data_ma = "2023-12-04 23:39:48,022 - INFO - Received command from ('127.0.0.1', 56785): login admin admin123"
# is_malicious = predictor.predict_malicious_activity(data)
# print(f"Is Malicious: {is_malicious}")
