import os
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_squared_error, precision_score, recall_score

# Preprocessing function to handle NaN and encoding categorical variables
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(data):
   
    X = data.drop(columns=['fraud_reported'])
    y = data['fraud_reported']

 
    # Encode categorical columns
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Impute numeric data with mean strategy
    numeric_imputer = SimpleImputer(strategy='mean')
    X[numeric_cols] = numeric_imputer.fit_transform(X[numeric_cols])

    # Impute categorical data with the most frequent value before encoding
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    X[categorical_cols] = categorical_imputer.fit_transform(X[categorical_cols])

    # Label encode categorical variables after imputation
    label_encoder = LabelEncoder()
    for col in categorical_cols:
        if col in X.columns:
            X[col] = label_encoder.fit_transform(X[col])

    k = 7  # Set the number of top features you want to select
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X, y)

    # Get the selected feature names
    selected_features = X.columns[selector.get_support()]
    print("Selected Features:", selected_features)

    return X_new,y

# Load the dataset
def load_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    return data

# Model training function
    models = {
    #'Logistic Regression': LogisticRegression(max_iter=10),
    #'Random Forest': RandomForestClassifier(),
    #'Support Vector Classifier': SVC(),
    #'Decision Tree': DecisionTreeClassifier(),
    #'K-Nearest Neighbors': KNeighborsClassifier()
}



def trmr(X_train,y_train):
    
    model=RandomForestClassifier()
    model.fit(X_train,y_train)
    print("traine completed")
    return model

# Model evaluation function
def evaluate_models(models, X_test, y_test):
    #accuracies = {}
    """for name, model in models.items():
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracies[name] = accuracy
        print(f'{name} Accuracy: {accuracy:.4f}')"""
    y_pred = models.predict(X_test)
    precision = precision_score(y_test, y_pred, average='weighted')  # Use 'binary' for binary classification
    recall = recall_score(y_test, y_pred, average='weighted')
    accuracy = accuracy_score(y_test, y_pred)

    # 10. Print Precision, Recall, Accuracy, and F1-Score
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"Accuracy: {accuracy:.2f}")

    return accuracy,precision,recall

# Main execution
def main():
    # Use a more flexible path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'media', 'insurance fraud claims.csv')
    
    # Load and preprocess data
    data = load_data(file_path)
    print(data)
    print("load is completed")
    X, y = preprocess_data(data)
    
    print('processing_completed')
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print('split completed')
    # Train the models
   
    models = trmr(X_train, y_train)
    print('traine completed')
    # Evaluate the models
    print(X_test)
    accuracy, precision, recall = evaluate_models(models, X_test, y_test)
    pred = models.predict(X_test)
    print(pred)

    conf_matrix = confusion_matrix(y_test, pred)

    plt.figure(figsize=(9, 5))
    sns.barplot(x=data['fraud_reported'], y=data['incident_severity'])
    plt.xlabel('fraud_reported')
    plt.ylabel('incident_severity')
    plt.title('fraudreport - incident_severity Count Bar Plot')
    # plt.show() # Commented out for production

    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d',
                xticklabels=models.classes_, yticklabels=models.classes_)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('Actual Labels')
    # plt.show() # Commented out for production
    
    return accuracy, precision, recall

if __name__ == "__main__":
    accuracies = main()
    print("Model Accuracies:", accuracies)

# Placeholder for future prediction functionality


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error


def prediction_value(message):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'media', 'insurance fraud claims.csv')
    
    # Load and preprocess data
   
    data = load_data(file_path)
    print('Data loaded successfully')
    
    input_df = pd.DataFrame([message])  # Wrap message in a list to create a DataFrame
    print("Input DataFrame:")
    print(input_df)
    print(input_df.dtypes)

    
    #input_df['age'] = input_df['age'].astype(float)

    feature=['policy_number','collision_type', 'incident_severity', 'authorities_contacted',
       'total_claim_amount', 'injury_claim', 'property_claim',
       'vehicle_claim']
    target='fraud_reported'

    um_encounder = LabelEncoder()
    collision_type = LabelEncoder()
    incident_severity = LabelEncoder()
    authorities_contacted = LabelEncoder()

    # Fit label encoders on the entire dataset
    #data['umbrella_limit'] = um_encounder.fit_transform(data['umbrella_limit'])
    data['collision_type'] = collision_type.fit_transform(data['collision_type'])
    data['incident_severity'] = incident_severity.fit_transform(data['incident_severity'])
    data['authorities_contacted'] = authorities_contacted.fit_transform(data['authorities_contacted'])


    # Encode the input DataFrame using correctly fitted encoders
    input_df['collision_type'] = collision_type.transform(input_df['collision_type'])
    input_df['incident_severity'] = incident_severity.transform(input_df['incident_severity'])
    input_df['authorities_contacted'] = authorities_contacted.transform(input_df['authorities_contacted'])

    # Get the selected feature names
         
    X=data[feature]
    y=data[target]

    model=RandomForestClassifier()
    model.fit(X,y)

    # Make prediction for the input sample
    prediction_score = model.predict(input_df[feature])

    # Return the predicted value
    print("Predicted value for input:", prediction_score[0])
    return (prediction_score)

def inputProcesing(input_df):

    #numeric_cols = input_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = [
         'policy_state', 'policy_csl', 'insured_sex', 
        'insured_education_level', 'insured_occupation', 'insured_hobbies',
        'insured_relationship', 'incident_date', 'incident_type', 
        'collision_type', 'incident_severity', 'authorities_contacted', 
        'incident_state', 'incident_city', 'incident_location', 
        'property_damage', 'police_report_available', 'auto_make', 
        'auto_model'
    ]

    # Applying Label Encoding to categorical columns
    le = LabelEncoder()

    for col in categorical_columns:
        input_df[col] = le.fit_transform(input_df[col].astype(object))  # Convert to string for consistency

    # Display the transformed DataFrame
    print(input_df)
    return input_df