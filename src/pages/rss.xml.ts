import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const newsletters = (await getCollection('newsletters'))
    .filter(n => n.data.type === 'newsletter')
    .sort((a, b) => (b.data.number ?? 0) - (a.data.number ?? 0));

  return rss({
    title: 'Sons To Glory — Newsletters',
    description: 'Theological newsletters and writings by Paul Jablonowski.',
    site: context.site!,
    items: newsletters.map(n => ({
      title: n.data.title,
      pubDate: n.data.date ? new Date(n.data.date) : undefined,
      description: n.data.description,
      link: `/newsletters/${n.slug}/`,
    })),
    customData: `<language>en-us</language>`,
  });
}
