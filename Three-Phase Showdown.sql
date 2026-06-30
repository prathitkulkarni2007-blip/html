import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { BOSS_PHASES, RANK_COLORS, clamp, damagePlayer, makePlayer } from './engine'
import { attackBoss, checkPhaseTransition, createBossFight, generateVictoryReport, getBossDamage, updateBossAI } from './student'

const ARENA = 28
const SAVE_KEY = 'three_phase_showdown_save'

function hpPct(v, max) { return `${(100 * v / max).toFixed(1)}%` }

export default function GameCanvas() {
  const mountRef = useRef(null)
  const [ui, setUi] = useState({
    player: makePlayer(),
    bossFight: createBossFight(),
    status: 'Move with WASD · Space to strike · R to restart · K to save',
    report: null,
    gameOver: false,
  })

  useEffect(() => {
    const root = mountRef.current
    if (!root) return

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0d1119)
    scene.fog = new THREE.FogExp2(0x10131d, 0.045)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(root.clientWidth, root.clientHeight)
    renderer.shadowMap.enabled = true
    root.appendChild(renderer.domElement)

    const camera = new THREE.PerspectiveCamera(60, root.clientWidth / root.clientHeight, 0.1, 200)
    camera.position.set(0, 12, 18)

    const ambient = new THREE.AmbientLight(0x8899cc, 1.1)
    scene.add(ambient)

    const moon = new THREE.DirectionalLight(0xc7ddff, 2.2)
    moon.position.set(6, 14, 10)
    moon.castShadow = true
    moon.shadow.mapSize.set(1024, 1024)
    scene.add(moon)

    const shrineGlow = new THREE.PointLight(0xff8f4d, 18, 18, 2)
    shrineGlow.position.set(0, 4, -10)
    scene.add(shrineGlow)

    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(ARENA, 80),
      new THREE.MeshStandardMaterial({ color: 0x283238, roughness: 0.93, metalness: 0.06 })
    )
    floor.rotation.x = -Math.PI / 2
    floor.receiveShadow = true
    scene.add(floor)

    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(ARENA - 0.5, 0.45, 16, 64),
      new THREE.MeshStandardMaterial({ color: 0x73879a, emissive: 0x233040, emissiveIntensity: 0.4 })
    )
    ring.rotation.x = Math.PI / 2
    ring.position.y = 0.15
    scene.add(ring)

    const makePillar = (x, z, h = 6) => {
      const g = new THREE.Group()
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 1, h, 10), new THREE.MeshStandardMaterial({ color: 0x68707d, roughness: 0.9 }))
      col.position.y = h / 2
      col.castShadow = true
      const cap = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.2, 0.5, 10), new THREE.MeshStandardMaterial({ color: 0x949fb0 }))
      cap.position.y = h + 0.1
      cap.castShadow = true
      g.add(col, cap)
      g.position.set(x, 0, z)
      scene.add(g)
    }
    ;[[-10,-10],[10,-10],[-10,10],[10,10],[-16,0],[16,0],[0,-16],[0,16]].forEach(([x,z])=>makePillar(x,z))

    const stairMat = new THREE.MeshStandardMaterial({ color: 0x3d4550 })
    for (let i = 0; i < 5; i++) {
      const step = new THREE.Mesh(new THREE.BoxGeometry(6 - i * 0.25, 0.5, 1.4), stairMat)
      step.position.set(0, 0.25 + i * 0.5, -20 + i * 1.1)
      step.castShadow = step.receiveShadow = true
      scene.add(step)
    }

    const altar = new THREE.Mesh(new THREE.BoxGeometry(6, 1.3, 3), new THREE.MeshStandardMaterial({
      color: 0x5a4a63, emissive: 0x43151a, emissiveIntensity: 0.65,
    }))
    altar.position.set(0, 3.3, -10)
    altar.castShadow = altar.receiveShadow = true
    scene.add(altar)

    const torchGeo = new THREE.CylinderGeometry(0.08, 0.08, 2.6, 6)
    const flameGeo = new THREE.SphereGeometry(0.34, 12, 12)
    const torchMat = new THREE.MeshStandardMaterial({ color: 0x3f2a1d })
    const flameMat = new THREE.MeshStandardMaterial({ color: 0xffa44a, emissive: 0xff6a1f, emissiveIntensity: 3.5 })
    ;[[-3.8,-9.2],[3.8,-9.2]].forEach(([x,z])=>{
      const stick = new THREE.Mesh(torchGeo, torchMat)
      stick.position.set(x,1.5,z)
      const flame = new THREE.Mesh(flameGeo, flameMat)
      flame.position.set(x,3.1,z)
      const p = new THREE.PointLight(0xff7b33, 12, 10, 2)
      p.position.set(x,3.1,z)
      scene.add(stick, flame, p)
    })

    const player = new THREE.Mesh(
      new THREE.CapsuleGeometry(0.55, 1.5, 6, 12),
      new THREE.MeshStandardMaterial({ color: 0x42c8f5, emissive: 0x0f3157, roughness: 0.38 })
    )
    player.position.set(0, 1.3, 11)
    player.castShadow = true
    scene.add(player)

    const bossCoreMat = new THREE.MeshStandardMaterial({ color: 0xff6247, emissive: 0x4e0f12, emissiveIntensity: 0.8, roughness: 0.3, metalness: 0.15 })
    const bossCore = new THREE.Mesh(new THREE.IcosahedronGeometry(1.5, 1), bossCoreMat)
    bossCore.castShadow = true
    const bossRing = new THREE.Mesh(new THREE.TorusGeometry(2.2, 0.22, 12, 50), new THREE.MeshStandardMaterial({ color: 0xffd6b0, emissive: 0xffa142, emissiveIntensity: 0.9 }))
    bossRing.rotation.x = Math.PI / 2
    const boss = new THREE.Group()
    boss.add(bossCore, bossRing)
    boss.position.set(0, 1.8, -10)
    scene.add(boss)

    const phasePulse = new THREE.PointLight(0xff6247, 9, 18, 2)
    phasePulse.position.set(0, 2.4, -10)
    scene.add(phasePulse)

    const keys = {}
    const onKeyDown = e => {
      const k = e.key.toLowerCase()
      keys[k] = true
      if (k === ' ') {
        state.current.attackQueued = true
      }
      if (k === 'r') reset()
      if (k === 'k') saveGame()
    }
    const onKeyUp = e => { keys[e.key.toLowerCase()] = false }
    window.addEventListener('keydown', onKeyDown)
    window.addEventListener('keyup', onKeyUp)

    const state = { current: { ...ui, attackQueued: false } }
    const syncUi = next => {
      state.current = { ...state.current, ...next }
      setUi(prev => ({ ...prev, ...next }))
    }

    const load = () => {
      try {
        const raw = localStorage.getItem(SAVE_KEY)
        if (!raw) return
        const save = JSON.parse(raw)
        if (save?.player && save?.bossFight) syncUi({ ...save, status:'Save loaded. Fight on.' })
      } catch {}
    }
    load()

    const saveGame = () => {
      const payload = { player: state.current.player, bossFight: state.current.bossFight }
      localStorage.setItem(SAVE_KEY, JSON.stringify(payload))
      syncUi({ status: 'Game saved to localStorage.' })
    }

    const reset = () => {
      syncUi({ player: makePlayer(), bossFight: createBossFight(), report: null, gameOver:false, status:'Arena reset. Temple Warden reforms…' })
    }

    const clock = new THREE.Clock()
    let raf = 0

    function handlePlayer(dt) {
      let p = state.current.player
      if (p.dead || state.current.report) return p
      let dx = 0, dz = 0
      if (keys['w'] || keys['arrowup']) dz -= 1
      if (keys['s'] || keys['arrowdown']) dz += 1
      if (keys['a'] || keys['arrowleft']) dx -= 1
      if (keys['d'] || keys['arrowright']) dx += 1

      if (dx || dz) {
        const len = Math.hypot(dx, dz) || 1
        dx /= len; dz /= len
        p = { ...p, x: clamp(p.x + dx * 9 * dt, -ARENA + 2, ARENA - 2), z: clamp(p.z + dz * 9 * dt, -ARENA + 2, ARENA - 2) }
        player.rotation.y = Math.atan2(dx, dz)
      }
      if (p.attackCd > 0) p = { ...p, attackCd: Math.max(0, p.attackCd - dt) }
      if (p.hurtCd > 0) p = { ...p, hurtCd: Math.max(0, p.hurtCd - dt) }

      if (state.current.attackQueued && p.attackCd <= 0) {
        state.current.attackQueued = false
        p = { ...p, attackCd: 0.42 }
        const bf = state.current.bossFight
        const d = Math.hypot(p.x - bf.entity.x, p.z - bf.entity.z)
        if (bf.entity.alive && d <= 3.6) {
          const strike = attackBoss(p, bf)
          p = strike.player
          let nextFight = strike.bossFight
          if (strike.killed) {
            const report = generateVictoryReport(p, nextFight, p.hitsOnBoss)
            syncUi({ report, status: `Victory! ${report.rank} rank achieved.` })
          } else {
            const transition = checkPhaseTransition(nextFight)
            nextFight = transition.bossFight
            syncUi({ bossFight: nextFight, status: transition.transitioned ? `${BOSS_PHASES[transition.newPhase].label} unleashed!` : (strike.isBig ? `Heavy combo hit for ${strike.damage}!` : `You dealt ${strike.damage}.`) })
          }
          state.current.bossFight = nextFight
        } else {
          syncUi({ status: 'Your strike cuts only air. Close the distance.' })
        }
      }
      return p
    }

    function animate() {
      const dt = Math.min(clock.getDelta(), 0.05)
      let p = handlePlayer(dt)
      let bf = state.current.bossFight

      if (!state.current.report && bf.entity.alive && !p.dead) {
        const ai = updateBossAI(p, bf, dt)
        bf = ai.bossFight
        const phaseMeta = BOSS_PHASES[bf.phase]
        if (ai.attackNow) {
          p = damagePlayer(p, getBossDamage(bf.phase))
          syncUi({ status: `${phaseMeta.label} strike! The Warden hits hard.` })
        }
      }
      if (p.dead && !state.current.gameOver) {
        syncUi({ gameOver:true, status:'You fell in the temple. Press R to try again.' })
      }

      state.current.player = p
      state.current.bossFight = bf
      setUi(prev => ({ ...prev, player: p, bossFight: bf, gameOver: p.dead || prev.gameOver, report: state.current.report, status: state.current.status }))

      player.position.set(p.x, 1.3 + (p.attackCd > 0 ? 0.1*Math.sin(clock.elapsedTime*28) : 0), p.z)
      boss.position.set(bf.entity.x, 1.8 + Math.sin(clock.elapsedTime * (1.8 + bf.phase*0.35)) * 0.22, bf.entity.z)
      boss.rotation.y += dt * (0.9 + bf.phase * 0.5)
      bossCore.scale.setScalar(1 + Math.sin(clock.elapsedTime * (2 + bf.phase)) * 0.05)
      bossRing.scale.setScalar(1 + Math.sin(clock.elapsedTime * 1.6) * 0.04)
      boss.visible = bf.entity.alive
      phasePulse.position.set(bf.entity.x, 2.4, bf.entity.z)
      phasePulse.color.set(BOSS_PHASES[bf.phase].color)
      phasePulse.intensity = 8 + Math.sin(clock.elapsedTime * (3 + bf.phase)) * 1.8
      bossCoreMat.color.set(BOSS_PHASES[bf.phase].color)
      bossCoreMat.emissive.set(BOSS_PHASES[bf.phase].color)

      const follow = new THREE.Vector3(p.x, 7.5, p.z + 11.5)
      camera.position.lerp(follow, 0.08)
      camera.lookAt(p.x, 1.6, p.z - 5)

      shrineGlow.intensity = 16 + Math.sin(clock.elapsedTime * 3) * 3
      renderer.render(scene, camera)
      raf = requestAnimationFrame(animate)
    }
    raf = requestAnimationFrame(animate)

    const onResize = () => {
      const w = root.clientWidth, h = root.clientHeight
      camera.aspect = w / h
      camera.updateProjectionMatrix()
      renderer.setSize(w, h)
    }
    window.addEventListener('resize', onResize)

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('keydown', onKeyDown)
      window.removeEventListener('keyup', onKeyUp)
      window.removeEventListener('resize', onResize)
      renderer.dispose()
      root.removeChild(renderer.domElement)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const phaseInfo = BOSS_PHASES[ui.bossFight.phase]
  return (
    <div className="game-shell">
      <div ref={mountRef} className="viewport" />
      <div className="hud top-left">
        <div className="title">Three-Phase Showdown</div>
        <div className="line"><span>Player HP</span><b>{ui.player.hp}/{ui.player.maxHp}</b></div>
        <div className="bar"><i style={{ width: hpPct(ui.player.hp, ui.player.maxHp), background: ui.player.dead ? '#ff5c5c' : '#4de2a8' }} /></div>
        <div className="line"><span>Boss HP</span><b>{ui.bossFight.entity.hp}/{ui.bossFight.entity.maxHp}</b></div>
        <div className="bar"><i style={{ width: hpPct(ui.bossFight.entity.hp, ui.bossFight.entity.maxHp), background: phaseInfo.color }} /></div>
        <div className="tag" style={{ borderColor: phaseInfo.color, color: phaseInfo.color }}>{phaseInfo.label}</div>
      </div>

      <div className="hud top-right">
        <div className="line"><span>Hits Landed</span><b>{ui.player.hitsOnBoss}</b></div>
        <div className="line"><span>Combo Index</span><b>{ui.player.comboCount + 1}/4</b></div>
        <div className="line"><span>Score</span><b>{ui.player.score}</b></div>
        <div className="small">WASD move · Space attack · K save · R reset</div>
      </div>

      <div className="status-strip">{ui.status}</div>

      {ui.report && (
        <div className="overlay">
          <div className="card victory">
            <div className="big-rank" style={{ color: RANK_COLORS[ui.report.rank] }}>{ui.report.rank}</div>
            <h2>Temple Warden Defeated</h2>
            <p>The three-phase boss battle is complete.</p>
            <div className="report-grid">
              <div><span>Boss</span><b>{ui.report.bossName}</b></div>
              <div><span>Hits to Win</span><b>{ui.report.turnsToWin}</b></div>
              <div><span>Phases Cleared</span><b>{ui.report.bossPhasesCleared}</b></div>
              <div><span>Total Score</span><b>{ui.report.score}</b></div>
            </div>
            <button onClick={() => window.location.reload()}>Restart Showdown</button>
          </div>
        </div>
      )}

      {ui.gameOver && !ui.report && (
        <div className="overlay">
          <div className="card">
            <h2>You Were Defeated</h2>
            <p>The Temple Warden claimed this round.</p>
            <button onClick={() => window.location.reload()}>Try Again</button>
          </div>
        </div>
      )}
    </div>
  )
}
