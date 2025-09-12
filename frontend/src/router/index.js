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
        path: '/myproject',
        name: 'MyProject',
        component: MyProject,
    },
    {
        path: '/myproject/:slug',
        name: 'ProjectDetail',
        component: () => import('@/pages/ProjectDetail.vue'),
    },
    {
        path: '/blog',
        name: 'Blog',
        component: Blog,
    },
    {
        path: '/display',
        name: 'Display',
        component: () => import('@/pages/Display.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
