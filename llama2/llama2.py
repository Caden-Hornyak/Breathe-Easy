# Load model directly
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
import torch


def run_chatbot(prompt):
    model_name="meta-llama/Llama-2-7b-chat-hf"
    access_token = "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"

    tokenizer = LlamaTokenizer.from_pretrained(model_name, use_auth_token=access_token)
    model = LlamaForCausalLM.from_pretrained(model_name, use_auth_token=access_token)

    new_pipeline = pipeline("text-generation", 
                        model=model,
                        tokenizer=tokenizer,                                 
                        torch_dtype=torch.float16, 
                        device = torch.device('cpu', index=0),
                        do_sample=True,
                        batch_size=64
                        )

    sequences = new_pipeline(prompt, 
                        temperature=0.9, 
                                    top_k=50, 
                                    top_p=0.9,
                        max_length=50)

    return sequences