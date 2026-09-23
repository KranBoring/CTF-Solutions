const net = require('net')

const listenHost = process.env.PROXY_HOST || '0.0.0.0'
const listenPort = Number(process.env.PROXY_PORT || 25565)
const backendHost = process.env.BACKEND_HOST || '127.0.0.1'
const backendPort = Number(process.env.BACKEND_PORT || 25566)
const reservedName = (process.env.RESERVED_NAME || 'W1_player').toLowerCase()
const maxHandshakeBytes = Number(process.env.MAX_HANDSHAKE_BYTES || 4096)

function readVarInt (buffer, offset) {
  let value = 0
  let size = 0

  while (offset + size < buffer.length) {
    const byte = buffer[offset + size]
    value |= (byte & 0x7f) << (7 * size)
    size++
    if ((byte & 0x80) !== 0x80) return { value, size }
    if (size > 5) throw new Error('varint too large')
  }

  return null
}

function readString (buffer, offset) {
  const length = readVarInt(buffer, offset)
  if (!length) return null

  const start = offset + length.size
  const end = start + length.value
  if (end > buffer.length) return null

  return { value: buffer.toString('utf8', start, end), size: length.size + length.value }
}

function readPacket (buffer, offset) {
  const length = readVarInt(buffer, offset)
  if (!length) return null

  const packetStart = offset + length.size
  const packetEnd = packetStart + length.value
  if (packetEnd > buffer.length) return null

  const id = readVarInt(buffer, packetStart)
  if (!id) return null

  return {
    id: id.value,
    body: buffer.subarray(packetStart + id.size, packetEnd),
    end: packetEnd
  }
}

function parseHandshake (body) {
  let offset = 0
  const protocol = readVarInt(body, offset)
  if (!protocol) return null
  offset += protocol.size

  const host = readString(body, offset)
  if (!host) return null
  offset += host.size

  offset += 2
  const nextState = readVarInt(body, offset)
  if (!nextState) return null

  return nextState.value
}

function parseLoginName (body) {
  const name = readString(body, 0)
  return name && name.value
}

function containsReservedName (buffer) {
  return buffer.toString('utf8').toLowerCase().includes(reservedName)
}

function closeClient (client, reason) {
  console.log(`[proxy] blocked connection: ${reason}`)
  client.destroy()
}

function forward (client, initialBuffer) {
  const backend = net.connect({ host: backendHost, port: backendPort }, () => {
    backend.write(initialBuffer)
    client.pipe(backend)
    backend.pipe(client)
  })

  const close = () => {
    client.destroy()
    backend.destroy()
  }

  client.on('error', close)
  backend.on('error', close)
}

net.createServer((client) => {
  let buffer = Buffer.alloc(0)

  client.on('data', function inspect (chunk) {
    buffer = Buffer.concat([buffer, chunk])
    if (buffer.length > maxHandshakeBytes) {
      closeClient(client, 'handshake too large')
      return
    }

    let first
    try {
      first = readPacket(buffer, 0)
    } catch (err) {
      client.destroy()
      return
    }

    if (!first) return

    let nextState
    try {
      nextState = first.id === 0 ? parseHandshake(first.body) : null
    } catch (err) {
      client.destroy()
      return
    }

    if (nextState !== 2) {
      client.removeListener('data', inspect)
      forward(client, buffer)
      return
    }

    const second = readPacket(buffer, first.end)
    if (!second) return

    const username = second.id === 0 ? parseLoginName(second.body) : ''
    if ((username && username.toLowerCase() === reservedName) || containsReservedName(buffer)) {
      closeClient(client, `reserved username ${username || '<unparsed>'}`)
      return
    }

    client.removeListener('data', inspect)
    forward(client, buffer)
  })
}).listen(listenPort, listenHost, () => {
  console.log(`[proxy] listening on ${listenHost}:${listenPort}, backend ${backendHost}:${backendPort}`)
})
