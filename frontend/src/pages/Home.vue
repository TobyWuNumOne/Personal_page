<script setup>
    import Footer from '@/components/baseic/Footer.vue';
    import Navbar from '@/components/baseic/Navbar.vue';

    import instagramLight from '@/assets/icon/instagram.svg';
    import instagramDark from '@/assets/icon/instagram.png';
    import githubLight from '@/assets/icon/gethub.svg';
    import githubDark from '@/assets/icon/github.png';
    import facebookLight from '@/assets/icon/facebook.svg';
    import facebookDark from '@/assets/icon/facebook.png';
    import linkedinLight from '@/assets/icon/linkedin.svg';
    import linkedinDark from '@/assets/icon/linkedin.png';
    import lineLight from '@/assets/icon/line.svg';
    import lineDark from '@/assets/icon/line.png';

    import { useTheme } from '@/composables/UseTheme';
    const { theme } = useTheme();
</script>
<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />
        <div
            class="flex-grow bg-background-light text-text dark:bg-background-dark dark:text-text-light transition-colors duration-500 pb-4"
        >
            <div
                class="container mx-auto flex flex-col lg:flex-row items-center lg:justify-around py-12"
            >
                <!-- Profile Header Start -->
                <div
                    class="w-full lg:w-1/2 flex flex-col items-center lg:flex lg:flex-row lg:justify-center mb-8 lg:mb-0"
                >
                    <div
                        class="bg-[url(@/assets/IMG_1643.jpg)] bg-no-repeat bg-center bg-cover w-32 h-32 rounded-full m-4"
                    ></div>
                    <div class="profile-names text-center lg:text-left">
                        <h1 class="username text-3xl font-bold">Cody Wu</h1>
                        <small class="page-title text-gray-500"
                            >TaiZanLer</small
                        >
                    </div>
                </div>
                <div class="w-full lg:w-1/2 flex flex-col items-center">
                    <div class="social_bar flex space-x-4 mb-4">
                        <!-- Social Icons -->
                        <a
                            href="https://www.instagram.com/taizanthebar?igsh=NWFla2wxeXBiamZu&utm_source=qr"
                            class="w-8 h-8"
                        >
                            <img
                                :src="
                                    theme === 'dark'
                                        ? instagramDark
                                        : instagramLight
                                "
                                alt="Instagram"
                                class="w-full h-full"
                            />
                        </a>
                        <a
                            href="https://github.com/TobyWuNumOne"
                            class="w-8 h-8"
                        >
                            <img
                                :src="
                                    theme === 'dark' ? githubDark : githubLight
                                "
                                alt="GitHub"
                                class="w-full h-full"
                            />
                        </a>
                        <a href="#" class="w-8 h-8">
                            <img
                                :src="
                                    theme === 'dark'
                                        ? facebookDark
                                        : facebookLight
                                "
                                alt="Facebook"
                                class="w-full h-full"
                            />
                        </a>
                        <a
                            href="//linkedin.com/in/wu-cody-6b3665357"
                            class="w-8 h-8"
                        >
                            <img
                                :src="
                                    theme === 'dark'
                                        ? linkedinDark
                                        : linkedinLight
                                "
                                alt="LinkedIn"
                                class="w-full h-full"
                            />
                        </a>
                        <a href="#" class="w-8 h-8">
                            <img
                                :src="theme === 'dark' ? lineDark : lineLight"
                                alt="Line"
                                class="w-full h-full"
                            />
                        </a>
                    </div>
                    <figure class="figure text-center">
                        <img
                            src="https://ghchart.rshah.org/303030/TobyWuNumOne"
                            class="rounded-lg shadow-md"
                            alt="GitHub Chart"
                        />
                        <figcaption class="text-sm text-gray-500 mt-2">
                            MURMUR on Github
                        </figcaption>
                    </figure>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>
