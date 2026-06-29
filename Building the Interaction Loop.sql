 
 export function spawnEnemy (type) {
   const enemy = createEnemyTemplate(type)
   enemy.angle = Math.randon() * Math.PI * 2
   return enemy
  }

  
  export function attackEnemy(player, enemy) {
    const newCombo = (player.comboCount + 1) % 4
    const isBig = newCombo === 3
    const damage = 12 + player.level * 3 + (isBig ? 22 : 0) + Math.floor(Math.random() * 8)
    const newHp = Math.max(0, enemy.hp - damage)
    const killed = newHp <= 0
    let p = { ...player, comboCount: newCombo }
    if (killed) {
    p.xp    += ENEMY_TYPES[enemy.type].xp
    p.gold  += Math.floor(ENEMY_TYPES[enemy.type].xp * 0.5)
    p.kills += 1
    p.score += ENEMY_TYPES[enemy.type].xp * 10
  }
    return { player: p, enemy: { ...enemy, hp: newHp, alive: !killed }, damage, killed, isBig }
    }


    export function enemyAttack(enemy, player) {
      const damage = ENEMY_TYPES[enemy.type].atk + Math.floor(Math.random() * 7)
      return {
        player: { ...player, hp: Math.max(0, player.hp - damage), invincible: 0.42 },
        damage,
       }
    }


    export function usePotion(player) {
      if (player.potions <= 0) return { player, healed: 0 }
      const heal = Math.min(55, player.maxHp - player.hp)
      return {
        player: { ...player, hp: player.hp + heal, potions: player.potions - 1 },
        healed: heal,
      }
    }

    
    export function updateQuestProgress(quests, type, amount) {
      return quests.map(q => {
        if (q.completed || q.type !== type) return q 
        const progress = (q.progress ?? 0) + amount
        return { ...q, progress, completed: progress >= (q.count ?? 1) }
      })
    }