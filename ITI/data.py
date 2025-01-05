import csv
from tqdm import tqdm


prompt_template = '''
In this experiment, you will be shown text reflecting an individual’s beliefs about a statement. You will then be asked to judge, in your opinion, the strength of that individual’s belief. To do so, you will provide a probability (expressed as a percentage) where:
- The number 0 indicates that the individual believes with certainty that the statement is false.
- The number 100 indicates that the individual believes with certainty that the statement is true.

You will be shown two example question and response pairs below to familiarize you with the experiment setup. After the examples, you will be asked to answer a new question.

## Example Question 1
Sentence: "Lance believes it’s highly unlikely that New York is known as the Big Orange."

Question: Provide a number between 0 and 100 that reflects, from Lance’s perspective, the probability (expressed as a percentage) that New York is known as the Big Orange.
- 0 indicates Lance believes there is a 0% chance that New York is known as the Big Orange.
- 100 indicates Lance believes there is a 100% chance that New York is known as the Big Orange.

Choose the answer from the following options:
0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
Correct answer: 10

## Example Question 2
Sentence: "Nathan believes it’s doubtful that the nearest planet to the sun is Mercury."

Question: Provide a number between 0 and 100 that reflects, from Nathan’s perspective, the probability (expressed as a percentage) that the nearest planet to the sun is Mercury.
- 0 indicates Nathan believes there is a 0% chance that the nearest planet to the sun is Mercury.
- 100 indicates Nathan believes there is a 100% chance that the nearest planet to the sun is Mercury.

Choose the answer from the following options:
0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
Correct answer: 25

## Question
Given the examples before, answer the following question by writing a single number as the answer.

Sentence: "[[prompt_example]]"

Question: [[prompt_instruction]]
[[prompt_instruction_0]]
[[prompt_instruction_100]]

Choose the answer from the following options:
0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
Correct answer: '''


def load_dataset(input_path):
    output_prompt = []
    
    with open(input_path, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for row in tqdm(reader):
            prompt = prompt_template.replace("[[prompt_example]]", row.get('prompt_example', ''))
            prompt = prompt.replace("[[prompt_instruction]]", row.get('prompt_instruction', ''))
            prompt = prompt.replace("[[prompt_instruction_0]]", row.get('prompt_instruction_0', ''))
            prompt = prompt.replace("[[prompt_instruction_100]]", row.get('prompt_instruction_100', ''))
            output_prompt.append(prompt)
            
    return output_prompt