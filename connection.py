import csv
import os

QUESTION_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data/question.csv'
ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data/answer.csv'
QUESTION_HEADER = ['id', 'submission_time', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'question_id', 'message', 'image']


def get_all_data(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)
        all_data = [record for record in reader]
        return all_data


def save_data_in_csvfile(filename, data, headers, append=True):
    all_data = get_all_data(filename)
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in all_data:
            if not append:
                if row['id'] == data['id']:
                    row = data
            writer.writerow(row)
        if append:
            writer.writerow(data)
