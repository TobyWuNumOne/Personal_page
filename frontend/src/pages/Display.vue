<template>
    <h2>顯示器</h2>
    <p>從pinia讀取到：{{ count }}</p>
</template>
<script setup>
    import { storeToRefs } from 'pinia';
    import { useCounterStore } from '@/stores/counter';

    //在storeToRefs(useCounterStore())回傳出來的資料型態中尋找{ count }{}中的count屬性的值
    const { count } = storeToRefs(useCounterStore());
    console.log(count);
</script>
