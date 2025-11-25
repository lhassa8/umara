/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--um-color-primary, #6366f1)',
          hover: 'var(--um-color-primary-hover, #4f46e5)',
          active: 'var(--um-color-primary-active, #4338ca)',
          light: 'var(--um-color-primary-light, #e0e7ff)',
          dark: 'var(--um-color-primary-dark, #3730a3)',
        },
        secondary: {
          DEFAULT: 'var(--um-color-secondary, #64748b)',
          hover: 'var(--um-color-secondary-hover, #475569)',
          light: 'var(--um-color-secondary-light, #f1f5f9)',
        },
        accent: {
          DEFAULT: 'var(--um-color-accent, #f59e0b)',
        },
        success: {
          DEFAULT: 'var(--um-color-success, #10b981)',
          light: 'var(--um-color-success-light, #d1fae5)',
          dark: 'var(--um-color-success-dark, #047857)',
        },
        warning: {
          DEFAULT: 'var(--um-color-warning, #f59e0b)',
          light: 'var(--um-color-warning-light, #fef3c7)',
          dark: 'var(--um-color-warning-dark, #b45309)',
        },
        error: {
          DEFAULT: 'var(--um-color-error, #ef4444)',
          light: 'var(--um-color-error-light, #fee2e2)',
          dark: 'var(--um-color-error-dark, #b91c1c)',
        },
        info: {
          DEFAULT: 'var(--um-color-info, #3b82f6)',
          light: 'var(--um-color-info-light, #dbeafe)',
          dark: 'var(--um-color-info-dark, #1d4ed8)',
        },
        surface: {
          DEFAULT: 'var(--um-color-surface, #ffffff)',
          hover: 'var(--um-color-surface-hover, #f8fafc)',
        },
        background: {
          DEFAULT: 'var(--um-color-background, #ffffff)',
          secondary: 'var(--um-color-background-secondary, #f8fafc)',
        },
        border: {
          DEFAULT: 'var(--um-color-border, #e2e8f0)',
          hover: 'var(--um-color-border-hover, #cbd5e1)',
          focus: 'var(--um-color-border-focus, #6366f1)',
        },
        text: {
          DEFAULT: 'var(--um-color-text, #0f172a)',
          secondary: 'var(--um-color-text-secondary, #475569)',
          tertiary: 'var(--um-color-text-tertiary, #94a3b8)',
          inverse: 'var(--um-color-text-inverse, #ffffff)',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'SF Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'um-sm': 'var(--um-shadow-sm, 0 1px 2px 0 rgba(0, 0, 0, 0.05))',
        'um-md': 'var(--um-shadow-md, 0 4px 6px -1px rgba(0, 0, 0, 0.1))',
        'um-lg': 'var(--um-shadow-lg, 0 10px 15px -3px rgba(0, 0, 0, 0.1))',
        'um-xl': 'var(--um-shadow-xl, 0 20px 25px -5px rgba(0, 0, 0, 0.1))',
        'um-primary': 'var(--um-shadow-primary, 0 4px 14px 0 rgba(99, 102, 241, 0.4))',
      },
      borderRadius: {
        'um-sm': 'var(--um-radius-sm, 4px)',
        'um-md': 'var(--um-radius-md, 8px)',
        'um-lg': 'var(--um-radius-lg, 12px)',
        'um-xl': 'var(--um-radius-xl, 16px)',
      },
      transitionDuration: {
        'um-fast': 'var(--um-duration-fast, 150ms)',
        'um-normal': 'var(--um-duration-normal, 200ms)',
        'um-slow': 'var(--um-duration-slow, 300ms)',
      },
    },
  },
  plugins: [],
}
