import random
import re

# Types of instructions
# - question_answering_generation_from_facts: "Using the facts given, write a question-answer pair."
#     - With and without context
# - story_composition: "Given the facts, compose them into a coherent and fascinating story."
#     - or compose them into legal summary
# - grammar_error_correction: "Tell me if the sentence is grammatical. If it is, output yes. Otherwise, correct the grammar errors."
# - unethical_behavior_at_workplace: "Write an example of unethical behavior at the workplace and explain why it is unethical."
# - fact_to_conversation: "Write a conversation based on the given facts."
# - word_definition: "Give me the definition of the word."
# - complete_the_lyrics: "Complete the lyrics."
#     - or sentence completion
# - fact_verification: "Verify if the claim is true or false based on factual knowledge. If false, explain why."
#     - might be most important
# - ner_fill-in-the-blank: "Replace the placeholders in the given text with appropriate named entities."
#     - Can be used for conversations. 
#     - Can also blank out entities
# - fill_in_the_blank: "Fill in the blank with a word or phrase."
#     - different from NER as it can be a phrase
# - writing_article_from_outline: "Expand the following outline into an article."
#     - Write outline
#     - Write article or paragraph from outline
# - ask_for_law: "Give me the laws that regulate the minimum wage for California, US."
#     - maybe RAG assist
# - paraphrasing_classification: "In this task, you need to compare the meaning of the two sentences and tell if they are the same. Output yes or no."
# - most_relevant_passage: "Given a user query, find out which of the following passages contains the answer to the query. Output the passage index."
#     - Without the answer this can be used to finetune embeddings
# - support_classification: "Does the information in the document supports the claim? You can answer \"Support\" or \"Unsupport\"."
#     - IMPORTANT
#     - Add reasoning
# - explain_behavior: "Explain human's behavior."
#     - setting up prompt will be tricky

# Others
# - antonym_relation
# - synonym_relation
# - analogy_relation
# - word_definition
# - word_usage
# - word_sense_disambiguation

# socratic_questioning = same as parse_question_answering_generation_from_facts

def parse_question_answering_generation_from_facts(output):
    output = output.replace('**', '')
    pattern = re.compile(r"Question(?: \d+)?: (.*?)(?:\n|$)Answer: (.*?)(?:\n|$)", re.DOTALL)
    matches = pattern.findall(output)
    parsed_examples = [{'question': match[0].strip(), 'answer': match[1].strip()} for match in matches]
    # parsed_examples = [(match[0].strip(), match[1].strip()) for match in matches]
    return parsed_examples

def parse_story_composition(output):
    output = output.replace('**', '')
    return {'story':output}

def parse_grammar_error_correction(output):
    output = output.replace('**', '')
    return output

def parse_fact_to_conversation(output):
    output = output.replace('**', '')
    return {'conversation': output}

def parse_word_definition(output):
    output = output.replace('**', '')
    lines = output.strip().split('\n')
    parsed_list = []
    term = None
    definition = None
    
    for line in lines:
        if line.startswith("Term:"):
            term = line.replace("Term:", "").strip()
        elif line.startswith("Definition:"):
            definition = line.replace("Definition:", "").strip()
            if term and definition:
                parsed_list.append({'Term': term, 'Definition': definition})
                # parsed_list.append((term, definition))
                term = None
                definition = None
    
    return parsed_list

def parse_text_completion(output):
    output = output.replace('**', '')
    pattern = re.compile(r"Prompt Text: (.*?)(?:\n|$)Generated Completion: (.*?)(?:\n|$)", re.DOTALL)
    matches = pattern.findall(output)
    parsed_examples = [{'prompt_text': match[0].strip(), 'generated_completion': match[1].strip()} for match in matches]
    # parsed_examples = [(match[0].strip(), match[1].strip()) for match in matches]
    return parsed_examples

def parse_fact_verification(output):
    output = output.replace('**', '')
    pattern = re.compile(r"Statement(?: \d+)?: (.*?)(?:\n|$)Answer: (.*?)\nExplanation: (.*?)\n", re.DOTALL)
    matches = pattern.findall(output)
    parsed_list = [{'statement':statement.strip(), 'answer':answer.strip(), 'explanation':explanation.strip()} for statement, answer, explanation in matches]
    # parsed_list = [(statement.strip(), answer.strip(), explanation.strip()) for statement, answer, explanation in matches]
    return parsed_list

def parse_ner_fill_in_the_blank(output):
    output = output.replace('**', '')
    output = output.replace("Correct Answers:", "Correct Answer:")
    samples = re.findall(r'Fill-in-the-Blank Sample:\n"(.*?)"\n\nCorrect Answer: (.*?) \(', output, re.DOTALL)
    parsed_list = [{'sample': sample, 'answer': answer} for sample, answer in samples]
    return parsed_list

def parse_fill_in_the_blank(output):
    output = output.replace('**', '')
    output = output.replace("Correct Answers:", "Correct Answer:")
    examples = output.strip().split("Fill-in-the-Blank Sample:")
    parsed_examples = []

    for example in examples[1:]:
        sample, correct_answers = example.split("Correct Answer:")
        sample = sample.strip().strip('"')
        correct_answers = correct_answers.strip()#.strip('"').split(", ")
        parsed_examples.append({'sample': sample, 'correct_answers': correct_answers})
        # parsed_examples.append((sample, correct_answers))
    
    return parsed_examples

def parse_writing_article_from_outline(output):
    output = output.replace('**', '')
    # Split the output at the first newline
    _, _, outline = output.partition('\n')
    # Return the outline without leading/trailing whitespace
    return {'outline',outline.strip()}

def parse_paraphrasing_classification(output):
    output = output.replace('**', '')
    pattern = r'Pair\s*\d+:\s*A\.\s*"(.*?)"\s*B\.\s*"(.*?)"\s*Classification:\s*(\w+)\s*Explanation:\s*(.*?)(?=\n\nPair|\n\n$)'
    matches = re.findall(pattern, output, re.DOTALL)
    result = []
    for a, b, classification, explanation in matches:
        result.append({'a': a.strip(), 'b': b.strip(), 'classification': classification.strip(), 'explanation': explanation.strip()})
        # result.append((a.strip(), b.strip(), classification.strip(), explanation.strip()))
    return result

def parse_most_relevant_passage(output):
    output = output.replace('**', '')
    pattern = re.compile(r"User Query(?: \d+)?: (.*?)(?:\n|$)Relevant Passage: (.*?)(?:\n|$)", re.DOTALL)
    matches = pattern.findall(output)
    parsed_examples = [{'user_query': match[0].strip(), 'relevant_passage': match[1].strip()} for match in matches]
    # parsed_examples = [(match[0].replace('"', '').strip(), match[1].replace('"', '').strip()) for match in matches]
    return parsed_examples

def parse_support_classification(output):
    output = output.replace('**', '')
    pattern = r'Statement:\s*"(.+?)"\s*Classification:\s*(\w+)\s*Justification:\s*(.*?)\s*(?=Statement:|$)'
    matches = re.findall(pattern, output, re.DOTALL)
    all_results =[]
    for statement, classification, justification in matches:
        result = {}
        result['Statement'] = statement.strip()
        result['Classification'] = classification.strip()
        result['Justification'] = justification.strip()
        all_results.append(result)
    return all_results


all_parsers = {"socratic_questioning": parse_question_answering_generation_from_facts,
               "question_answering_generation_from_facts": parse_question_answering_generation_from_facts,
               "story_composition": parse_story_composition,
               "grammar_error_correction": parse_grammar_error_correction,
               "fact_to_conversation": parse_fact_to_conversation,
               "word_definition": parse_word_definition,
               "text_completion": parse_text_completion,
               "fact_verification": parse_fact_verification,
               "ner_fill-in-the-blank": parse_question_answering_generation_from_facts,
               "fill_in_the_blank": parse_question_answering_generation_from_facts,
               "writing_article_from_outline": parse_writing_article_from_outline,
               "paraphrasing_classification": parse_paraphrasing_classification,
               "most_relevant_passage": parse_most_relevant_passage,
               "support_classification": parse_support_classification,
               }
