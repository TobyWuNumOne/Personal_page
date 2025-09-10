<script setup>
    import { ref, onMounted } from 'vue';
    import Footer from '@/components/baseic/Footer.vue';
    import Navbar from '@/components/baseic/Navbar.vue';
    import { pb } from '@/composables/usePB';

    const projects = ref([]);
    const isLoading = ref(true);
    const error = ref(null);

    const loadProjects = async () => {
        try {
            isLoading.value = true;
            // 直接使用 pb 來載入專案並擴展關聯資料
            const data = await pb.collection('projects').getFullList({
                filter: 'published=true',
                sort: '-created',
                expand: 'skills,tags,gallery'
            });
            projects.value = data;
        } catch (err) {
            error.value = err;
            console.error('Failed to load projects:', err);
        } finally {
            isLoading.value = false;
        }
    };

    // 獲取圖片 URL（用於專案封面）
    const getImageUrl = (mediaItem, filename) => {
        if (!filename || !mediaItem) return null;
        return `https://cms.taizanthebar.com/api/files/${mediaItem.collectionName}/${mediaItem.id}/${filename}`;
    };

    // 生成漸變背景（如果沒有封面圖片）
    const getGradientClass = (index) => {
        const gradients = [
            'from-blue-500 to-purple-600',
            'from-green-500 to-teal-600',
            'from-pink-500 to-rose-600',
            'from-yellow-500 to-orange-600',
            'from-indigo-500 to-blue-600',
            'from-purple-500 to-pink-600'
        ];
        return gradients[index % gradients.length];
    };

    onMounted(() => {
        loadProjects();
    });
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div class="flex-grow bg-background-light text-text dark:bg-background-dark dark:text-text-light transition-colors duration-500 pb-4">
            <div class="container mx-auto px-4 py-12">
                <div class="max-w-4xl mx-auto">
                    <h1 class="text-4xl font-bold text-center mb-12 text-gray-800 dark:text-white">
                        我的專案
                    </h1>
                    
                    <!-- 載入中 -->
                    <div v-if="isLoading" class="text-center">
                        <div class="text-xl">載入專案中...</div>
                    </div>

                    <!-- 錯誤訊息 -->
                    <div v-else-if="error" class="text-center text-red-500">
                        <div class="text-xl">載入專案失敗</div>
                        <button @click="loadProjects" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            重新載入
                        </button>
                    </div>

                    <!-- 專案列表 -->
                    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <div 
                            v-for="(project, index) in projects" 
                            :key="project.id"
                            class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer"
                            @click="$router.push(`/myproject/${project.slug}`)"
                        >
                            <!-- 專案封面 -->
                            <div 
                                v-if="project.expand?.gallery && project.expand.gallery.length > 0"
                                class="h-48 bg-cover bg-center"
                                :style="{ backgroundImage: `url(${getImageUrl(project.expand.gallery[0], project.expand.gallery[0].file)})` }"
                            ></div>
                            <div 
                                v-else
                                :class="`h-48 bg-gradient-to-r ${getGradientClass(index)}`"
                            ></div>
                            
                            <div class="p-6">
                                <h3 class="text-xl font-semibold mb-2 text-gray-800 dark:text-white">
                                    {{ project.title }}
                                </h3>
                                <p class="text-gray-600 dark:text-gray-300 mb-4">
                                    {{ project.excerpt || '點擊查看詳細資訊...' }}
                                </p>
                                
                                <!-- 技能標籤 -->
                                <div v-if="project.expand?.skills?.length > 0" class="flex flex-wrap gap-2 mb-4">
                                    <span 
                                        v-for="skill in project.expand.skills.slice(0, 3)" 
                                        :key="skill.id"
                                        class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full"
                                    >
                                        {{ skill.name }}
                                    </span>
                                    <span 
                                        v-if="project.expand.skills.length > 3"
                                        class="px-3 py-1 bg-gray-100 text-gray-800 text-sm rounded-full"
                                    >
                                        +{{ project.expand.skills.length - 3 }}
                                    </span>
                                </div>
                                
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-500">
                                        點擊查看詳情
                                    </span>
                                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 空狀態 -->
                    <div v-if="!isLoading && !error && projects.length === 0" class="text-center text-gray-500">
                        <div class="text-xl mb-4">還沒有專案資料</div>
                        <p>請先在 CMS 中新增一些專案。</p>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>
