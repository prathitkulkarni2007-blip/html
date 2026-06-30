  // ――― TASK 1 ――――――――――――――――――――――――――――――――――――――――――――――――――――――
  export  function createBossFight() {
    return {
      entity: {
        name: 'Demon Overlord',
        x: 0,
        y: 0,
        hp: BOSS_HP,
        maxHp: BOSS_UP,
        alive: true,
       },
       phase: 1,
       phaseTimer: 0,
      }
    }

    // ――― TASK 2 ――――――――――――――――――――――――――――――――――――――――――――――――――――――
    export function checkPhaseTransition(bossFight) {
      const { entity, phase } = bossFight
      const pct = entity.hp / entity.maxHp

      if (phase < 2 && pct < 0.66) {
        return {
          bossFight: { ...bossFight, phase: 2, phaseTimer: 0 },
          transitioned: true,
          newPhase: 2,
        }
       }
       if (phase < 3 && pct < 0.33) {
         return {
           bossFight: { ...bossFight, phase: 3, phaseTimer: 0 },
           transitioned: true,
           newPhase: 3,
          }
        }
        return { bossFight, transitioned: false, newPhase: phase }
      }

      // ――― TASK 3 ――――――――――――――――――――――――――――――――――――――――――――――――――――――
      export function attackBoss(player, bossFight) {
        const newCombo = (player.comboCount + 1) % 4
        const isBig = newCombo === 3
        const damage = 14 + player.level * 4 + (isBig ? 30 : 0) + Math.floor(Math.random() * 10)
        const newHp = Math.max(0, bossFight.entity.hp - damage)
        const killed = newHp <= 0
        let p = { ..player, comboCount: newCombo }
        const newEntity = { ...bossFight.entity, hp: newHp, alive: !killed }
        if (killed) {
          p.xp    += 300
          p.gold  += 150
          p.score += 5000
        }
        return {
          player: p,
          bossFight: { ...bossFight, entity: newEntity },
          damage,
          killed,
          isBig,
        }
       }       

       // ――― TASK 4 ――――――――――――――――――――――――――――――――――――――――――――――――――――――
       export  function generateVictoryReport(player, bossFight, turns) {
         const rank = turns <= 5 ? 'S' : turns <= 10 ? 'A' : turns <= 20 ? 'B' : 'C'
         return {
           winner: 'Hero',
           bossName: bossFight.entity.name,
           turnsToWin: turns,
           goldEarned: player.gold,
           xpEarned: 300,
           rank,
           score: 5000,
          }
        }