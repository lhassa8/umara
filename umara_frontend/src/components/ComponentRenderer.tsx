import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ComponentTree } from '../App'

// Import individual components
import { Text, Header, Subheader, Markdown, Code, StreamingText } from './Typography'
import { Button } from './Button'
import { Input, TextArea } from './Input'
import { Slider } from './Slider'
import { Select, MultiSelect } from './Select'
import { Checkbox, Toggle, Radio } from './Checkbox'
import { Card, Container, Columns, Column, Grid, Sidebar } from './Layout'
import { Tabs } from './Tabs'
import { Alert } from './Alert'
import { Metric, Progress, Spinner } from './DataDisplay'
import { Divider, Spacer } from './Divider'
import { DataTable } from './DataTable'
import { Image, Video, Audio, LeafletMap } from './Media'

// CopyButton component with its own state
function CopyButton({ text, label, successLabel, style }: {
  text: string
  label?: string
  successLabel?: string
  style?: React.CSSProperties
}) {
  const [copied, setCopied] = React.useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <button
      className="inline-flex items-center gap-2 px-4 py-2 bg-surface border border-border rounded-lg text-text hover:bg-surface-hover transition-colors mb-4"
      onClick={handleCopy}
      style={style}
    >
      {copied ? (
        <>
          <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          {successLabel || 'Copied!'}
        </>
      ) : (
        <>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          {label || 'Copy'}
        </>
      )}
    </button>
  )
}

// FileUploader component with drag & drop and file selection
function FileUploader({
  label,
  accept,
  multiple,
  disabled,
  maxFileSize,
  stateKey,
  onStateUpdate,
  style
}: {
  label?: string
  accept?: string[]
  multiple?: boolean
  disabled?: boolean
  maxFileSize?: number
  stateKey?: string
  onStateUpdate: (key: string, value: unknown) => void
  style?: React.CSSProperties
}) {
  const fileInputRef = React.useRef<HTMLInputElement>(null)
  const [dragActive, setDragActive] = React.useState(false)
  const [uploadedFiles, setUploadedFiles] = React.useState<Array<{name: string, size: number, type: string}>>([])
  const [error, setError] = React.useState<string | null>(null)

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return
    setError(null)

    const fileArray = Array.from(files)
    const processedFiles: Array<{name: string, size: number, type: string, data?: string}> = []

    for (const file of fileArray) {
      // Check file size
      if (maxFileSize && file.size > maxFileSize) {
        setError(`File "${file.name}" exceeds maximum size of ${Math.round(maxFileSize / 1024 / 1024)}MB`)
        continue
      }

      // Read file as base64
      const data = await new Promise<string>((resolve) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result as string)
        reader.readAsDataURL(file)
      })

      processedFiles.push({
        name: file.name,
        size: file.size,
        type: file.type,
        data: data
      })
    }

    if (processedFiles.length > 0) {
      setUploadedFiles(processedFiles.map(f => ({ name: f.name, size: f.size, type: f.type })))
      const result = multiple ? processedFiles : processedFiles[0]
      if (stateKey) {
        onStateUpdate(stateKey, result)
      }
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (!disabled && e.dataTransfer.files) {
      handleFiles(e.dataTransfer.files)
    }
  }

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click()
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files)
  }

  const acceptString = accept?.join(',')

  return (
    <div style={style} className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-text mb-1.5">{label}</label>
      )}
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer
          ${dragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'}
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <svg className="w-10 h-10 mx-auto text-text-secondary mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p className="text-text-secondary text-sm">
          {dragActive ? 'Drop files here' : 'Drop files here or click to upload'}
        </p>
        {accept && accept.length > 0 && (
          <p className="text-text-secondary text-xs mt-1">
            Accepted: {accept.join(', ')}
          </p>
        )}
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept={acceptString}
          multiple={multiple}
          disabled={disabled}
          onChange={handleChange}
        />
      </div>
      {error && (
        <p className="text-red-500 text-sm mt-2">{error}</p>
      )}
      {uploadedFiles.length > 0 && (
        <div className="mt-3 space-y-2">
          {uploadedFiles.map((file, index) => (
            <div key={index} className="flex items-center gap-2 p-2 bg-surface rounded border border-border">
              <svg className="w-4 h-4 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span className="text-sm text-text flex-1 truncate">{file.name}</span>
              <span className="text-xs text-text-secondary">{Math.round(file.size / 1024)}KB</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

interface ComponentRendererProps {
  component: ComponentTree
  onEvent: (componentId: string, eventType: string, payload?: Record<string, unknown>) => void
  onStateUpdate: (key: string, value: unknown) => void
  state: Record<string, unknown>
}

export function ComponentRenderer({
  component,
  onEvent,
  onStateUpdate,
  state,
}: ComponentRendererProps) {
  const { id, type, props, children, style } = component

  // Helper to render children
  const renderChildren = () => {
    if (!children || children.length === 0) return null
    return children.map((child, index) => (
      <ComponentRenderer
        key={child.id || index}
        component={child}
        onEvent={onEvent}
        onStateUpdate={onStateUpdate}
        state={state}
      />
    ))
  }

  // Apply custom styles
  const customStyle = style ? Object.entries(style).reduce((acc, [key, value]) => {
    // Convert kebab-case to camelCase
    const camelKey = key.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())
    return { ...acc, [camelKey]: value }
  }, {} as React.CSSProperties) : undefined

  // Render based on component type
  switch (type) {
    case 'root':
      return (
        <AnimatePresence mode="wait">
          <motion.div
            key="root"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            {renderChildren()}
          </motion.div>
        </AnimatePresence>
      )

    // Typography
    case 'text':
      // Handle caption variant
      if (props.variant === 'caption') {
        return (
          <p className="text-sm text-text-secondary mb-2" style={customStyle}>
            {props.content as string}
          </p>
        )
      }
      return (
        <Text
          content={props.content as string}
          style={customStyle}
        />
      )

    case 'streaming_text':
      return (
        <StreamingText
          content={props.content as string || ''}
          streaming={props.streaming as boolean}
          style={customStyle}
        />
      )

    case 'header':
      return (
        <Header
          content={props.content as string}
          level={props.level as number}
          style={customStyle}
        />
      )

    // heading type (used by title() with level="title")
    case 'heading':
      if (props.level === 'title') {
        return (
          <h1 className="text-3xl font-bold text-text mb-4" style={customStyle}>
            {props.content as string}
          </h1>
        )
      }
      return (
        <Header
          content={props.content as string}
          level={props.level as number}
          style={customStyle}
        />
      )

    case 'subheader':
      return (
        <Subheader
          content={props.content as string}
          style={customStyle}
        />
      )

    case 'markdown':
      return (
        <Markdown
          content={props.content as string}
          style={customStyle}
        />
      )

    case 'code':
      return (
        <Code
          content={props.content as string}
          language={props.language as string}
          lineNumbers={props.lineNumbers as boolean}
          style={customStyle}
        />
      )

    // Widgets
    case 'button':
      return (
        <Button
          label={props.label as string}
          variant={props.variant as 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'}
          disabled={props.disabled as boolean}
          fullWidth={props.fullWidth as boolean}
          onClick={() => onEvent(id, 'click')}
          style={customStyle}
        />
      )

    case 'input':
      return (
        <Input
          id={id}
          label={props.label as string}
          value={(props.value ?? '') as string}
          placeholder={props.placeholder as string}
          type={props.type as string}
          disabled={props.disabled as boolean}
          maxChars={props.maxChars as number | undefined}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    case 'textarea':
      return (
        <TextArea
          id={id}
          label={props.label as string}
          value={(props.value ?? '') as string}
          placeholder={props.placeholder as string}
          rows={props.rows as number}
          height={props.height as number | undefined}
          disabled={props.disabled as boolean}
          maxChars={props.maxChars as number | undefined}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    case 'slider':
      return (
        <Slider
          label={props.label as string}
          value={(props.value ?? props.min ?? 0) as number}
          min={props.min as number}
          max={props.max as number}
          step={props.step as number}
          disabled={props.disabled as boolean}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    case 'select':
      return (
        <Select
          label={props.label as string}
          value={props.value as string}
          options={props.options as Array<string | { value: string; label: string }>}
          placeholder={props.placeholder as string}
          disabled={props.disabled as boolean}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    case 'multiselect':
      return (
        <MultiSelect
          label={props.label as string}
          value={(props.value ?? []) as string[]}
          options={props.options as Array<string | { value: string; label: string }>}
          placeholder={props.placeholder as string}
          disabled={props.disabled as boolean}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    case 'checkbox':
      return (
        <Checkbox
          label={props.label as string}
          checked={(props.value ?? false) as boolean}
          disabled={props.disabled as boolean}
          onChange={(checked) => onStateUpdate(props.stateKey as string || id, checked)}
          style={customStyle}
        />
      )

    case 'toggle':
      return (
        <Toggle
          label={props.label as string}
          checked={(props.value ?? false) as boolean}
          disabled={props.disabled as boolean}
          onChange={(checked) => onStateUpdate(props.stateKey as string || id, checked)}
          style={customStyle}
        />
      )

    case 'radio':
      return (
        <Radio
          label={props.label as string}
          value={props.value as string}
          options={props.options as string[]}
          horizontal={props.horizontal as boolean}
          disabled={props.disabled as boolean}
          onChange={(value) => onStateUpdate(props.stateKey as string || id, value)}
          style={customStyle}
        />
      )

    // Layout
    case 'container':
      return (
        <Container style={customStyle}>
          {renderChildren()}
        </Container>
      )

    case 'columns':
      return (
        <Columns
          count={props.count as number}
          gap={props.gap as string}
          style={customStyle}
        >
          {renderChildren()}
        </Columns>
      )

    case 'column':
      return (
        <Column style={customStyle}>
          {renderChildren()}
        </Column>
      )

    case 'grid':
      return (
        <Grid
          columns={props.columns as number | string}
          gap={props.gap as string}
          rowGap={props.rowGap as string}
          style={customStyle}
        >
          {renderChildren()}
        </Grid>
      )

    case 'card':
      return (
        <Card
          title={props.title as string}
          subtitle={props.subtitle as string}
          style={customStyle}
        >
          {renderChildren()}
        </Card>
      )

    case 'sidebar':
      return (
        <Sidebar
          width={props.width as string}
          collapsed={props.collapsed as boolean}
          style={customStyle}
        >
          {renderChildren()}
        </Sidebar>
      )

    case 'tabs':
      const activeTabIndex = (props.activeTab ?? 0) as number
      // Find the tab child that matches the active index
      const activeTabContent = children?.find(
        (child) => child.type === 'tab' && child.props.index === activeTabIndex
      )
      return (
        <div>
          <Tabs
            tabs={props.tabs as string[]}
            activeTab={activeTabIndex}
            onChange={(index) => onStateUpdate(props.stateKey as string || id, index)}
            style={customStyle}
          />
          {activeTabContent && (
            <ComponentRenderer
              component={activeTabContent}
              onEvent={onEvent}
              onStateUpdate={onStateUpdate}
              state={state}
            />
          )}
        </div>
      )

    case 'tab':
      // Tab content is rendered by parent tabs component
      return (
        <div style={customStyle}>
          {renderChildren()}
        </div>
      )

    case 'accordion':
      const accordionItems = (props.items as string[]) || []
      const openItems = (props.openItems as string[]) || []
      const allowMultiple = props.allowMultiple as boolean
      const accordionStateKey = props.stateKey as string

      return (
        <div className="space-y-2" style={customStyle}>
          {accordionItems.map((item, index) => {
            const isOpen = openItems.includes(item)
            return (
              <div key={index} className="border border-border rounded-lg overflow-hidden">
                <button
                  className="w-full px-4 py-3 flex items-center justify-between bg-surface hover:bg-surface-hover text-text font-medium text-left transition-colors"
                  onClick={() => {
                    let newOpenItems: string[]
                    if (isOpen) {
                      newOpenItems = openItems.filter(i => i !== item)
                    } else {
                      newOpenItems = allowMultiple ? [...openItems, item] : [item]
                    }
                    onStateUpdate(accordionStateKey, newOpenItems)
                  }}
                >
                  <span>{item}</span>
                  <svg
                    className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {isOpen && (
                  <div className="px-4 py-3 bg-background border-t border-border">
                    {renderChildren()}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )

    // Feedback
    case 'success':
      return <Alert type="success" message={props.message as string} style={customStyle} />

    case 'error':
      return (
        <Alert
          type="error"
          message={props.message as string}
          traceback={props.traceback as string}
          style={customStyle}
        />
      )

    case 'warning':
      return <Alert type="warning" message={props.message as string} style={customStyle} />

    case 'info':
      return <Alert type="info" message={props.message as string} style={customStyle} />

    // Data Display
    case 'metric':
      return (
        <Metric
          label={props.label as string}
          value={props.value as string}
          delta={props.delta as number}
          deltaLabel={props.deltaLabel as string}
          style={customStyle}
        />
      )

    case 'progress':
      return (
        <Progress
          value={props.value as number}
          label={props.label as string}
          style={customStyle}
        />
      )

    case 'spinner':
      return <Spinner text={props.text as string} style={customStyle} />

    case 'stat_card':
      const statTitle = props.title as string
      const statValue = props.value as string
      const statDescription = props.description as string
      const statTrend = props.trend as number | undefined
      const statTrendLabel = props.trendLabel as string | undefined

      return (
        <div className="bg-surface border border-border rounded-xl p-6 mb-4" style={customStyle}>
          <div className="text-text-secondary text-sm font-medium mb-1">{statTitle}</div>
          <div className="text-3xl font-bold text-text mb-2">{statValue}</div>
          {(statTrend !== undefined || statDescription) && (
            <div className="flex items-center gap-2">
              {statTrend !== undefined && (
                <span className={`inline-flex items-center text-sm font-medium ${
                  statTrend > 0 ? 'text-green-600' : statTrend < 0 ? 'text-red-600' : 'text-text-secondary'
                }`}>
                  {statTrend > 0 ? (
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                    </svg>
                  ) : statTrend < 0 ? (
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                  ) : null}
                  {statTrend > 0 ? '+' : ''}{statTrend}%
                </span>
              )}
              {statTrendLabel && (
                <span className="text-text-secondary text-sm">{statTrendLabel}</span>
              )}
              {statDescription && !statTrendLabel && (
                <span className="text-text-secondary text-sm">{statDescription}</span>
              )}
            </div>
          )}
        </div>
      )

    case 'dataframe':
      return (
        <DataTable
          data={props.data as Record<string, unknown>[]}
          columns={props.columns as string[]}
          height={props.height as string}
          style={customStyle}
        />
      )

    case 'table':
      // Table component accepts 2D array (list of lists) where first row is headers
      const tableData = props.data as unknown[][]
      if (!tableData || !Array.isArray(tableData) || tableData.length === 0) {
        return <div className="text-sm text-text-tertiary mb-4">No data to display</div>
      }
      const headers = tableData[0] as string[]
      const rows = tableData.slice(1)
      return (
        <div style={customStyle} className="mb-4 overflow-hidden rounded-lg border border-border">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-background-secondary border-b border-border">
                {headers.map((header, i) => (
                  <th key={i} className="px-4 py-3 text-left font-medium text-text">
                    {String(header)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, rowIdx) => (
                <tr key={rowIdx} className="border-b border-border last:border-b-0 hover:bg-surface-hover">
                  {(row as unknown[]).map((cell, cellIdx) => (
                    <td key={cellIdx} className="px-4 py-3 text-text">
                      {String(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )

    // Utility
    case 'divider':
      return <Divider style={customStyle} />

    case 'spacer':
      return <Spacer height={props.height as string} />

    // Media
    case 'image':
      return (
        <Image
          src={props.src as string}
          alt={props.alt as string}
          width={props.width as string}
          height={props.height as string}
          caption={props.caption as string}
          style={customStyle}
        />
      )

    case 'video':
      return (
        <Video
          src={props.src as string}
          autoplay={props.autoplay as boolean}
          controls={props.controls as boolean}
          loop={props.loop as boolean}
          muted={props.muted as boolean}
          width={props.width as string}
          height={props.height as string}
          style={customStyle}
        />
      )

    case 'audio':
      return (
        <Audio
          src={props.src as string}
          autoplay={props.autoplay as boolean}
          controls={props.controls as boolean}
          loop={props.loop as boolean}
          style={customStyle}
        />
      )

    // Form submit button - renders like a primary button
    case 'form_submit_button':
      return (
        <Button
          label={props.label as string}
          variant={(props.variant as 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger') || 'primary'}
          disabled={props.disabled as boolean}
          fullWidth={props.fullWidth as boolean}
          onClick={() => onEvent(id, 'click', { is_form_submit: true })}
          style={customStyle}
        />
      )

    // Expander - collapsible section
    case 'expander':
      return (
        <div className="border border-border/50 rounded-lg mb-4" style={customStyle}>
          <button
            className="w-full px-4 py-3 flex items-center justify-between text-left hover:bg-surface-hover transition-colors rounded-lg"
            onClick={() => onStateUpdate(props.stateKey as string || id, !(props.expanded as boolean))}
          >
            <span className="font-medium text-text">{props.title as string}</span>
            <svg
              className={`w-5 h-5 text-text-secondary transition-transform ${props.expanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {(props.expanded as boolean) && (
            <div className="px-4 pb-4">
              {renderChildren()}
            </div>
          )}
        </div>
      )

    // Date input
    case 'date':
      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <input
            type="date"
            value={(props.value as string) || ''}
            min={props.minDate as string}
            max={props.maxDate as string}
            disabled={props.disabled as boolean}
            onChange={(e) => onStateUpdate(props.stateKey as string || id, e.target.value)}
            className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-text focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>
      )

    // Time input
    case 'time':
      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <input
            type="time"
            value={(props.value as string) || ''}
            disabled={props.disabled as boolean}
            onChange={(e) => onStateUpdate(props.stateKey as string || id, e.target.value)}
            className="w-full px-4 py-2.5 bg-surface border border-border rounded-lg text-text focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>
      )

    // Number input
    case 'number_input':
      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <div className="flex items-center">
            <button
              className="px-3 py-2.5 bg-surface border border-border rounded-l-lg text-text hover:bg-surface-hover disabled:opacity-50"
              onClick={() => {
                const current = (props.value as number) || 0
                const step = (props.step as number) || 1
                const min = props.min as number
                const newVal = min !== undefined ? Math.max(min, current - step) : current - step
                onStateUpdate(props.stateKey as string || id, newVal)
              }}
              disabled={props.disabled as boolean}
            >
              -
            </button>
            <input
              type="number"
              value={(props.value as number) ?? 0}
              min={props.min as number}
              max={props.max as number}
              step={props.step as number}
              disabled={props.disabled as boolean}
              onChange={(e) => onStateUpdate(props.stateKey as string || id, parseFloat(e.target.value) || 0)}
              className="flex-1 px-4 py-2.5 bg-surface border-y border-border text-text text-center focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              className="px-3 py-2.5 bg-surface border border-border rounded-r-lg text-text hover:bg-surface-hover disabled:opacity-50"
              onClick={() => {
                const current = (props.value as number) || 0
                const step = (props.step as number) || 1
                const max = props.max as number
                const newVal = max !== undefined ? Math.min(max, current + step) : current + step
                onStateUpdate(props.stateKey as string || id, newVal)
              }}
              disabled={props.disabled as boolean}
            >
              +
            </button>
          </div>
        </div>
      )

    // Badge
    case 'badge':
      const badgeVariants: Record<string, string> = {
        default: 'bg-secondary-light text-secondary',
        success: 'bg-success-light text-success-dark',
        warning: 'bg-warning-light text-warning-dark',
        error: 'bg-error-light text-error-dark',
        info: 'bg-info-light text-info-dark',
      }
      return (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeVariants[(props.variant as string) || 'default'] || badgeVariants.default}`}
          style={customStyle}
        >
          {props.text as string}
        </span>
      )

    // Avatar
    case 'avatar':
      const avatarSizes: Record<string, string> = {
        sm: 'w-8 h-8 text-xs',
        md: 'w-10 h-10 text-sm',
        lg: 'w-12 h-12 text-base',
        xl: 'w-16 h-16 text-lg',
      }
      const avatarSize = avatarSizes[(props.size as string) || 'md'] || avatarSizes.md
      const initials = props.name ? (props.name as string).split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : '?'
      return (
        <div
          className={`${avatarSize} rounded-full bg-primary flex items-center justify-center text-white font-medium overflow-hidden`}
          style={customStyle}
        >
          {props.src ? (
            <img src={props.src as string} alt={props.name as string || 'Avatar'} className="w-full h-full object-cover" />
          ) : (
            initials
          )}
        </div>
      )

    // Toast notification (renders as a fixed notification)
    case 'toast':
      return (
        <div
          className="fixed bottom-4 right-4 z-50 bg-surface border border-border rounded-lg shadow-lg p-4 max-w-sm"
          style={customStyle}
        >
          <div className="flex items-center gap-2">
            {props.icon ? <span>{String(props.icon)}</span> : null}
            <span className="text-text">{String(props.message)}</span>
          </div>
        </div>
      )

    // Modal dialog
    case 'modal':
      if (!(props.isOpen as boolean)) return null
      const modalSizes: Record<string, string> = {
        sm: 'max-w-sm',
        md: 'max-w-md',
        lg: 'max-w-lg',
        xl: 'max-w-xl',
        full: 'max-w-4xl',
      }
      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => props.closeOnOverlay && onStateUpdate(props.stateKey as string || id, false)}
          />
          <div className={`relative bg-surface rounded-xl shadow-xl p-6 ${modalSizes[(props.size as string) || 'md']} w-full mx-4`} style={customStyle}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-text">{props.title as string}</h2>
              <button
                className="text-text-secondary hover:text-text p-1"
                onClick={() => onStateUpdate(props.stateKey as string || id, false)}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            {renderChildren()}
          </div>
        </div>
      )

    // Breadcrumbs navigation
    case 'breadcrumbs':
      const items = (props.items as Array<{ label: string; href?: string }>) || []
      const separator = (props.separator as string) || '/'
      return (
        <nav className="flex items-center space-x-2 text-sm mb-4" style={customStyle}>
          {items.map((item, index) => (
            <React.Fragment key={index}>
              {index > 0 && <span className="text-text-secondary">{separator}</span>}
              {item.href ? (
                <a href={item.href} className="text-primary hover:underline">{item.label}</a>
              ) : (
                <span className="text-text-secondary">{item.label}</span>
              )}
            </React.Fragment>
          ))}
        </nav>
      )

    // Steps indicator
    case 'steps':
      const steps = (props.steps as string[]) || []
      const currentStep = (props.current as number) || 0
      return (
        <div className="flex items-center mb-4" style={customStyle}>
          {steps.map((step, index) => (
            <React.Fragment key={index}>
              {index > 0 && (
                <div className={`flex-1 h-0.5 mx-2 ${index <= currentStep ? 'bg-primary' : 'bg-border'}`} />
              )}
              <div className="flex items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    index < currentStep
                      ? 'bg-primary text-white'
                      : index === currentStep
                      ? 'bg-primary text-white ring-4 ring-primary/20'
                      : 'bg-surface border border-border text-text-secondary'
                  }`}
                >
                  {index < currentStep ? '✓' : index + 1}
                </div>
                <span className={`ml-2 text-sm ${index <= currentStep ? 'text-text' : 'text-text-secondary'}`}>
                  {step}
                </span>
              </div>
            </React.Fragment>
          ))}
        </div>
      )

    // JSON viewer
    case 'json_viewer':
      return (
        <pre
          className="bg-surface border border-border rounded-lg p-4 overflow-auto text-sm font-mono text-text mb-4"
          style={customStyle}
        >
          {JSON.stringify(props.data, null, 2)}
        </pre>
      )

    // HTML embed
    case 'html':
      return (
        <div
          className="mb-4"
          style={customStyle}
          dangerouslySetInnerHTML={{ __html: props.content as string }}
        />
      )

    // Pagination
    case 'pagination':
      const totalPages = (props.totalPages as number) || 1
      const currentPage = (props.currentPage as number) || 1
      return (
        <div className="flex items-center justify-center gap-2 mb-4" style={customStyle}>
          <button
            className="px-3 py-1.5 rounded-lg bg-surface border border-border text-text hover:bg-surface-hover disabled:opacity-50"
            onClick={() => onStateUpdate(props.stateKey as string || id, Math.max(1, currentPage - 1))}
            disabled={currentPage <= 1}
          >
            Prev
          </button>
          <span className="px-3 py-1.5 text-text">
            {currentPage} / {totalPages}
          </span>
          <button
            className="px-3 py-1.5 rounded-lg bg-surface border border-border text-text hover:bg-surface-hover disabled:opacity-50"
            onClick={() => onStateUpdate(props.stateKey as string || id, Math.min(totalPages, currentPage + 1))}
            disabled={currentPage >= totalPages}
          >
            Next
          </button>
        </div>
      )

    // Color picker
    case 'colorpicker':
      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <div className="flex items-center gap-3">
            <input
              type="color"
              value={(props.value as string) || '#6366f1'}
              disabled={props.disabled as boolean}
              onChange={(e) => onStateUpdate(props.stateKey as string || id, e.target.value)}
              className="w-12 h-10 p-1 bg-surface border border-border rounded-lg cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <input
              type="text"
              value={(props.value as string) || '#6366f1'}
              disabled={props.disabled as boolean}
              onChange={(e) => onStateUpdate(props.stateKey as string || id, e.target.value)}
              className="flex-1 px-4 py-2.5 bg-surface border border-border rounded-lg text-text font-mono text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="#000000"
            />
            <div
              className="w-10 h-10 rounded-lg border border-border"
              style={{ backgroundColor: (props.value as string) || '#6366f1' }}
            />
          </div>
        </div>
      )

    // Star rating
    case 'rating':
      const maxStars = (props.maxValue as number) || 5
      const currentRating = (props.value as number) || 0
      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <div className="flex items-center gap-1">
            {Array.from({ length: maxStars }, (_, i) => (
              <button
                key={i}
                type="button"
                disabled={props.disabled as boolean}
                onClick={() => onStateUpdate(props.stateKey as string || id, i + 1)}
                className="text-2xl transition-colors focus:outline-none disabled:cursor-not-allowed"
              >
                <span className={i < currentRating ? 'text-yellow-400' : 'text-gray-300'}>
                  ★
                </span>
              </button>
            ))}
            <span className="ml-2 text-sm text-text-secondary">
              {currentRating} / {maxStars}
            </span>
          </div>
        </div>
      )

    // Pills / segmented control
    case 'pills':
      const pillOptions = (props.options as string[]) || []
      const pillValue = props.value as string | string[] | null
      const selectionMode = (props.selectionMode as string) || 'single'
      const isMulti = selectionMode === 'multi'
      const selectedPills = isMulti
        ? (Array.isArray(pillValue) ? pillValue : [])
        : (pillValue ? [pillValue] : [])

      return (
        <div className="mb-4" style={customStyle}>
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-2">{String(props.label)}</label>
          ) : null}
          <div className="flex flex-wrap gap-2">
            {pillOptions.map((option) => {
              const isSelected = selectedPills.includes(option)
              return (
                <button
                  key={option}
                  type="button"
                  disabled={props.disabled as boolean}
                  onClick={() => {
                    if (isMulti) {
                      const newValue = isSelected
                        ? selectedPills.filter((v) => v !== option)
                        : [...selectedPills, option]
                      onStateUpdate(props.stateKey as string || id, newValue)
                    } else {
                      onStateUpdate(props.stateKey as string || id, option)
                    }
                  }}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all focus:outline-none focus:ring-2 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed ${
                    isSelected
                      ? 'bg-primary text-white'
                      : 'bg-surface border border-border text-text hover:bg-surface-hover'
                  }`}
                >
                  {option}
                </button>
              )
            })}
          </div>
        </div>
      )

    // Empty state placeholder
    case 'empty_state':
      const emptyIcon = props.icon as string
      const emptyDescription = props.description as string
      const emptyActionLabel = props.actionLabel as string
      return (
        <div className="flex flex-col items-center justify-center py-12 px-4 text-center" style={customStyle}>
          {emptyIcon ? (
            <div className="mb-4 text-text-secondary">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {emptyIcon === 'search' && (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                )}
                {emptyIcon === 'inbox' && (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                )}
                {emptyIcon === 'document' && (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                )}
                {emptyIcon === 'folder' && (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                )}
                {!['search', 'inbox', 'document', 'folder'].includes(emptyIcon) && (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                )}
              </svg>
            </div>
          ) : null}
          <h3 className="text-lg font-semibold text-text mb-2">{props.title as string}</h3>
          {emptyDescription ? (
            <p className="text-text-secondary mb-4 max-w-md">{emptyDescription}</p>
          ) : null}
          {emptyActionLabel ? (
            <button
              className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-hover transition-colors"
              onClick={() => onEvent(id, 'click', {})}
            >
              {emptyActionLabel}
            </button>
          ) : null}
        </div>
      )

    // Copy button
    case 'copy_button':
      return (
        <CopyButton
          text={props.text as string}
          label={props.label as string}
          successLabel={props.successLabel as string}
          style={customStyle}
        />
      )

    // Download button
    case 'download_button':
      const downloadLabel = props.label as string || 'Download'
      const downloadData = props.data as string
      const downloadFileName = props.file_name as string || 'download.txt'
      const downloadMime = props.mime as string || 'text/plain'
      const downloadDisabled = props.disabled as boolean
      const downloadVariant = props.variant as string || 'secondary'

      const variantClasses: Record<string, string> = {
        primary: 'bg-primary text-white hover:bg-primary-hover',
        secondary: 'bg-surface border border-border text-text hover:bg-surface-hover',
        outline: 'bg-transparent border border-primary text-primary hover:bg-primary/10',
      }

      const handleDownload = () => {
        const blob = new Blob([downloadData], { type: downloadMime })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = downloadFileName
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        onEvent(id, 'click', {})
      }

      return (
        <button
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg transition-colors mb-4 disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses[downloadVariant] || variantClasses.secondary}`}
          onClick={handleDownload}
          disabled={downloadDisabled}
          style={customStyle}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          {downloadLabel}
        </button>
      )

    // Tooltip
    case 'tooltip':
      const tooltipContent = props.content as string
      const tooltipText = props.text as string
      const tooltipPosition = (props.position as string) || 'top'
      const [showTooltip, setShowTooltip] = React.useState(false)

      const tooltipPositionClasses: Record<string, string> = {
        top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
        bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
        left: 'right-full top-1/2 -translate-y-1/2 mr-2',
        right: 'left-full top-1/2 -translate-y-1/2 ml-2',
      }

      return (
        <div
          className="relative inline-block"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          style={customStyle}
        >
          <span className="cursor-help text-text underline decoration-dotted underline-offset-2">
            {tooltipContent}
          </span>
          {showTooltip && (
            <div className={`absolute z-50 px-3 py-2 text-sm bg-gray-900 text-white rounded-lg shadow-lg whitespace-nowrap ${tooltipPositionClasses[tooltipPosition]}`}>
              {tooltipText}
              <div className={`absolute w-2 h-2 bg-gray-900 rotate-45 ${
                tooltipPosition === 'top' ? 'top-full left-1/2 -translate-x-1/2 -mt-1' :
                tooltipPosition === 'bottom' ? 'bottom-full left-1/2 -translate-x-1/2 -mb-1' :
                tooltipPosition === 'left' ? 'left-full top-1/2 -translate-y-1/2 -ml-1' :
                'right-full top-1/2 -translate-y-1/2 -mr-1'
              }`} />
            </div>
          )}
        </div>
      )

    // Tag input
    case 'tag_input':
      const tagLabel = props.label as string
      const tagPlaceholder = props.placeholder as string || 'Add a tag...'
      const tagValues = (props.value as string[]) || []
      const [tagInputValue, setTagInputValue] = React.useState('')

      const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && tagInputValue.trim()) {
          e.preventDefault()
          const newTags = [...tagValues, tagInputValue.trim()]
          onStateUpdate(props.stateKey as string || id, newTags)
          setTagInputValue('')
        }
      }

      const handleRemoveTag = (indexToRemove: number) => {
        const newTags = tagValues.filter((_, index) => index !== indexToRemove)
        onStateUpdate(props.stateKey as string || id, newTags)
      }

      return (
        <div className="mb-4" style={customStyle}>
          {tagLabel && (
            <label className="block text-sm font-medium text-text mb-1.5">{tagLabel}</label>
          )}
          <div className="flex flex-wrap gap-2 p-2 bg-surface border border-border rounded-lg min-h-[42px]">
            {tagValues.map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center gap-1 px-2 py-1 bg-primary/10 text-primary rounded-md text-sm"
              >
                {tag}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(index)}
                  className="hover:text-primary-dark"
                >
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
            ))}
            <input
              type="text"
              value={tagInputValue}
              onChange={(e) => setTagInputValue(e.target.value)}
              onKeyDown={handleAddTag}
              placeholder={tagValues.length === 0 ? tagPlaceholder : ''}
              className="flex-1 min-w-[100px] bg-transparent border-none outline-none text-text text-sm"
            />
          </div>
        </div>
      )

    // Avatar group
    case 'avatar_group':
      const avatars = (props.avatars as Array<{ name?: string; src?: string }>) || []
      const maxDisplay = (props.maxDisplay as number) || 4
      const displayAvatars = avatars.slice(0, maxDisplay)
      const remainingCount = avatars.length - maxDisplay
      const groupSize = (props.size as string) || 'md'
      const groupSizeClasses: Record<string, string> = {
        sm: 'w-8 h-8 text-xs',
        md: 'w-10 h-10 text-sm',
        lg: 'w-12 h-12 text-base',
        xl: 'w-16 h-16 text-lg',
      }

      return (
        <div className="flex -space-x-2 mb-4" style={customStyle}>
          {displayAvatars.map((avatar, index) => {
            const avatarInitials = avatar.name
              ? avatar.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
              : '?'
            return (
              <div
                key={index}
                className={`${groupSizeClasses[groupSize]} rounded-full bg-primary flex items-center justify-center text-white font-medium ring-2 ring-background overflow-hidden`}
                title={avatar.name}
              >
                {avatar.src ? (
                  <img src={avatar.src} alt={avatar.name || 'Avatar'} className="w-full h-full object-cover" />
                ) : (
                  avatarInitials
                )}
              </div>
            )
          })}
          {remainingCount > 0 && (
            <div
              className={`${groupSizeClasses[groupSize]} rounded-full bg-surface border border-border flex items-center justify-center text-text-secondary font-medium ring-2 ring-background`}
            >
              +{remainingCount}
            </div>
          )}
        </div>
      )

    // Loading skeleton (backend sends 'skeleton')
    case 'skeleton':
      const skeletonVariant = (props.variant as string) || 'text'
      const skeletonLines = (props.lines as number) || 3
      const skeletonHeight = props.height as string

      if (skeletonVariant === 'avatar') {
        return (
          <div className="animate-pulse mb-4" style={customStyle}>
            <div className="w-12 h-12 bg-gray-200 rounded-full" />
          </div>
        )
      }

      if (skeletonVariant === 'card') {
        return (
          <div className="animate-pulse mb-4" style={{ ...customStyle, height: skeletonHeight || '120px' }}>
            <div className="bg-gray-200 rounded-lg h-full w-full" />
          </div>
        )
      }

      if (skeletonVariant === 'image') {
        return (
          <div className="animate-pulse mb-4" style={{ ...customStyle, height: skeletonHeight || '200px' }}>
            <div className="bg-gray-200 rounded-lg h-full w-full flex items-center justify-center">
              <svg className="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        )
      }

      // Default: text variant
      return (
        <div className="animate-pulse space-y-2 mb-4" style={customStyle}>
          {Array.from({ length: skeletonLines }).map((_, i) => (
            <div
              key={i}
              className="bg-gray-200 rounded h-4"
              style={{ width: `${100 - (i * 15)}%` }}
            />
          ))}
        </div>
      )

    // Timeline
    case 'timeline':
      const timelineItems = (props.items as Array<{ title: string; description?: string; date?: string; icon?: string }>) || []

      return (
        <div className="relative mb-4" style={customStyle}>
          {/* Vertical line */}
          <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-border" />

          <div className="space-y-6">
            {timelineItems.map((item, index) => (
              <div key={index} className="relative flex gap-4">
                {/* Dot */}
                <div className="relative z-10 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white text-sm font-medium shrink-0">
                  {item.icon || (index + 1)}
                </div>

                {/* Content */}
                <div className="flex-1 bg-surface border border-border rounded-lg p-4 -mt-1">
                  <div className="flex items-start justify-between gap-2">
                    <h4 className="font-medium text-text">{item.title}</h4>
                    {item.date && (
                      <span className="text-xs text-text-secondary whitespace-nowrap">{item.date}</span>
                    )}
                  </div>
                  {item.description && (
                    <p className="text-sm text-text-secondary mt-1">{item.description}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )

    // Status indicator
    case 'status':
      const statusLabel = props.label as string
      const statusState = (props.state as string) || 'running'
      const statusExpanded = (props.expanded as boolean) !== false

      const statusColors: Record<string, string> = {
        running: 'text-blue-500',
        complete: 'text-green-500',
        error: 'text-red-500',
      }

      const statusIcons: Record<string, JSX.Element> = {
        running: (
          <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        ),
        complete: (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ),
        error: (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ),
      }

      return (
        <div className="border border-border rounded-lg mb-4" style={customStyle}>
          <div className="flex items-center gap-3 px-4 py-3">
            <span className={statusColors[statusState]}>
              {statusIcons[statusState]}
            </span>
            <span className="font-medium text-text">{statusLabel}</span>
          </div>
          {statusExpanded && children && children.length > 0 && (
            <div className="px-4 pb-3 border-t border-border pt-3">
              {renderChildren()}
            </div>
          )}
        </div>
      )

    // Select slider
    case 'select_slider':
      const selectSliderLabel = props.label as string
      const selectSliderOptions = (props.options as string[]) || []
      const selectSliderValue = props.value as string
      const selectSliderCurrentIndex = selectSliderOptions.indexOf(selectSliderValue)
      const selectSliderIndex = selectSliderCurrentIndex >= 0 ? selectSliderCurrentIndex : 0

      return (
        <div className="mb-4" style={customStyle}>
          {selectSliderLabel && (
            <label className="block text-sm font-medium text-text mb-2">{selectSliderLabel}</label>
          )}
          <div className="space-y-2">
            <input
              type="range"
              min={0}
              max={selectSliderOptions.length - 1}
              value={selectSliderIndex}
              onChange={(e) => {
                const newIndex = parseInt(e.target.value)
                onStateUpdate(props.stateKey as string || id, selectSliderOptions[newIndex])
              }}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary"
            />
            <div className="flex justify-between text-xs text-text-secondary">
              {selectSliderOptions.map((option, i) => (
                <span key={i} className={i === selectSliderIndex ? 'text-primary font-medium' : ''}>
                  {option}
                </span>
              ))}
            </div>
          </div>
        </div>
      )

    // Feedback component
    case 'feedback':
      const feedbackMapping = (props.sentimentMapping as Record<number, string>) || { 0: 'Bad', 1: 'Okay', 2: 'Good' }
      const feedbackValue = props.value as number | null
      const feedbackOptions = Object.entries(feedbackMapping)

      return (
        <div className="mb-4" style={customStyle}>
          <div className="flex items-center gap-2">
            {feedbackOptions.map(([score, label]) => {
              const scoreNum = parseInt(score)
              const isSelected = feedbackValue === scoreNum
              return (
                <button
                  key={score}
                  type="button"
                  onClick={() => onStateUpdate(props.stateKey as string || id, scoreNum)}
                  disabled={props.disabled as boolean}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    isSelected
                      ? 'bg-primary text-white'
                      : 'bg-surface border border-border text-text hover:bg-surface-hover'
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  {label}
                </button>
              )
            })}
          </div>
        </div>
      )

    // Segmented control
    case 'segmented_control':
      const segmentLabel = props.label as string
      const segmentOptions = (props.options as string[]) || []
      const segmentValue = props.value as string

      return (
        <div className="mb-4" style={customStyle}>
          {segmentLabel && (
            <label className="block text-sm font-medium text-text mb-2">{segmentLabel}</label>
          )}
          <div className="inline-flex p-1 bg-gray-100 rounded-lg">
            {segmentOptions.map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => onStateUpdate(props.stateKey as string || id, option)}
                disabled={props.disabled as boolean}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-all ${
                  segmentValue === option
                    ? 'bg-white text-text shadow-sm'
                    : 'text-text-secondary hover:text-text'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      )

    // Nav link
    case 'nav_link':
      const navLabel = props.label as string
      const navHref = props.href as string
      const navIcon = props.icon as string
      const navActive = props.active as boolean

      const iconMap: Record<string, JSX.Element> = {
        home: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />,
        settings: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />,
        user: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />,
      }

      return (
        <a
          href={navHref || '#'}
          className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors mb-1 ${
            navActive
              ? 'bg-primary/10 text-primary'
              : 'text-text hover:bg-surface-hover'
          }`}
          style={customStyle}
          onClick={(e) => {
            if (!navHref || navHref === '#') {
              e.preventDefault()
              onEvent(id, 'click')
            }
          }}
        >
          {navIcon && (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {iconMap[navIcon] || <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />}
            </svg>
          )}
          <span>{navLabel}</span>
        </a>
      )

    // Data editor (simplified table editor)
    case 'data_editor':
      const editorData = (props.data as Record<string, unknown>[]) || []

      if (editorData.length === 0) {
        return <div className="text-text-secondary mb-4">No data</div>
      }

      const editorColumns = Object.keys(editorData[0] || {})

      return (
        <div className="overflow-auto mb-4" style={customStyle}>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-surface">
                {editorColumns.map((col) => (
                  <th key={col} className="px-4 py-2 text-left text-sm font-medium text-text border border-border">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {editorData.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {editorColumns.map((col) => (
                    <td key={col} className="px-4 py-2 border border-border">
                      <input
                        type="text"
                        value={String(row[col] ?? '')}
                        onChange={(e) => {
                          const newData = [...editorData]
                          newData[rowIndex] = { ...newData[rowIndex], [col]: e.target.value }
                          onStateUpdate(props.stateKey as string || id, newData)
                        }}
                        className="w-full bg-transparent text-text text-sm focus:outline-none focus:ring-1 focus:ring-primary rounded px-1"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )

    // Popover
    case 'popover':
      const popoverTrigger = props.triggerLabel as string
      const [popoverOpen, setPopoverOpen] = React.useState(false)

      return (
        <div className="relative inline-block mb-4" style={customStyle}>
          <button
            type="button"
            onClick={() => setPopoverOpen(!popoverOpen)}
            className="px-4 py-2 bg-surface border border-border rounded-lg text-text hover:bg-surface-hover transition-colors"
          >
            {popoverTrigger}
          </button>
          {popoverOpen && (
            <>
              <div
                className="fixed inset-0 z-40"
                onClick={() => setPopoverOpen(false)}
              />
              <div className="absolute z-50 mt-2 p-4 bg-surface border border-border rounded-lg shadow-lg min-w-[200px]">
                {renderChildren()}
              </div>
            </>
          )}
        </div>
      )

    // Dialog (alias for modal with different styling)
    case 'dialog':
      if (!(props.isOpen as boolean)) return null

      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => onStateUpdate(props.stateKey as string || id, false)}
          />
          <div className="relative bg-surface rounded-xl shadow-xl p-6 max-w-md w-full mx-4" style={customStyle}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-text">{props.title as string}</h2>
              <button
                className="text-text-secondary hover:text-text p-1"
                onClick={() => onStateUpdate(props.stateKey as string || id, false)}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            {renderChildren()}
          </div>
        </div>
      )

    // Logo
    case 'logo':
      const logoImage = props.image as string
      const logoLink = props.link as string

      const logoElement = (
        <img
          src={logoImage}
          alt="Logo"
          className="max-h-12 w-auto"
          style={customStyle}
        />
      )

      return logoLink ? (
        <a href={logoLink} className="inline-block mb-4">
          {logoElement}
        </a>
      ) : (
        <div className="mb-4">{logoElement}</div>
      )

    // Title (large header)
    case 'title':
      return (
        <h1 className="text-3xl font-bold text-text mb-4" style={customStyle}>
          {props.content as string}
        </h1>
      )

    // Caption (small muted text)
    case 'caption':
      return (
        <p className="text-sm text-text-secondary mb-2" style={customStyle}>
          {props.content as string}
        </p>
      )

    // Write (generic display)
    case 'write':
      const writeContent = props.content
      if (typeof writeContent === 'string') {
        return <p className="text-text mb-2" style={customStyle}>{writeContent}</p>
      }
      return (
        <pre className="text-text mb-2 font-mono text-sm" style={customStyle}>
          {JSON.stringify(writeContent, null, 2)}
        </pre>
      )

    // Charts (backend sends type 'chart' with chartType prop)
    case 'chart':
      const chartType = props.chartType as string
      const chartData = (props.data as Record<string, unknown>[]) || []
      const chartX = props.x as string
      const chartY = props.y as string
      const chartTitle = props.title as string
      const chartHeight = (props.height as string) || '300px'

      // Simple chart rendering using SVG
      if (chartData.length === 0) {
        return (
          <div className="flex items-center justify-center bg-surface border border-border rounded-lg mb-4" style={{ height: chartHeight, ...customStyle }}>
            <span className="text-text-secondary">No data to display</span>
          </div>
        )
      }

      // Get values for charts
      const getValues = () => {
        if (chartType === 'pie') {
          const valueKey = props.value as string || 'value'
          const labelKey = props.label as string || 'label'
          return chartData.map((d, i) => ({
            value: Number(d[valueKey]) || 0,
            label: String(d[labelKey] || `Item ${i + 1}`),
          }))
        }
        // For scatter charts, keep x as numeric
        if (chartType === 'scatter') {
          return chartData.map((d) => ({
            x: Number(d[chartX]) || 0,
            y: Number(d[chartY]) || 0,
          }))
        }
        return chartData.map((d) => ({
          x: String(d[chartX] || ''),
          y: Number(d[chartY]) || 0,
        }))
      }

      const values = getValues()

      // For pie chart
      if (chartType === 'pie') {
        const total = values.reduce((sum, v) => sum + (v as { value: number }).value, 0)
        const pieColors = ['#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16']
        let cumulativeAngle = 0

        return (
          <div className="mb-4" style={customStyle}>
            {chartTitle && <h3 className="text-lg font-semibold text-text mb-3">{chartTitle}</h3>}
            <div className="flex items-center gap-6">
              <svg viewBox="0 0 100 100" className="w-48 h-48">
                {values.map((item, i) => {
                  const pieItem = item as { value: number; label: string }
                  const angle = (pieItem.value / total) * 360
                  const startAngle = cumulativeAngle
                  cumulativeAngle += angle

                  // Convert to radians
                  const startRad = (startAngle - 90) * (Math.PI / 180)
                  const endRad = (startAngle + angle - 90) * (Math.PI / 180)

                  // Calculate arc points
                  const x1 = 50 + 40 * Math.cos(startRad)
                  const y1 = 50 + 40 * Math.sin(startRad)
                  const x2 = 50 + 40 * Math.cos(endRad)
                  const y2 = 50 + 40 * Math.sin(endRad)

                  const largeArc = angle > 180 ? 1 : 0

                  return (
                    <path
                      key={i}
                      d={`M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArc} 1 ${x2} ${y2} Z`}
                      fill={pieColors[i % pieColors.length]}
                      className="hover:opacity-80 transition-opacity"
                    />
                  )
                })}
              </svg>
              <div className="space-y-2">
                {values.map((item, i) => {
                  const pieItem = item as { value: number; label: string }
                  return (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <div className="w-3 h-3 rounded" style={{ backgroundColor: pieColors[i % pieColors.length] }} />
                      <span className="text-text">{pieItem.label}</span>
                      <span className="text-text-secondary">({pieItem.value})</span>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )
      }

      // For line, bar, area, scatter charts
      const chartWidth = 400
      const chartHeightNum = 200
      const padding = { top: 20, right: 20, bottom: 40, left: 50 }
      const innerWidth = chartWidth - padding.left - padding.right
      const innerHeight = chartHeightNum - padding.top - padding.bottom

      // For scatter charts, use numeric x values
      if (chartType === 'scatter') {
        const scatterValues = values as { x: number; y: number }[]
        const maxY = Math.max(...scatterValues.map((v) => v.y), 1)
        const minY = Math.min(...scatterValues.map((v) => v.y), 0)
        const rangeY = maxY - minY || 1
        const maxX = Math.max(...scatterValues.map((v) => v.x), 1)
        const minX = Math.min(...scatterValues.map((v) => v.x), 0)
        const rangeX = maxX - minX || 1

        const xScaleScatter = (v: number) => padding.left + ((v - minX) / rangeX) * innerWidth
        const yScaleScatter = (v: number) => padding.top + innerHeight - ((v - minY) / rangeY) * innerHeight

        return (
          <div className="mb-4" style={customStyle}>
            {chartTitle && <h3 className="text-lg font-semibold text-text mb-3">{chartTitle}</h3>}
            <svg viewBox={`0 0 ${chartWidth} ${chartHeightNum}`} className="w-full" style={{ maxHeight: chartHeight }}>
              {/* Grid lines */}
              {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => (
                <line
                  key={i}
                  x1={padding.left}
                  y1={padding.top + innerHeight * (1 - ratio)}
                  x2={chartWidth - padding.right}
                  y2={padding.top + innerHeight * (1 - ratio)}
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
              ))}

              {/* Y-axis labels */}
              {[0, 0.5, 1].map((ratio, i) => (
                <text
                  key={i}
                  x={padding.left - 5}
                  y={padding.top + innerHeight * (1 - ratio)}
                  textAnchor="end"
                  alignmentBaseline="middle"
                  className="text-xs fill-gray-500"
                >
                  {Math.round(minY + rangeY * ratio)}
                </text>
              ))}

              {/* Scatter points */}
              {scatterValues.map((v, i) => (
                <circle
                  key={i}
                  cx={xScaleScatter(v.x)}
                  cy={yScaleScatter(v.y)}
                  r="6"
                  fill="#6366f1"
                  className="hover:fill-indigo-400 transition-colors"
                />
              ))}

              {/* X-axis labels */}
              {[0, 0.5, 1].map((ratio, i) => (
                <text
                  key={i}
                  x={padding.left + innerWidth * ratio}
                  y={chartHeightNum - 10}
                  textAnchor="middle"
                  className="text-xs fill-gray-500"
                >
                  {Math.round(minX + rangeX * ratio)}
                </text>
              ))}
            </svg>
          </div>
        )
      }

      // For line, bar, area charts (string x values)
      const chartValues = values as { x: string; y: number }[]
      const maxY = Math.max(...chartValues.map((v) => v.y), 1)
      const minY = Math.min(...chartValues.map((v) => v.y), 0)
      const range = maxY - minY || 1

      const xScale = (i: number) => padding.left + (i / (chartValues.length - 1 || 1)) * innerWidth
      const yScale = (v: number) => padding.top + innerHeight - ((v - minY) / range) * innerHeight

      return (
        <div className="mb-4" style={customStyle}>
          {chartTitle && <h3 className="text-lg font-semibold text-text mb-3">{chartTitle}</h3>}
          <svg viewBox={`0 0 ${chartWidth} ${chartHeightNum}`} className="w-full" style={{ maxHeight: chartHeight }}>
            {/* Grid lines */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => (
              <line
                key={i}
                x1={padding.left}
                y1={padding.top + innerHeight * (1 - ratio)}
                x2={chartWidth - padding.right}
                y2={padding.top + innerHeight * (1 - ratio)}
                stroke="#e5e7eb"
                strokeWidth="1"
              />
            ))}

            {/* Y-axis labels */}
            {[0, 0.5, 1].map((ratio, i) => (
              <text
                key={i}
                x={padding.left - 5}
                y={padding.top + innerHeight * (1 - ratio)}
                textAnchor="end"
                alignmentBaseline="middle"
                className="text-xs fill-gray-500"
              >
                {Math.round(minY + range * ratio)}
              </text>
            ))}

            {/* Area chart */}
            {chartType === 'area' && (
              <path
                d={`M ${xScale(0)} ${yScale(chartValues[0].y)} ${chartValues.map((v, i) => `L ${xScale(i)} ${yScale(v.y)}`).join(' ')} L ${xScale(chartValues.length - 1)} ${padding.top + innerHeight} L ${xScale(0)} ${padding.top + innerHeight} Z`}
                fill="rgba(99, 102, 241, 0.2)"
              />
            )}

            {/* Line chart */}
            {(chartType === 'line' || chartType === 'area') && (
              <path
                d={`M ${chartValues.map((v, i) => `${xScale(i)} ${yScale(v.y)}`).join(' L ')}`}
                fill="none"
                stroke="#6366f1"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            )}

            {/* Line chart points */}
            {(chartType === 'line' || chartType === 'area') && chartValues.map((v, i) => (
              <circle
                key={i}
                cx={xScale(i)}
                cy={yScale(v.y)}
                r="4"
                fill="#6366f1"
                className="hover:r-6 transition-all"
              />
            ))}

            {/* Bar chart */}
            {chartType === 'bar' && chartValues.map((v, i) => {
              const barWidth = (innerWidth / chartValues.length) * 0.7
              const barX = xScale(i) - barWidth / 2
              const barHeight = ((v.y - minY) / range) * innerHeight
              return (
                <rect
                  key={i}
                  x={barX}
                  y={yScale(v.y)}
                  width={barWidth}
                  height={barHeight}
                  fill="#6366f1"
                  rx="2"
                  className="hover:fill-indigo-400 transition-colors"
                />
              )
            })}


            {/* X-axis labels */}
            {chartValues.map((v, i) => (
              <text
                key={i}
                x={xScale(i)}
                y={chartHeightNum - 10}
                textAnchor="middle"
                className="text-xs fill-gray-500"
              >
                {v.x}
              </text>
            ))}
          </svg>
        </div>
      )

    // Link button
    case 'link_button':
      const linkLabel = props.label as string
      const linkUrl = props.url as string
      const linkVariant = (props.variant as string) || 'secondary'
      const linkVariantClasses: Record<string, string> = {
        primary: 'bg-primary text-white hover:bg-primary-hover',
        secondary: 'bg-surface border border-border text-text hover:bg-surface-hover',
        outline: 'bg-transparent border border-primary text-primary hover:bg-primary/10',
      }

      return (
        <a
          href={linkUrl}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg transition-colors mb-4 ${linkVariantClasses[linkVariant] || linkVariantClasses.secondary}`}
          style={customStyle}
        >
          {linkLabel}
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      )

    // Search input
    case 'search_input':
      const searchLabel = props.label as string
      return (
        <div className="mb-4 relative" style={customStyle}>
          {searchLabel ? (
            <label className="block text-sm font-medium text-text mb-1.5">{searchLabel}</label>
          ) : null}
          <div className="relative">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="search"
              value={(props.value ?? '') as string}
              placeholder={props.placeholder as string || 'Search...'}
              disabled={props.disabled as boolean}
              onChange={(e) => onStateUpdate(props.stateKey as string || id, e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-surface border border-border rounded-lg text-text focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>
        </div>
      )

    // LaTeX component - renders math using KaTeX
    case 'latex':
      const latexContent = props.content as string
      let renderedLatex = ''
      try {
        if (typeof window !== 'undefined' && (window as any).katex) {
          renderedLatex = (window as any).katex.renderToString(latexContent, {
            throwOnError: false,
            displayMode: true
          })
        }
      } catch (e) {
        renderedLatex = ''
      }
      return renderedLatex ? (
        <div
          style={customStyle}
          className="mb-4 p-4 bg-surface-hover rounded-lg overflow-x-auto text-text"
          dangerouslySetInnerHTML={{ __html: renderedLatex }}
        />
      ) : (
        <div style={customStyle} className="mb-4 p-4 bg-surface-hover rounded-lg font-mono text-sm">
          <code className="text-text">{latexContent}</code>
        </div>
      )

    // Exception display
    case 'exception':
      return (
        <div style={customStyle} className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-semibold text-red-700 dark:text-red-400">{props.exception_type as string}</span>
          </div>
          <p className="text-red-600 dark:text-red-300 mb-2">{props.message as string}</p>
          {props.traceback ? (
            <pre className="text-xs text-red-500 dark:text-red-400 overflow-auto p-2 bg-red-100 dark:bg-red-900/40 rounded">
              {String(props.traceback)}
            </pre>
          ) : null}
        </div>
      )

    // Chat message
    case 'chat_message':
      const isUser = (props.role as string) === 'user'
      return (
        <div style={customStyle} className={`mb-3 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-[80%] p-3 rounded-2xl ${
            isUser
              ? 'bg-primary text-white rounded-br-md'
              : 'bg-surface-hover text-text rounded-bl-md'
          }`}>
            {props.name ? (
              <div className={`text-xs font-medium mb-1 ${isUser ? 'text-primary-foreground/70' : 'text-text-secondary'}`}>
                {String(props.name)}
              </div>
            ) : null}
            <div className="text-sm">{props.content as string}</div>
            {props.timestamp ? (
              <div className={`text-xs mt-1 ${isUser ? 'text-primary-foreground/60' : 'text-text-secondary'}`}>
                {String(props.timestamp)}
              </div>
            ) : null}
          </div>
        </div>
      )

    // Chat container
    case 'chat_container':
      return (
        <div
          style={{ height: props.height as string || '500px', ...customStyle }}
          className="mb-4 overflow-y-auto border border-border rounded-lg p-4 bg-surface"
        >
          {renderChildren()}
        </div>
      )

    // Chat input - uses uncontrolled input with ref for better UX
    case 'chat_input':
      const chatInputRef = React.useRef<HTMLInputElement>(null)
      const handleChatInputSubmit = () => {
        const input = chatInputRef.current
        if (input && input.value.trim()) {
          onStateUpdate(props.stateKey as string || id, input.value.trim())
          input.value = ''
        }
      }
      return (
        <div style={customStyle} className="mb-4 flex gap-2">
          <input
            ref={chatInputRef}
            type="text"
            defaultValue=""
            placeholder={props.placeholder as string || 'Type a message...'}
            disabled={props.disabled as boolean}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleChatInputSubmit()
              }
            }}
            className="flex-1 px-4 py-2.5 bg-surface border border-border rounded-lg text-text focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
          />
          <button
            className="px-4 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
            onClick={handleChatInputSubmit}
          >
            Send
          </button>
        </div>
      )

    // Full chat interface
    case 'chat':
      const chatRef = React.useRef<HTMLInputElement>(null)
      const handleChatSubmit = () => {
        const input = chatRef.current
        if (input && input.value.trim()) {
          onStateUpdate(props.stateKey as string || id, input.value.trim())
          input.value = ''
        }
      }
      return (
        <div style={customStyle} className="mb-4 border border-border rounded-lg overflow-hidden">
          <div style={{ height: props.height as string || '500px' }} className="overflow-y-auto p-4 bg-surface">
            {renderChildren()}
          </div>
          {(props.show_input !== false) && (
            <div className="p-3 border-t border-border bg-surface-hover">
              <div className="flex gap-2">
                <input
                  ref={chatRef}
                  type="text"
                  defaultValue=""
                  placeholder={props.input_placeholder as string || 'Type a message...'}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault()
                      handleChatSubmit()
                    }
                  }}
                  className="flex-1 px-4 py-2 bg-surface border border-border rounded-lg text-text"
                />
                <button
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                  onClick={handleChatSubmit}
                >
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      )

    // Iframe
    case 'iframe':
      return (
        <div style={customStyle} className="mb-4">
          <iframe
            src={props.src as string}
            width={props.width as string || '100%'}
            height={props.height as string || '400px'}
            title={props.title as string || 'Embedded content'}
            className="border border-border rounded-lg"
            sandbox="allow-scripts allow-same-origin"
          />
        </div>
      )

    // File uploader
    case 'file_uploader':
      return (
        <FileUploader
          label={props.label as string}
          accept={props.accept as string[] || props.type as string[]}
          multiple={props.multiple as boolean || props.acceptMultipleFiles as boolean}
          disabled={props.disabled as boolean}
          maxFileSize={props.maxFileSize as number}
          stateKey={props.stateKey as string || id}
          onStateUpdate={onStateUpdate}
          style={customStyle}
        />
      )

    // Camera input
    case 'camera_input':
      return (
        <div style={customStyle} className="mb-4">
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <div className="border border-border rounded-lg p-4 text-center bg-surface">
            <svg className="w-12 h-12 mx-auto text-text-secondary mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <button className="px-4 py-2 bg-primary text-white rounded-lg text-sm">Take Photo</button>
          </div>
        </div>
      )

    // Audio input
    case 'audio_input':
      return (
        <div style={customStyle} className="mb-4">
          {props.label ? (
            <label className="block text-sm font-medium text-text mb-1.5">{String(props.label)}</label>
          ) : null}
          <div className="border border-border rounded-lg p-4 text-center bg-surface">
            <svg className="w-12 h-12 mx-auto text-text-secondary mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <button className="px-4 py-2 bg-primary text-white rounded-lg text-sm">Record Audio</button>
          </div>
        </div>
      )

    // Map component
    case 'map':
      return (
        <LeafletMap
          data={props.data as Array<Record<string, unknown>> || []}
          latitude={props.latitude as string || 'lat'}
          longitude={props.longitude as string || 'lon'}
          zoom={props.zoom as number || 4}
          height={props.height as string || '400px'}
          style={customStyle}
        />
      )

    // Plotly chart
    case 'plotly_chart':
      return (
        <div style={customStyle} className="mb-4 border border-border rounded-lg p-4 bg-surface min-h-[300px] flex items-center justify-center">
          <div className="text-center text-text-secondary">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p className="text-sm">Plotly Chart</p>
          </div>
        </div>
      )

    // Write stream
    case 'write_stream':
      return (
        <div style={customStyle} className="mb-4">
          <span className="text-text">{props.content as string}</span>
          <span className="inline-block w-2 h-4 bg-primary animate-pulse ml-0.5"></span>
        </div>
      )

    // Echo (code display)
    case 'echo':
      return (
        <div style={customStyle} className="mb-4 space-y-2">
          <pre className="p-4 bg-gray-900 text-gray-100 rounded-lg overflow-auto text-sm">
            <code>{props.code as string}</code>
          </pre>
          {renderChildren()}
        </div>
      )

    default:
      // Generic container for unknown types
      return (
        <div style={customStyle} className="um-unknown">
          {props.content as string}
          {renderChildren()}
        </div>
      )
  }
}
