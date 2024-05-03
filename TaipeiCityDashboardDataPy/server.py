import sys

from LLM import LLM

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


def GetResponseFromLLM(topK: int, user_input: str):
	llm = LLM()
	top_k_content = llm.cos_similarity(user_input=user_input,top_k=topK)
	
	prompt =f"role:你會根據以下內容以繁體中文回答問題{top_k_content} Q:{user_input} A: "
	print(prompt, file=sys.stderr)
	return llm.text_generate(prompt=prompt)

# 建立伺服器，指定serve的地址和端口
server = SimpleJSONRPCServer(('0.0.0.0', 5555))

# 註冊函數，使其可以被遠端調用
server.register_function(GetResponseFromLLM, 'GetResponseFromLLM')

# 運行伺服器
server.serve_forever()