<script setup>
    import lightlogo from '@/assets/light-logo.png';
    import logo from '@/assets/logo.png';

    import { useTheme } from '@/composables/UseTheme';
    import { useRoute } from 'vue-router';

    const { theme, toggleTheme } = useTheme();
    const route = useRoute();
</script>
<template>
    <nav
        class="nav flex flex-wrap items-center bg-background-light dark:bg-background-dark justify-between px-4"
    >
        <div
            class="flex flex-no-shrink items-center mr-6 py-3 text-grey-darkest dark:text-white"
        >
            <!-- logo -->
            <img
                :src="theme === 'dark' ? logo : lightlogo"
                alt="Logo"
                class="h-8 w-20 mr-2"
            />
        </div>

        <input class="menu-btn hidden" type="checkbox" id="menu-btn" />
        <label
            class="menu-icon block cursor-pointer md:hidden px-2 py-4 relative select-none"
            for="menu-btn"
        >
            <span
                class="navicon bg-gray-600 dark:bg-gray-300 flex items-center relative"
            ></span>
        </label>

        <ul
            class="menu border-b md:border-none flex justify-end list-reset m-0 w-full md:w-auto"
        >
            <li class="border-t md:border-none">
                <Router-link
                    to="/"
                    :class="[
                        'block md:inline-block px-4 py-3 no-underline text-grey-darkest dark:text-white hover:text-grey-darker dark:hover:text-gray-300',
                        route.path === '/' ? 'font-bold' : ''
                    ]"
                >
                    Home
                </Router-link>
            </li>

            <li class="border-t md:border-none">
                <Router-link
                    to="/profile"
                    :class="[
                        'block md:inline-block px-4 py-3 no-underline text-grey-darkest dark:text-white hover:text-grey-darker dark:hover:text-gray-300',
                        route.path === '/profile' ? 'font-bold' : ''
                    ]"
                >
                    Profile
                </Router-link>
            </li>

            <li class="border-t md:border-none">
                <Router-link
                    to="/blog/"
                    :class="[
                        'block md:inline-block px-4 py-3 no-underline text-grey-darkest dark:text-white hover:text-grey-darker dark:hover:text-gray-300',
                        route.path === '/blog/' ? 'font-bold' : ''
                    ]"
                >
                    Blog
                </Router-link>
            </li>
        </ul>
    </nav>
</template>

<style scoped>
    @media (max-width: 767px) {
        .navicon {
            width: 1.125em;
            height: 0.125em;
        }

        .navicon::before,
        .navicon::after {
            display: block;
            position: absolute;
            width: 100%;
            height: 100%;
            transition: all 0.2s ease-out;
            content: '';
            background-color: inherit;
        }

        .navicon::before {
            top: 5px;
        }

        .navicon::after {
            top: -5px;
        }

        .menu-btn:not(:checked) ~ .menu {
            display: none;
        }

        .menu-btn:checked ~ .menu {
            display: block;
        }

        .menu-btn:checked ~ .menu-icon .navicon {
            background: transparent;
        }

        .menu-btn:checked ~ .menu-icon .navicon::before {
            transform: rotate(-45deg);
            background-color: rgb(75 85 99); /* gray-600 */
        }

        .menu-btn:checked ~ .menu-icon .navicon::after {
            transform: rotate(45deg);
            background-color: rgb(75 85 99); /* gray-600 */
        }

        @media (prefers-color-scheme: dark) {
            .menu-btn:checked ~ .menu-icon .navicon::before,
            .menu-btn:checked ~ .menu-icon .navicon::after {
                background-color: rgb(245, 245, 245); /* gray-300 */
            }
        }

        .menu-btn:checked ~ .menu-icon .navicon::before,
        .menu-btn:checked ~ .menu-icon .navicon::after {
            top: 0;
        }
    }
</style>
