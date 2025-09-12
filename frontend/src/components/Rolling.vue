<script setup>
    import { onMounted } from 'vue';
    const loadInstagramEmbeds = () => {
        // 檢查是否已經載入過腳本
        if (window.instgrm) {
            window.instgrm.Embeds.process();
            return;
        }

        // 創建並載入腳本
        const script = document.createElement('script');
        script.async = true;
        script.src = '//www.instagram.com/embed.js';
        document.head.appendChild(script);
    };
    onMounted(() => {
        const carousel = document.getElementById('carousel');
        const nextButton = document.getElementById('next');
        const prevButton = document.getElementById('prev');
        loadInstagramEmbeds();
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
    <div class="bg-gray-50"></div>
    <div
        class="relative max-w-7xl px-4 sm:px-6 mx-auto lg:px-8 min-h-screen overflow-x-hidden"
    >
        <section class="py-32">
            <h2
                class="px-28 text-xs/4 font-semibold uppercase tracking-widest text-gray-500"
            >
                What everyone is saying
            </h2>
            <p
                class="mt-2 px-28 text-6xl font-medium tracking-tighter text-gray-800"
            >
                Trusted by professionals
            </p>

            <div class="relative mt-16 flex items-center">
                <div
                    id="carousel"
                    class="relative scrollbar-hide flex w-full snap-x snap-mandatory scroll-pl-28 scroll-pr-8 gap-8 overflow-x-auto overscroll-x-contain"
                >
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <blockquote
                            class="instagram-media"
                            data-instgrm-permalink="https://www.instagram.com/reel/DOV1KcyAY9x/?utm_source=ig_embed&amp;utm_campaign=loading"
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
                            "
                        ></blockquote>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Amy Chase"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                BarelyHR made onboarding our new remote
                                employees a breeze.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Amy Chase
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of Marketing, TaxPal
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Veronica Winton"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                I was able to create a new job posting in
                                literally a few minutes.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Veronica Winton
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of People Operations, Pocket
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <!-- Add more testimonial cards as needed -->

                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1517365830460-955ce3ccd263?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Tina Yards"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                Thanks to BarelyHR, we’re now finding new
                                candidates that we never would have found with
                                our previous methods.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Tina Yards
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    VP of Human Resources, Protocol
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Amy Chase"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                BarelyHR made onboarding our new remote
                                employees a breeze.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Amy Chase
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of Marketing, TaxPal
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Veronica Winton"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                I was able to create a new job posting in
                                literally a few minutes.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Veronica Winton
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of People Operations, Pocket
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <!-- Add more testimonial cards as needed -->

                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1517365830460-955ce3ccd263?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Tina Yards"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                Thanks to BarelyHR, we’re now finding new
                                candidates that we never would have found with
                                our previous methods.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Tina Yards
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    VP of Human Resources, Protocol
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Amy Chase"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                BarelyHR made onboarding our new remote
                                employees a breeze.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Amy Chase
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of Marketing, TaxPal
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <div
                        class="carousel-item relative flex aspect-[3/4] w-96 shrink-0 snap-start flex-col justify-end overflow-hidden rounded-3xl shadow-lg"
                    >
                        <img
                            src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=1024&h=1024&q=80"
                            alt="Veronica Winton"
                            class="absolute inset-0 h-full w-full object-cover"
                        />
                        <div
                            class="absolute inset-0 rounded-3xl bg-gradient-to-t from-black from-25% inset-ring inset-ring-gray-950/10"
                        ></div>
                        <figure class="relative p-10">
                            <blockquote
                                class="relative text-xl/7 text-white before:absolute before:-ml-5 before:translate-x-full before:content-['“'] after:absolute after:content-['”']"
                            >
                                I was able to create a new job posting in
                                literally a few minutes.
                            </blockquote>
                            <figcaption
                                class="mt-6 border-t border-white/20 pt-6"
                            >
                                <p class="text-sm font-medium text-white">
                                    Veronica Winton
                                </p>
                                <p
                                    class="bg-gradient-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-sm font-medium text-transparent"
                                >
                                    Head of People Operations, Pocket
                                </p>
                            </figcaption>
                        </figure>
                    </div>
                    <!-- Add more testimonial cards as needed -->
                </div>
            </div>

            <div class="mx-28 mt-16 flex justify-center">
                <div class="flex gap-x-4 mt-4">
                    <button
                        id="prev"
                        aria-label="Previous testimonial"
                        class="inline-flex h-12 w-12 items-center justify-center rounded-full ring shadow-sm ring-gray-950/10"
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
                        class="inline-flex h-12 w-12 items-center justify-center rounded-full ring shadow-sm ring-gray-950/10"
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
