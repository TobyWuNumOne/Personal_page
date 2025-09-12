import PocketBase from 'pocketbase';

export const pb = new PocketBase('https://cms.taizanthebar.com');

export async function getSiteSettings() {
    try {
        return await pb.collection('site_settings').getFirstListItem('');
    } catch (error) {
        console.error('Failed to fetch site settings:', error);
        return null;
    }
}

export async function getPage(slug: string) {
    try {
        return await pb.collection('pages').getFirstListItem(`slug="${slug}"`);
    } catch (error) {
        console.error(`Failed to fetch page ${slug}:`, error);
        return null;
    }
}

export async function listProjects() {
    try {
        return await pb.collection('projects').getFullList({
            filter: 'published=true',
            sort: '-created',
        });
    } catch (error) {
        console.error('Failed to fetch projects:', error);
        return [];
    }
}

export async function listRollingItems() {
    try {
        return await pb.collection('rolling_items').getFullList({
            filter: 'published=true',
            sort: 'order,created',
        });
    } catch (error) {
        console.error('Failed to fetch rolling items:', error);
        return [];
    }
}
