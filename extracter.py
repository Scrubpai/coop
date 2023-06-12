import os

def extract_sections(file_path):
    with open(file_path, 'r') as file:
        transcript = file.read()

    prepared_remarks_start = transcript.find("Operator:")
    prepared_remarks_end = transcript.find("Questions & Answers:")
    prepared_remarks = transcript[prepared_remarks_start:prepared_remarks_end]

    questions_answers_start = transcript.find("Questions & Answers:")
    questions_answers_end = transcript.find("Call participants:")
    questions_answers = transcript[questions_answers_start:questions_answers_end]

    return prepared_remarks, questions_answers

def split_into_paragraphs(prepared_remarks):
    paragraphs = prepared_remarks.split('\n\n')
    return paragraphs

def walk_directory(root_dir):
    for root, dirs, files in os.walk(root_dir):
        print(f"Current directory: {root}")
        
        # Iterate over subdirectories
        for dir in dirs:
            subdir_path = os.path.join(root, dir)
            print(f"Subdirectory: {subdir_path}")
        
        # Iterate over files
        for file in files:
            file_path = os.path.join(root, file)

            prepared_remarks, questions_answers = extract_sections(file_path)
            prepared_remarks = split_into_paragraphs(prepared_remarks=prepared_remarks)

            print(f"File: {file_path}")

            print("Prepared Remarks:")
            print(prepared_remarks)

            print("\nQuestions and Answers:")
            print(questions_answers)


# Usage example
root_directory = '/Users/amirk.khandani/Documents/retriever'
walk_directory(root_directory)


