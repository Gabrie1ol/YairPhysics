<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <title>סימולציית חללית פוטונית</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            direction: rtl;
        }

        canvas {
            background-color: black;
            display: block;
            margin: 20px auto;
        }

        .controls {
            margin: 10px auto;
            max-width: 600px;
        }

        input {
            width: 100px;
        }

        label {
            margin-left: 10px;
        }

        button {
            padding: 8px 16px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }

        #info {
            margin-top: 10px;
            font-size: 14px;
            white-space: pre-line;
        }
    </style>
</head>
<body>

<h1>🚀 סימולציית חללית פוטונית</h1>

<canvas id="canvas" width="2000" height="600"></canvas>

<div class="controls">
    <div>
        <label>מסה (ק"ג):</label>
        <input id="mass" type="number" value="1000">
    </div>
    <div>
        <label>שטח קליטה (מ"ר):</label>
        <input id="area" type="number" value="10">
    </div>
    <div>
        <label>עוצמת אור (W/m²):</label>
        <input id="intensity" type="number" value="1e8">
    </div>
    <div>
        <label>משך (שניות):</label>
        <input id="duration" type="number" value="20">
    </div>
    <button onclick="startSimulation()">🚀 התחל סימולציה</button>
</div>

<div id="info"></div>

<script>
    const c = 3e8;  // מהירות האור

    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    let mass, area, intensity, duration;
    let t, velocity, position;
    let dt = 0.1;
    let simulating = false;
    let trail = [];
    let rocketY = 300;
    const scale = 1e3;  // 1000 מטר לפיקסל

    function drawRocket(x) {
        const y = rocketY;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw trail
        ctx.fillStyle = "lightgray";
        trail.forEach(([tx, ty]) => {
            ctx.beginPath();
            ctx.arc(tx, ty, 1, 0, 2 * Math.PI);
            ctx.fill();
        });

        // Draw rocket body
        ctx.fillStyle = "white";
        ctx.fillRect(x - 15, y - 5, 30, 10);

        // Top wing
        ctx.fillStyle = "gray";
        ctx.beginPath();
        ctx.moveTo(x - 5, y - 5);
        ctx.lineTo(x - 15, y - 15);
        ctx.lineTo(x - 10, y - 5);
        ctx.closePath();
        ctx.fill();

        // Bottom wing
        ctx.beginPath();
        ctx.moveTo(x - 5, y + 5);
        ctx.lineTo(x - 15, y + 15);
        ctx.lineTo(x - 10, y + 5);
        ctx.closePath();
        ctx.fill();

        // Nose
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.moveTo(x + 15, y - 5);
        ctx.lineTo(x + 15, y + 5);
        ctx.lineTo(x + 25, y);
        ctx.closePath();
        ctx.fill();
    }

    function updateSimulation() {
        if (simulating && t <= duration) {
            const acceleration = (intensity * area) / (mass * c);

            velocity += acceleration * dt;
            position += velocity * dt;
            t += dt;

            const x = 10 + position * scale;
            trail.push([x - 15, rocketY]);
            if (trail.length > 100) trail.shift();

            drawRocket(x);

            document.getElementById("info").textContent =
                `זמן: ${t.toFixed(1)} שניות | מהירות: ${velocity.toFixed(3)} m/s`;

            requestAnimationFrame(updateSimulation);
        } else {
            simulating = false;
            document.getElementById("info").textContent += "\n✔️ סימולציה הסתיימה!";
        }
    }

    function startSimulation() {
        mass = parseFloat(document.getElementById("mass").value);
        area = parseFloat(document.getElementById("area").value);
        intensity = parseFloat(document.getElementById("intensity").value);
        duration = parseFloat(document.getElementById("duration").value);

        if (isNaN(mass) || isNaN(area) || isNaN(intensity) || isNaN(duration)) {
            document.getElementById("info").textContent = "יש להזין ערכים תקינים";
            return;
        }

        t = 0;
        velocity = 0;
        position = 0;
        simulating = true;
        trail = [];

        drawRocket(10);
        updateSimulation();
    }
</script>

</body>
</html>
