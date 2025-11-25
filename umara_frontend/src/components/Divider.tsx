import React from 'react'

interface DividerProps {
  style?: React.CSSProperties
}

export function Divider({ style }: DividerProps) {
  return (
    <hr
      className="border-0 border-t border-border my-6"
      style={style}
    />
  )
}

interface SpacerProps {
  height?: string
}

export function Spacer({ height = '24px' }: SpacerProps) {
  return <div style={{ height }} />
}
