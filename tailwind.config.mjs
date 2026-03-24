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
        primary: '#1B3A5C',
        accent: '#C8912A',
        muted: '#6B7280',
        surface: '#FFFFFF',
        bg: '#FAFAF5',
        ink: '#1A1A2E',
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
