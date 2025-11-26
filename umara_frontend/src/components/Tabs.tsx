import React from 'react'
import { motion } from 'framer-motion'
import { ComponentTree } from '../App'

interface TabsProps {
  tabs: string[]
  activeTab: number
  children?: ComponentTree[]
  onChange?: (index: number) => void
  style?: React.CSSProperties
}

export function Tabs({
  tabs,
  activeTab,
  children: _children,
  onChange,
  style,
}: TabsProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      {/* Tab List */}
      <div className="flex border-b border-border mb-4">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => onChange?.(index)}
            className={`
              relative px-4 py-3 text-sm font-medium
              transition-colors duration-200
              ${index === activeTab
                ? 'text-primary'
                : 'text-text-secondary hover:text-text'
              }
            `}
          >
            {tab}
            {index === activeTab && (
              <motion.div
                layoutId="tab-indicator"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>

      {/* Tab Content - rendered by parent via ComponentRenderer */}
    </motion.div>
  )
}
