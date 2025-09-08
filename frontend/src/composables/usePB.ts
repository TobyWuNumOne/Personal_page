import PocketBase from 'pocketbase';

export const pb = new PocketBase('https://cms.taizanthebar.com');

export async function getSiteSettings() {
    return await pb.collection('site_settings').getFirstListItem('');
}

export async function getPage(slug: string) {
    return await pb.collection('pages').getFirstListItem(`slug="${slug}"`);
}

export async function listProjects() {
    return await pb.collection('projects').getFullList({
        filter: 'published=true',
        sort: '-created',
    });
}

export async function listPosts() {
    return await pb.collection('posts').getFullList({
        filter: 'published=true',
        sort: '-created',
    });
}
