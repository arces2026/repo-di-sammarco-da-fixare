# README.md Section - Vue Frontend Development Setup

## Table of Contents

- [README.md Section - Vue Frontend Development Setup](#readmemd-section---vue-frontend-development-setup)
  - [Table of Contents](#table-of-contents)
  - [Frontend Development with Hot Reload](#frontend-development-with-hot-reload)
    - [Multi-Stage Dockerfile Configuration](#multi-stage-dockerfile-configuration)
    - [Docker Compose Configuration](#docker-compose-configuration)
    - [Getting Started](#getting-started)
      - [1. Development Mode (with Hot Reload)](#1-development-mode-with-hot-reload)
      - [2. Production Mode (Static Files)](#2-production-mode-static-files)
    - [Development Workflow](#development-workflow)
      - [With Hot Reload (Development Mode)](#with-hot-reload-development-mode)
      - [Without Hot Reload (Production Mode)](#without-hot-reload-production-mode)
    - [Switching Between Modes](#switching-between-modes)
    - [Package.json Requirements](#packagejson-requirements)
    - [Common Commands](#common-commands)
    - [Verify Hot Reload is Working](#verify-hot-reload-is-working)
    - [Important Notes](#important-notes)
    - [Troubleshooting](#troubleshooting)
    - [File Structure](#file-structure)

---

## Frontend Development with Hot Reload

### Multi-Stage Dockerfile Configuration

The frontend uses a multi-stage Dockerfile that supports both development (with hot reload) and production modes using Docker build targets.

**File: `frontend-vue/Dockerfile`**

```dockerfile
# ============================================
# DEVELOPMENT STAGE
# ============================================
FROM node:20-slim AS development

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# ============================================
# BUILD STAGE (for production)
# ============================================
FROM node:20-slim AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build


# ============================================
# PRODUCTION STAGE (serves built files with Nginx)
# ============================================
FROM nginx:alpine AS production

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

[↑ Go up](#table-of-contents)

### Docker Compose Configuration

The `docker-compose.yml` defines two separate frontend services - one for development and one for production:

```yaml
services:
  # DEVELOPMENT MODE - with hot reload
  frontend-dev:
    build:
      context: ./frontend-vue
      target: development  # Build ONLY the 'development' stage
    container_name: frontend-vue-dev
    ports:
      - "8080:5173"  # Vite dev server port
    volumes:
      - ./frontend-vue:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
    depends_on:
      - backend

  # PRODUCTION MODE - serving static files with Nginx
  frontend-prod:
    build:
      context: ./frontend-vue
      target: production  # Build ONLY the 'production' stage
    container_name: frontend-vue-prod
    ports:
      - "8080:80"  # Nginx serves on port 80
    # No volume mounts - files are baked into the image
    depends_on:
      - backend
```

[↑ Go up](#table-of-contents)

### Getting Started

#### 1. Development Mode (with Hot Reload)

Start the frontend in development mode:

```bash
docker-compose up frontend-dev
```

Or start all services:

```bash
docker-compose up db backend frontend-dev
```

**Access your application:**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- Database: localhost:3307

[↑ Go up](#table-of-contents)

#### 2. Production Mode (Static Files)

Start the frontend in production mode:

```bash
docker-compose up frontend-prod
```

Or start all services:

```bash
docker-compose up db backend frontend-prod
```

**Access your application:**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000

[↑ Go up](#table-of-contents)

### Development Workflow

#### With Hot Reload (Development Mode)

1. **Make changes** to any Vue file in `./frontend-vue/`
2. **Save the file** - Vite's HMR automatically detects changes
3. **See updates** instantly in your browser without page refresh
4. **No rebuild needed** - changes are reflected immediately

[↑ Go up](#table-of-contents)

#### Without Hot Reload (Production Mode)

1. **Make changes** to Vue files in `./frontend-vue/`
2. **Rebuild the image** for changes to take effect:

```bash
docker-compose build frontend-prod
```

3. **Restart the container**:

```bash
docker-compose up -d frontend-prod
```

[↑ Go up](#table-of-contents)

### Switching Between Modes

**From Development to Production:**

```bash
# 1. Stop development container
docker-compose stop frontend-dev

# 2. Start production container
docker-compose up frontend-prod
```

**From Production to Development:**

```bash
# 1. Stop production container
docker-compose stop frontend-prod

# 2. Start development container
docker-compose up frontend-dev
```

[↑ Go up](#table-of-contents)

### Package.json Requirements

Ensure your `frontend-vue/package.json` includes these scripts:

```json
{
  "scripts": {
    "dev": "vite --host 0.0.0.0",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

The `--host 0.0.0.0` flag makes the dev server accessible from outside the Docker container.

[↑ Go up](#table-of-contents)

### Common Commands

```bash
# View logs for development container
docker-compose logs -f frontend-dev

# View logs for production container
docker-compose logs -f frontend-prod

# Stop a specific service
docker-compose stop frontend-dev

# Restart a specific service
docker-compose restart frontend-dev

# Rebuild images
docker-compose build frontend-dev
docker-compose build frontend-prod

# Stop all services
docker-compose down
```

[↑ Go up](#table-of-contents)

### Verify Hot Reload is Working

To confirm hot reload is active in development mode:

1. Open your browser to http://localhost:8080
2. Open the browser's Developer Tools (F12)
3. Check the Console tab - you should see Vite's HMR connection messages
4. Make a change to a Vue component and save - the page should update automatically

[↑ Go up](#table-of-contents)

### Important Notes

- **Port Conflict**: Both services use port `8080` on your host. You cannot run both `frontend-dev` and `frontend-prod` simultaneously. Stop one before starting the other.

- **Volume Mount**: In development mode, your local `./frontend-vue` is mounted into the container, enabling hot reload. In production mode, no volume is mounted - the files are baked into the image.

- **node_modules**: The `/app/node_modules` volume in development prevents conflicts between your local `node_modules` and the container's dependencies.

- **File Watching**: `CHOKIDAR_USEPOLLING=true` enables file watching in Docker (required on Windows and macOS).

[↑ Go up](#table-of-contents)

### Troubleshooting

**Issue**: Hot reload not working in development mode

- **Solution**: Ensure `CHOKIDAR_USEPOLLING=true` is set in environment variables
- **Solution**: Verify source code is mounted: `./frontend-vue:/app`
- **Solution**: Check that `node_modules` is NOT mounted from the host (use `/app/node_modules` volume)

**Issue**: Port 8080 already in use

- **Solution**: Change the host port mapping: `"8081:5173"` or `"8081:80"`
- **Solution**: Stop other services using port 8080

**Issue**: Changes not reflecting in browser

- **Solution**: Clear browser cache or do a hard refresh (Ctrl+Shift+R)
- **Solution**: Check terminal for compilation errors
- **Solution**: Verify your Vue file is in `./frontend-vue/src/`

**Issue**: "Cannot find module" errors

- **Solution**: Rebuild the container: `docker-compose build frontend-dev`
- **Solution**: Check that `package.json` exists in `./frontend-vue/`

[↑ Go up](#table-of-contents)

### File Structure

```text
project-root/
├── frontend-vue/
│   ├── Dockerfile              # Multi-stage Dockerfile (dev & prod)
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── nginx.conf              # Custom Nginx config (optional)
│   ├── src/                    # Source code
│   │   ├── components/
│   │   ├── views/
│   │   └── App.vue
│   ├── public/                 # Static assets
|   ├── README.md
|   └── HMR-guide               # this file
├── docker-compose.yml          # Docker Compose configuration
└── README.md
```

[↑ Go up](#table-of-contents)