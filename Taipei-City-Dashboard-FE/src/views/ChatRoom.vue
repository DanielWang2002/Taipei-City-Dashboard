<template>
	<div class="chatroom">
		<div class="messages">
			<div v-for="message in messages" :key="message.id" class="message">
				<p>{{ message.text }}</p>
			</div>
		</div>
		<input
			class="inputbar"
			v-model="newMessage"
			@keyup.enter="sendMessage"
			placeholder="Type a message..."
		/>
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

<style>
.inputbar {
	color: black;
	padding: 10px; /* 文字與邊框的距離為10px */
	width: calc(100% - 10px - 10px); /* 計算寬度以適應邊距和內邊距 */
	font-size: 12px;
	height: 30px;
}
.chatroom {
	background-color: #f9f9f9;
	max-width: 600px;
	margin: 20px auto;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.messages {
	height: 300px;
	overflow-y: auto;
	margin-bottom: 20px;
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
</style>
