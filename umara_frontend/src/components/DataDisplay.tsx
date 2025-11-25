import React from 'react'
import { motion } from 'framer-motion'

interface MetricProps {
  label: string
  value: string
  delta?: number
  deltaLabel?: string
  style?: React.CSSProperties
}

export function Metric({
  label,
  value,
  delta,
  deltaLabel,
  style,
}: MetricProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="mb-4"
      style={style}
    >
      <div className="text-sm text-text-secondary mb-1">
        {label}
      </div>
      <div className="text-3xl font-bold text-text tabular-nums">
        {value}
      </div>
      {delta !== undefined && (
        <div className={`
          text-sm font-medium mt-1 flex items-center gap-1
          ${delta >= 0 ? 'text-success' : 'text-error'}
        `}>
          <span>
            {delta >= 0 ? (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            )}
          </span>
          <span>{delta >= 0 ? '+' : ''}{delta}%</span>
          {deltaLabel && <span className="text-text-tertiary">{deltaLabel}</span>}
        </div>
      )}
    </motion.div>
  )
}

interface ProgressProps {
  value: number
  label?: string
  style?: React.CSSProperties
}

export function Progress({ value, label, style }: ProgressProps) {
  const clampedValue = Math.max(0, Math.min(100, value))

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      {label && (
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-text">{label}</span>
          <span className="text-sm font-medium text-text tabular-nums">
            {Math.round(clampedValue)}%
          </span>
        </div>
      )}
      <div className="h-2 bg-border rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${clampedValue}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>
    </motion.div>
  )
}

interface SpinnerProps {
  text?: string
  style?: React.CSSProperties
}

export function Spinner({ text = 'Loading...', style }: SpinnerProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex items-center gap-3 mb-4"
      style={style}
    >
      <div className="w-5 h-5 border-2 border-border border-t-primary rounded-full animate-spin" />
      <span className="text-sm text-text-secondary">{text}</span>
    </motion.div>
  )
}
