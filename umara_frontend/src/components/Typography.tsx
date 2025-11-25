import React from 'react'
import { motion } from 'framer-motion'

interface TextProps {
  content: string
  style?: React.CSSProperties
}

export function Text({ content, style }: TextProps) {
  return (
    <motion.p
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-text leading-relaxed mb-3"
      style={style}
    >
      {content}
    </motion.p>
  )
}

interface HeaderProps {
  content: string
  level?: number
  style?: React.CSSProperties
}

export function Header({ content, level = 1, style }: HeaderProps) {
  const Tag = `h${Math.min(Math.max(level, 1), 6)}` as keyof JSX.IntrinsicElements

  const sizeClasses: Record<number, string> = {
    1: 'text-4xl font-bold tracking-tight',
    2: 'text-3xl font-bold tracking-tight',
    3: 'text-2xl font-semibold',
    4: 'text-xl font-semibold',
    5: 'text-lg font-medium',
    6: 'text-base font-medium',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -5 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <Tag
        className={`${sizeClasses[level]} text-text mb-4`}
        style={style}
      >
        {content}
      </Tag>
    </motion.div>
  )
}

interface SubheaderProps {
  content: string
  style?: React.CSSProperties
}

export function Subheader({ content, style }: SubheaderProps) {
  return (
    <motion.h3
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-xl font-semibold text-text mb-3"
      style={style}
    >
      {content}
    </motion.h3>
  )
}

interface MarkdownProps {
  content: string
  style?: React.CSSProperties
}

export function Markdown({ content, style }: MarkdownProps) {
  // Simple markdown rendering - in production, use a proper markdown parser
  return (
    <div
      className="prose prose-slate max-w-none mb-4"
      style={style}
      dangerouslySetInnerHTML={{ __html: content }}
    />
  )
}

interface CodeProps {
  content: string
  language?: string
  lineNumbers?: boolean
  style?: React.CSSProperties
}

export function Code({ content, language = 'text', lineNumbers = true, style }: CodeProps) {
  const lines = content.split('\n')

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      <div className="bg-slate-900 rounded-lg overflow-hidden">
        {language && (
          <div className="px-4 py-2 bg-slate-800 text-slate-400 text-xs font-mono">
            {language}
          </div>
        )}
        <pre className="p-4 overflow-x-auto">
          <code className="text-sm font-mono text-slate-100">
            {lineNumbers ? (
              <table className="border-collapse">
                <tbody>
                  {lines.map((line, i) => (
                    <tr key={i}>
                      <td className="pr-4 text-slate-500 select-none text-right w-8">
                        {i + 1}
                      </td>
                      <td className="whitespace-pre">{line}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              content
            )}
          </code>
        </pre>
      </div>
    </motion.div>
  )
}
