# Git Worktrees Setup

This project uses git worktrees to enable parallel development workflows for different features. All feature worktrees live under the shared directory `govee_lights_worktrees/` at the same level as the main project folder for a cleaner layout.

## Available Worktrees

1. **Main Repository** (`govee_lights/`)
   - Branch: `main`
   - Purpose: Main development branch, stable code

2. **Audio Feature** (`govee_lights_worktrees/audio/`)
   - Branch: `audio-feature`
   - Purpose: Audio processing, frequency analysis, microphone integration

3. **API Feature** (`govee_lights_worktrees/api/`)
   - Branch: `api-feature`
   - Purpose: Govee API integration, device communication

4. **Frontend Feature** (`govee_lights_worktrees/frontend/`)
   - Branch: `frontend-feature`
   - Purpose: Web interface, UI/UX, client-side JavaScript

## Usage

### Switching Between Worktrees

Each worktree is located inside the shared `govee_lights_worktrees/` directory adjacent to the main repo. Navigate to the desired worktree directory:

```bash
cd ../govee_lights_worktrees/audio     # Work on audio features
cd ../govee_lights_worktrees/api       # Work on API features
cd ../govee_lights_worktrees/frontend  # Work on frontend features
```

### Committing Changes

1. Make changes in the appropriate worktree directory
2. Commit normally: `git add .` and `git commit -m "message"`
3. Push to remote: `git push origin <branch-name>`

### Merging Worktrees

When ready to merge features back to main:

```bash
# From main worktree
git merge audio-feature
git merge api-feature
git merge frontend-feature
```

## Benefits

- **Parallel Development**: Work on multiple features simultaneously without switching branches
- **Isolated Testing**: Test each feature independently
- **Clean History**: Each feature branch maintains its own commit history
- **Task Delegation**: Different agents/developers can work on different worktrees simultaneously

