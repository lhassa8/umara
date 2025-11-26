import { useEffect, useState, useCallback } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import { ComponentRenderer } from './components/ComponentRenderer'
import { Theme, applyTheme } from './styles/theme'

interface AppState {
  tree: ComponentTree | null
  theme: Theme | null
  state: Record<string, unknown>
  connected: boolean
  error: string | null
}

export interface ComponentTree {
  id: string
  type: string
  props: Record<string, unknown>
  children?: ComponentTree[]
  style?: Record<string, string>
  events?: Record<string, string>
}

// Helper to find sidebar in component tree and get its width
function findSidebar(tree: ComponentTree | null): { found: boolean; width: string; collapsed: boolean } {
  if (!tree) return { found: false, width: '280px', collapsed: false }

  if (tree.type === 'sidebar') {
    return {
      found: true,
      width: (tree.props.width as string) || '280px',
      collapsed: (tree.props.collapsed as boolean) || false,
    }
  }

  if (tree.children) {
    for (const child of tree.children) {
      const result = findSidebar(child)
      if (result.found) return result
    }
  }

  return { found: false, width: '280px', collapsed: false }
}

function App() {
  const [appState, setAppState] = useState<AppState>({
    tree: null,
    theme: null,
    state: {},
    connected: false,
    error: null,
  })

  const handleMessage = useCallback((data: unknown) => {
    const message = data as { type: string; data?: { tree: ComponentTree; theme: Theme; state: Record<string, unknown> }; error?: string }

    if (message.type === 'init' || message.type === 'update') {
      if (message.data) {
        setAppState(prev => ({
          ...prev,
          tree: message.data!.tree,
          theme: message.data!.theme,
          state: message.data!.state || {},
          error: null,
        }))

        if (message.data.theme) {
          applyTheme(message.data.theme)
        }
      }
    } else if (message.type === 'error') {
      setAppState(prev => ({
        ...prev,
        error: message.error || 'Unknown error',
      }))
    }
  }, [])

  const { sendMessage, connected } = useWebSocket(handleMessage)

  useEffect(() => {
    setAppState(prev => ({ ...prev, connected }))
  }, [connected])

  const handleEvent = useCallback((componentId: string, eventType: string, payload: Record<string, unknown> = {}) => {
    sendMessage({
      type: 'event',
      componentId,
      eventType,
      payload,
    })
  }, [sendMessage])

  const handleStateUpdate = useCallback((key: string, value: unknown) => {
    sendMessage({
      type: 'state',
      key,
      value,
    })
  }, [sendMessage])

  if (!connected) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="w-10 h-10 border-3 border-border border-t-primary rounded-full animate-spin mx-auto mb-4" />
          <p className="text-text-secondary text-sm">Connecting to Umara...</p>
        </div>
      </div>
    )
  }

  if (appState.error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background p-4">
        <div className="bg-error-light border border-error rounded-lg p-6 max-w-lg">
          <h2 className="text-error-dark font-semibold mb-2">Error</h2>
          <p className="text-error-dark text-sm">{appState.error}</p>
        </div>
      </div>
    )
  }

  // Check if there's a sidebar in the tree
  const sidebar = findSidebar(appState.tree)
  const mainContentStyle = sidebar.found
    ? { marginLeft: sidebar.collapsed ? '64px' : sidebar.width }
    : {}

  return (
    <div className="min-h-screen bg-background">
      <div
        className="max-w-5xl mx-auto px-4 py-8 sm:px-6 lg:px-8 transition-[margin] duration-300"
        style={mainContentStyle}
      >
        {appState.tree && (
          <ComponentRenderer
            component={appState.tree}
            onEvent={handleEvent}
            onStateUpdate={handleStateUpdate}
            state={appState.state}
          />
        )}
      </div>
    </div>
  )
}

export default App
