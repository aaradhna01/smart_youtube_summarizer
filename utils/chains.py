from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def get_summary_chain(openai_api_key):
    llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain
