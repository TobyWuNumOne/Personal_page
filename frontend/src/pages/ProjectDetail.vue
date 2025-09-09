<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useRoute } from 'vue-router';
    import Footer from '@/components/baseic/Footer.vue';
    import Navbar from '@/components/baseic/Navbar.vue';
    import { pb } from '@/composables/usePB';
    import { marked } from 'marked';

    const route = useRoute();
    const project = ref(null);
    const isLoading = ref(true);
    const error = ref(null);

    // 配置 marked 選項
    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    const loadProject = async () => {
        try {
            isLoading.value = true;
            const data = await pb.collection('projects').getFirstListItem(
                `slug="${route.params.slug}"`,
                {
                    expand: 'skills,tags,gallery'
                }
            );
            project.value = data;
        } catch (err) {
            error.value = err;
            console.error('Failed to load project:', err);
        } finally {
            isLoading.value = false;
        }
    };

    // 將 Markdown 轉換為 HTML
    const renderedBody = computed(() => {
        if (!project.value?.body) return '';
        return marked(project.value.body);
    });

    // 獲取圖片 URL
    const getImageUrl = (item, filename) => {
        if (!filename) return null;
        return `https://cms.taizanthebar.com/api/files/${item.collectionName}/${item.id}/${filename}`;
    };

    onMounted(() => {
        loadProject();
    });
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div class="flex-grow bg-background-light text-text dark:bg-background-dark dark:text-text-light transition-colors duration-500 pb-4">
            
            <!-- 載入中 -->
            <div v-if="isLoading" class="container mx-auto px-4 py-12 text-center">
                <div class="text-xl">載入中...</div>
            </div>

            <!-- 錯誤訊息 -->
            <div v-else-if="error" class="container mx-auto px-4 py-12 text-center">
                <div class="text-red-500 text-xl">專案不存在或載入失敗</div>
                <router-link to="/myproject" class="text-blue-600 hover:underline mt-4 inline-block">
                    返回專案列表
                </router-link>
            </div>

            <!-- 專案詳細內容 -->
            <div v-else-if="project" class="container mx-auto px-4 py-12">
                <div class="max-w-4xl mx-auto">
                    <!-- 返回按鈕 -->
                    <router-link 
                        to="/myproject" 
                        class="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6"
                    >
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                        </svg>
                        返回專案列表
                    </router-link>

                    <!-- 專案標題 -->
                    <h1 class="text-4xl font-bold mb-4 text-gray-800 dark:text-white">
                        {{ project.title }}
                    </h1>

                    <!-- 專案摘要 -->
                    <div v-if="project.excerpt" class="text-xl text-gray-600 dark:text-gray-300 mb-8">
                        {{ project.excerpt }}
                    </div>

                    <!-- 技能標籤 -->
                    <div v-if="project.expand?.skills?.length" class="flex flex-wrap gap-2 mb-8">
                        <span 
                            v-for="skill in project.expand.skills" 
                            :key="skill.id"
                            class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                        >
                            {{ skill.name }}
                        </span>
                    </div>

                    <!-- 圖片畫廊 -->
                    <div v-if="project.expand?.gallery?.length" class="mb-8">
                        <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">專案截圖</h2>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            <img 
                                v-for="media in project.expand.gallery" 
                                :key="media.id"
                                :src="getImageUrl(media, media.file)"
                                :alt="media.alt"
                                class="w-full h-48 object-cover rounded-lg shadow-md hover:shadow-lg transition-shadow"
                            />
                        </div>
                    </div>

                    <!-- 專案內容 -->
                    <div v-if="project.body" class="prose prose-lg dark:prose-invert max-w-none mb-8">
                        <div 
                            v-html="renderedBody"
                            class="markdown-content"
                        ></div>
                    </div>

                    <!-- 標籤 -->
                    <div v-if="project.expand?.tags?.length" class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
                        <h3 class="text-lg font-semibold mb-4 text-gray-800 dark:text-white">標籤</h3>
                        <div class="flex flex-wrap gap-2">
                            <span 
                                v-for="tag in project.expand.tags" 
                                :key="tag.id"
                                class="px-3 py-1 bg-gray-100 text-gray-800 text-sm rounded-full"
                            >
                                {{ tag.name }}
                            </span>
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
    color: rgb(55 65 81);
    line-height: 1.625;
}

.dark .markdown-content {
    color: rgb(209 213 219);
}

/* 標題樣式 */
.markdown-content :deep(h1) {
    font-size: 1.875rem;
    font-weight: 700;
    color: rgb(31 41 55);
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.dark .markdown-content :deep(h1) {
    color: white;
}

.markdown-content :deep(h2) {
    font-size: 1.5rem;
    font-weight: 700;
    color: rgb(31 41 55);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

.dark .markdown-content :deep(h2) {
    color: white;
}

.markdown-content :deep(h3) {
    font-size: 1.25rem;
    font-weight: 600;
    color: rgb(31 41 55);
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.dark .markdown-content :deep(h3) {
    color: white;
}

.markdown-content :deep(h4) {
    font-size: 1.125rem;
    font-weight: 600;
    color: rgb(55 65 81);
    margin-top: 0.75rem;
    margin-bottom: 0.5rem;
}

.dark .markdown-content :deep(h4) {
    color: rgb(229 231 235);
}

/* 段落樣式 */
.markdown-content :deep(p) {
    margin-bottom: 1rem;
    line-height: 1.625;
}

/* 列表樣式 */
.markdown-content :deep(ul) {
    list-style-type: disc;
    list-style-position: inside;
    margin-bottom: 1rem;
    margin-left: 1rem;
}

.markdown-content :deep(ol) {
    list-style-type: decimal;
    list-style-position: inside;
    margin-bottom: 1rem;
    margin-left: 1rem;
}

.markdown-content :deep(li) {
    margin-bottom: 0.25rem;
}

/* 程式碼樣式 */
.markdown-content :deep(code) {
    background-color: rgb(243 244 246);
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    font-family: ui-monospace, SFMono-Regular, Monaco, Consolas, monospace;
}

.dark .markdown-content :deep(code) {
    background-color: rgb(31 41 55);
}

.markdown-content :deep(pre) {
    background-color: rgb(243 244 246);
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin-bottom: 1rem;
}

.dark .markdown-content :deep(pre) {
    background-color: rgb(31 41 55);
}

.markdown-content :deep(pre code) {
    background-color: transparent;
    padding: 0;
}

/* 引用樣式 */
.markdown-content :deep(blockquote) {
    border-left: 4px solid rgb(59 130 246);
    padding-left: 1rem;
    font-style: italic;
    color: rgb(75 85 99);
    margin-bottom: 1rem;
}

.dark .markdown-content :deep(blockquote) {
    color: rgb(156 163 175);
}

/* 連結樣式 */
.markdown-content :deep(a) {
    color: rgb(37 99 235);
    text-decoration: underline;
}

.dark .markdown-content :deep(a) {
    color: rgb(96 165 250);
}

.markdown-content :deep(a:hover) {
    text-decoration: underline;
}

/* 強調樣式 */
.markdown-content :deep(strong) {
    font-weight: 700;
    color: rgb(31 41 55);
}

.dark .markdown-content :deep(strong) {
    color: white;
}

.markdown-content :deep(em) {
    font-style: italic;
}

/* 分隔線樣式 */
.markdown-content :deep(hr) {
    border-color: rgb(209 213 219);
    margin: 1.5rem 0;
}

.dark .markdown-content :deep(hr) {
    border-color: rgb(75 85 99);
}
</style>
