<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { marked } from 'marked'
    import Footer from '@/components/baseic/Footer.vue';
    import Navbar from '@/components/baseic/Navbar.vue';
    import { pb } from '@/composables/usePB'

    const loading = ref(true)
    const error = ref('')
    
    // 網站設定資料（基本資訊 + 技能）
    const siteSettings = ref(null)
    
    // 關於頁面內容
    const aboutPage = ref(null)

    // 配置 marked 選項
    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    // 將 Markdown 轉換為 HTML
    const aboutContent = computed(() => {
        if (!aboutPage.value?.content) return '';
        return marked(aboutPage.value.content);
    });

    // 載入資料
    const loadData = async () => {
        try {
            loading.value = true
            error.value = ''
            
            // 載入網站設定（含技能）
            const settingsData = await pb.collection('site_settings').getFirstListItem('', {
                expand: 'skills'
            })
            siteSettings.value = settingsData
            
            // 載入關於頁面
            const pageData = await pb.collection('pages').getFirstListItem('slug="about"')
            aboutPage.value = pageData
            
        } catch (err) {
            console.error('載入資料失敗:', err)
            error.value = '載入資料失敗，請稍後再試'
        } finally {
            loading.value = false
        }
    }

    onMounted(() => {
        loadData()
    })
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div class="flex-grow bg-background-light text-text dark:bg-background-dark dark:text-text-light transition-colors duration-500 pb-4">
            
            <!-- 載入狀態 -->
            <div v-if="loading" class="container mx-auto px-4 py-12 text-center">
                <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
                <p class="mt-4 text-gray-600 dark:text-gray-300">載入中...</p>
            </div>

            <!-- 錯誤狀態 -->
            <div v-else-if="error" class="container mx-auto px-4 py-12 text-center">
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    {{ error }}
                </div>
            </div>

            <!-- 主要內容 -->
            <div v-else class="container mx-auto px-4 py-12">
                <div class="max-w-4xl mx-auto">
                    <h1 class="text-4xl font-bold text-center mb-12 text-gray-800 dark:text-white">
                        {{ aboutPage?.title || '個人資料' }}
                    </h1>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <!-- 個人照片和基本資訊 -->
                        <div class="lg:col-span-1">
                            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 text-center">
                                <div class="w-32 h-32 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                                    <span class="text-white text-4xl font-bold">CW</span>
                                </div>
                                <h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">
                                    {{ siteSettings?.siteTitle?.split(' - ')[0] || 'Cody Wu' }}
                                </h2>
                                <p class="text-gray-600 dark:text-gray-300 mb-4">
                                    {{ siteSettings?.siteTitle?.split(' - ')[1] || 'TaiZanLer' }}
                                </p>
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
                                <!-- 技能 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">技能</h3>
                                    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                                        <div 
                                            v-for="skill in siteSettings?.expand?.skills" 
                                            :key="skill.id"
                                            class="text-center"
                                        >
                                            <div class="w-16 h-16 mx-auto mb-2 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                                                <span class="text-blue-600 dark:text-blue-300 font-bold text-xs">
                                                    {{ skill.name.substring(0, 4) }}
                                                </span>
                                            </div>
                                            <p class="text-sm text-gray-600 dark:text-gray-300">{{ skill.name }}</p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Markdown 內容 -->
                                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                                    <div v-if="aboutPage?.content" class="prose prose-lg dark:prose-invert max-w-none">
                                        <div 
                                            v-html="aboutContent"
                                            class="markdown-content"
                                        ></div>
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

<style scoped>
/* Markdown 內容樣式 */
.markdown-content {
    color: #374151;
}

.dark .markdown-content {
    color: #d1d5db;
}

.markdown-content h1 {
    font-size: 1.875rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: #1f2937;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 0.5rem;
}

.dark .markdown-content h1 {
    color: #ffffff;
    border-bottom-color: #374151;
}

.markdown-content h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    margin-top: 2rem;
    color: #1f2937;
}

.dark .markdown-content h2 {
    color: #ffffff;
}

.markdown-content h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
    color: #1f2937;
}

.dark .markdown-content h3 {
    color: #ffffff;
}

.markdown-content p {
    margin-bottom: 1rem;
    line-height: 1.625;
}

.markdown-content ul {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
}

.markdown-content li {
    margin-bottom: 0.5rem;
    list-style-type: disc;
}

.markdown-content strong {
    font-weight: 600;
    color: #1f2937;
}

.dark .markdown-content strong {
    color: #ffffff;
}

.markdown-content em {
    font-style: italic;
    color: #4b5563;
}

.dark .markdown-content em {
    color: #9ca3af;
}

.markdown-content code {
    background-color: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
}

.dark .markdown-content code {
    background-color: #374151;
}

.markdown-content blockquote {
    border-left: 4px solid #3b82f6;
    padding-left: 1rem;
    font-style: italic;
    color: #4b5563;
    margin: 1rem 0;
}

.dark .markdown-content blockquote {
    color: #9ca3af;
}
</style>
