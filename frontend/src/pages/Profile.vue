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
                        個人資料
                    </h1>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <!-- 個人照片和基本資訊 -->
                        <div class="lg:col-span-1">
                            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 text-center">
                                <div class="w-32 h-32 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                    <span class="text-white text-4xl font-bold">CW</span>
                                </div>
                                <h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">Cody Wu</h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4">TaiZanLer</p>
                                <p class="text-gray-600 dark:text-gray-300 mb-6">Web Developer & Tech Enthusiast</p>
                                
                                <div class="space-y-2 text-sm">
                                    <div class="flex items-center justify-center space-x-2">
                                        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path>
                                        </svg>
                                        <span class="text-gray-600 dark:text-gray-300">台灣</span>
                                    </div>
                                    <div class="flex items-center justify-center space-x-2">
                                        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                                            <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path>
                                            <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
                                        </svg>
                                        <span class="text-gray-600 dark:text-gray-300">o@gmail.com</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 詳細資訊 -->
                        <div class="lg:col-span-2">
                            <div class="space-y-6">
                                <!-- 關於我 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">關於我</h3>
                                    <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
                                        我是一名熱愛技術的 Web 開發者，專注於前端開發和用戶體驗設計。
                                        喜歡學習新技術，並將它們應用到實際專案中。目前專精於 Vue.js、React 等現代前端框架，
                                        並持續探索 Web 技術的新發展。
                                    </p>
                                </div>

                                <!-- 技能 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">技能</h3>
                                    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-green-100 rounded-lg flex items-center justify-center">
                                                <span class="text-green-600 font-bold">Vue</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">Vue.js</p>
                                        </div>
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-blue-100 rounded-lg flex items-center justify-center">
                                                <span class="text-blue-600 font-bold">JS</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">JavaScript</p>
                                        </div>
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-purple-100 rounded-lg flex items-center justify-center">
                                                <span class="text-purple-600 font-bold">CSS</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">CSS/Tailwind</p>
                                        </div>
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-yellow-100 rounded-lg flex items-center justify-center">
                                                <span class="text-yellow-600 font-bold">Node</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">Node.js</p>
                                        </div>
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-gray-100 rounded-lg flex items-center justify-center">
                                                <span class="text-gray-600 font-bold">Git</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">Git</p>
                                        </div>
                                        <div class="text-center">
                                            <div class="w-16 h-16 mx-auto mb-2 bg-red-100 rounded-lg flex items-center justify-center">
                                                <span class="text-red-600 font-bold">HTML</span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">HTML5</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- 經歷 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">經歷</h3>
                                    <div class="space-y-4">
                                        <div class="border-l-4 border-blue-500 pl-4">
                                            <h4 class="font-semibold text-gray-800 dark:text-white">自由工作者</h4>
                                            <p class="text-sm text-gray-500">2023 - 現在</p>
                                            <p class="text-gray-600 dark:text-gray-300 mt-1">
                                                專注於 Web 開發專案，包括個人網站、揪團系統等。
                                            </p>
                                        </div>
                                        <div class="border-l-4 border-green-500 pl-4">
                                            <h4 class="font-semibold text-gray-800 dark:text-white">學習中</h4>
                                            <p class="text-sm text-gray-500">2022 - 2023</p>
                                            <p class="text-gray-600 dark:text-gray-300 mt-1">
                                                自學 Web 開發技術，包括前端和後端相關技術。
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                <!-- 興趣愛好 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">興趣愛好</h3>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">程式設計</span>
                                        <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">新技術學習</span>
                                        <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">開源專案</span>
                                        <span class="px-3 py-1 bg-pink-100 text-pink-800 text-sm rounded-full">設計</span>
                                        <span class="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">攝影</span>
                                        <span class="px-3 py-1 bg-gray-100 text-gray-800 text-sm rounded-full">音樂</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>
