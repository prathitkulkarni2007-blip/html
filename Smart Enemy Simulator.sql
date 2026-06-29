import React, { useEffect, useMemo, useRef, useState } from 'react'
import {
  WORLD, createPlayer, seedEnemies, movePlayer, updateEnemy,
  attackEnemies, usePotion, ENEMY_TYPES
} from './engine'
import { saveGame, loadGame } from './SaveSystem'
import { applyEnemyDamage, tickMessages, respawnIfCleared, keepInsideWorld } from './student'

const colors = {
  grassA: '#15281e', grassB: '#1b3327', path: '#534536', temple: '#85725f'
}

function drawWorld(ctx, player, enemies, messages) {
  ctx.clearRect(0, 0, WORLD.width, WORLD.height)
  const bg = ctx.createLinearGradient(0, 0, 0, WORLD.height)
  bg.addColorStop(0, '#1a2437')
  bg.addColorStop(1, '#0d121d')
  ctx.fillStyle = bg
  ctx.fillRect(0, 0, WORLD.width, WORLD.height)

  for (let y = 0; y < WORLD.height; y += 40) {
    for (let x = 0; x < WORLD.width; x += 40) {
      ctx.fillStyle = ((x + y) / 40) % 2 ? colors.grassA : colors.grassB
      ctx.fillRect(x, y, 40, 40)
    }
  }

  ctx.fillStyle = colors.path
  ctx.fillRect(100, 280, 760, 34)
  ctx.fillRect(462, 90, 36, 420)

  ctx.fillStyle = colors.temple
  ctx.fillRect(350, 170, 260, 160)
  ctx.fillStyle = '#d8c4a4'
  ctx.fillRect(390, 145, 180, 26)
  ctx.fillStyle = '#b24e3d'
  ctx.fillRect(335, 136, 290, 14)

  const torch = (x, y, flicker) => {
    const g = ctx.createRadialGradient(x, y, 3, x, y, 44)
    g.addColorStop(0, `rgba(255,200,90,${0.55 + flicker})`)
    g.addColorStop(1, 'rgba(255,120,40,0)')
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(x, y, 44, 0, Math.PI * 2)
    ctx.fill()
    ctx.fillStyle = '#ffd166'
    ctx.beginPath()
    ctx.arc(x, y, 5, 0, Math.PI * 2)
    ctx.fill()
  }

  const t = performance.now() * 0.002
  torch(380, 180, Math.sin(t) * 0.08)
  torch(580, 180, Math.cos(t * 1.2) * 0.08)

  enemies.forEach(enemy => {
    if (!enemy.alive) return
    const stats = ENEMY_TYPES[enemy.type]
    ctx.fillStyle = enemy.hitFlash > 0 ? '#ffffff' : stats.color
    ctx.beginPath()
    ctx.arc(enemy.x, enemy.y, 16, 0, Math.PI * 2)
    ctx.fill()

    ctx.fillStyle = enemy.state === 'patrol' ? '#8ff7a9' : enemy.state === 'chase' ? '#ffd166' : '#ff6b6b'
    ctx.fillRect(enemy.x - 18, enemy.y - 28, 36, 5)

    ctx.fillStyle = '#281f2e'
    ctx.fillRect(enemy.x - 20, enemy.y - 40, 40, 6)
    ctx.fillStyle = '#ff6b6b'
    ctx.fillRect(enemy.x - 20, enemy.y - 40, 40 * (enemy.hp / enemy.maxHp), 6)
  })

  ctx.fillStyle = player.hitFlash > 0 ? '#ffffff' : '#6ee7ff'
  ctx.beginPath()
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2)
  ctx.fill()
  ctx.strokeStyle = '#b7f4ff'
  ctx.lineWidth = 3
  ctx.stroke()

  messages.forEach(m => {
    ctx.fillStyle = '#fff4b3'
    ctx.font = 'bold 16px system-ui'
    ctx.fillText(m.text, m.x, m.y)
  })
}

export default function GameCanvas() {
  const canvasRef = useRef(null)
  const keys = useRef({})
  const initial = useMemo(() => loadGame(), [])
  const [player, setPlayer] = useState(initial?.player ?? createPlayer())
  const [enemies, setEnemies] = useState(initial?.enemies ?? seedEnemies())
  const [messages, setMessages] = useState([])
  const [status, setStatus] = useState('Sneak in, watch enemy states, and survive the temple grounds.')

  useEffect(() => {
    const down = e => {
      keys.current[e.key] = true
      if (e.key === ' ') e.preventDefault()
      if (e.key.toLowerCase() === 'e') {
        setEnemies(es => {
          const res = attackEnemies(player, es)
          setPlayer(res.player)
          setMessages(m => [...m, ...res.messages])
          if (res.messages.length) setStatus('You struck nearby enemies. Watch patrol switch to chase and attack.')
          return res.enemies
        })
      }
      if (e.key.toLowerCase() === 'f') {
        setPlayer(p => usePotion(p))
        setStatus('Potion used. Healing respects your max HP.')
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') {
        e.preventDefault()
        const ok = saveGame({ player, enemies })
        setStatus(ok ? 'Game saved to localStorage.' : 'Could not save your game.')
      }
    }
    const up = e => { keys.current[e.key] = false }
    window.addEventListener('keydown', down)
    window.addEventListener('keyup', up)
    return () => {
      window.removeEventListener('keydown', down)
      window.removeEventListener('keyup', up)
    }
  }, [player, enemies])

  useEffect(() => {
    let raf = 0
    let last = performance.now()
    const loop = now => {
      const dt = Math.min((now - last) / 1000, 0.033)
      last = now

      setPlayer(p => keepInsideWorld(movePlayer(p, keys.current, dt), p.radius))
      setMessages(m => tickMessages(m, dt))
      setEnemies(prev => {
        let totalDamage = 0
        const next = prev.map(enemy => {
          const { enemy: updated, damage } = updateEnemy(enemy, player, dt)
          totalDamage += damage
          return updated
        })
        if (totalDamage > 0) {
          setStatus(`Enemies attacked for ${totalDamage} damage. Red = attack, yellow = chase, green = patrol.`)
        }
        setPlayer(p => applyEnemyDamage(p, totalDamage, dt))
        return respawnIfCleared(next, seedEnemies)
      })

      const ctx = canvasRef.current?.getContext('2d')
      if (ctx) drawWorld(ctx, player, enemies, messages)
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [player, enemies, messages])

  const alive = enemies.filter(e => e.alive)
  const counts = {
    patrol: alive.filter(e => e.state === 'patrol').length,
    chase: alive.filter(e => e.state === 'chase').length,
    attack: alive.filter(e => e.state === 'attack').length
  }

  return (
    <div className="game-shell">
      <div className="hud-row">
        <div className="card stat"><b>HP</b><span>{Math.round(player.hp)} / {player.maxHp}</span></div>
        <div className="card stat"><b>Potions</b><span>{player.potions}</span></div>
        <div className="card stat"><b>Kills</b><span>{player.kills}</span></div>
        <div className="card stat"><b>Score</b><span>{player.score}</span></div>
      </div>

      <div className="play-layout">
        <div className="play-area card">
          <canvas ref={canvasRef} width={WORLD.width} height={WORLD.height} />
        </div>

        <div className="side-panel">
          <div className="card">
            <h3>Enemy AI States</h3>
            <div className="state-grid">
              <div><span className="dot patrol"></span> Patrol: {counts.patrol}</div>
              <div><span className="dot chase"></span> Chase: {counts.chase}</div>
              <div><span className="dot attack"></span> Attack: {counts.attack}</div>
            </div>
            <p className="muted">Enemies wander near their home spot, switch to chase when you enter detect range, and attack when you get too close.</p>
          </div>

          <div className="card">
            <h3>Controls</h3>
            <p><b>WASD / Arrow Keys</b> Move</p>
            <p><b>E</b> Attack nearby enemies</p>
            <p><b>F</b> Use potion</p>
            <p><b>Ctrl/Cmd + S</b> Save game</p>
          </div>

          <div className="card">
            <h3>Live Status</h3>
            <p className="status">{status}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
