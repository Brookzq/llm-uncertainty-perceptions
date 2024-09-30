This is the official code of the paper titled _Perceptions of Linguistic Uncertainty by Language Models and Humans_, accepted at EMNLP 2024 Main.


**Abstract**: 
_Uncertainty expressions_ such as 'probably' or 'highly unlikely' are pervasive in human language.
While prior work has established that there is population-level agreement in terms of how humans interpret these expressions, there has been little inquiry into the abilities of language models to interpret such expressions. 
In this paper, we investigate how language models map linguistic expressions of uncertainty to numerical responses. 
Our approach assesses whether language models can employ theory of mind in this setting: 
understanding the uncertainty of another agent about a particular statement, independently of the model's own certainty about that statement. 
Unexpectedly, we find that 8 out of 10 models are able to map uncertainty expressions to probabilistic responses in a human-like manner. 
However, we observe systematically different behavior depending on whether a statement is actually true or false. 
This sensitivity indicates that language models are substantially more susceptible to bias based on their prior knowledge (as compared to humans). 
These findings raise important questions and have broad implications for human-AI and AI-AI communication.

## Datasets 

In this section, we list the datasets used to run the model experiments. The provided files are structured as CSV files, each row containing information about the `statement_type`,`name` and `gender` of the speaker, as well as the corresponding `pronouns`. Each row corresponds to a combination of `name`, `uncertainty_expression`, `statement`.


- Non-verifiable dataset: [./data/non-verifiable.csv](./data/non-verifiable.csv)
- Verifiable dataset: 
    - [60 statements based on the trivia multiple choice question-answering dataset](./data/verifiable.csv)
    - [200 statements based on the easy subset of AI2-Arc dataset](./data/verifiable_ai2arc-easy.csv)
    - [200 statements based on the challenge subset of AI2-Arc dataset](./data/verifiable_ai2arc-challenge.csv)




