import React from 'react'
import { motion } from 'framer-motion'

interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  traceback?: string
  style?: React.CSSProperties
}

const alertConfig = {
  success: {
    bg: 'bg-success-light',
    border: 'border-success/20',
    text: 'text-success-dark',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  error: {
    bg: 'bg-error-light',
    border: 'border-error/20',
    text: 'text-error-dark',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  warning: {
    bg: 'bg-warning-light',
    border: 'border-warning/20',
    text: 'text-warning-dark',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    ),
  },
  info: {
    bg: 'bg-info-light',
    border: 'border-info/20',
    text: 'text-info-dark',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
}

export function Alert({ type, message, traceback, style }: AlertProps) {
  const config = alertConfig[type]

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`
        ${config.bg} ${config.border} ${config.text}
        border rounded-lg p-4 mb-4
        flex items-start gap-3
      `}
      style={style}
    >
      <div className="flex-shrink-0 mt-0.5">
        {config.icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium">{message}</p>
        {traceback && (
          <pre className="mt-2 text-xs font-mono overflow-x-auto opacity-80 whitespace-pre-wrap">
            {traceback}
          </pre>
        )}
      </div>
    </motion.div>
  )
}
