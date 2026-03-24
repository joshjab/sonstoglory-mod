import { defineCollection, z } from 'astro:content';

const newsletterCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string().default('Paul Jablonowski'),
    date: z.string().optional(),
    type: z.string(),
    number: z.number().optional(),
    description: z.string().optional().default(''),
    tags: z.array(z.string()).default([]),
    legacy_url: z.string().optional(),
    pdf: z.string().optional(),
  }),
});

const bookCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string().default('Paul Jablonowski'),
    type: z.string(),
    chapter: z.number().optional(),
    description: z.string().optional().default(''),
    tags: z.array(z.string()).default([]),
    legacy_url: z.string().optional(),
  }),
});

const articleCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string().default('Paul Jablonowski'),
    date: z.string().optional(),
    type: z.string(),
    description: z.string().optional().default(''),
    tags: z.array(z.string()).default([]),
    legacy_url: z.string().optional(),
  }),
});

const authorCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string(),
    type: z.string(),
    description: z.string().optional().default(''),
    tags: z.array(z.string()).default([]),
    legacy_url: z.string().optional(),
  }),
});

export const collections = {
  newsletters: newsletterCollection,
  book: bookCollection,
  articles: articleCollection,
  authors: authorCollection,
};
