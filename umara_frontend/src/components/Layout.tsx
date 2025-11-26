import React from 'react'
import { motion } from 'framer-motion'

interface ContainerProps {
  children: React.ReactNode
  style?: React.CSSProperties
}

export function Container({ children, style }: ContainerProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      {children}
    </motion.div>
  )
}

interface ColumnsProps {
  children: React.ReactNode
  count?: number
  gap?: string
  style?: React.CSSProperties
}

export function Columns({
  children,
  count = 2,
  gap = '16px',
  style,
}: ColumnsProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${count}, 1fr)`,
        gap,
        ...style,
      }}
    >
      {children}
    </motion.div>
  )
}

interface ColumnProps {
  children: React.ReactNode
  style?: React.CSSProperties
}

export function Column({ children, style }: ColumnProps) {
  return (
    <div style={style}>
      {children}
    </div>
  )
}

interface GridProps {
  children: React.ReactNode
  columns?: number | string
  gap?: string
  rowGap?: string
  style?: React.CSSProperties
}

export function Grid({
  children,
  columns = 3,
  gap = '16px',
  rowGap,
  style,
}: GridProps) {
  const gridColumns = typeof columns === 'number'
    ? `repeat(${columns}, 1fr)`
    : columns

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={{
        display: 'grid',
        gridTemplateColumns: gridColumns,
        gap,
        rowGap: rowGap || gap,
        ...style,
      }}
    >
      {children}
    </motion.div>
  )
}

interface CardProps {
  children: React.ReactNode
  title?: string
  subtitle?: string
  style?: React.CSSProperties
}

export function Card({
  children,
  title,
  subtitle,
  style,
}: CardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-surface rounded-xl p-6 shadow-um-md mb-4 border border-border/50"
      style={style}
    >
      {title && (
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-text">{title}</h3>
          {subtitle && (
            <p className="text-sm text-text-secondary mt-1">{subtitle}</p>
          )}
        </div>
      )}
      {children}
    </motion.div>
  )
}

interface SidebarProps {
  children: React.ReactNode
  width?: string
  collapsed?: boolean
  style?: React.CSSProperties
}

export function Sidebar({
  children,
  width = '280px',
  collapsed = false,
  style,
}: SidebarProps) {
  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-0 h-screen bg-surface border-r border-border/50 overflow-y-auto z-40"
      style={{
        width: collapsed ? '64px' : width,
        padding: collapsed ? '16px 8px' : '24px 16px',
        ...style,
      }}
    >
      <div className="space-y-4">
        {children}
      </div>
    </motion.aside>
  )
}

interface SidebarWrapperProps {
  children: React.ReactNode
  sidebarWidth?: string
  collapsed?: boolean
}

export function SidebarWrapper({
  children,
  sidebarWidth = '280px',
  collapsed = false,
}: SidebarWrapperProps) {
  return (
    <div
      style={{
        marginLeft: collapsed ? '64px' : sidebarWidth,
        transition: 'margin-left 0.3s ease',
      }}
    >
      {children}
    </div>
  )
}
