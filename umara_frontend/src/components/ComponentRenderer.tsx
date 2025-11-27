import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ComponentTree } from '../App'

// Import individual components
import { Text, Header, Subheader, Markdown, Code } from './Typography'
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
import { Image, Video, Audio } from './Media'

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
      return (
        <Text
          content={props.content as string}
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
          disabled={props.disabled as boolean}
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

    case 'dataframe':
    case 'table':
      return (
        <DataTable
          data={props.data as Record<string, unknown>[]}
          columns={props.columns as string[]}
          height={props.height as string}
          style={customStyle}
        />
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
