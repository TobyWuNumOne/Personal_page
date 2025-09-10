import { ref, computed } from 'vue';
import { getSiteSettings } from './usePB';

interface NavItem {
    label: string;
    route: string;
    visible: boolean;
    order: number;
}

interface SiteSettings {
    id: string;
    siteTitle?: string;
    logo?: string;
    nav?: NavItem[] | string;
    [key: string]: any;
}

const siteSettings = ref<SiteSettings | null>(null);
const isLoading = ref(false);
const error = ref<Error | null>(null);

// 預設導航結構（作為 fallback）
const defaultNav: NavItem[] = [
    { label: '首頁', route: '/', visible: true, order: 1 },
    { label: '關於我', route: '/profile', visible: true, order: 2 },
    { label: '我的專案', route: '/myproject', visible: true, order: 3 },
    { label: '部落格', route: '/blog', visible: true, order: 4 },
];

export function useSiteSettings() {
    const loadSiteSettings = async () => {
        if (siteSettings.value) return; // 已載入過就不重複載入

        isLoading.value = true;
        error.value = null;

        try {
            const data = await getSiteSettings();
            siteSettings.value = data as SiteSettings;
        } catch (err) {
            error.value = err as Error;
            console.error('Failed to load site settings:', err);
        } finally {
            isLoading.value = false;
        }
    };

    // 計算屬性：導航項目
    const navigation = computed(() => {
        if (!siteSettings.value?.nav) {
            return defaultNav;
        }

        try {
            const navItems = Array.isArray(siteSettings.value.nav)
                ? siteSettings.value.nav
                : JSON.parse(siteSettings.value.nav as string);

            return navItems
                .filter((item: NavItem) => item.visible !== false)
                .sort(
                    (a: NavItem, b: NavItem) => (a.order || 0) - (b.order || 0)
                );
        } catch (err) {
            console.error('Failed to parse navigation:', err);
            return defaultNav;
        }
    });

    // 計算屬性：網站標題
    const siteTitle = computed(() => {
        return siteSettings.value?.siteTitle || 'Cody Wu';
    });

    // 計算屬性：Logo URL
    const logoUrl = computed(() => {
        if (!siteSettings.value?.logo) return null;
        return `https://cms.taizanthebar.com/api/files/site_settings/${siteSettings.value.id}/${siteSettings.value.logo}`;
    });

    return {
        siteSettings,
        isLoading,
        error,
        navigation,
        siteTitle,
        logoUrl,
        loadSiteSettings,
    };
}
