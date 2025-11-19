# Task Delegation Agents

This project uses an agent-based architecture for task delegation and parallel processing.

## Agent System Overview

The task manager (`agents/task_manager.py`) coordinates specialized agents that handle different aspects of the Govee Lights Controller.

## Available Agents

### 1. Light Control Agent (`agents/light_control_agent.py`)
**Purpose**: Handles basic light control operations

**Capabilities**:
- Turn lights on/off
- Set color (RGB)
- Adjust brightness
- Control individual devices

**Usage**:
```python
from agents.task_manager import task_manager

task_manager.submit_task('light_control', {
    'device_id': 'device_123',
    'action': 'color',
    'params': {'r': 255, 'g': 0, 'b': 0}
})
```

### 2. Audio Reactive Agent (`agents/audio_agent.py`)
**Purpose**: Handles audio-reactive lighting based on microphone input

**Capabilities**:
- Process microphone audio input
- Analyze frequency spectrum
- Map frequencies to colors
- Update lights in real-time based on audio

**Usage**:
```python
task_manager.submit_task('audio_reactive', {
    'action': 'start',
    'device_ids': ['device_123', 'device_456'],
    'duration': 60  # Optional: seconds
})
```

### 3. Synchronization Agent (`agents/sync_agent.py`)
**Purpose**: Coordinates synchronized effects across multiple light strips

**Capabilities**:
- Create rolling effects across multiple strips
- Synchronize timing between devices
- Coordinate complex multi-strip patterns

**Usage**:
```python
task_manager.submit_task('sync_effect', {
    'action': 'start_rolling',
    'strips': ['device_123', 'device_456'],
    'led_counts': [100, 100],
    'speed': 2.0,
    'color': (255, 255, 255)
})
```

## Task Manager

The `TaskManager` class manages all agents and processes tasks asynchronously.

**Features**:
- Thread-safe task queue
- Automatic task processing
- Error handling
- Agent registration system

**Initialization**:
The task manager starts automatically when imported. Agents register themselves on import.

## Adding New Agents

To add a new agent:

1. Create a new file in `agents/` directory
2. Define an agent handler function
3. Register with task manager:

```python
from agents.task_manager import task_manager

def my_agent_handler(task_data: dict):
    # Process task_data
    pass

task_manager.register_agent('my_agent', my_agent_handler)
```

4. Submit tasks using:
```python
task_manager.submit_task('my_agent', {'key': 'value'})
```

## Integration with Web Server

The web server (`server/main.py`) uses agents through WebSocket events:

- Audio frequency updates → Audio Reactive Agent
- Light control requests → Light Control Agent
- Sync effect requests → Synchronization Agent

