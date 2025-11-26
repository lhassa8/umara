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
import { Card, Container, Columns, Column, Grid } from './Layout'
import { Tabs } from './Tabs'
import { Alert } from './Alert'
import { Metric, Progress, Spinner } from './DataDisplay'
import { Divider, Spacer } from './Divider'
import { DataTable } from './DataTable'
import { Image, Video, Audio } from './Media'

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

  // Animation variants
  const fadeIn = {
    initial: { opacity: 0, y: 5 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.2 },
  }

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

    case 'tabs':
      return (
        <Tabs
          tabs={props.tabs as string[]}
          activeTab={(props.activeTab ?? 0) as number}
          onChange={(index) => onStateUpdate(props.stateKey as string || id, index)}
          style={customStyle}
        >
          {children}
        </Tabs>
      )

    case 'tab':
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
