const mc = require('minecraft-protocol')
const autoVersionForge = require('minecraft-protocol-forge').autoVersionForge

const host = process.env.W1_HOST || '127.0.0.1'
const port = Number(process.env.W1_PORT || 25565)
const username = process.env.W1_NAME || 'W1_player'
const reconnectMs = Number(process.env.W1_RECONNECT_MS || 3000)

function connect () {
  const position = { x: 0, y: 64, z: 0, yaw: 0, pitch: 0 }
  let positionReady = false
  let movementTimer = null
  const client = mc.createClient({
    host,
    port,
    username,
    auth: 'offline',
    version: false
  })

  autoVersionForge(client)

  client.on('login', () => {
    console.log(`[W1_player] connected to ${host}:${port}`)
    movementTimer = setInterval(() => {
      if (!positionReady) return
      client.write('position_look', {
        x: position.x,
        y: position.y,
        z: position.z,
        yaw: position.yaw,
        pitch: position.pitch,
        onGround: true
      })
    }, 1000)
  })

  client.on('position', (packet) => {
    const flags = packet.flags || 0
    position.x = (flags & 0x01) ? position.x + packet.x : packet.x
    position.y = (flags & 0x02) ? position.y + packet.y : packet.y
    position.z = (flags & 0x04) ? position.z + packet.z : packet.z
    position.yaw = (flags & 0x08) ? position.yaw + packet.yaw : packet.yaw
    position.pitch = (flags & 0x10) ? position.pitch + packet.pitch : packet.pitch
    positionReady = true

    client.write('teleport_confirm', { teleportId: packet.teleportId })
    client.write('position_look', {
      x: position.x,
      y: position.y,
      z: position.z,
      yaw: position.yaw,
      pitch: position.pitch,
      onGround: true
    })
  })

  client.on('end', (reason) => {
    if (movementTimer !== null) clearInterval(movementTimer)
    console.log(`[W1_player] disconnected: ${reason || 'connection closed'}`)
    setTimeout(connect, reconnectMs)
  })

  client.on('error', (err) => {
    console.log(`[W1_player] error: ${err.message}`)
  })
}

connect()
