import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'

const app = document.querySelector('#app')
app.innerHTML = `
  <div class="overlay">
    <span class="pill">Three.js + Vite</span>
    <h1>3D Temple Explorer</h1>
    <p>Walk through a compact temple world with procedural terrain, cinematic lighting, bloom, instanced trees, and AI-generated textures.</p>
    <div class="grid">
      <div class="card"><b>Topics Covered</b>Terrain, lighting, post-processing, instancing, textures</div>
      <div class="card"><b>Controls</b>WASD or arrow keys, drag to orbit, scroll to zoom</div>
      <div class="card"><b>Temple Mood</b>Dawn fog, lantern glow, shrine-like stone steps</div>
      <div class="card"><b>AI Texture Mode</b>Online textures fade in when available</div>
    </div>
    <div class="footer">Optimised as a small, readable build with reusable helpers and fallback materials.</div>
  </div>
  <div class="notice">Tip: the world starts with clean materials and upgrades itself with AI textures in the background.</div>
`

const scene = new THREE.Scene()
scene.background = new THREE.Color(0x9ac7f5)
scene.fog = new THREE.FogExp2(0xadcff8, 0.0048)

const camera = new THREE.PerspectiveCamera(58, innerWidth / innerHeight, 0.1, 600)
camera.position.set(0, 24, 34)

const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setPixelRatio(Math.min(devicePixelRatio, 2))
renderer.setSize(innerWidth, innerHeight)
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap
app.appendChild(renderer.domElement)

const composer = new EffectComposer(renderer)
composer.addPass(new RenderPass(scene, camera))
composer.addPass(new UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), 0.38, 0.6, 0.88))

const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true
controls.target.set(0, 3, 0)
controls.maxPolarAngle = Math.PI * 0.46
controls.maxDistance = 70
controls.minDistance = 12

const lights = {
  ambient: new THREE.AmbientLight(0xfff2de, 0.8),
  sun: new THREE.DirectionalLight(0xffefc7, 2.8),
  hemi: new THREE.HemisphereLight(0xa9dcff, 0x365c26, 0.72)
}
lights.sun.position.set(35, 42, 20)
lights.sun.castShadow = true
lights.sun.shadow.mapSize.set(2048, 2048)
lights.sun.shadow.camera.left = -60
lights.sun.shadow.camera.right = 60
lights.sun.shadow.camera.top = 60
lights.sun.shadow.camera.bottom = -60
scene.add(lights.ambient, lights.hemi, lights.sun)

const textureLoader = new THREE.TextureLoader()
const texCache = new Map()
const temp = new THREE.Object3D()
const clock = new THREE.Clock()
const keys = new Set()

const mats = {
  ground: new THREE.MeshStandardMaterial({ color: 0x547f35, roughness: 0.94 }),
  path: new THREE.MeshStandardMaterial({ color: 0xb29366, roughness: 1 }),
  stone: new THREE.MeshStandardMaterial({ color: 0x8c8f95, roughness: 0.92 }),
  roof: new THREE.MeshStandardMaterial({ color: 0x6e2f28, roughness: 0.8 }),
  wood: new THREE.MeshStandardMaterial({ color: 0x6b4b30, roughness: 0.95 }),
  leaf: new THREE.MeshStandardMaterial({ color: 0x2f5d31, roughness: 0.98 }),
  lantern: new THREE.MeshStandardMaterial({ color: 0x2e1e16, emissive: 0xff8a3d, emissiveIntensity: 0.55 }),
  water: new THREE.MeshStandardMaterial({ color: 0x4f91d8, roughness: 0.25, metalness: 0.06 })
}

const player = new THREE.Mesh(
  new THREE.CapsuleGeometry(0.7, 1.8, 4, 8),
  new THREE.MeshStandardMaterial({ color: 0xeef1fb, roughness: 0.55 })
)
player.castShadow = true
scene.add(player)

function loadAiTexture(prompt, repeat = 4, seed = 1) {
  const key = `${prompt}|${repeat}|${seed}`
  if (texCache.has(key)) return Promise.resolve(texCache.get(key))
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(`${prompt}, seamless tileable texture, top down texture, detailed`)}?width=512&height=512&seed=${seed}&model=flux`
  return new Promise(resolve => {
    textureLoader.load(url, tex => {
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping
      tex.repeat.set(repeat, repeat)
      tex.colorSpace = THREE.SRGBColorSpace
      texCache.set(key, tex)
      resolve(tex)
    }, undefined, () => resolve(null))
  })
}

function applyAiTextures() {
  Promise.all([
    loadAiTexture('lush mossy grass for a temple garden', 8, 1),
    loadAiTexture('ancient carved stone blocks, mossy temple wall', 4, 2),
    loadAiTexture('old dark timber wood grain', 3, 3),
    loadAiTexture('red temple roof tiles', 3, 4),
    loadAiTexture('calm reflective pond water pattern', 6, 5)
  ]).then(([ground, stone, wood, roof, water]) => {
    if (ground) mats.ground.map = ground
    if (stone) mats.stone.map = mats.path.map = stone
    if (wood) mats.wood.map = wood
    if (roof) mats.roof.map = roof
    if (water) mats.water.map = water
    Object.values(mats).forEach(m => { m.needsUpdate = true })
  })
}

function heightAt(x, z) {
  const ridge = Math.sin(x * 0.18) * 1.7 + Math.cos(z * 0.22) * 1.4
  const detail = Math.sin((x + z) * 0.11) * 1.1 + Math.cos((x - z) * 0.16) * 0.75
  const templePad = Math.exp(-(x * x + z * z) / 220) * -2.8
  const pond = Math.exp(-((x + 18) ** 2 + (z - 10) ** 2) / 70) * -2.1
  return ridge + detail + templePad + pond
}

function buildTerrain() {
  const geo = new THREE.PlaneGeometry(120, 120, 120, 120)
  geo.rotateX(-Math.PI / 2)
  const pos = geo.attributes.position
  for (let i = 0; i < pos.count; i++) {
    pos.setY(i, heightAt(pos.getX(i), pos.getZ(i)))
  }
  geo.computeVertexNormals()
  const mesh = new THREE.Mesh(geo, mats.ground)
  mesh.receiveShadow = true
  scene.add(mesh)

  const pond = new THREE.Mesh(new THREE.CircleGeometry(10, 48), mats.water)
  pond.rotation.x = -Math.PI / 2
  pond.position.set(-18, -1.15, 10)
  pond.receiveShadow = true
  scene.add(pond)
}

function addTemple() {
  const group = new THREE.Group()
  const add = (geo, mat, x, y, z, rx = 0, ry = 0, rz = 0) => {
    const m = new THREE.Mesh(geo, mat)
    m.position.set(x, y, z); m.rotation.set(rx, ry, rz)
    m.castShadow = m.receiveShadow = true
    group.add(m)
    return m
  }
  add(new THREE.BoxGeometry(14, 1.8, 14), mats.stone, 0, 0.9, 0)
  add(new THREE.BoxGeometry(10, 5.5, 10), mats.wood, 0, 4.1, 0)
  add(new THREE.ConeGeometry(8.8, 3.8, 4), mats.roof, 0, 8.5, 0, 0, Math.PI * 0.25, 0)
  ;[-4.2, 4.2].forEach(x => [-4.2, 4.2].forEach(z => add(new THREE.CylinderGeometry(0.45, 0.55, 5.5, 10), mats.stone, x, 4.05, z)))
  for (let i = 0; i < 5; i++) add(new THREE.BoxGeometry(7.8 + i * 1.2, 0.35, 2.2), mats.path, 0, 0.18 + i * 0.26, 8.8 + i * 1.45)
  const gate = new THREE.Group()
  gate.add(new THREE.Mesh(new THREE.BoxGeometry(0.6, 4.8, 0.6), mats.wood))
  gate.children[0].position.set(-2.4, 2.4, 0)
  const p2 = gate.children[0].clone(); p2.position.x = 2.4; gate.add(p2)
  const beam = new THREE.Mesh(new THREE.BoxGeometry(6, 0.65, 0.75), mats.roof); beam.position.set(0, 4.9, 0); gate.add(beam)
  const top = new THREE.Mesh(new THREE.BoxGeometry(7.4, 0.32, 1.4), mats.roof); top.position.set(0, 5.35, 0); gate.add(top)
  gate.position.set(0, 0.1, 19.5)
  gate.traverse(m => { m.castShadow = m.receiveShadow = true })
  group.add(gate)
  scene.add(group)
}

function scatterInstances() {
  const treeGeo = new THREE.CylinderGeometry(0.22, 0.35, 3.4, 8)
  const crownGeo = new THREE.ConeGeometry(1.8, 3.8, 9)
  const trunk = new THREE.InstancedMesh(treeGeo, mats.wood, 85)
  const crown = new THREE.InstancedMesh(crownGeo, mats.leaf, 85)
  trunk.castShadow = crown.castShadow = true
  trunk.receiveShadow = crown.receiveShadow = true
  let n = 0
  for (let x = -45; x <= 45; x += 6) for (let z = -45; z <= 45; z += 6) {
    if ((Math.abs(x) < 16 && z > -12 && z < 28) || ((x + 18) ** 2 + (z - 10) ** 2 < 140) || Math.random() < 0.38) continue
    const y = heightAt(x, z)
    const scale = 0.8 + Math.random() * 0.65
    temp.position.set(x + (Math.random() - 0.5) * 1.8, y + 1.7 * scale, z + (Math.random() - 0.5) * 1.8)
    temp.rotation.set(0, Math.random() * Math.PI * 2, 0)
    temp.scale.set(scale, scale, scale)
    temp.updateMatrix(); trunk.setMatrixAt(n, temp.matrix)
    temp.position.y += 2.6 * scale; temp.updateMatrix(); crown.setMatrixAt(n, temp.matrix)
    n++
    if (n === 85) break
  }
  trunk.count = crown.count = n
  scene.add(trunk, crown)

  const postGeo = new THREE.CylinderGeometry(0.12, 0.14, 2.7, 8)
  const glowGeo = new THREE.BoxGeometry(0.48, 0.7, 0.48)
  const postMesh = new THREE.InstancedMesh(postGeo, mats.wood, 8)
  const glowMesh = new THREE.InstancedMesh(glowGeo, mats.lantern, 8)
  const points = [[-4,12], [4,12], [-7,16], [7,16], [-10,20], [10,20], [-13,24], [13,24]]
  points.forEach(([x, z], i) => {
    const y = heightAt(x, z)
    temp.position.set(x, y + 1.35, z); temp.updateMatrix(); postMesh.setMatrixAt(i, temp.matrix)
    temp.position.y += 1.18; temp.updateMatrix(); glowMesh.setMatrixAt(i, temp.matrix)
    const p = new THREE.PointLight(0xff9145, 1.35, 15)
    p.position.set(x, y + 2.55, z); scene.add(p)
  })
  postMesh.castShadow = glowMesh.castShadow = true
  scene.add(postMesh, glowMesh)
}

function addPath() {
  const pts = []
  for (let z = 34; z >= 7; z -= 2.2) pts.push(new THREE.Vector3(Math.sin(z * 0.08) * 1.6, heightAt(Math.sin(z * 0.08) * 1.6, z) + 0.03, z))
  const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 1.6, 12)
  const path = new THREE.Mesh(geo, mats.path)
  path.receiveShadow = true
  scene.add(path)
}

buildTerrain()
addTemple()
addPath()
scatterInstances()
applyAiTextures()

const bounds = 52
const speed = 13
player.position.set(0, heightAt(0, 28) + 1.4, 28)
controls.target.copy(player.position).add(new THREE.Vector3(0, 4, 0))

addEventListener('keydown', e => keys.add(e.key.toLowerCase()))
addEventListener('keyup', e => keys.delete(e.key.toLowerCase()))
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(innerWidth, innerHeight)
  composer.setSize(innerWidth, innerHeight)
})

function movePlayer(dt) {
  const dir = new THREE.Vector3(
    (keys.has('a') || keys.has('arrowleft') ? -1 : 0) + (keys.has('d') || keys.has('arrowright') ? 1 : 0),
    0,
    (keys.has('w') || keys.has('arrowup') ? -1 : 0) + (keys.has('s') || keys.has('arrowdown') ? 1 : 0)
  )
  if (!dir.lengthSq()) return
  dir.normalize().multiplyScalar(speed * dt)
  const next = player.position.clone().add(dir)
  next.x = THREE.MathUtils.clamp(next.x, -bounds, bounds)
  next.z = THREE.MathUtils.clamp(next.z, -bounds, bounds)
  player.position.set(next.x, heightAt(next.x, next.z) + 1.4, next.z)
  player.rotation.y = Math.atan2(dir.x, dir.z)
  controls.target.lerp(player.position.clone().add(new THREE.Vector3(0, 4, 0)), 0.1)
}

function animate() {
  const dt = clock.getDelta()
  const t = clock.elapsedTime
  movePlayer(dt)
  mats.water.emissive = new THREE.Color(0x1e4c73).multiplyScalar(0.15 + Math.sin(t * 1.5) * 0.03)
  lights.ambient.intensity = 0.72 + Math.sin(t * 0.2) * 0.04
  controls.update()
  composer.render()
  requestAnimationFrame(animate)
}
animate()
