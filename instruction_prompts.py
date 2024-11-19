import random

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

socratic_questioning = """Objective: Analyze the provided financial theory text using the Socratic method.  

Instructions:  

You will be given a passage of text related to financial theory or concepts.  
Your task is to engage in a Socratic-style analysis by asking {num_count} thoughtful, probing questions about the text to explore its meaning, implications, and potential applications.  
For each of the {num_count} question, provide an answer that reflects the intent and nuances of the financial theory, exploring both direct interpretations and deeper implications.  
Structure the {num_count} questions to encourage critical thinking and gradually deepen understanding of the text, addressing definitions, assumptions, relationships between variables, potential scenarios, and broader implications.  
Output only the Question and Answer pairs in the following format: "Question: [Your question here] Answer: [Your answer here]"  

Example:  

Financial Text:  
"The Efficient Market Hypothesis (EMH) posits that financial markets are 'informationally efficient,' meaning that asset prices reflect all available information at any given time."  

Generated Socratic Question and Answers:  

Question: What does it mean for a market to be "informationally efficient"?  
Answer: An informationally efficient market is one where asset prices immediately and accurately reflect all relevant information, leaving no opportunities for consistently achieving above-average returns through information-based strategies.  

Question: What assumptions underpin the Efficient Market Hypothesis?  
Answer: Key assumptions include that investors are rational, information is freely and quickly available to all participants, and transaction costs are negligible.   

Financial Text to Use:  
{financial_text}
"""  

question_answering_generation_from_facts="""Objective: Generate a set of synthetic financial theory questions and answers based on the factual information provided.  

Instructions:  

You will be given a paragraph containing factual information related to financial theory or concepts.  
Your task is to generate {num_count} questions that reflect inquiries about financial principles, strategies, or implications. These should include straightforward factual questions as well as more nuanced questions that explore interpretations, assumptions, or potential consequences.  
Provide concise, accurate answers based only on the information provided.  
The {num_count} questions should vary in complexity, including basic fact identification, theoretical implications, practical applications, and broader considerations.
The {num_count} questions and answers should vary in focus, depth, and length to demonstrate a range of understanding and analytical thinking.
Do not mention or reference the paragraph of information in your {num_count} questions so that they can be answered independently.
All answers should be one string without any line breaks.

Example:  

Financial Text:  
"Modern Portfolio Theory (MPT) suggests that investors can construct a portfolio that maximizes expected return for a given level of risk by combining assets with different risk-return profiles. Diversification plays a critical role in minimizing unsystematic risk, while systematic risk, inherent to the market, cannot be eliminated through diversification. The theory assumes rational behavior and efficient markets."  

Generated Questions and Answers:  

Question: What is the main goal of Modern Portfolio Theory (MPT)?  
Answer: The main goal is to construct a portfolio that maximizes expected return for a given level of risk.  

Question: How does diversification help according to MPT?  
Answer: Diversification minimizes unsystematic risk by combining assets with different risk-return profiles.   

Financial Text to Use:  
{financial_text}
"""

story_composition="""Objective: Generate a financial scenario and construct a reasonable theoretical argument based on the provided financial text.  

Instructions:  

You will be given a passage of text outlining a financial theory or principle applicable to a particular type of scenario.  
Your task is to create a fictional but plausible financial scenario involving a decision or dispute.  
You will make the argument from the perspective of an investor or financial analyst.  
Construct a coherent, theoretically sound argument using the information in the provided financial text. The argument should be well-structured, citing relevant parts of the theory or principle to support the position.  
Ensure the argument stays grounded in the provided financial text and reflects typical reasoning in financial analysis, referencing assumptions, calculations, or strategic considerations.  

Example:  

Financial Text:  
"Modern Portfolio Theory (MPT) posits that an investor can maximize returns for a given level of risk or minimize risk for a given level of return by constructing an optimized portfolio of assets. It emphasizes diversification to reduce unsystematic risk and assumes that investors are rational and markets are efficient."  

Scenario: An investor, Alice, is reviewing her portfolio, which is heavily weighted toward technology stocks. She is considering whether to diversify into bonds and other asset classes but is concerned that this might reduce her overall return.  

Generated Argument: From a financial theory perspective, Alice should diversify her portfolio to reduce unsystematic risk. According to Modern Portfolio Theory (MPT), while concentrating investments in a single sector like technology might offer high potential returns, it also exposes her to significant unsystematic risk specific to that sector. By diversifying into bonds and other asset classes, Alice can construct a portfolio that balances her desired return with a lower risk level. Diversification achieves this by including assets with different risk-return profiles and correlations. Furthermore, MPT assumes that rational investors prioritize maximizing returns for a given level of risk, and diversification is a key strategy for achieving that goal. While Alice might be concerned about potential reduced returns, MPT suggests that the trade-off between risk and return should guide her decision-making, particularly if the diversification aligns with her overall risk tolerance and financial goals.  

Financial Text to Use:
{financial_text}
"""

grammar_error_correction = """Objective: Modify the provided financial theory text by introducing slightly poor grammar, while keeping the meaning intact. The final text should still be understandable but exhibit some grammatical errors, such as awkward sentence structure, misuse of tenses, or occasional punctuation mistakes.

Instructions:

You will be given a passage of financial theory text.
Modify the text by introducing minor grammatical issues. This may include:
Misuse of verb tenses.
Incomplete or run-on sentences.
Minor punctuation errors (e.g., missing or extra commas).
Slightly awkward or incorrect sentence structure.
Ensure that while the grammar is somewhat flawed, the overall meaning of the financial theory text remains clear.
Only output the modified text without any additional information or context.
Example:

Financial Theory Text:
"According to the Efficient Market Hypothesis (EMH), stock prices reflect all available information. As a result, it is impossible to consistently achieve returns exceeding average market returns without assuming additional risk. The theory suggests that markets are inherently efficient, leaving little opportunity for arbitrage."

Modified Financial Theory Text (with slightly poor grammar):
"Accordin' to Efficient Market Hypothesis (EMH), stock price reflects all informations available. So it is impossible consistently to get returns that exceed average market return, unless taking extra risk. The theory suggesting that markets is inherently efficient, leaving not much chance for arbitrage."

Financial Theory Text to Modify:
{financial_text}
"""

fact_to_conversation = """Objective: Generate a conversation between two or more individuals discussing the theoretical implications or applications of the provided financial theory.

Instructions:

You will be given a financial theory or concept that outlines a principle, hypothesis, or framework.
Generate a dialogue between two or more individuals (e.g., colleagues, analysts, investors) discussing the theoretical implications or practical applications of the concept.
The discussion should reflect an understanding of the financial theory, including key points, potential scenarios, and how the concept might apply to specific situations in finance, investing, or economics.
The conversation should be realistic, with participants raising questions, concerns, or interpretations of the theory and its consequences.
Example:

Financial Theory:
"According to the Efficient Market Hypothesis (EMH), stock prices reflect all available information. As a result, it is impossible to consistently achieve returns exceeding average market returns without assuming additional risk. The theory suggests that markets are inherently efficient, leaving little opportunity for arbitrage."

Generated Conversation:
Alex: "I was reading about the Efficient Market Hypothesis, and it’s pretty interesting. Does it really mean that no one can consistently beat the market?"

Jamie: "Essentially, yes. The idea is that since all available information is already factored into stock prices, there’s no way to find 'hidden' opportunities without taking on more risk."

Alex: "But what about those hedge funds and famous investors who seem to outperform the market year after year? Isn’t that proof that the theory isn’t always right?"

Jamie: "It could be, but some argue that those cases might be outliers, or they’re benefiting from short-term inefficiencies. EMH is more about the broader market over the long term."

Alex: "Interesting. So, does that mean strategies like technical analysis or trying to time the market aren’t worth it?"

Jamie: "Depends on who you ask. EMH would suggest those strategies might not work consistently, but there are debates. Behavioral finance, for instance, points out that markets aren’t always perfectly rational, which could leave room for strategies to succeed in certain cases."

Financial Theory to Use:
{financial_text}
"""

word_definition = """Objective: Extract {num_count} definitions of financial theory terms from the provided financial text.

Instructions:

You will be given a financial theory text that includes specific terms and concepts relevant to finance and economics.
Identify and extract {num_count} definitions or explanations of the key financial terms used in the text.
Provide concise, clear definitions for each term, based on how the term is used within the context of the financial text.
If a term is not explicitly defined in the text, use the surrounding context to infer a reasonable definition.

Example:

Financial Text:
"In modern portfolio theory (MPT), 'beta' measures a stock's volatility relative to the market. 'Diversification' refers to spreading investments across different assets to reduce risk. 'Risk premium' is the additional return investors expect for taking on more risk compared to a risk-free asset."

Generated Definitions:

Term: Beta
Definition: A measure of a stock's volatility in relation to the overall market.

Term: Diversification
Definition: The strategy of spreading investments across different assets to reduce risk.

Term: Risk premium
Definition: The additional return investors expect above the risk-free rate for taking on more risk.

Financial Text to Use:
{financial_text}
"""

text_completion ="""Objective: Generate text completions based on provided financial content.

Instructions:

You will be given a passage about finance, economics, or investment concepts.
Your task is to split the text into several pairs of segments that demonstrate natural continuation points.
The first segment should set up a financial concept, while the second should complete the explanation.

Example:

Financial Text: "Modern Portfolio Theory suggests that investors can maximize returns while minimizing risk through diversification. By combining assets with different correlations, investors can create portfolios that offer optimal risk-adjusted returns. This fundamental principle has shaped how institutional investors approach asset allocation and risk management in contemporary finance."

Pair 1
Prompt Text: "Modern Portfolio Theory suggests that investors can maximize returns while minimizing risk through diversification. By combining assets with different correlations"

Generated Completion: "investors can create portfolios that offer optimal risk-adjusted returns. This fundamental principle has shaped how institutional investors approach asset allocation and risk management in contemporary finance."

Pair 2 ...

Financial Text to Use:
{financial_text}
"""

fact_verification = """Objective: Generate data samples for a fact verification task based on provided financial text.

Instructions:

You will be given a passage about financial concepts, markets, or economic theory.
Your task is to generate fact verification statements based on the text. These statements may be either true or false.
For each statement, provide an answer indicating whether it is true or false, and briefly explain why based on evidence from the financial text.
Ensure the explanation references specific financial details from the text to justify the answer.

Example:

Financial Text:
"The Federal Reserve uses several tools to implement monetary policy, including open market operations and setting the federal funds rate. Through open market operations, the Fed buys and sells government securities to control the money supply. The federal funds rate is the interest rate at which banks lend reserve balances to other banks overnight."

Generated Fact Verification Statements:

Statement: The Federal Reserve's only monetary policy tool is setting the federal funds rate.
Answer: False
Explanation: The text mentions multiple tools, including both open market operations and setting the federal funds rate.

Statement: Open market operations involve the Fed buying and selling government securities.
Answer: True
Explanation: The text explicitly states that open market operations involve the Fed "buys and sells government securities to control the money supply."

Financial Text to Use:
{financial_text}
"""

ner_fill_in_the_blank = """Objective: Generate data samples for a Named Entity Recognition (NER) fill-in-the-blank task based on provided financial text.

Instructions:

You will be given a passage about finance, economics, or investment concepts.
Your task is to generate sentences with specific financial entities, terms, or metrics removed and replaced with blanks (e.g., market indicators, financial instruments, institutions, ratios, etc.).
For each blank, identify the correct financial term, metric, or entity that should fill it, and provide the correct answer as a reference.
Ensure the blanks focus on key financial concepts such as market indices, financial metrics, trading terminology, or important economic indicators.
The output should be in the following format: Question: Sentence with blanks Answer: Correct terms to fill the blanks.

Example:

Financial Text:
"The S&P 500 index is widely considered the benchmark for US stock market performance. When calculating a portfolio's beta coefficient, investors compare their returns against the S&P 500's movements to measure market sensitivity."

Question: "The _________ is widely considered the benchmark for US stock market performance. When calculating a portfolio's _________, investors compare their returns against the S&P 500's movements to measure market sensitivity."
Answer: S&P 500 index, beta coefficient

Financial Text to Use:
{financial_text}
"""

fill_in_the_blank = """Objective: Generate data samples for a fill-in-the-blank task using financial phrases based on provided text.

Instructions:

You will be given a passage about finance, investments, or economic concepts.
Your task is to identify key financial phrases within the text and create sentences with these phrases removed, replaced with blanks.
Ensure that the blanks require the completion of important financial concepts, terms, or metrics to maintain the context and meaning of the original text.
Provide the correct phrases that should fill each blank as a reference.
The output should be in the following format: Question: Sentence with blanks Answer: Correct terms to fill the blanks.

Example:

Financial Text:
"The Federal Reserve uses monetary policy tools like the federal funds rate to control inflation and promote economic stability. Changes in interest rates directly affect bond yields and market liquidity."

Question: "The _________ uses _________ tools like the federal funds rate to control inflation and promote economic stability. Changes in _________ directly affect bond yields and market _________."
Answer: Federal Reserve, monetary policy, interest rates, liquidity

Financial Text to Use:
{financial_text}
"""

writing_article_from_outline = """Objective: Generate an outline based on provided financial text.

Instructions:

You will be given a passage about finance, economics, or investment concepts.
Your task is to read the financial text and create a structured outline that summarizes its key points and organizes the information logically.
The outline should include main headings, subheadings, and bullet points to capture the essential financial concepts, metrics, and principles.
Ensure that the outline reflects the hierarchy of information and highlights important definitions, market mechanics, and investment strategies mentioned in the text.

Example:

Financial Text:
"Modern Portfolio Theory (MPT) emphasizes the benefits of diversification in investment management. The theory suggests that investors can optimize their portfolios by considering both return and risk. Key components include the efficient frontier, risk-free rate, and the capital asset pricing model (CAPM). MPT demonstrates how diversification can reduce portfolio risk without necessarily sacrificing returns."

Generated Outline:
I. Modern Portfolio Theory (MPT)
   A. Core Principles
      1. Risk-return relationship
      2. Benefits of diversification
   
   B. Key Components
      1. Efficient frontier
      2. Risk-free rate
      3. CAPM

   C. Portfolio Optimization
      1. Risk reduction strategies
      2. Return maximization
      3. Diversification benefits

Financial Text to Use:
{financial_text}
"""

paraphrasing_classification = """Objective: Generate pairs of sentences based on the provided financial text and classify whether they convey the same meaning.

Instructions:

You will be given a passage about finance, economics, or investment concepts.
Your task is to create pairs of sentences derived from the financial text.
For each pair, classify whether the sentences convey the same meaning (True) or not (False).
Provide a brief explanation for your classification, highlighting the key differences or similarities in meaning.

Example:

Financial Text:
"Market capitalization represents the total value of a company's outstanding shares. It is calculated by multiplying the current share price by the total number of shares in circulation."

Generated Sentence Pairs:

Pair 1:

A. "A company's market capitalization is determined by multiplying its share price by total outstanding shares."
B. "The total value of a firm's traded shares is calculated using share price times number of shares."
Classification: True
Explanation: Both sentences describe the same method of calculating market capitalization.

Pair 2:

A. "Market capitalization reflects only the price of newly issued shares."
B. "Market capitalization represents the total value of all outstanding shares in circulation."
Classification: False
Explanation: The first sentence incorrectly limits market cap to new shares, while the second correctly describes it as including all outstanding shares.

Pair 3: ...

Financial Text to Use:
{financial_text}
"""

most_relevant_passage = """Objective: Generate a user query and identify the most relevant passage from the provided financial text in response to that query.

Instructions:

You will be given a passage about finance, investments, or economic concepts.
Your task is to formulate user queries that could arise from the financial text.
After creating the user queries, identify the most relevant passage from the text that answers or addresses the queries.
Provide the selected passage along with a brief explanation of why it is the most relevant to the user queries.

Example:

Financial Text:
"The price-to-earnings (P/E) ratio is a key valuation metric that compares a company's stock price to its earnings per share. A high P/E ratio may indicate that investors expect higher earnings growth in the future, while a low P/E ratio could suggest that a company is undervalued or has limited growth prospects."

User Query: "How do investors interpret different P/E ratio levels?"
Relevant Passage: "A high P/E ratio may indicate that investors expect higher earnings growth in the future, while a low P/E ratio could suggest that a company is undervalued or has limited growth prospects."
Explanation: This passage directly explains how to interpret both high and low P/E ratios, providing investors with crucial context for valuation analysis.

Financial Text to Use:
{financial_text}
"""

support_classification = """Objective: Generate a statement based on the provided financial text, and classify whether the statement is supported or unsupported by the text, providing justification.

Instructions:

You will be given a passage about finance, economics, or investment concepts.
Your task is to create statements that are either supported or unsupported by the financial text.
After creating the statements, classify them as Supported or Unsupported.
Provide a brief justification explaining why the statements are supported or unsupported based on the content of the financial text.

Example:

Financial Text:
"The Federal Reserve implements monetary policy through open market operations and adjustments to the federal funds rate. These tools are used to manage inflation, employment levels, and overall economic stability in the United States."

Generated Statement:
Statement: "The Federal Reserve uses cryptocurrency trading to implement monetary policy."
Classification: Unsupported
Justification: The text specifically mentions open market operations and federal funds rate adjustments as the Fed's monetary policy tools, with no mention of cryptocurrency trading.

Financial Text to Use:
{financial_text}
"""


all_questions = {"socratic_questioning": socratic_questioning,
                 "question_answering_generation_from_facts": question_answering_generation_from_facts,
                 "story_composition": story_composition,
                 "grammar_error_correction": grammar_error_correction,
                 "fact_to_conversation": fact_to_conversation,
                 "word_definition": word_definition,
                 "text_completion": text_completion,
                 "fact_verification": fact_verification,
                 "ner_fill-in-the-blank": question_answering_generation_from_facts,
                 "fill_in_the_blank": question_answering_generation_from_facts,
                 "writing_article_from_outline": writing_article_from_outline,
                 "paraphrasing_classification": paraphrasing_classification,
                 "most_relevant_passage": most_relevant_passage,
                 "support_classification": support_classification,
                 }
