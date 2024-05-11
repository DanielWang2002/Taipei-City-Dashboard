<template>
	<div class="content">
		<div class="content-header">
			<div class="icon-box">
				<div class="icon-1"></div>
				<div class="icon-2"></div>
				<div class="icon-3"></div>
				<div class="icon-4"></div>
			</div>
		</div>
		<div class="message-div">
			<div v-for="message in messages" :key="message.id" class="message">
				<div class="message-content">
					<span class="material-icons-round">{{
						message.inputStatus
					}}</span>
					<p>{{ message.text }}</p>
				</div>
			</div>
		</div>

		<div class="input-area">
			<div class="text-div">
				<textarea
					class="text-area"
					placeholder="Ask something"
					v-model="newMessage"
					@keyup.enter="sendMessage"
				></textarea>
			</div>
			<div class="icon-div">
				<button
					@click="sendMessage"
					id="btn-icon"
					class="material-icons-round"
				>
					send
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import http from "../router/axios";

const messages = ref([]);
const newMessage = ref("");
const inputStatus = ref("");
async function sendMessage() {
	if (newMessage.value.trim()) {
		inputStatus.value = "person";
		const message = {
			id: messages.value.length + 1,
			text: newMessage.value,
			inputStatus: inputStatus.value,
		};
		messages.value.push(message);
		const processingMessage = newMessage.value;
		newMessage.value = "";
		await getResponse(processingMessage);
	}
}
async function getResponse(message) {
	// get response from LLM
	// inputStatus.value = "smart_toy";
	try {
		// 調用 API 並取得回應
		const response = await http.post("/llm/", {
			jsonrpc: "2.0",
			method: "GetResponseFromLLM",
			params: [5, message],
			id: 1,
		});

		// 處理 API 回應
		if (response.data.result) {
			const res = response.data;
			if (res.role == "tpe") {
				inputStatus.value = "smart_toy";
			}

			const message = {
				id: messages.value.length + 1,
				text: res.result,
				inputStatus: inputStatus.value,
			};

			messages.value.push(message);
		} else {
			console.error("API 回應中缺少結果");
		}
	} catch (error) {
		console.error("調用 API 時出錯:", error);
	}
}
</script>
<style scoped>
.content {
	background-color: rgb(226, 231, 225);
	height: 70%;
	width: 60%;
	z-index: 100;
	position: fixed; /* 使用 fixed 或 absolute 都可 */
	top: 50%; /* 設置 top 和 left 至 50% 來將容器中心對齊頁面中心 */
	left: 50%;
	transform: translate(
		-50%,
		-50%
	); /* 使用 transform 移動元素位置使其完全居中 */
	border-radius: 15px;
}

.content-header {
	width: 100%;
	height: 10%;
	background-color: rgba(
		238.00000101327896,
		243.00000071525574,
		237.0000010728
	);
	border-radius: 20px;
	box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
	margin-bottom: 20px;
}
.icon-box {
	width: 100%;
	top: 15px;
	position: absolute;
	left: 20px;
	display: flex;
}
.content-header .icon-1 {
	top: 5.5px;
	background-color: rgba(
		254.00000005960464,
		2.000000118277967,
		2.000000118277967,
		1
	);
	width: 11.442305564880371px;
	height: 12.400948524475098px;
	position: relative;
	margin-right: 4px;
}
.content-header .icon-2 {
	position: relative;
	margin-right: 4px;
	background-color: rgba(
		254.00000005960464,
		230.00000149011612,
		2.000000118277967,
		1
	);
	width: 6.241257667541504px;
	height: 28.183971405029297px;
	position: relative;
}
.content-header .icon-3 {
	top: 3px;
	position: relative;
	margin-right: 3px;
	background-color: rgba(
		75.00000312924385,
		170.0000050663948,
		39.00000147521496,
		1
	);
	width: 7.281468391418457px;
	height: 40.58491897583008px;
}
.content-header .icon-4 {
	top: 6.5px;
	position: relative;
	margin-right: 3px;
	background-color: rgba(
		9.000000413507223,
		43.00000123679638,
		144.00000661611557,
		1
	);
	width: 13.522725105285645px;
	height: 12.400948524475098px;
}
.message p {
	margin: 5px 0;
	color: black;
}
.message-div {
	width: calc(100% - 20px); /* 減去左右內距 */
	height: 80%; /* 保持高度為容器的 90% */
	background-color: rgb(226, 231, 225);
	overflow-y: auto; /* 設置垂直滾動條 */
	padding: 10px; /* 添加內距 */
	box-sizing: border-box; /* 包含內距和邊框在內的總寬度和高度 */
	transform: translate(0%, 0%); /* 使用 transform 移動元素位置使其完全居中 */
}

.message {
	background-color: #c0bfbf; /* 每個消息的背景色 */
	border-radius: 8px; /* 圓角邊框 */
	margin-bottom: 10px; /* 消息間隔 */
	padding: 8px; /* 消息內距 */
	word-wrap: break-word; /* 長單詞或 URL 自動換行 */
}
.message-content {
	display: flex; /* 使用 flex 布局 */
	align-items: center; /* 垂直居中對齊內容 */
}

.message-content .material-icons-round {
	margin-right: 10px; /* 圖標和文字之間的距離 */
}

.message p {
	margin: 0; /* 移除 p 標籤的外邊距 */
}

.text-div {
	width: 95%;
	height: 80px;
}
.text-area {
	overflow-y: hidden;
	height: 70px;
	line-height: 70px;
	padding-top: 5px;
	padding-bottom: 0;
	padding-left: 10px;
	padding-right: 10px;
	border: none;
	box-sizing: border-box;
}

.input-area {
	width: 100%;
	height: 60px;
	background-color: rgba(129, 156, 175, 1);
	position: absolute;
	bottom: 0px;
	border-radius: 15px;
	display: flex;
	justify-content: center;
	align-items: center;
}
.text-area::placeholder {
	color: rgb(218, 230, 235);
}
.material-icons-round {
	background-color: rgb(226, 231, 225);
}
#btn-icon {
	height: 200px;
	width: 100%;
}
.icon-div {
	width: 7%;
}
</style>
