<template>
	<div ref="parentDiv" class="parentDiv" @click="showChatRoom()">
		<span>ASK something</span>
		<h3>ask for help</h3>
		<div
			v-if="showDiv"
			class="centered-div"
			:style="{ left: leftPosition }"
		>
			<p class="contered-title">顯示的內容</p>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";

const showDiv = ref(false);
const divWidth = ref(0);
const parentDiv = ref(null);

function showChatRoom() {
	showDiv.value = !showDiv.value;
}

onMounted(() => {
	divWidth.value = parentDiv.value.clientWidth;
	console.log("Div 的寬度是: ", divWidth.value);
});

const leftPosition = computed(() => {
	return `calc(${divWidth.value}px + 200px)`;
});
</script>

<style scoped>
.centered-div {
	border-radius: 50px;
	position: fixed;
	top: 50%;
	transform: translate(-50%, -50%);
	width: 300px;
	height: 300px;
	background-color: lightgray;
	border: 1px solid black;
	text-align: center;
	z-index: 100;
}
.contered-title {
	font-size: 16px;
	color: #000;
}
</style>
