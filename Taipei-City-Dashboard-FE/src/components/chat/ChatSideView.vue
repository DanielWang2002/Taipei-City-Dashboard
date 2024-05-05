<template>
	<div @click="showChatRoom()">
		<span>ASK something</span>
		<h3>ask for help</h3>
		<div v-if="showDiv" class="centered-div">
			<p>顯示的內容</p>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
const showDiv = ref(false);
function showChatRoom() {
	showDiv.value = !showDiv.value;
}
</script>

<style scoped>
.centered-div {
	position: fixed;
	top: 50%;
	left: calc(30% + 50px); /* 將左邊位置改為 30% + 50px */
	transform: translate(-50%, -50%);
	width: 300px;
	height: 300px;
	background-color: lightgray;
	border: 1px solid black;
	text-align: center;
	z-index: 100;
}
</style>
