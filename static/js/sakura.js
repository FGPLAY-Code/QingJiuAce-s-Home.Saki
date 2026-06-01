class SakuraPetal {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.reset();
    }

    reset() {
        this.x = Math.random() * this.canvas.width;
        this.y = -20 - Math.random() * 100;
        this.size = 6 + Math.random() * 10;
        this.speedY = 1 + Math.random() * 2;
        this.speedX = -0.5 + Math.random();
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = -0.05 + Math.random() * 0.1;
        this.opacity = 0.5 + Math.random() * 0.5;
        this.color = this.getRandomSakuraColor();
    }

    getRandomSakuraColor() {
        const colors = [
            'rgba(255, 183, 197, ',
            'rgba(255, 133, 162, ',
            'rgba(255, 228, 233, ',
            'rgba(244, 143, 177, ',
            'rgba(255, 200, 210, '
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
        this.y += this.speedY;
        this.x += this.speedX + Math.sin(this.y * 0.01) * 0.5;
        this.rotation += this.rotationSpeed;

        if (this.y > this.canvas.height + 20) {
            this.reset();
        }
    }

    draw() {
        this.ctx.save();
        this.ctx.translate(this.x, this.y);
        this.ctx.rotate(this.rotation);
        this.ctx.globalAlpha = this.opacity;
        
        this.ctx.fillStyle = this.color + this.opacity + ')';
        this.ctx.beginPath();
        
        for (let i = 0; i < 5; i++) {
            const angle = (i * Math.PI * 2) / 5;
            const nextAngle = ((i + 0.5) * Math.PI * 2) / 5;
            const radius = this.size / 2;
            const innerRadius = radius * 0.4;
            
            if (i === 0) {
                this.ctx.moveTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
            } else {
                this.ctx.lineTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
            }
            this.ctx.quadraticCurveTo(
                Math.cos(nextAngle) * innerRadius,
                Math.sin(nextAngle) * innerRadius,
                Math.cos(nextAngle) * radius,
                Math.sin(nextAngle) * radius
            );
        }
        
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.restore();
    }
}

class SakuraAnimation {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.container = document.getElementById('sakura-container');
        this.container.appendChild(this.canvas);
        this.petals = [];
        this.numPetals = 30;
        
        this.resize();
        this.init();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    init() {
        for (let i = 0; i < this.numPetals; i++) {
            const petal = new SakuraPetal(this.canvas);
            petal.y = Math.random() * this.canvas.height;
            this.petals.push(petal);
        }
    }

    animate() {
        const ctx = this.canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.petals.forEach(petal => {
            petal.update();
            petal.draw();
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

window.addEventListener('DOMContentLoaded', () => {
    new SakuraAnimation();
});
