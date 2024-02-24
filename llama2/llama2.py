from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import sys

model_name_or_path = "TheBloke/Llama-2-7b-Chat-GPTQ"

model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                            device_map="cuda",
                                            trust_remote_code=False,
                                            revision="gptq-4bit-128g-actorder_True",
                                            )

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

def run_chatbot(prompt):
    global model, model_name_or_path, tokenizer
    print("Chatbot",file=sys.stderr)
    

    curr_prompt = prompt
    prompt_template=f'''[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible. You take in user prompts and generate recommended activities in as little words as possible. Tell them your answer is based on their interests. Number any reccomendations you give them.
    <</SYS>>
    {curr_prompt}[/INST]

    '''

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
    response = tokenizer.decode(output[0])
    return response[response.find("[/INST]")+9:response.find('</s>')]
