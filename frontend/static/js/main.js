// Main JavaScript for Govee Lights Controller
const socket = io();

let audioContext = null;
let microphone = null;
let audioAnalyzer = null;
let isAudioActive = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadLights();
    setupAudioControls();
    setupSyncControls();
    setupSocketListeners();
});

// Load available lights
async function loadLights() {
    try {
        const response = await fetch('/api/lights');
        const data = await response.json();
        
        const container = document.getElementById('lights-container');
        const strip1Select = document.getElementById('strip1');
        const strip2Select = document.getElementById('strip2');
        
        if (data.lights && data.lights.length > 0) {
            container.innerHTML = '';
            data.lights.forEach(light => {
                // Add to lights list
                const lightItem = createLightItem(light);
                container.appendChild(lightItem);
                
                // Add to select dropdowns
                const option1 = new Option(light.name, light.id);
                const option2 = new Option(light.name, light.id);
                strip1Select.appendChild(option1);
                strip2Select.appendChild(option2);
            });
        } else {
            container.innerHTML = '<p>No lights found. Make sure your Govee devices are connected.</p>';
        }
    } catch (error) {
        console.error('Error loading lights:', error);
        document.getElementById('lights-container').innerHTML = 
            '<p>Error loading lights. Check console for details.</p>';
    }
}

function createLightItem(light) {
    const div = document.createElement('div');
    div.className = 'light-item';
    div.innerHTML = `
        <h3>${light.name}</h3>
        <p>Status: <span class="light-status ${light.status}">${light.status.toUpperCase()}</span></p>
        <p>Type: ${light.type || 'Unknown'}</p>
        <button class="btn btn-primary" onclick="controlLight('${light.id}', 'toggle')">
            Toggle
        </button>
    `;
    return div;
}

// Audio-reactive controls
function setupAudioControls() {
    document.getElementById('start-audio').addEventListener('click', startAudioReactive);
    document.getElementById('stop-audio').addEventListener('click', stopAudioReactive);
}

async function startAudioReactive() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        microphone = audioContext.createMediaStreamSource(stream);
        audioAnalyzer = audioContext.createAnalyser();
        audioAnalyzer.fftSize = 2048;
        
        microphone.connect(audioAnalyzer);
        
        isAudioActive = true;
        document.getElementById('start-audio').disabled = true;
        document.getElementById('stop-audio').disabled = false;
        
        // Start processing audio
        processAudio();
        
        socket.emit('audio_started');
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Could not access microphone. Please check permissions.');
    }
}

function stopAudioReactive() {
    isAudioActive = false;
    if (microphone) {
        microphone.disconnect();
    }
    if (audioContext) {
        audioContext.close();
    }
    
    document.getElementById('start-audio').disabled = false;
    document.getElementById('stop-audio').disabled = true;
    
    socket.emit('audio_stopped');
}

function processAudio() {
    if (!isAudioActive || !audioAnalyzer) return;
    
    const bufferLength = audioAnalyzer.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    audioAnalyzer.getByteFrequencyData(dataArray);
    
    // Find dominant frequency
    let maxIndex = 0;
    let maxValue = 0;
    for (let i = 0; i < bufferLength; i++) {
        if (dataArray[i] > maxValue) {
            maxValue = dataArray[i];
            maxIndex = i;
        }
    }
    
    // Calculate frequency (approximate)
    const sampleRate = audioContext.sampleRate;
    const frequency = (maxIndex * sampleRate) / (2 * bufferLength);
    
    // Send frequency to server for color mapping
    socket.emit('audio_frequency', { frequency: frequency });
    
    // Visualize
    visualizeFrequency(dataArray);
    
    // Continue processing
    requestAnimationFrame(processAudio);
}

function visualizeFrequency(dataArray) {
    const canvas = document.getElementById('frequency-canvas');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    ctx.clearRect(0, 0, width, height);
    
    const barWidth = width / dataArray.length;
    let x = 0;
    
    for (let i = 0; i < dataArray.length; i++) {
        const barHeight = (dataArray[i] / 255) * height;
        ctx.fillStyle = `rgb(${dataArray[i]}, ${255 - dataArray[i]}, 100)`;
        ctx.fillRect(x, height - barHeight, barWidth, barHeight);
        x += barWidth;
    }
}

// Synchronized rolling effect controls
function setupSyncControls() {
    document.getElementById('speed').addEventListener('input', (e) => {
        document.getElementById('speed-value').textContent = e.target.value;
    });
    
    document.getElementById('start-rolling').addEventListener('click', startRollingEffect);
    document.getElementById('stop-rolling').addEventListener('click', stopRollingEffect);
}

function startRollingEffect() {
    const strip1 = document.getElementById('strip1').value;
    const strip2 = document.getElementById('strip2').value;
    const speed = parseFloat(document.getElementById('speed').value);
    
    if (!strip1 || !strip2) {
        alert('Please select both light strips');
        return;
    }
    
    socket.emit('start_rolling', {
        strip1: strip1,
        strip2: strip2,
        speed: speed
    });
    
    document.getElementById('start-rolling').disabled = true;
    document.getElementById('stop-rolling').disabled = false;
}

function stopRollingEffect() {
    socket.emit('stop_rolling');
    document.getElementById('start-rolling').disabled = false;
    document.getElementById('stop-rolling').disabled = true;
}

// Socket event listeners
function setupSocketListeners() {
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('status', (data) => {
        console.log('Status:', data.message);
    });
    
    socket.on('color_update', (data) => {
        console.log('Color update:', data);
        // Update UI with new color
    });
    
    socket.on('effect_status', (data) => {
        console.log('Effect status:', data);
    });
}

// Control individual light
async function controlLight(lightId, action) {
    try {
        const response = await fetch(`/api/lights/${lightId}/control`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            loadLights(); // Refresh lights list
        }
    } catch (error) {
        console.error('Error controlling light:', error);
    }
}

