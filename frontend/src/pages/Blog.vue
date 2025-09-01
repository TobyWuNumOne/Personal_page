<script setup>
    import Footer from '@/components/baseic/Footer.vue';
    import Navbar from '@/components/baseic/Navbar.vue';
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div class="flex-grow bg-background-light text-text dark:bg-background-dark dark:text-text-light transition-colors duration-500 pb-4">
            <div class="container mx-auto px-4 py-12">
                <div class="max-w-4xl mx-auto">
                    <h1 class="text-4xl font-bold text-center mb-12 text-gray-800 dark:text-white">
                        部落格
                    </h1>
                    
                    <div class="space-y-8">
                        <!-- 文章卡片 1 -->
                        <article class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                            <div class="p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <div class="flex items-center space-x-2">
                                        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">技術分享</span>
                                        <span class="text-gray-500 text-sm">2025-01-01</span>
                                    </div>
                                </div>
                                <h2 class="text-2xl font-bold mb-3 text-gray-800 dark:text-white hover:text-blue-600 cursor-pointer">
                                    從 HTML 到 Vue 3：個人網站升級之路
                                </h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                                    分享我如何將傳統的 HTML/CSS 個人網站升級為現代化的 Vue 3 + Vite + Tailwind CSS 架構。
                                    從項目初始化、組件設計到部署，記錄整個升級過程中遇到的挑戰和解決方案...
                                </p>
                                <div class="flex items-center justify-between">
                                    <div class="flex space-x-2">
                                        <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Vue 3</span>
                                        <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Vite</span>
                                        <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Tailwind</span>
                                    </div>
                                    <a href="#" class="text-blue-600 hover:text-blue-800 font-medium">閱讀更多 →</a>
                                </div>
                            </div>
                        </article>

                        <!-- 文章卡片 2 -->
                        <article class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                            <div class="p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <div class="flex items-center space-x-2">
                                        <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">開發心得</span>
                                        <span class="text-gray-500 text-sm">2024-12-28</span>
                                    </div>
                                </div>
                                <h2 class="text-2xl font-bold mb-3 text-gray-800 dark:text-white hover:text-blue-600 cursor-pointer">
                                    揪團系統開發記錄
                                </h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                                    記錄開發揪團活動管理平台的過程，包括需求分析、技術選型、架構設計等。
                                    這個系統讓朋友們更容易組織和參與各種聚會活動...
                                </p>
                                <div class="flex items-center justify-between">
                                    <div class="flex space-x-2">
                                        <span class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">JavaScript</span>
                                        <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Node.js</span>
                                        <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Express</span>
                                    </div>
                                    <a href="#" class="text-blue-600 hover:text-blue-800 font-medium">閱讀更多 →</a>
                                </div>
                            </div>
                        </article>

                        <!-- 文章卡片 3 -->
                        <article class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                            <div class="p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <div class="flex items-center space-x-2">
                                        <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">學習筆記</span>
                                        <span class="text-gray-500 text-sm">2024-12-20</span>
                                    </div>
                                </div>
                                <h2 class="text-2xl font-bold mb-3 text-gray-800 dark:text-white hover:text-blue-600 cursor-pointer">
                                    Tailwind CSS 深入學習
                                </h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                                    深入探索 Tailwind CSS 的進階用法，包括自定義配置、響應式設計、暗黑模式實現等。
                                    分享一些實用的技巧和最佳實踐...
                                </p>
                                <div class="flex items-center justify-between">
                                    <div class="flex space-x-2">
                                        <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">CSS</span>
                                        <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Tailwind</span>
                                        <span class="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded">UI/UX</span>
                                    </div>
                                    <a href="#" class="text-blue-600 hover:text-blue-800 font-medium">閱讀更多 →</a>
                                </div>
                            </div>
                        </article>

                        <!-- 文章卡片 4 -->
                        <article class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                            <div class="p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <div class="flex items-center space-x-2">
                                        <span class="px-3 py-1 bg-pink-100 text-pink-800 text-sm rounded-full">生活分享</span>
                                        <span class="text-gray-500 text-sm">2024-12-15</span>
                                    </div>
                                </div>
                                <h2 class="text-2xl font-bold mb-3 text-gray-800 dark:text-white hover:text-blue-600 cursor-pointer">
                                    開發者的日常生活
                                </h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                                    分享作為一個開發者的日常生活，包括學習新技術的心得、工作中遇到的有趣問題，
                                    以及如何在技術學習和生活之間找到平衡...
                                </p>
                                <div class="flex items-center justify-between">
                                    <div class="flex space-x-2">
                                        <span class="px-2 py-1 bg-pink-100 text-pink-800 text-xs rounded">生活</span>
                                        <span class="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded">心得</span>
                                    </div>
                                    <a href="#" class="text-blue-600 hover:text-blue-800 font-medium">閱讀更多 →</a>
                                </div>
                            </div>
                        </article>
                    </div>

                    <!-- 分頁 -->
                    <div class="flex justify-center mt-12">
                        <nav class="flex items-center space-x-2">
                            <button class="px-3 py-2 text-gray-500 hover:text-gray-700 disabled:opacity-50" disabled>
                                上一頁
                            </button>
                            <button class="px-3 py-2 bg-blue-600 text-white rounded">1</button>
                            <button class="px-3 py-2 text-gray-500 hover:text-gray-700">2</button>
                            <button class="px-3 py-2 text-gray-500 hover:text-gray-700">3</button>
                            <button class="px-3 py-2 text-gray-500 hover:text-gray-700">
                                下一頁
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script>
export default {
    name: 'Blog'
}
</script>

<style scoped>
/* 限制文字行數 */
.line-clamp-3 {
    display: -webkit-box;
    line-clamp: 3;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
