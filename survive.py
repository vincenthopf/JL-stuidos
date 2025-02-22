<!DOCTYPE html>
<html>
<head>
    <title>Space Shooter</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        canvas {
            border: 2px solid #333;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // Set canvas size
        canvas.width = 800;
        canvas.height = 600;

        // Game constants
        const PLAYER_SIZE = 40;
        const ENEMY_SIZE = 30;
        const BULLET_SIZE = 8;

        // Game state
        let gameState = {
            player: {
                x: canvas.width / 2,
                y: canvas.height / 2,
                speed: 5,
                health: 100,
                score: 0,
                bullets: [],
                dashCooldown: 0,
                trail: []
            },
            enemies: [],
            currentWave: 1,
            wavesTotal: 5,
            enemiesPerWave: 10,
            enemiesDefeated: 0,
            waveComplete: false,
            gameOver: false,
            gameWon: false,
            keys: {},
            mousePos: { x: 0, y: 0 },
            mouseDown: false
        };

        // Input handling
        document.addEventListener('keydown', (e) => gameState.keys[e.key.toLowerCase()] = true);
        document.addEventListener('keyup', (e) => gameState.keys[e.key.toLowerCase()] = false);
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            gameState.mousePos.x = e.clientX - rect.left;
            gameState.mousePos.y = e.clientY - rect.top;
        });
        canvas.addEventListener('mousedown', () => gameState.mouseDown = true);
        canvas.addEventListener('mouseup', () => gameState.mouseDown = false);

        function spawnEnemy() {
            const side = Math.floor(Math.random() * 4);
            let x, y;
            
            switch(side) {
                case 0: // Top
                    x = Math.random() * canvas.width;
                    y = -ENEMY_SIZE;
                    break;
                case 1: // Right
                    x = canvas.width + ENEMY_SIZE;
                    y = Math.random() * canvas.height;
                    break;
                case 2: // Bottom
                    x = Math.random() * canvas.width;
                    y = canvas.height + ENEMY_SIZE;
                    break;
                case 3: // Left
                    x = -ENEMY_SIZE;
                    y = Math.random() * canvas.height;
                    break;
            }

            return {
                x,
                y,
                speed: 2 + (gameState.currentWave - 1) * 0.5,
                health: 100 + (gameState.currentWave - 1) * 20,
                particles: []
            };
        }

        function createBullet(startX, startY, targetX, targetY) {
            const angle = Math.atan2(targetY - startY, targetX - startX);
            const speed = 10;
            return {
                x: startX,
                y: startY,
                dx: Math.cos(angle) * speed,
                dy: Math.sin(angle) * speed,
                lifetime: 60,
                particles: []
            };
        }

        function updateGame() {
            const player = gameState.player;

            // Player movement
            if (gameState.keys['w']) player.y -= player.speed;
            if (gameState.keys['s']) player.y += player.speed;
            if (gameState.keys['a']) player.x -= player.speed;
            if (gameState.keys['d']) player.x += player.speed;

            // Keep player in bounds
            player.x = Math.max(PLAYER_SIZE, Math.min(canvas.width - PLAYER_SIZE, player.x));
            player.y = Math.max(PLAYER_SIZE, Math.min(canvas.height - PLAYER_SIZE, player.y));

            // Update dash cooldown
            if (player.dashCooldown > 0) player.dashCooldown--;

            // Dash
            if (gameState.keys[' '] && player.dashCooldown === 0) {
                const dashDistance = 100;
                const dx = (gameState.keys['d'] - gameState.keys['a']);
                const dy = (gameState.keys['s'] - gameState.keys['w']);
                if (dx !== 0 || dy !== 0) {
                    const length = Math.sqrt(dx * dx + dy * dy);
                    player.x += (dx / length) * dashDistance;
                    player.y += (dy / length) * dashDistance;
                    player.dashCooldown = 30;
                }
            }

            // Shooting
            if (gameState.mouseDown) {
                player.bullets.push(createBullet(player.x, player.y, 
                                               gameState.mousePos.x, gameState.mousePos.y));
            }

            // Update bullets
            player.bullets.forEach((bullet, i) => {
                bullet.x += bullet.dx;
                bullet.y += bullet.dy;
                bullet.lifetime--;
                
                if (bullet.lifetime <= 0) {
                    player.bullets.splice(i, 1);
                }
            });

            // Spawn enemies
            if (!gameState.waveComplete && gameState.enemies.length < 3 && 
                gameState.enemiesDefeated < gameState.enemiesPerWave) {
                if (Math.random() < 0.02) {
                    gameState.enemies.push(spawnEnemy());
                }
            }

            // Update enemies
            gameState.enemies.forEach((enemy, i) => {
                const dx = player.x - enemy.x;
                const dy = player.y - enemy.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                enemy.x += (dx / dist) * enemy.speed;
                enemy.y += (dy / dist) * enemy.speed;

                // Check collision with player
                if (dist < (PLAYER_SIZE + ENEMY_SIZE) / 2) {
                    player.health -= 10;
                    gameState.enemies.splice(i, 1);
                    if (player.health <= 0) {
                        gameState.gameOver = true;
                    }
                }

                // Check collision with bullets
                player.bullets.forEach((bullet, j) => {
                    const bulletDist = Math.sqrt(
                        Math.pow(bullet.x - enemy.x, 2) + 
                        Math.pow(bullet.y - enemy.y, 2)
                    );
                    
                    if (bulletDist < (BULLET_SIZE + ENEMY_SIZE) / 2) {
                        gameState.enemies.splice(i, 1);
                        player.bullets.splice(j, 1);
                        player.score += 100 * gameState.currentWave;
                        gameState.enemiesDefeated++;
                        
                        if (gameState.enemiesDefeated >= gameState.enemiesPerWave) {
                            gameState.waveComplete = true;
                            if (gameState.currentWave >= gameState.wavesTotal) {
                                gameState.gameWon = true;
                            } else {
                                setTimeout(startNextWave, 3000);
                            }
                        }
                    }
                });
            });

            // Update trail
            player.trail.push({x: player.x, y: player.y});
            if (player.trail.length > 10) player.trail.shift();
        }

        function startNextWave() {
            gameState.currentWave++;
            gameState.enemiesDefeated = 0;
            gameState.waveComplete = false;
            gameState.enemies = [];
            gameState.player.health = Math.min(100, gameState.player.health + 30);
        }

        function drawGame() {
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw player trail
            gameState.player.trail.forEach((pos, i) => {
                ctx.beginPath();
                ctx.arc(pos.x, pos.y, PLAYER_SIZE/2, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(50, 50, 255, ${i / gameState.player.trail.length * 0.5})`;
                ctx.fill();
            });

            // Draw player
            ctx.beginPath();
            ctx.arc(gameState.player.x, gameState.player.y, PLAYER_SIZE/2, 0, Math.PI * 2);
            ctx.fillStyle = 'rgb(50, 50, 255)';
            ctx.fill();

            // Draw enemies
            gameState.enemies.forEach(enemy => {
                ctx.beginPath();
                ctx.arc(enemy.x, enemy.y, ENEMY_SIZE/2, 0, Math.PI * 2);
                ctx.fillStyle = 'rgb(255, 50, 50)';
                ctx.fill();
            });

            // Draw bullets
            gameState.player.bullets.forEach(bullet => {
                ctx.beginPath();
                ctx.arc(bullet.x, bullet.y, BULLET_SIZE/2, 0, Math.PI * 2);
                ctx.fillStyle = 'yellow';
                ctx.fill();
            });

            // Draw UI
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText(`Health: ${gameState.player.health}`, 10, 30);
            ctx.fillText(`Score: ${gameState.player.score}`, 10, 60);
            ctx.fillText(`Wave: ${gameState.currentWave}/${gameState.wavesTotal}`, 10, 90);
            ctx.fillText(`Enemies: ${gameState.enemiesDefeated}/${gameState.enemiesPerWave}`, 10, 120);

            if (gameState.waveComplete && !gameState.gameWon) {
                ctx.fillStyle = 'white';
                ctx.font = '30px Arial';
                ctx.fillText(`Wave ${gameState.currentWave} Complete!`, 
                           canvas.width/2 - 100, canvas.height/2);
            }

            if (gameState.gameOver) {
                ctx.fillStyle = 'white';
                ctx.font = '40px Arial';
                ctx.fillText('Game Over!', canvas.width/2 - 100, canvas.height/2);
                ctx.font = '20px Arial';
                ctx.fillText('Press R to restart', canvas.width/2 - 70, canvas.height/2 + 40);
            }

            if (gameState.gameWon) {
                ctx.fillStyle = 'white';
                ctx.font = '40px Arial';
                ctx.fillText('Victory!', canvas.width/2 - 70, canvas.height/2);
                ctx.font = '20px Arial';
                ctx.fillText('Press R to play again', canvas.width/2 - 80, canvas.height/2 + 40);
            }
        }

        function resetGame() {
            gameState = {
                player: {
                    x: canvas.width / 2,
                    y: canvas.height / 2,
                    speed: 5,
                    health: 100,
                    score: 0,
                    bullets: [],
                    dashCooldown: 0,
                    trail: []
                },
                enemies: [],
                currentWave: 1,
                wavesTotal: 5,
                enemiesPerWave: 10,
                enemiesDefeated: 0,
                waveComplete: false,
                gameOver: false,
                gameWon: false,
                keys: gameState.keys,
                mousePos: gameState.mousePos,
                mouseDown: gameState.mouseDown
            };
        }

        document.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'r' && (gameState.gameOver || gameState.gameWon)) {
                resetGame();
            }
        });

        function gameLoop() {
            if (!gameState.gameOver && !gameState.gameWon) {
                updateGame();
            }
            drawGame();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
