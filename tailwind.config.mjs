/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        heading: ['Lora', 'Georgia', 'serif'],
        body: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
      colors: {
        primary: '#1A2350',   // deep cosmic navy (book cover tone)
        accent: '#C8912A',    // crown gold — unchanged
        cosmic: '#0D1122',    // deep space background
        nebula: '#3B2A6A',    // purple nebula accent
        muted: '#6B7280',
        surface: '#FFFFFF',
        bg: '#FAFAF5',
        ink: '#0F1525',       // near-black for body text
      },
      typography: {
        DEFAULT: {
          css: {
            fontSize: '1.125rem',
            maxWidth: '42rem',
            color: '#1A1A2E',
            a: { color: '#1B3A5C' },
            'h1,h2,h3,h4': { fontFamily: 'Lora, Georgia, serif', color: '#1B3A5C' },
          },
        },
      },
    },
  },
  plugins: [],
};
