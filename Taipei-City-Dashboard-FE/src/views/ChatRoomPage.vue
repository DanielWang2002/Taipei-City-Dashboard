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
				<p>{{ message.text }}</p>
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
				<button @click="sendMessage" class="material-icons-round">
					send
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";

const messages = ref([]);
const newMessage = ref("");

function sendMessage() {
	if (newMessage.value.trim()) {
		const message = {
			id: messages.value.length + 1,
			text: newMessage.value,
		};
		messages.value.push(message);
		newMessage.value = "";
	}
}
</script>
<style scoped>
.content {
	background-color: rgba(
		238.00000101327896,
		243.00000071525574,
		237.0000010728
	);
	height: 500px;
	width: 500px;
	z-index: 100;
	position: relative;
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
	border-radius: 50px;
	box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
	margin-bottom: 20px;
}
.icon-box {
	width: 100%;
	top: 5px;
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
	background-color: rgba(
		238.00000101327896,
		243.00000071525574,
		237.0000010728
	);
	overflow-y: auto; /* 設置垂直滾動條 */
	padding: 10px; /* 添加內距 */
	box-sizing: border-box; /* 包含內距和邊框在內的總寬度和高度 */
}

.message {
	background-color: #c0bfbf; /* 每個消息的背景色 */
	border-radius: 8px; /* 圓角邊框 */
	margin-bottom: 10px; /* 消息間隔 */
	padding: 8px; /* 消息內距 */
	word-wrap: break-word; /* 長單詞或 URL 自動換行 */
}

.text-div {
	width: 90%;
}
.text-area {
	overflow-y: hidden;
	height: 44px;
	line-height: 44px;
	padding-top: 5px;
	padding-bottom: 0;
	padding-left: 10px;
	padding-right: 10px;
	border: none;
	box-sizing: border-box;
}

.input-area {
	width: 100%;
	height: 50px;
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
</style>
