import React from 'react'
import { motion } from 'framer-motion'

interface ImageProps {
  src: string
  alt?: string
  width?: string
  height?: string
  caption?: string
  style?: React.CSSProperties
}

export function Image({
  src,
  alt = '',
  width,
  height,
  caption,
  style,
}: ImageProps) {
  return (
    <motion.figure
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      <img
        src={src}
        alt={alt}
        className="rounded-lg max-w-full h-auto"
        style={{ width, height }}
      />
      {caption && (
        <figcaption className="mt-2 text-sm text-text-secondary text-center">
          {caption}
        </figcaption>
      )}
    </motion.figure>
  )
}

interface VideoProps {
  src: string
  autoplay?: boolean
  controls?: boolean
  loop?: boolean
  muted?: boolean
  width?: string
  height?: string
  style?: React.CSSProperties
}

export function Video({
  src,
  autoplay = false,
  controls = true,
  loop = false,
  muted = false,
  width,
  height,
  style,
}: VideoProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      <video
        src={src}
        autoPlay={autoplay}
        controls={controls}
        loop={loop}
        muted={muted}
        className="rounded-lg max-w-full"
        style={{ width, height }}
      />
    </motion.div>
  )
}

interface AudioProps {
  src: string
  autoplay?: boolean
  controls?: boolean
  loop?: boolean
  style?: React.CSSProperties
}

export function Audio({
  src,
  autoplay = false,
  controls = true,
  loop = false,
  style,
}: AudioProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      <audio
        src={src}
        autoPlay={autoplay}
        controls={controls}
        loop={loop}
        className="w-full"
      />
    </motion.div>
  )
}
