import os, json, time
import hashlib, uuid
from instruction_prompts import task_instructions
from parse_instruction_output import task_parsers
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser

class SyntheticDataGenerator:
    def __init__(self, embed_model, llm, task_list, max_gen_attempts=2, output_dir="./syth_dataset"):
        self.embed_model = embed_model
        self.llm = llm
        self.task_list = task_list
        self.output_dir = output_dir
        self.parser = SemanticSplitterNodeParser(buffer_size=1, embed_model=self.embed_model)
        self._ensure_output_dir_exists()
        self.max_gen_attempts = max_gen_attempts
        self.parse_attempt_counters = {}

    def _ensure_output_dir_exists(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_random_hash(self):
        random_uuid = uuid.uuid4()
        hash_object = hashlib.sha256(random_uuid.bytes)
        return hash_object.hexdigest()

    def generate_synthetic_data(self, documents, num_generate=1, specific_context_instruction=''):
        print("Parsing documents...")
            
        nodes = self.parser.get_nodes_from_documents(documents, show_progress=False)
        # the corpus will be the same for all tasks, only need to save it once
        if not os.path.exists(os.path.join(self.output_dir, f"corpus.json")):
            corpus = {node.node_id: node.text for node in nodes}
            with open(os.path.join(self.output_dir, f"corpus.json"), 'w', encoding='utf-8') as f:
                json.dump(corpus, f, ensure_ascii=False, indent=2)
        print(f"Number of nodes: {len(nodes)}")
        for task in self.task_list:
            self._process_task(task, nodes, num_generate, specific_context_instruction)

    def _process_task(self, task, nodes, num_generate, specific_context_instruction):
        print(f"  Processing {task}...")
        # corpus = {}
        collection = {}
        output_path = os.path.join(self.output_dir, f"dataset_{task}.json")
        
        for node_counter, node in enumerate(nodes):
            self._process_node(task, node, num_generate, specific_context_instruction, corpus, collection)
            if node_counter % max(5, int(len(nodes) / 10)) == 0 or node_counter == len(nodes) - 1:
                self._save_to_file(output_path, collection)
                # self._save_to_file(corpus_path, corpus)
                print(f"    Processed {node_counter+1}/{len(nodes)} nodes...")
                corpus = {}
                collection = {}

    def _process_node(self, task, node, num_generate, specific_context_instruction, corpus, collection):
        # Reset counter for new node
        node_key = f"{task}_{node.metadata['filename']}"
        self.parse_attempt_counters[node_key] = 0
        
        instruct_prompt = task_instructions[task]
        parser = task_parsers[task]
        prompt = instruct_prompt.format(text=node.text, num_generate=num_generate, specific_context_instruction=specific_context_instruction)
        
        while True:
            response = self.llm.complete(prompt)
            clean_response = parser(response.text)
            
            if clean_response == []:
                if self._handle_failed_parse(task, node):
                    break
                continue
            else:
                self._handle_successful_parse(clean_response, node, task, corpus, collection)
                break

    def _handle_failed_parse(self, task, node):
        node_key = f"{task}_{node.metadata['filename']}"
        self.parse_attempt_counters[node_key] += 1
        
        if self.parse_attempt_counters[node_key] == self.max_gen_attempts:
            print(f"    Failed to parse {task} for {node.metadata['filename']}...")
            return True
        return False

    def _handle_successful_parse(self, clean_response, node, task, corpus, collection):
        if isinstance(clean_response, str):
            clean_response = [clean_response]

        hashes = [self.generate_random_hash() for _ in range(len(clean_response))]
        
        corpus[node.node_id] = node.text
        for i in range(len(hashes)):
            collection[hashes[i]] = {
                'response': clean_response[i],
                'hash_id': hashes[i],
                'relevant_doc': node.node_id,
                'task': task
            }

    def _save_to_file(self, file_path, data):
        # Load existing data if file exists
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # Merge new data with existing data (preserving uniqueness)
        merged_data = {**existing_data, **data}
        
        # Save merged data back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)


# TEST one task
# from instruction_prompts import task_instructions
# from parse_instruction_output import task_parsers
# from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser

# def generate_random_hash():
#     import hashlib
#     import uuid
#     random_uuid = uuid.uuid4()
#     hash_object = hashlib.sha256(random_uuid.bytes)
#     return hash_object.hexdigest()

# task_list = [
#  'socratic_questioning',
#  'question_answering_generation_from_facts',
#  'story_composition',
#  'grammar_error_correction',
#  'unethical_behavior_at_workplace',
#  'fact_to_conversation',
#  'word_definition',
#  'text_completion',
#  'fact_verification',
#  'ner_fill-in-the-blank',
#  'fill_in_the_blank',
#  'writing_article_from_outline',
#  'ask_for_law',
#  'paraphrasing_classification',
#  'most_relevant_passage',
#  'support_classification',
#  'explain_behavior'
#  ]

# def test_one_task(llm, task, node, specific_content_instruction='',num_generate=1):
#     response = llm.complete(task_instructions[task].format(text=node.text, specific_context_instruction=specific_content_instruction, num_generate=num_generate))
#     # print(task_instructions[task].format(text=node.text, specific_context_instruction='', num_generate=1))
#     clean_response = task_parsers[task](response.text)
#     return response, clean_response


# print("Parsing documents...")
# parser = SemanticSplitterNodeParser(buffer_size=1, embed_model=uvu_policy_manual_embed_model)
# nodes = parser.get_nodes_from_documents(final_policy_docs[:10], show_progress=False)
# print(f"Number of nodes: {len(nodes)}")

# %load_ext autoreload
# %autoreload 2
# from instruction_prompts import task_instructions
# from parse_instruction_output import task_parsers
# task_idx = 3
# response, parsed_response = test_one_task(llm, task_list[task_idx], nodes[5], '', 1)
# print(task_list[task_idx])
# print(response.text)
# print()
# print('-'*100)
# print()
# parsed_response


