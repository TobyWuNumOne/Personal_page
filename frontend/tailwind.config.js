/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                // === 色彩設計 ===
                brand: {
                    DEFAULT: '#ffffff', // 主色（黑）
                    light: '#ffffff', // 主色反白版
                    dark: '#111111', // 深色背景
                },
                accent: {
                    DEFAULT: '#6366F1', // Indigo-500（Vercel 的點綴色）
                    hover: '#4F46E5', // Indigo-600
                },
                background: {
                    light: '#ffffff',
                    dark: '#0A0A0A', // 幾乎全黑
                },
                text: {
                    DEFAULT: '#111111',
                    light: '#f5f5f5',
                    subtle: '#9CA3AF', // 灰色文字
                },
                border: {
                    DEFAULT: '#e5e7eb', // 灰色邊框
                    dark: '#2A2A2A', // 暗色邊框
                },
            },

            // === 字體 ===
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui'],
                mono: ['Fira Code', 'ui-monospace'],
            },

            // === 響應式斷點（跟原版相同） ===
            screens: {
                xs: '420px',
                sm: '640px',
                md: '768px',
                lg: '1024px',
                xl: '1280px',
                '2xl': '1536px',
            },

            // === 陰影 ===
            boxShadow: {
                subtle: '0 1px 3px rgba(0,0,0,0.05)',
                medium: '0 4px 12px rgba(0,0,0,0.1)',
                dark: '0 0 0 1px rgba(255,255,255,0.05)',
            },

            // === 寬高 ===
            spacing: {
                128: '32rem',
                144: '36rem',
            },
        },
    },

    // === Plugin 可加 DaisyUI / Flowbite / Typography 等 ===
    plugins: [],
};
