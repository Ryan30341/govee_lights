# Govee Lights Controller

A web-based interface to control Govee smart lights with advanced coordination features for multiple light strips.

## Project Goals

### Primary Objectives

1. **Web Interface**: Create a web-based control panel for Govee lights accessible over WiFi
2. **Light Discovery**: List all available lights and their supported functions
3. **Multi-Strip Coordination**: Coordinate actions between two light strips

### Key Features

#### Example 1: Audio-Reactive Lighting
- Use microphone input to output colors based on sound frequency
- Map microphone frequency range to color gradients
- Real-time audio visualization through light colors

#### Example 2: Synchronized Rolling Effect
- Create a rolling light effect that starts at one end of light strip 1
- Continue seamlessly to the end of light strip 2
- Overcome limitations of Govee's built-in sync/grouping modes
- Achieve true coordinated timing across multiple strips

## Technical Stack

- **Backend**: Python web server (Flask/FastAPI)
- **API**: Govee Open Source API
- **Frontend**: Web interface with real-time controls
- **Audio**: Microphone input processing for frequency analysis
- **Network**: WiFi connection to Govee devices

## Project Structure

```
govee_lights/
├── server/              # Web server code
├── govee_api/          # Govee API integration
├── audio/              # Audio processing and frequency analysis
├── frontend/           # Web interface files
├── agents/             # Task delegation agents
└── tests/              # Test files
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Govee API credentials (if needed)

3. Run the web server:
```bash
python server/main.py
```

4. Access the web interface at `http://localhost:5000`

## Development

This project uses git worktrees for parallel development workflows.

