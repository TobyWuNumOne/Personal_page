import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import Profile from '@/pages/Profile.vue';
import MyProject from '@/pages/MyProject.vue';
import Blog from '@/pages/Blog.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
    },
    {
        path: '/MyProject',
        name: 'MyProject',
        component: MyProject,
    },
    {
        path: '/blog',
        name: 'Blog',
        component: Blog,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
