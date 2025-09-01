<template>
    <div class="counter">
        <h2>計數器</h2>
        <p>{{ counter.count }}</p>
        <button @click="counter.increment">+1</button>
        <button @click="counter.decrement">-1</button>
    </div>
</template>
<script setup>
    import { useCounterStore } from '@/stores/counter';
    const counter = useCounterStore();
</script>
