<template>
	<div class="chatroom">
		<div class="messages">
			<div v-for="message in messages" :key="message.id" class="message">
				<p>{{ message.text }}</p>
			</div>
		</div>
		<div class="input-area">
			<!-- 新增容器用於並排顯示 -->
			<input
				class="inputbar"
				v-model="newMessage"
				@keyup.enter="sendMessage"
				placeholder="Type a message..."
			/>
			<button @click="sendMessage" class="material-icons-round">
				send
			</button>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import http from "../router/axios";

const messages = ref([]);
const newMessage = ref("");

async function sendMessage() {
	if (newMessage.value.trim()) {
		const message = {
			id: messages.value.length + 1,
			text: newMessage.value,
		};
		messages.value.push(message);
		newMessage.value = "";

		try {
			// 調用 API 並取得回應
			const response = await http.post("/llm/", {
				jsonrpc: "2.0",
				method: "GetResponseFromLLM",
				params: [5, message.text],
				id: 1,
			});
			console.log(response);

			// 處理 API 回應
			if (response.data.result) {
				const llmMessage = {
					id: messages.value.length + 1,
					text: response.data.result,
				};
				messages.value.push(llmMessage);
				console.log(messages);
			} else {
				console.error("API 回應中缺少結果");
			}
		} catch (error) {
			console.error("調用 API 時出錯:", error);
		}
	}
}
</script>

<style>
.inputbar {
	color: black;
	padding: 10px; /* 文字與邊框的距離為10px */
	width: calc(100% - 10px - 10px); /* 計算寬度以適應邊距和內邊距 */
	font-size: 12px;
	height: 30px;
}
.chatroom {
	background-color: #fff;
	max-width: 600px;
	/* margin: 20px auto; */
	padding: 10px;
	border-radius: 8px;
	/* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
	height: 90%;
	width: 90%;
}

.messages {
	height: 50%;
	overflow-y: auto;
	margin-bottom: 10px;
	padding: 10px;
	background: white;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.message p {
	margin: 5px 0;
	color: black;
}

input {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 4px;
}
.material-icons-round {
	color: black;
}
.input-area {
	display: flex; /* 設置為 flex 布局 */
	align-items: center; /* 垂直居中對齊 */
}

.inputbar {
	flex-grow: 1; /* 讓 input 擴展填滿多餘空間 */
	margin-right: 10px; /* 在 button 和 input 之間添加一些空間 */
	color: black;
	padding: 10px;
	font-size: 12px;
	height: 30px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.material-icons-round {
	cursor: pointer; /* 添加指針游標，使按鈕看起來可點擊 */
	background-color: #eee; /* 為按鈕添加背景色 */
	border: none; /* 去掉邊框 */
	padding: 10px;
	border-radius: 4px;
	height: 50px; /* 確保按鈕高度與輸入框相匹配 */
	width: 50px; /* 設置按鈕寬度 */
	display: flex;
	justify-content: center;
	align-items: center;
}

.material-icons-round:hover {
	background-color: #ddd; /* 滑鼠懸停效果 */
}
</style>
