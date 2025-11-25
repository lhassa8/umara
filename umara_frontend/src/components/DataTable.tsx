import React from 'react'
import { motion } from 'framer-motion'

interface DataTableProps {
  data: Record<string, unknown>[]
  columns?: string[]
  height?: string
  style?: React.CSSProperties
}

export function DataTable({
  data,
  columns,
  height,
  style,
}: DataTableProps) {
  // If columns not provided, infer from first row
  const tableColumns = columns || (data.length > 0 ? Object.keys(data[0]) : [])

  if (tableColumns.length === 0) {
    return (
      <div className="text-sm text-text-tertiary mb-4">
        No data to display
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4 overflow-hidden rounded-lg border border-border"
      style={{
        maxHeight: height,
        overflowY: height ? 'auto' : undefined,
        ...style,
      }}
    >
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-background-secondary border-b border-border">
            {tableColumns.map((col, i) => (
              <th
                key={i}
                className="px-4 py-3 text-left font-semibold text-text"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <motion.tr
              key={rowIndex}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: rowIndex * 0.02 }}
              className={`
                border-b border-border last:border-b-0
                ${rowIndex % 2 === 0 ? 'bg-surface' : 'bg-background-secondary/50'}
                hover:bg-surface-hover transition-colors
              `}
            >
              {tableColumns.map((col, colIndex) => (
                <td
                  key={colIndex}
                  className="px-4 py-3 text-text"
                >
                  {formatCellValue(row[col])}
                </td>
              ))}
            </motion.tr>
          ))}
        </tbody>
      </table>
    </motion.div>
  )
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return '-'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}
