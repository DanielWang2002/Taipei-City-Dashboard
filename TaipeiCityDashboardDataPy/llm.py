from llama_cpp import Llama	
import torch




class LLM():
	def __init__(self) -> None:
		self.llm = Llama(model_path="/Users/zhouchenghan/vue-project/Taipei-City-Dashboard/TaipeiCityDashboardDataPy/model/Phi 3 mini 128k instruct.gguf",
			n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
			n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
			n_gpu_layers=35, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
			)
		
	
		self.prompt ='Q: What are the names of the days of the week? A:'
		
	def text_generate(self,prompt):
	

		output = self.llm(
		f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
		max_tokens=256,  # Generate up to 256 tokens
		stop=["<|end|>"], 
		echo=True,  # Whether to echo the prompt
		)
	
		print(output["choices"][0]["text"])




if __name__ == "__main__":
	llm = LLM()
	prompt ="role:你叫做王昱翔，你喜歡生魚片、目前是中興大學的研究生、居住於屏東萬丹、有一台貨車 Q:你是誰？ A: "
	file_path ='/Users/zhouchenghan/vue-project/Taipei-City-Dashboard/TaipeiCityDashboardDataPy/db/conten.txt'
	


	llm.text_generate(prompt=prompt)
