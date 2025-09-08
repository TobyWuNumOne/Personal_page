<template>
    <footer
        v-show="isVisible"
        class="w-full bg-white dark:bg-background-dark text-gray-500 dark:text-gray-400 text-center py-4 border-t border-border dark:border-border-dark"
    >
        <div class="w-full max-w-screen-xl mx-auto px-4">
            <div class="sm:flex sm:items-center sm:justify-between">
                <a
                    href="#"
                    class="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse"
                >
                    <img
                        :src="theme === 'dark' ? logo : lightlogo"
                        alt="Logo"
                        class="h-8 w-20 mr-2"
                    />
                    <span
                        class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white"
                        >TaiZanTheBar</span
                    >
                </a>
                <ul
                    class="flex flex-wrap items-center mb-6 text-sm font-medium text-gray-500 sm:mb-0 dark:text-gray-400"
                >
                    <li>
                        <a href="#" class="hover:underline me-4 md:me-6"
                            >About</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:underline me-4 md:me-6"
                            >Privacy Policy</a
                        >
                    </li>

                    <li>
                        <a href="#" class="hover:underline me-4 md:me-6"
                            >Contact</a
                        >
                    </li>
                    <li>
                        <button
                            @click="toggleTheme"
                            class="me-4 md:me-6 px-2 py-2 border border-border dark:border-border-dark rounded-lg"
                        >
                            {{ theme === 'dark' ? '淺色' : '深色' }}主題
                        </button>
                    </li>
                </ul>
            </div>
            <hr
                class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8"
            />
            <span
                class="block text-sm text-gray-500 sm:text-center dark:text-gray-400"
                >© 2025 太讚了吧. All Rights Reserved.</span
            >
            <p
                class="block text-sm text-gray-500 sm:text-center dark:text-gray-400"
            >
                I Love Lia !!!!
            </p>
        </div>
    </footer>
</template>

<script setup>
    import { ref, onMounted, onUnmounted } from 'vue';
    import lightlogo from '@/assets/light-logo.png';
    import logo from '@/assets/logo.png';

    import { useTheme } from '@/composables/UseTheme.ts';
    const { theme, toggleTheme } = useTheme();

    const isVisible = ref(false);

    const handleScroll = () => {
        const scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        // 當滾動到頁面底部附近時顯示 footer（距離底部 100px 內）
        const distanceFromBottom = documentHeight - (scrollTop + windowHeight);
        isVisible.value = distanceFromBottom <= 100;
    };

    onMounted(() => {
        window.addEventListener('scroll', handleScroll);
        // 初始檢查
        handleScroll();
    });

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll);
    });
</script>

<style scoped>
    /* 移除 body 的 padding-bottom，因為 footer 不再固定在底部 */
</style>
