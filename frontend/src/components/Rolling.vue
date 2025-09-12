<script setup>
    import { onMounted, ref } from 'vue';
    import { useTheme } from '@/composables/UseTheme';
    import { listRollingItems, pb } from '@/composables/usePB';

    const { theme } = useTheme();
    const rollingItems = ref([]);
    const loading = ref(true);

    // 獲取完整的圖片 URL
    const getImageUrl = (item, filename) => {
        if (!filename) return '';
        return pb.files.getUrl(item, filename);
    };

    // 載入 Rolling Items 資料
    const loadRollingItems = async () => {
        try {
            loading.value = true;
            console.log('開始載入 Rolling Items...');
            const items = await listRollingItems();
            console.log('載入的資料:', items);
            console.log('資料數量:', items?.length || 0);
            rollingItems.value = items || [];
        } catch (error) {
            console.error('Failed to load rolling items:', error);
            rollingItems.value = [];
        } finally {
            loading.value = false;
        }
    };

    const loadInstagramEmbeds = () => {
        try {
            // 檢查是否已經載入過腳本
            if (window.instgrm) {
                window.instgrm.Embeds.process();
                return;
            }

            // 創建並載入腳本
            const script = document.createElement('script');
            script.async = true;
            script.defer = true;
            script.src = 'https://www.instagram.com/embed.js';
            script.onload = () => {
                if (window.instgrm) {
                    window.instgrm.Embeds.process();
                }
            };
            script.onerror = (error) => {
                console.warn('Instagram embed script failed to load:', error);
            };
            document.head.appendChild(script);
        } catch (error) {
            console.warn('Failed to load Instagram embeds:', error);
        }
    };
    onMounted(async () => {
        // 載入資料
        await loadRollingItems();

        const carousel = document.getElementById('carousel');
        const nextButton = document.getElementById('next');
        const prevButton = document.getElementById('prev');

        // 延遲載入 Instagram embeds 以避免阻塞
        setTimeout(() => {
            loadInstagramEmbeds();
        }, 1000);

        // 確保元素存在才添加事件監聽器
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                if (carousel) {
                    carousel.scrollBy({
                        left: carousel.clientWidth,
                        behavior: 'smooth',
                    });
                }
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                if (carousel) {
                    carousel.scrollBy({
                        left: -carousel.clientWidth,
                        behavior: 'smooth',
                    });
                }
            });
        }

        // 設置 Intersection Observer
        if (carousel) {
            const observerOptions = {
                root: carousel,
                rootMargin: '0px',
                threshold: 0.5,
            };

            const observerCallback = (entries) => {
                entries.forEach((entry) => {
                    if (entry.intersectionRatio > 0.5) {
                        entry.target.style.opacity = '1';
                    } else {
                        entry.target.style.opacity = '0.5';
                    }
                });
            };

            const observer = new IntersectionObserver(
                observerCallback,
                observerOptions
            );

            document.querySelectorAll('.carousel-item').forEach((item) => {
                observer.observe(item);
            });

            carousel.dispatchEvent(new Event('scroll'));
        }
    });
</script>
<template>
    <div
        class="relative max-w-7xl px-4 sm:px-6 mx-auto lg:px-8 min-h-screen overflow-x-hidden bg-background-light dark:bg-background-dark transition-colors duration-500"
    >
        <section class="py-3">
            <p
                class="mt-2 px-28 text-4xl font-medium tracking-tighter text-text dark:text-text-light transition-colors duration-500"
            >
                最近在幹嘛
            </p>
            <div class="relative mt-16 flex items-center">
                <!-- Loading 狀態 -->
                <div v-if="loading" class="w-full text-center py-8">
                    <div class="text-text dark:text-text-light">載入中...</div>
                </div>

                <!-- 主要內容 -->
                <div v-else class="w-full">
                    <!-- 有資料時顯示輪播 -->
                    <div
                        v-if="rollingItems.length > 0"
                        id="carousel"
                        class="relative scrollbar-hide flex w-full snap-x snap-mandatory scroll-pl-28 scroll-pr-8 gap-8 overflow-x-auto overscroll-x-contain"
                    >
                        <!-- 動態渲染項目 -->
                        <div
                            v-for="item in rollingItems"
                            :key="item.id"
                            class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg bg-white dark:bg-gray-800 ring-1 ring-gray-200 dark:ring-gray-700 transition-colors duration-500"
                        >
                            <!-- Instagram 類型 -->
                            <div
                                v-if="item.field === 'instagram'"
                                class="w-full h-full"
                            >
                                <blockquote
                                    class="instagram-media"
                                    :data-instgrm-permalink="item.content"
                                    data-instgrm-version="14"
                                    style="
                                        background: #fff;
                                        border: 0;
                                        border-radius: 8px;
                                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                                            0 2px 4px -1px rgba(0, 0, 0, 0.06);
                                        margin: 0;
                                        max-width: 540px;
                                        min-width: 326px;
                                        padding: 0;
                                        width: 100%;
                                        height: 100%;
                                    "
                                >
                                    <div style="padding: 16px">
                                        <a
                                            :href="item.content"
                                            style="
                                                background: #ffffff;
                                                line-height: 0;
                                                padding: 0 0;
                                                text-align: center;
                                                text-decoration: none;
                                                width: 100%;
                                            "
                                            target="_blank"
                                        >
                                            <div style="padding: 19% 0"></div>
                                            <div
                                                style="
                                                    display: block;
                                                    height: 50px;
                                                    margin: 0 auto 12px;
                                                    width: 50px;
                                                "
                                            >
                                                <svg
                                                    width="50px"
                                                    height="50px"
                                                    viewBox="0 0 60 60"
                                                    version="1.1"
                                                    xmlns="https://www.w3.org/2000/svg"
                                                >
                                                    <g
                                                        stroke="none"
                                                        stroke-width="1"
                                                        fill="none"
                                                        fill-rule="evenodd"
                                                    >
                                                        <g
                                                            transform="translate(-511.000000, -20.000000)"
                                                            fill="#000000"
                                                        >
                                                            <g>
                                                                <path
                                                                    d="M556.869,30.41 C554.814,30.41 553.148,32.076 553.148,34.131 C553.148,36.186 554.814,37.852 556.869,37.852 C558.924,37.852 560.59,36.186 560.59,34.131 C560.59,32.076 558.924,30.41 556.869,30.41 M541,60.657 C535.114,60.657 530.342,55.887 530.342,50 C530.342,44.114 535.114,39.342 541,39.342 C546.887,39.342 551.658,44.114 551.658,50 C551.658,55.887 546.887,60.657 541,60.657 M541,33.886 C532.1,33.886 524.886,41.1 524.886,50 C524.886,58.899 532.1,66.113 541,66.113 C549.9,66.113 557.115,58.899 557.115,50 C557.115,41.1 549.9,33.886 541,33.886 M565.378,62.101 C565.244,65.022 564.756,66.606 564.346,67.663 C563.803,69.06 563.154,70.057 562.106,71.106 C561.058,72.155 560.06,72.803 558.662,73.347 C557.607,73.757 556.021,74.244 553.102,74.378 C549.944,74.521 548.997,74.552 541,74.552 C533.003,74.552 532.056,74.521 528.898,74.378 C525.979,74.244 524.393,73.757 523.338,73.347 C521.94,72.803 520.942,72.155 519.894,71.106 C518.846,70.057 518.197,69.06 517.654,67.663 C517.244,66.606 516.755,65.022 516.623,62.101 C516.479,58.943 516.448,57.996 516.448,50 C516.448,42.003 516.479,41.056 516.623,37.899 C516.755,34.978 517.244,33.391 517.654,32.338 C518.197,30.938 518.846,29.942 519.894,28.894 C520.942,27.846 521.94,27.196 523.338,26.654 C524.393,26.244 525.979,25.756 528.898,25.623 C532.057,25.479 533.004,25.448 541,25.448 C548.997,25.448 549.943,25.479 553.102,25.623 C556.021,25.756 557.607,26.244 558.662,26.654 C560.06,27.196 561.058,27.846 562.106,28.894 C563.154,29.942 563.803,30.938 564.346,32.338 C564.756,33.391 565.244,34.978 565.378,37.899 C565.522,41.056 565.552,42.003 565.552,50 C565.552,57.996 565.522,58.943 565.378,62.101 M570.82,37.631 C570.674,34.438 570.167,32.258 569.425,30.349 C568.659,28.377 567.633,26.702 565.965,25.035 C564.297,23.368 562.623,22.342 560.652,21.575 C558.743,20.834 556.562,20.326 553.369,20.18 C550.169,20.033 549.148,20 541,20 C532.853,20 531.831,20.033 528.631,20.18 C525.438,20.326 523.257,20.834 521.349,21.575 C519.376,22.342 517.703,23.368 516.035,25.035 C514.368,26.702 513.342,28.377 512.574,30.349 C511.834,32.258 511.326,34.438 511.181,37.631 C511.035,40.831 511,41.851 511,50 C511,58.147 511.035,59.17 511.181,62.369 C511.326,65.562 511.834,67.743 512.574,69.651 C513.342,71.625 514.368,73.296 516.035,74.965 C517.703,76.634 519.376,77.658 521.349,78.425 C523.257,79.167 525.438,79.673 528.631,79.82 C531.831,79.965 532.853,80.001 541,80.001 C549.148,80.001 550.169,79.965 553.369,79.82 C556.562,79.673 558.743,79.167 560.652,78.425 C562.623,77.658 564.297,76.634 565.965,74.965 C567.633,73.296 568.659,71.625 569.425,69.651 C570.167,67.743 570.674,65.562 570.82,62.369 C570.966,59.17 571,58.147 571,50 C571,41.851 570.966,40.831 570.82,37.631"
                                                                ></path>
                                                            </g>
                                                        </g>
                                                    </g>
                                                </svg>
                                            </div>
                                            <div style="padding-top: 8px">
                                                <div
                                                    style="
                                                        color: #3897f0;
                                                        font-family: Arial,
                                                            sans-serif;
                                                        font-size: 14px;
                                                        font-style: normal;
                                                        font-weight: 550;
                                                        line-height: 18px;
                                                    "
                                                >
                                                    在 Instagram 查看這則貼文
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                                </blockquote>
                            </div>

                            <!-- 圖片類型 -->
                            <div
                                v-else-if="item.field === 'image'"
                                class="w-full h-full relative"
                            >
                                <img
                                    :src="getImageUrl(item, item.image)"
                                    :alt="item.title || 'Image'"
                                    class="absolute inset-0 h-full w-full object-cover"
                                />
                                <div
                                    class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                                ></div>
                                <figure
                                    class="relative p-10 h-full flex flex-col justify-end"
                                >
                                    <blockquote
                                        v-if="item.content"
                                        class="relative text-xl/7 text-white mb-4"
                                    >
                                        {{ item.content }}
                                    </blockquote>
                                    <figcaption
                                        v-if="item.author"
                                        class="mt-6 border-t border-white/20 pt-6"
                                    >
                                        <p
                                            class="text-sm font-medium text-white"
                                        >
                                            {{ item.author }}
                                        </p>
                                        <p
                                            v-if="item.author_title"
                                            class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                        >
                                            {{ item.author_title }}
                                        </p>
                                    </figcaption>
                                </figure>
                            </div>

                            <!-- 純文字類型 -->
                            <div
                                v-else-if="item.field === 'text'"
                                class="w-full h-full flex flex-col justify-center p-10 bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500"
                            >
                                <div class="text-center text-white">
                                    <h3
                                        v-if="item.title"
                                        class="text-2xl font-bold mb-4"
                                    >
                                        {{ item.title }}
                                    </h3>
                                    <p
                                        v-if="item.content"
                                        class="text-lg leading-relaxed mb-6"
                                    >
                                        {{ item.content }}
                                    </p>
                                    <div
                                        v-if="item.author"
                                        class="border-t border-white/20 pt-6 mt-auto"
                                    >
                                        <p class="text-sm font-medium">
                                            {{ item.author }}
                                        </p>
                                        <p
                                            v-if="item.author_title"
                                            class="text-sm opacity-80"
                                        >
                                            {{ item.author_title }}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <!-- 調試：顯示原始資料 -->
                            <div
                                v-else
                                class="w-full h-full flex items-center justify-center p-4 bg-red-100 dark:bg-red-900"
                            >
                                <div class="text-center">
                                    <p
                                        class="text-red-800 dark:text-red-200 mb-2"
                                    >
                                        未知類型: {{ item.field }}
                                    </p>
                                    <pre class="text-xs text-left">{{
                                        JSON.stringify(item, null, 2)
                                    }}</pre>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 沒有資料時的訊息 -->
                    <div v-else class="w-full text-center py-16">
                        <p class="text-text dark:text-text-light text-lg mb-4">
                            目前沒有內容可以顯示
                        </p>
                        <div class="text-sm text-gray-500">
                            <p>請確認：</p>
                            <ul class="mt-2 space-y-1">
                                <li>
                                    1. PocketBase 中的 rolling_items collection
                                    已建立
                                </li>
                                <li>2. 有資料且 published = true</li>
                                <li>3. PocketBase 伺服器正在運行</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mx-28 mt-16 flex justify-center">
                <div class="flex gap-x-4 mt-4">
                    <button
                        id="prev"
                        aria-label="Previous testimonial"
                        class="inline-flex h-12 w-12 items-center justify-center rounded-full ring shadow-sm ring-gray-950/10 dark:ring-gray-50/20 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-300"
                    >
                        <svg
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            class="h-5 w-5"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z"
                                clip-rule="evenodd"
                            />
                        </svg>
                    </button>
                    <button
                        id="next"
                        aria-label="Next testimonial"
                        class="inline-flex h-12 w-12 items-center justify-center rounded-full ring shadow-sm ring-gray-950/10 dark:ring-gray-50/20 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-300"
                    >
                        <svg
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            class="h-5 w-5"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z"
                                clip-rule="evenodd"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </section>
    </div>
</template>
<style scoped>
    .scrollbar-hide::-webkit-scrollbar {
        display: none;
    }
    .scrollbar-hide {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
    .snap-center {
        scroll-snap-align: center;
    }
    .carousel-item {
        transition: opacity 0.3s ease;
    }
</style>
