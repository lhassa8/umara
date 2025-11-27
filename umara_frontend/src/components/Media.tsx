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

// Leaflet Map types
interface LeafletMapProps {
  data: Array<Record<string, unknown>>
  latitude?: string
  longitude?: string
  zoom?: number
  height?: string
  style?: React.CSSProperties
}

export function LeafletMap({
  data = [],
  latitude = 'lat',
  longitude = 'lon',
  zoom = 4,
  height = '400px',
  style,
}: LeafletMapProps) {
  const mapRef = React.useRef<HTMLDivElement>(null)
  const mapInstanceRef = React.useRef<unknown>(null)

  React.useEffect(() => {
    const L = (window as unknown as Record<string, unknown>).L as {
      map: (el: HTMLElement) => unknown
      tileLayer: (url: string, options: Record<string, unknown>) => { addTo: (map: unknown) => void }
      marker: (latlng: [number, number]) => { addTo: (map: unknown) => { bindPopup: (content: string) => void } }
    }

    if (!L || !mapRef.current || mapInstanceRef.current) return

    // Calculate center from markers or default to US center
    let centerLat = 39.8283
    let centerLon = -98.5795
    if (data.length > 0) {
      const lats = data.map(d => Number(d[latitude]) || 0)
      const lons = data.map(d => Number(d[longitude]) || 0)
      centerLat = lats.reduce((a, b) => a + b, 0) / lats.length
      centerLon = lons.reduce((a, b) => a + b, 0) / lons.length
    }

    const map = L.map(mapRef.current) as { setView: (latlng: [number, number], zoom: number) => unknown; remove: () => void }
    map.setView([centerLat, centerLon], zoom)
    mapInstanceRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map)

    // Add markers
    data.forEach(point => {
      const lat = Number(point[latitude])
      const lon = Number(point[longitude])
      if (!isNaN(lat) && !isNaN(lon)) {
        const marker = L.marker([lat, lon]).addTo(map)
        const name = point.name as string
        if (name) {
          marker.bindPopup(name)
        }
      }
    })

    return () => {
      if (mapInstanceRef.current) {
        (mapInstanceRef.current as { remove: () => void }).remove()
        mapInstanceRef.current = null
      }
    }
  }, [data, latitude, longitude, zoom])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mb-4"
      style={style}
    >
      <div
        ref={mapRef}
        style={{ height }}
        className="rounded-lg overflow-hidden z-0"
      />
    </motion.div>
  )
}
