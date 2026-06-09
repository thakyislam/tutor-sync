/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563EB',
          50:  '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        },
        accent: {
          DEFAULT: '#7C3AED',
          50:  '#F5F3FF',
          100: '#EDE9FE',
          200: '#DDD6FE',
          300: '#C4B5FD',
          400: '#A78BFA',
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
          800: '#5B21B6',
          900: '#4C1D95',
        },
        ink: {
          DEFAULT: '#0F1B33',
          soft:    '#1E293B',
          muted:   '#475569',
          subtle:  '#64748B',
          faint:   '#94A3B8',
        },
      },
      fontFamily: {
        sans:    ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'Inter', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
      },
      letterSpacing: {
        tight:   '-0.02em',
        tighter: '-0.03em',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      boxShadow: {
        card:  '0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.06)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.08), 0 12px 32px rgba(0,0,0,0.08)',
        glow:  '0 0 0 3px rgba(37,99,235,0.15)',
        'glow-accent': '0 0 0 3px rgba(124,58,237,0.15)',
      },
      backgroundImage: {
        'gradient-brand':  'linear-gradient(135deg, #2563EB, #7C3AED)',
        'gradient-brand-r':'linear-gradient(135deg, #7C3AED, #2563EB)',
        'gradient-subtle': 'linear-gradient(135deg, #EFF6FF, #F5F3FF)',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.2, 0.7, 0.3, 1)',
      },
      animation: {
        'fade-in':   'fadeIn 0.2s ease-out',
        'slide-up':  'slideUp 0.25s cubic-bezier(0.2, 0.7, 0.3, 1)',
        'slide-down':'slideDown 0.25s cubic-bezier(0.2, 0.7, 0.3, 1)',
      },
      keyframes: {
        fadeIn:    { from: { opacity: '0' },                  to: { opacity: '1' } },
        slideUp:   { from: { opacity: '0', transform: 'translateY(8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideDown: { from: { opacity: '0', transform: 'translateY(-8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
