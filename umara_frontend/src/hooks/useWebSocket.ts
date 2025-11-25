import { useEffect, useRef, useState, useCallback } from 'react'

interface UseWebSocketOptions {
  reconnectAttempts?: number
  reconnectInterval?: number
}

export function useWebSocket(
  onMessage: (data: unknown) => void,
  options: UseWebSocketOptions = {}
) {
  const { reconnectAttempts = 5, reconnectInterval = 1000 } = options
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  const reconnectCountRef = useRef(0)
  const messageQueueRef = useRef<unknown[]>([])

  const connect = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws`

    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('WebSocket connected')
      setConnected(true)
      reconnectCountRef.current = 0

      // Send queued messages
      while (messageQueueRef.current.length > 0) {
        const msg = messageQueueRef.current.shift()
        if (msg) {
          ws.send(JSON.stringify(msg))
        }
      }
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setConnected(false)
      wsRef.current = null

      // Attempt to reconnect
      if (reconnectCountRef.current < reconnectAttempts) {
        reconnectCountRef.current++
        const delay = reconnectInterval * reconnectCountRef.current
        console.log(`Reconnecting in ${delay}ms (attempt ${reconnectCountRef.current})`)
        setTimeout(connect, delay)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }, [onMessage, reconnectAttempts, reconnectInterval])

  useEffect(() => {
    connect()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])

  const sendMessage = useCallback((message: unknown) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    } else {
      // Queue message to send when connected
      messageQueueRef.current.push(message)
    }
  }, [])

  return { sendMessage, connected }
}
