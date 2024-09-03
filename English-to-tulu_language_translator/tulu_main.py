
import numpy as np  # Import NumPy for numerical operations.
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TfidfVectorizer for converting text to TF-IDF features.
from sklearn.neighbors import NearestNeighbors  # Import NearestNeighbors for finding the nearest neighbors based on cosine similarity.
import mouth  # Import the mouth module (assumed to have a speak function).
# from mouth import speak  # Alternative import statement (commented out as not used).
from listen_1 import listen_and_print  # Import the listen_and_print function for speech recognition.

# Load data from text file
def load_data(file_path):
    # Try opening the file with UTF-8 encoding
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines from the file.
    except UnicodeDecodeError:
        # Fallback to another encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()  # Read all lines from the file with a different encoding.
    
    queries = []  # Initialize list for queries.
    responses = []  # Initialize list for responses.
    
    for line in lines:
        # Split each line by colon and ensure it has exactly two parts
        parts = line.split(":")
        if len(parts) == 2:
            query = parts[0].strip()  # Strip leading/trailing whitespace from the query.
            response = parts[1].strip()  # Strip leading/trailing whitespace from the response.
            queries.append(query)  # Add query to the queries list.
            responses.append(response)  # Add response to the responses list.
        else:
            print(f"Skipping malformed line: {line.strip()}")  # Print a message for malformed lines.
    
    return queries, responses  # Return lists of queries and responses.

# Train the model
def train_model(queries):
    vectorizer = TfidfVectorizer()  # Initialize the TF-IDF vectorizer.
    X = vectorizer.fit_transform(queries)  # Transform queries into TF-IDF features.
    model = NearestNeighbors(n_neighbors=1, metric='cosine').fit(X)  # Train the NearestNeighbors model with cosine similarity.
    return model, vectorizer  # Return the trained model and vectorizer.

# Find the best match for the input query
def find_best_match(model, vectorizer, query):
    query_vec = vectorizer.transform([query])  # Transform the input query into TF-IDF features.
    distances, indices = model.kneighbors(query_vec)  # Find the nearest neighbors.
    return indices[0][0], distances[0][0]  # Return the index and distance of the best match.

# Main function
def t_main():
    # Define the file path
    file_path = r'C:\Users\l\OneDrive\Desktop\Code\tulu_language_tranlator\tulu_data.txt'  # change the path of tulu_data.txt file
    
    # Load and prepare data
    queries, responses = load_data(file_path)  # Load data from the file.
    
    # Train model
    model, vectorizer = train_model(queries)  # Train the model with the loaded queries.

    # Initial input method selection
    input_method = input("Would you like to type your query or speak it? (t/s): ").strip().lower()
    
    while True:
        if input_method == 's':
            # Listen to user input
            user_query = listen_and_print()  # Use speech recognition to get the user's query.
            if user_query is None:
                print("Could not process your query. Please try again.")  # Handle cases where speech recognition fails.
                continue
        elif input_method == 't':
            # Get user input via typing
            user_query = input("Please type in English: ").strip()  # Get the user's query by typing.
        else:
            print("Invalid option. Please choose 'type' or 'speak'.")  # Handle invalid input options.
            input_method = input("Would you like to type your query or speak it? [t/s]: ").strip().lower()
            continue
        
        # Find the best match
        best_index, _ = find_best_match(model, vectorizer, user_query)  # Find the closest match for the user's query.
        
        # Get the corresponding response
        response = responses[best_index]  # Retrieve the response associated with the best match.
        
        # Speak the response
        mouth.speak(response)  # Use the mouth module to speak the response.
        print(f"Response: {response}")  # Print the response to the console.
        
        # Ask if the user wants to continue or terminate
        continue_query = input("Do you want to continue? [y] | press [t] to terminate: ").strip().lower()
        if continue_query == 't':
            print("Thank you for using the translator!")  # Print a thank you message if the user chooses to exit.
            break
        elif continue_query != 'y':
            print("Invalid option. Exiting.")
            break
        # If the user chooses to continue and the input method was valid, keep using the previous input method
        # and continue processing without asking for input method again.

if __name__ == "__main__":
    t_main()  # Run the main function if this script is executed.

