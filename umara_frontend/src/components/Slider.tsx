import React from 'react'
import { motion } from 'framer-motion'

interface SliderProps {
  label?: string
  value: number
  min?: number
  max?: number
  step?: number
  disabled?: boolean
  onChange?: (value: number) => void
  style?: React.CSSProperties
}

export function Slider({
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  disabled = false,
  onChange,
  style,
}: SliderProps) {
  const percentage = ((value - min) / (max - min)) * 100

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-4"
      style={style}
    >
      {label && (
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-medium text-text">
            {label}
          </label>
          <span className="text-sm font-medium text-primary tabular-nums">
            {value}
          </span>
        </div>
      )}
      <div className="relative">
        <div className="h-2 bg-border rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-primary rounded-full"
            initial={false}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 0.1 }}
          />
        </div>
        <input
          type="range"
          value={value}
          min={min}
          max={max}
          step={step}
          disabled={disabled}
          onChange={(e) => onChange?.(parseFloat(e.target.value))}
          className={`
            absolute inset-0 w-full h-full opacity-0 cursor-pointer
            disabled:cursor-not-allowed
          `}
        />
        <motion.div
          className="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-primary rounded-full shadow-md pointer-events-none"
          initial={false}
          animate={{ left: `calc(${percentage}% - 10px)` }}
          transition={{ duration: 0.1 }}
          style={{
            boxShadow: '0 2px 8px rgba(99, 102, 241, 0.4)',
          }}
        />
      </div>
    </motion.div>
  )
}
