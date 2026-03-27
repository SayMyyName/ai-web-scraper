import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are an expert data extractor.\n"
    "Extract ONLY the information that matches: {parse_description}\n\n"
    
    "Rules:\n"
    "- Return ONLY valid JSON\n"
    "- No explanations\n"
    "- No extra text\n"
    "- If nothing found, return an empty string ('').\n\n"
    "- Ensure consistent structure across all entries\n\n"
    
    "Content:\n{dom_content}"
)

model = OllamaLLM(model='qwen3:8b')

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunks in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunks, "parse_description": parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)
        
    final_results = []

    for res in parsed_results:
        try:
            data = json.loads(res)
            if isinstance(data, list):
                final_results.extend(data)
            else:
                final_results.append(data)
        except:
            continue
    
    return json.dumps(final_results)