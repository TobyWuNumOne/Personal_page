import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import Profile from '@/pages/Profile.vue';
// import About from '@/pages/About.vue';
// import Exmp from '@/pages/Exmp.vue';
// import HelloWorld from '@/components/HelloWorld.vue';
// import UserList from '.@/pages/UserList.vue';

const routes = [
    {
        path: '/',
        component: Home,
    },
    {
        path: '/profile',
        component: Profile,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
