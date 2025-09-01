<script setup>
    import { useTheme } from '@/composables/UseTheme';

    const { theme, toggleTheme } = useTheme();
</script>

<template>
    <button @click="toggleTheme">切換 {{ theme }} 模式</button>
</template>
