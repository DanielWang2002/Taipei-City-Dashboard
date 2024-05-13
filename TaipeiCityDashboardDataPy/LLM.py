from llama_cpp import Llama	
import torch
from sentence_transformers import SentenceTransformer, util
import pickle

class LLM():
	def __init__(self) -> None:
		self.llm = Llama(model_path="./Phi 3 mini 128k instruct.gguf",
			n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
			n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
			n_gpu_layers=35, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
			)
	
		self.prompt ='Q: What are the names of the days of the week? A:'
		self.model = SentenceTransformer("all-MiniLM-L6-v2")
		self.content_file_path = "./db/content.txt"

    # def content_embedding(self):
	def content_embedding(self):	

		contents = []

		with open(self.content_file_path,'r') as file:
			contents = file.readlines()
			
		contents_embedding = []
		for content in contents:
			contents_embedding.append(self.model.encode(content))

		with open('./db/embedding.pkl', 'wb') as pkl_file:
			pickle.dump(contents_embedding,pkl_file)
		
    
	def cos_similarity(self, user_input, top_k=3):
		contents = []

		with open(self.content_file_path,'r') as file:
			contents = file.readlines()
		
		contents_embedding = []
		
		with open('./db/embedding.pkl', 'rb') as pkl_file:
					contents_embedding = pickle.load(pkl_file)
		print(f"content embedding:{contents_embedding[0]}")


		input_embedding = self.model.encode([user_input])
		print(f"input_embedding:{input_embedding}")
		cos_scores = util.cos_sim(input_embedding, contents_embedding)[0]
		# Adjust top_k if it's greater than the number of available scores
		top_k = min(top_k, len(cos_scores))
		# Sort the scores and get the top-k indices
		top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
		# Get the corresponding context from the vault

		relevant_context = [contents[idx].strip() for idx in top_indices]
		print(f"relevant_context :{relevant_context}")

		return relevant_context

	def text_generate(self, prompt: str) -> str:
		output = self.llm(
		f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
		max_tokens=256,  # Generate up to 256 tokens
		stop=["<|end|>"], 
		echo=True,  # Whether to echo the prompt
		)
	
		print(output["choices"][0]["text"])
		return output["choices"][0]["text"].split("<|assistant|> ")[1]

if __name__ == "__main__":
	llm = LLM()
	user_input = '我的建築被列為黃單是什麼意思？'
	top_k_content = llm.cos_similarity(user_input=user_input,top_k=3)

	prompt =f"role:你會根據以DB中的內容回答問題 DB:{top_k_content} Q:{user_input} A: "

	llm.text_generate(prompt=prompt)
	# llm.content_embedding()