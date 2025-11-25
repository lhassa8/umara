export interface Theme {
  name: string
  colors: Record<string, string>
  spacing: Record<string, string>
  typography: Record<string, string | number>
  borders: Record<string, string>
  shadows: Record<string, string>
  transitions: Record<string, string>
}

export function applyTheme(theme: Theme): void {
  const root = document.documentElement

  // Apply colors
  if (theme.colors) {
    Object.entries(theme.colors).forEach(([key, value]) => {
      const cssKey = `--um-color-${key.replace(/_/g, '-')}`
      root.style.setProperty(cssKey, value)
    })
  }

  // Apply shadows
  if (theme.shadows) {
    Object.entries(theme.shadows).forEach(([key, value]) => {
      const cssKey = `--um-shadow-${key.replace(/_/g, '-')}`
      root.style.setProperty(cssKey, value)
    })
  }

  // Apply borders
  if (theme.borders) {
    Object.entries(theme.borders).forEach(([key, value]) => {
      const cssKey = `--um-${key.replace(/_/g, '-')}`
      root.style.setProperty(cssKey, String(value))
    })
  }

  // Apply transitions
  if (theme.transitions) {
    Object.entries(theme.transitions).forEach(([key, value]) => {
      const cssKey = `--um-${key.replace(/_/g, '-')}`
      root.style.setProperty(cssKey, value)
    })
  }

  // Update body background
  document.body.style.backgroundColor = theme.colors?.background || '#ffffff'
  document.body.style.color = theme.colors?.text || '#0f172a'
}

export function getCssVariable(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim()
}
