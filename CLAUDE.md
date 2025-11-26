# CLAUDE.md - AI Assistant Guide for JK-Boilerplate

> **Last Updated**: 2025-11-26
> **Project**: JK-Boilerplate v0.1.0
> **Purpose**: Guide for AI assistants working with this Python application framework

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Core Architecture](#core-architecture)
4. [Key Files and Components](#key-files-and-components)
5. [Development Workflows](#development-workflows)
6. [Configuration System](#configuration-system)
7. [Logging Strategy](#logging-strategy)
8. [Service Integration Patterns](#service-integration-patterns)
9. [Git Workflow](#git-workflow)
10. [Testing Strategy](#testing-strategy)
11. [Code Conventions](#code-conventions)
12. [Common Patterns](#common-patterns)
13. [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## 🎯 Project Overview

**JK-Boilerplate** is a production-ready Python application framework designed as a reusable template for building scalable CLI-based applications. It supports both **long-running services** (apps) and **one-off batch jobs**.

### Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **CLI Framework** | Typer | 0.9.0+ | Command-line interface with type hints |
| **Configuration** | Pydantic Settings | 2.0.0+ | Type-safe environment variable management |
| **Logging** | Loguru | 0.7.0+ | Structured, colorful logging |
| **HTTP Client** | HTTPX | 0.25.0+ | Modern async HTTP client |
| **Database** | Supabase | 2.0.0+ | PostgreSQL with realtime capabilities |
| **Notifications** | python-telegram-bot | 20.0+ | Telegram bot integration |
| **Package Manager** | uv | latest | Ultra-fast Python dependency manager |
| **Linting/Formatting** | Ruff | 0.1.0+ | Fast Python linter and formatter |
| **Testing** | Pytest | 7.0.0+ | Testing framework |

### Python Version

- **Required**: Python 3.9+
- **Target**: Python 3.9 (Ruff configuration)

### Key Features

- **Unified CLI**: Two entry points (`app`, `batch`) for different workload types
- **Type-Safe Configuration**: Pydantic models with `.env` support
- **Structured Logging**: Console + daily-rotated file logging with emoji prefixes
- **Lifecycle Management**: Automatic event tracking to Supabase and Telegram notifications
- **Modular Design**: Clear separation between core logic, utilities, and services
- **Production-Ready**: Built-in error handling, graceful degradation, and observability

---

## 📁 Repository Structure

```
/home/user/JK-Boilerplate/
├── app/                          # Main application package
│   ├── core/                     # Business logic implementations
│   │   ├── app.py               # Base class for long-running apps
│   │   └── batch.py             # Base class for batch jobs
│   ├── utils/                    # Shared utilities and services
│   │   ├── config.py            # Pydantic configuration management
│   │   ├── logger.py            # Loguru logging setup
│   │   ├── supabase.py          # Supabase service wrapper
│   │   └── telegram.py          # Telegram bot service wrapper
│   └── main.py                   # CLI entry point and routing
├── docs/                         # Documentation
│   └── framework_guide.md       # Comprehensive framework guide (500+ lines)
├── scripts/                      # Standalone utility scripts
│   └── README.md                # Scripts documentation
├── tests/                        # Test suite
│   └── test_basic.py            # Basic configuration and import tests
├── pyproject.toml               # Project metadata, dependencies, and tool configs
├── uv.lock                      # Dependency lock file (1,579 lines)
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore patterns
└── README.md                    # Quick start guide
```

### Important Notes

- **No `__init__.py` files**: This project uses explicit imports instead of package initialization files
- **Logs directory**: Created at runtime (`logs/`) - not tracked in git
- **Config files**: `config/*.yaml` files are gitignored (environment-specific)

---

## 🏗 Core Architecture

### Design Principles

1. **Separation of Concerns**
   - **Core Logic** (`app/core/`): Business logic, isolated from infrastructure
   - **Utils** (`app/utils/`): Cross-cutting concerns (logging, config, services)
   - **Entry Points** (`app/main.py`): CLI routing and orchestration

2. **Dependency Injection**
   - Global singleton instances for services (config, logger, supabase, telegram)
   - Import where needed for explicit dependencies
   - Graceful degradation when optional services are unavailable

3. **Type Safety**
   - Extensive use of Python type hints
   - Pydantic models for runtime validation
   - No mypy configuration (relies on Pydantic for runtime checks)

4. **Lifecycle Management**
   - Consistent start/stop/error event tracking
   - Automatic notifications via Telegram
   - Supabase event logging for observability

### Architectural Layers

```
┌─────────────────────────────────────┐
│   CLI Entry Points (main.py)       │  ← User interaction
├─────────────────────────────────────┤
│   Core Business Logic (core/)      │  ← App-specific logic
├─────────────────────────────────────┤
│   Utilities & Services (utils/)    │  ← Shared infrastructure
├─────────────────────────────────────┤
│   External Services                │  ← Supabase, Telegram, etc.
└─────────────────────────────────────┘
```

---

## 🔑 Key Files and Components

### 1. CLI Entry Point: `app/main.py`

**Location**: `app/main.py`

**Purpose**: Routes CLI commands to appropriate core modules

**Key Functions**:

```python
def run_app(app_name: str, env: str):
    """Start a long-running application"""
    # Updates config, sets up file logging
    # Routes to appropriate app class based on app_name

def run_batch(batch_name: str, env: str):
    """Run a batch job"""
    # Updates config, sets up file logging
    # Routes to appropriate batch class based on batch_name

def app_entry():
    """Entry point for 'app' command in pyproject.toml"""

def batch_entry():
    """Entry point for 'batch' command in pyproject.toml"""
```

**Routing Pattern**:

```python
# In run_app() or run_batch()
if app_name == "my-app":
    from app.core.app import App
    app_instance = App()
    app_instance.run()
else:
    logger.warning(f"Unknown app: {app_name}")
```

**When to Modify**:
- Adding a new app or batch job (add new `if` clause)
- Changing CLI argument structure

**Line References**:
- `run_app()`: app/main.py:5-28
- `run_batch()`: app/main.py:30-53
- Entry points: app/main.py:56-60

---

### 2. Configuration: `app/utils/config.py`

**Location**: `app/utils/config.py`

**Purpose**: Type-safe configuration management using Pydantic

**Structure**:

```python
class SupabaseConfig(BaseSettings):
    url: Optional[str] = Field(None, alias="SUPABASE_URL")
    key: Optional[str] = Field(None, alias="SUPABASE_KEY")

class TelegramConfig(BaseSettings):
    token: Optional[str] = Field(None, alias="TELEGRAM_TOKEN")
    chat_id: Optional[str] = Field(None, alias="TELEGRAM_CHAT_ID")

class AppConfig(BaseSettings):
    env: str = "dev"
    name: str = "jk-boilerplate"
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    # Nested configurations
    supabase: SupabaseConfig = Field(default_factory=SupabaseConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)

    # Generic API configs (for dynamic services)
    api_configs: Dict[str, Any] = Field(default_factory=dict)

# Global singleton instance
config = AppConfig()
```

**Configuration Priority** (highest to lowest):
1. Runtime assignment (e.g., `config.name = app_name`)
2. Environment variables (OS-level)
3. `.env` file
4. Default values in model

**Usage Pattern**:

```python
from app.utils.config import config

# Access configuration
print(f"Environment: {config.env}")
print(f"Log level: {config.log_level}")

# Access nested config
if config.supabase.url:
    # Supabase is configured
    pass

# Runtime modification (CLI sets these)
config.name = "my-app"
config.env = "prod"
```

**When to Modify**:
- Adding new configuration fields (add to appropriate Config class)
- Adding new service integrations (create new nested config class)

---

### 3. Logging: `app/utils/logger.py`

**Location**: `app/utils/logger.py`

**Purpose**: Configures Loguru for console and file logging

**Key Functions**:

```python
def setup_logger():
    """Configure console logging with colors and formatting"""
    # Removes default handler, adds custom console handler

def configure_file_logging(app_name: str):
    """Add daily-rotated file logging"""
    # Creates logs/{app_name}_{YYYYMMDD}.log
    # Rotates at midnight, keeps 30 days
```

**Console Format**:
```
<green>2025-11-26 10:30:45</green> | <level>INFO    </level> | <cyan>app.core.app</cyan>:<cyan>run</cyan>:<cyan>23</cyan> - <level>Starting app</level>
```

**File Format**:
```
2025-11-26 10:30:45 | INFO     | app.core.app:run:23 - Starting app
```

**Logging Configuration**:
- **Rotation**: Daily at midnight (00:00)
- **Retention**: 30 days
- **File Pattern**: `logs/{app_name}_{YYYYMMDD}.log`
- **Level**: Controlled by `LOG_LEVEL` env var (default: INFO)

**Usage Pattern**:

```python
from app.utils.logger import logger

logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)  # Include exception traceback
logger.critical("Critical failure")

# Emoji prefixes for key events (convention, not enforced)
logger.info("🚀 App Started")
logger.info("🏁 App Stopped")
logger.error("🚨 Error occurred")
logger.info("✅ Success")
logger.info("📈 Trading signal")
logger.info("🔄 Processing batch")
```

**When to Modify**:
- Changing log format or rotation schedule
- Adding custom log handlers (e.g., remote logging)

---

### 4. Core App Class: `app/core/app.py`

**Location**: `app/core/app.py`

**Purpose**: Base class/example for long-running applications

**Structure**:

```python
class App:
    def __init__(self):
        # Load configuration
        self.stop_loss = config.api_configs.get("app.stop_loss", 2.0)
        self.take_profit = config.api_configs.get("app.take_profit", 5.0)

    def run(self):
        """Main application lifecycle"""
        logger.info("📈 Starting App")

        # 1. Log start event
        supabase.insert_event("start", {"type": "app"})
        telegram.send_sync("🚀 App Started")

        try:
            self._validate_config()
            # Main application logic here
            logger.info("🎯 App execution finished")

        except Exception as e:
            # 2. Handle errors
            logger.error(f"App Error: {e}")
            telegram.send_sync(f"🚨 App Failed: {e}")
            supabase.insert_event("abnormal_stop", {"error": str(e)})
            raise

        finally:
            # 3. Log stop event (always runs)
            supabase.insert_event("stop", {"type": "app"})
            telegram.send_sync("🏁 App Stopped")

    def _validate_config(self):
        """Validate configuration before running"""
        pass
```

**Lifecycle Pattern**:
1. **Start**: Log to Supabase + Telegram notification
2. **Execute**: Run business logic (should be in try block)
3. **Error Handling**: Log errors, send alerts, mark as abnormal stop
4. **Stop**: Always log completion (in finally block)

**When to Modify**:
- Creating new app types (create new class in `app/core/`)
- Extending base functionality (inherit from App class)

---

### 5. Core Batch Class: `app/core/batch.py`

**Location**: `app/core/batch.py`

**Purpose**: Base class/example for batch jobs

**Structure**:

```python
class BatchJob:
    def __init__(self):
        self.batch_size = config.api_configs.get("batch.size", 50)

    def run(self):
        """Main batch job lifecycle"""
        logger.info("🔄 Starting Sample Batch Job")

        supabase.insert_event("start", {"type": "batch", "batch_size": self.batch_size})

        try:
            # Process items
            items = range(1, 11)
            processed_count = 0

            for item in items:
                self._process_item(item)
                processed_count += 1

            # Log success with metrics
            logger.info(f"✅ Batch Job Completed Successfully - Processed {processed_count} items")
            telegram.send_sync(f"✅ Sample Batch Job Completed ({processed_count} items)")
            supabase.insert_event("stop", {"type": "batch", "items_processed": processed_count})

        except Exception as e:
            logger.error(f"Batch Job Error: {e}", exc_info=True)
            telegram.send_sync(f"🚨 Batch Job Failed: {e}")
            supabase.insert_event("abnormal_stop", {"type": "batch", "error": str(e)})
            raise

    def _process_item(self, item):
        """Process a single item. Override in subclasses."""
        logger.debug(f"Processing item {item}...")
```

**Key Differences from App**:
- Finite execution (processes items and exits)
- Tracks metrics (processed_count)
- Uses `exc_info=True` for detailed error logging

**When to Modify**:
- Creating new batch job types (create new class in `app/core/`)
- Implementing specific processing logic (override `_process_item()`)

---

### 6. Supabase Service: `app/utils/supabase.py`

**Location**: `app/utils/supabase.py`

**Purpose**: Wrapper for Supabase database operations

**Structure**:

```python
class SupabaseService:
    def __init__(self):
        self.client: Client = None
        if config.supabase.url and config.supabase.key:
            try:
                self.client = create_client(config.supabase.url, config.supabase.key)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase: {e}")
        else:
            logger.warning("Supabase credentials not found. Skipping initialization.")

    def insert_event(self, event_type: str, payload: dict):
        """Insert lifecycle event to app_events table"""
        if not self.client:
            return  # Graceful degradation

        try:
            data = {
                "app_name": config.name,
                "env": config.env,
                "event_type": event_type,
                "payload": payload
            }
            self.client.table("app_events").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to insert event to Supabase: {e}")

# Global singleton
supabase = SupabaseService()
```

**Graceful Degradation**:
- If credentials are missing, service initializes but does nothing
- All methods check `if not self.client:` before operations
- Errors are logged but don't crash the application

**Expected Database Schema**:

```sql
create table public.app_events (
  id bigint generated by default as identity primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  app_name text not null,
  env text not null,
  event_type text not null,
  payload jsonb default '{}'::jsonb
);
```

**Usage Pattern**:

```python
from app.utils.supabase import supabase

# Insert lifecycle events
supabase.insert_event("start", {"type": "app"})
supabase.insert_event("stop", {"type": "app"})
supabase.insert_event("abnormal_stop", {"error": "Connection failed"})

# Custom events
supabase.insert_event("trade_executed", {
    "symbol": "BTC/USD",
    "amount": 0.1,
    "price": 50000
})
```

**When to Modify**:
- Adding new database operations (add methods to SupabaseService)
- Extending event tracking (modify insert_event or add new methods)

---

### 7. Telegram Service: `app/utils/telegram.py`

**Location**: `app/utils/telegram.py`

**Purpose**: Wrapper for Telegram bot notifications

**Structure**:

```python
class TelegramService:
    def __init__(self):
        self.bot = None
        self.chat_id = config.telegram.chat_id
        if config.telegram.token:
            self.bot = Bot(token=config.telegram.token)
            logger.info("Telegram bot initialized")
        else:
            logger.warning("Telegram token not found. Skipping initialization.")

    async def send_message(self, message: str):
        """Async message sending"""
        if not self.bot or not self.chat_id:
            return
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    def send_sync(self, message: str):
        """Synchronous wrapper for send_message"""
        if not self.bot:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in async context - create task
                loop.create_task(self.send_message(message))
            else:
                # Sync context - run until complete
                loop.run_until_complete(self.send_message(message))
        except RuntimeError:
            # No event loop exists - create new one
            asyncio.run(self.send_message(message))
        except Exception as e:
            logger.error(f"Failed to send sync Telegram message: {e}")

# Global singleton
telegram = TelegramService()
```

**Two Message Methods**:
- `send_message()`: Async method for use in async code
- `send_sync()`: Sync wrapper for use in sync code (most common)

**Usage Pattern**:

```python
from app.utils.telegram import telegram

# Synchronous code (most common in apps/batches)
telegram.send_sync("🚀 App Started")
telegram.send_sync(f"✅ Processed {count} items")
telegram.send_sync(f"🚨 Error: {error_message}")

# Async code (if your app is async)
await telegram.send_message("Message from async context")
```

**Emoji Convention** (not enforced, but recommended):
- 🚀 App/batch started
- 🏁 App/batch stopped normally
- 🚨 Error/failure
- ✅ Success/completion
- 📈 Trading/market signal
- 🔄 Processing/in progress
- 💰 Financial transaction

**When to Modify**:
- Adding rich message formatting (markdown, buttons)
- Adding file/image sending capabilities
- Supporting multiple chat IDs

---

## 🔧 Development Workflows

### Adding a New Application

1. **Create App Class** in `app/core/`:

```python
# app/core/my_new_app.py
from app.utils.logger import logger
from app.utils.config import config
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class MyNewApp:
    def __init__(self):
        # Load any app-specific configuration
        self.setting = config.api_configs.get("my_app.setting", "default")

    def run(self):
        logger.info("🚀 Starting My New App")
        supabase.insert_event("start", {"type": "my_new_app"})
        telegram.send_sync("🚀 My New App Started")

        try:
            # Your business logic here
            self._do_work()

            logger.info("✅ My New App completed successfully")

        except Exception as e:
            logger.error(f"My New App Error: {e}", exc_info=True)
            telegram.send_sync(f"🚨 My New App Failed: {e}")
            supabase.insert_event("abnormal_stop", {"error": str(e)})
            raise

        finally:
            supabase.insert_event("stop", {"type": "my_new_app"})
            telegram.send_sync("🏁 My New App Stopped")

    def _do_work(self):
        """Implement your business logic"""
        pass
```

2. **Register in CLI** (`app/main.py`):

```python
def run_app(app_name: str, env: str):
    # ... existing code ...

    if app_name == "my-app":
        from app.core.app import App
        app_instance = App()
        app_instance.run()
    elif app_name == "my-new-app":  # ADD THIS
        from app.core.my_new_app import MyNewApp
        app_instance = MyNewApp()
        app_instance.run()
    else:
        logger.warning(f"Unknown app: {app_name}")
```

3. **Run**:

```bash
uv run app my-new-app --env dev
```

---

### Adding a New Batch Job

1. **Create Batch Class** in `app/core/`:

```python
# app/core/data_processor.py
from app.utils.logger import logger
from app.utils.config import config
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class DataProcessor:
    def __init__(self):
        self.batch_size = config.api_configs.get("data_processor.batch_size", 100)

    def run(self):
        logger.info("🔄 Starting Data Processor Batch")
        supabase.insert_event("start", {"type": "data_processor", "batch_size": self.batch_size})

        try:
            # Fetch items to process
            items = self._fetch_items()
            processed = 0
            failed = 0

            for item in items:
                try:
                    self._process_item(item)
                    processed += 1
                except Exception as e:
                    logger.error(f"Failed to process item {item}: {e}")
                    failed += 1

            # Report results
            logger.info(f"✅ Batch completed: {processed} processed, {failed} failed")
            telegram.send_sync(f"✅ Data Processor: {processed}/{len(items)} succeeded")
            supabase.insert_event("stop", {
                "type": "data_processor",
                "processed": processed,
                "failed": failed
            })

        except Exception as e:
            logger.error(f"Batch Error: {e}", exc_info=True)
            telegram.send_sync(f"🚨 Data Processor Failed: {e}")
            supabase.insert_event("abnormal_stop", {"error": str(e)})
            raise

    def _fetch_items(self):
        """Fetch items to process"""
        return []

    def _process_item(self, item):
        """Process a single item"""
        pass
```

2. **Register in CLI** (`app/main.py`):

```python
def run_batch(batch_name: str, env: str):
    # ... existing code ...

    if batch_name == "my-batch":
        from app.core.batch import BatchJob
        batch_instance = BatchJob()
        batch_instance.run()
    elif batch_name == "data-processor":  # ADD THIS
        from app.core.data_processor import DataProcessor
        batch_instance = DataProcessor()
        batch_instance.run()
    else:
        logger.warning(f"Unknown batch: {batch_name}")
```

3. **Run**:

```bash
uv run batch data-processor --env dev
```

---

### Adding Dependencies

1. **Install package**:

```bash
uv pip install <package_name>
```

2. **Update `pyproject.toml`** manually:

```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "new-package>=1.0.0",
]
```

3. **Lock dependencies**:

```bash
uv lock
```

---

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_basic.py

# Run with coverage (if configured)
uv run pytest --cov=app
```

**Writing Tests**:

```python
# tests/test_my_feature.py
from app.utils.config import config

def test_my_feature():
    """Test description"""
    # Arrange
    expected = "value"

    # Act
    actual = some_function()

    # Assert
    assert actual == expected

def test_config_loading():
    """Test that config loads correctly"""
    assert config.env in ["dev", "prod"]
    assert config.name != ""
```

---

### Code Formatting and Linting

```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .
```

**Ruff Configuration** (from `pyproject.toml`):
- Line length: 88 characters
- Quote style: double quotes
- Rules: pycodestyle (E), Pyflakes (F), isort (I)

---

## ⚙️ Configuration System

### Environment Variables

Configuration is loaded from `.env` file and environment variables using Pydantic Settings.

**Priority** (highest to lowest):
1. Runtime assignment (e.g., `config.name = "my-app"` in code)
2. OS environment variables
3. `.env` file
4. Default values in Pydantic models

### .env File Structure

```ini
# Application Settings
LOG_LEVEL=INFO

# Telegram Notifications (optional)
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789

# Supabase Database (optional)
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Custom API Configs (app-specific, not used by framework)
# These are loaded into config.api_configs dict
```

### Accessing Configuration

```python
from app.utils.config import config

# Basic config
print(config.env)          # "dev" or "prod"
print(config.name)         # "my-app"
print(config.log_level)    # "INFO"

# Service configs
if config.supabase.url:
    print(f"Supabase URL: {config.supabase.url}")

if config.telegram.token:
    print(f"Telegram configured: {config.telegram.chat_id}")

# Generic API configs (for app-specific settings)
stop_loss = config.api_configs.get("trading.stop_loss", 2.0)
api_key = config.api_configs.get("external_api.key")
```

### Adding New Configuration Fields

1. **Add to config model** (`app/utils/config.py`):

```python
class AppConfig(BaseSettings):
    # ... existing fields ...

    # Add new field
    max_retries: int = Field(3, alias="MAX_RETRIES")
    timeout: float = Field(30.0, alias="TIMEOUT")
```

2. **Add to `.env.example`**:

```ini
# Add documentation for new fields
MAX_RETRIES=3
TIMEOUT=30.0
```

3. **Use in code**:

```python
from app.utils.config import config

retries = config.max_retries
timeout = config.timeout
```

---

## 📝 Logging Strategy

### Log Levels

- **DEBUG**: Detailed debugging information (not shown by default)
- **INFO**: General informational messages (default level)
- **WARNING**: Warning messages (potential issues)
- **ERROR**: Error messages (failures that don't stop execution)
- **CRITICAL**: Critical failures (system-level issues)

### Logging Patterns

```python
from app.utils.logger import logger

# Standard logging
logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")

# Error logging with exception info
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)

# Structured logging with context
logger.info(f"Processing item {item_id}: {item_name}")
logger.info(f"Batch completed: {processed} processed, {failed} failed")

# Emoji prefixes for key events (recommended convention)
logger.info("🚀 App Started")
logger.info("🏁 App Stopped")
logger.error("🚨 Error occurred")
logger.info("✅ Success")
```

### Log Files

- **Location**: `logs/` directory (created at runtime)
- **Naming**: `{app_name}_{YYYYMMDD}.log`
- **Rotation**: Daily at midnight (00:00)
- **Retention**: 30 days
- **Format**: Plain text without colors

**Example log files**:
```
logs/my-app_20251126.log
logs/my-batch_20251126.log
logs/data-processor_20251125.log
```

### Changing Log Level

1. **Via environment variable**:

```bash
# .env
LOG_LEVEL=DEBUG
```

2. **Via command line**:

```bash
LOG_LEVEL=DEBUG uv run app my-app --env dev
```

3. **At runtime** (not recommended):

```python
from loguru import logger

logger.remove()  # Remove all handlers
logger.add(sys.stderr, level="DEBUG")
```

---

## 🔌 Service Integration Patterns

### Graceful Degradation

All services are designed to gracefully degrade if credentials are missing:

```python
# Services initialize but do nothing if unconfigured
supabase.insert_event("start", {...})  # No-op if credentials missing
telegram.send_sync("Started")           # No-op if token missing
```

### Service Initialization

Services are initialized as global singletons at import time:

```python
# app/utils/supabase.py
supabase = SupabaseService()  # Initialized once

# app/utils/telegram.py
telegram = TelegramService()  # Initialized once
```

**Initialization Flow**:
1. Check if credentials exist in config
2. If yes, create client and log success
3. If no, log warning and set client to None
4. All methods check for None before operations

### Adding New Services

1. **Create service module** (`app/utils/my_service.py`):

```python
from app.utils.config import config
from app.utils.logger import logger

class MyServiceConfig(BaseSettings):
    api_key: Optional[str] = Field(None, alias="MY_SERVICE_API_KEY")
    endpoint: str = Field("https://api.example.com", alias="MY_SERVICE_ENDPOINT")

class MyService:
    def __init__(self):
        self.client = None
        if config.my_service.api_key:
            try:
                # Initialize client
                self.client = create_client(config.my_service.api_key)
                logger.info("MyService initialized")
            except Exception as e:
                logger.error(f"Failed to initialize MyService: {e}")
        else:
            logger.warning("MyService API key not found. Skipping initialization.")

    def do_something(self, data):
        """Perform service operation"""
        if not self.client:
            return  # Graceful degradation

        try:
            result = self.client.api_call(data)
            return result
        except Exception as e:
            logger.error(f"MyService operation failed: {e}")
            return None

# Global singleton
my_service = MyService()
```

2. **Add config to AppConfig** (`app/utils/config.py`):

```python
class AppConfig(BaseSettings):
    # ... existing fields ...
    my_service: MyServiceConfig = Field(default_factory=MyServiceConfig)
```

3. **Add to `.env.example`**:

```ini
# MyService Configuration (optional)
MY_SERVICE_API_KEY=your_api_key_here
MY_SERVICE_ENDPOINT=https://api.example.com
```

4. **Use in apps/batches**:

```python
from app.utils.my_service import my_service

class MyApp:
    def run(self):
        result = my_service.do_something({"data": "value"})
        if result:
            logger.info(f"Service returned: {result}")
```

---

## 🌳 Git Workflow

### Two-Remote Strategy

This project uses a two-remote strategy for managing boilerplate updates:

- **`upstream`**: Original boilerplate repository (read-mostly)
- **`origin`**: Your application repository (read/write)

### Initial Setup

```bash
# 1. Clone boilerplate
git clone https://github.com/taein2301/jk-boilerplate.git my-awesome-app
cd my-awesome-app

# 2. Rename origin to upstream
git remote rename origin upstream

# 3. Add your app repository as origin
git remote add origin https://github.com/my-account/my-awesome-app.git

# 4. Verify
git remote -v
# origin   https://github.com/my-account/my-awesome-app.git (fetch/push)
# upstream https://github.com/taein2301/jk-boilerplate.git (fetch/push)
```

### Syncing Boilerplate Updates

```bash
# 1. Fetch upstream changes
git fetch upstream

# 2. Merge into your branch
git merge upstream/main

# 3. Resolve conflicts if any
# Edit conflicted files, then:
git add .
git commit -m "Merge upstream updates"

# 4. Push to your repo
git push origin main
```

### Contributing Fixes Back to Boilerplate

**Method A: Using Git Worktree (Recommended)**

```bash
# 1. Create isolated worktree
git worktree add ../boilerplate-fix upstream/main

# 2. Work in isolated directory
cd ../boilerplate-fix

# 3. Make fixes (only framework code, no app-specific code)
# Edit files...
git commit -am "Fix: critical bug in utils"

# 4. Push to upstream
git push upstream HEAD:main

# 5. Return to main project and cleanup
cd ../my-awesome-app
git worktree remove ../boilerplate-fix
```

**Method B: Using Branches**

```bash
# 1. Create fix branch from upstream
git checkout -b fix/core-bug upstream/main

# 2. Make fixes
# Edit files...
git commit -am "Fix: critical bug in utils"

# 3. Push to upstream
git push upstream HEAD:main

# 4. Return to main branch
git checkout main
```

### Important Git Commands

| Command | Description |
|---------|-------------|
| `git remote rename origin upstream` | Rename original remote to upstream |
| `git remote add origin <URL>` | Add your app repo as origin |
| `git fetch upstream` | Fetch updates from boilerplate |
| `git merge upstream/main` | Merge boilerplate updates |
| `git push origin main` | Push your app code |
| `git push upstream main` | Push framework fixes (careful!) |

---

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── test_basic.py          # Basic sanity checks
├── test_config.py         # Configuration tests
├── test_services.py       # Service integration tests
└── test_apps.py           # App/batch logic tests
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific file
uv run pytest tests/test_basic.py

# Run specific test
uv run pytest tests/test_basic.py::test_config_defaults

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

### Writing Tests

**Basic Test**:

```python
# tests/test_my_feature.py

def test_simple_assertion():
    """Test basic functionality"""
    result = 2 + 2
    assert result == 4
```

**Config Test**:

```python
from app.utils.config import config

def test_config_defaults():
    """Test default configuration values"""
    assert config.env == "dev"
    assert config.name == "jk-boilerplate"
    assert config.log_level == "INFO"
```

**Import Test**:

```python
def test_app_import():
    """Test that modules can be imported"""
    from app.main import run_app
    from app.core.app import App
    from app.core.batch import BatchJob

    assert callable(run_app)
    assert App is not None
    assert BatchJob is not None
```

**Service Test** (with mocking):

```python
from unittest.mock import Mock, patch
from app.utils.supabase import SupabaseService

def test_supabase_insert_event():
    """Test Supabase event insertion"""
    with patch('app.utils.supabase.create_client') as mock_create:
        # Setup mock
        mock_client = Mock()
        mock_create.return_value = mock_client

        # Test
        service = SupabaseService()
        service.insert_event("test", {"data": "value"})

        # Verify
        mock_client.table.assert_called_once_with("app_events")
```

### Test Conventions

- Test files start with `test_`
- Test functions start with `test_`
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Add docstrings to complex tests
- Group related tests in classes (optional)

---

## 📐 Code Conventions

### Python Style

- **Line length**: 88 characters (Black default)
- **Quote style**: Double quotes (`"string"`)
- **Indentation**: 4 spaces
- **Import order**: Standard library → Third-party → Local (enforced by isort/Ruff)

### Import Organization

```python
# Standard library
import asyncio
import sys
from typing import Optional, Dict, Any

# Third-party packages
from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings

# Local imports
from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
```

### Naming Conventions

- **Modules**: `snake_case` (e.g., `my_service.py`)
- **Classes**: `PascalCase` (e.g., `MyService`, `DataProcessor`)
- **Functions**: `snake_case` (e.g., `run_app`, `insert_event`)
- **Variables**: `snake_case` (e.g., `processed_count`, `api_key`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private methods**: `_snake_case` (e.g., `_process_item`, `_validate_config`)

### Type Hints

Use type hints for function signatures:

```python
def process_items(items: list[str], batch_size: int = 10) -> dict[str, int]:
    """Process items in batches"""
    processed = 0
    failed = 0

    # ... processing ...

    return {"processed": processed, "failed": failed}
```

### Docstrings

Use docstrings for public functions and classes:

```python
def run_batch(batch_name: str, env: str):
    """
    Run a batch job.

    Args:
        batch_name: Name of the batch to run (e.g., "my-batch")
        env: Environment to run in ("dev" or "prod")
    """
    # Implementation...
```

### Error Handling

```python
# DO: Catch specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")

# DON'T: Catch all exceptions silently
try:
    risky_operation()
except:
    pass  # Bad: Suppresses all errors

# DO: Include exception info for debugging
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise  # Re-raise for proper error handling
```

---

## 🎨 Common Patterns

### Lifecycle Management Pattern

All apps and batches should follow this pattern:

```python
def run(self):
    logger.info("🚀 Starting {Name}")
    supabase.insert_event("start", {"type": "..."})
    telegram.send_sync("🚀 {Name} Started")

    try:
        # Business logic here
        self._do_work()

        logger.info("✅ {Name} completed successfully")

    except Exception as e:
        logger.error(f"{Name} Error: {e}", exc_info=True)
        telegram.send_sync(f"🚨 {Name} Failed: {e}")
        supabase.insert_event("abnormal_stop", {"error": str(e)})
        raise

    finally:
        supabase.insert_event("stop", {"type": "..."})
        telegram.send_sync("🏁 {Name} Stopped")
```

### Configuration Loading Pattern

```python
class MyApp:
    def __init__(self):
        # Load configuration with defaults
        self.setting1 = config.api_configs.get("my_app.setting1", "default")
        self.setting2 = config.api_configs.get("my_app.setting2", 100)

        # Validate configuration
        if self.setting2 < 0:
            raise ValueError("setting2 must be positive")
```

### Batch Processing Pattern

```python
def run(self):
    items = self._fetch_items()
    processed = 0
    failed = 0

    for item in items:
        try:
            self._process_item(item)
            processed += 1
        except Exception as e:
            logger.error(f"Failed to process {item}: {e}")
            failed += 1

    # Report metrics
    logger.info(f"Completed: {processed} processed, {failed} failed")
    telegram.send_sync(f"✅ Batch: {processed}/{len(items)} succeeded")
    supabase.insert_event("stop", {
        "processed": processed,
        "failed": failed,
        "total": len(items)
    })
```

### Service Singleton Pattern

```python
# app/utils/my_service.py

class MyService:
    def __init__(self):
        self.client = None
        if config.my_service.api_key:
            # Initialize
            self.client = create_client(config.my_service.api_key)
            logger.info("MyService initialized")
        else:
            logger.warning("MyService not configured")

    def operation(self, data):
        if not self.client:
            return  # Graceful degradation

        try:
            return self.client.call(data)
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            return None

# Global singleton
my_service = MyService()
```

---

## 🤖 AI Assistant Guidelines

### When Modifying Code

1. **Always Read First**: Never propose changes without reading the file first
2. **Preserve Patterns**: Follow existing patterns in the codebase
3. **Maintain Type Safety**: Use type hints for new functions
4. **Update Documentation**: Update this file if making architectural changes
5. **Test Changes**: Ensure changes don't break existing functionality

### Code Modification Checklist

- [ ] Read the file being modified
- [ ] Follow existing code style (Ruff formatting)
- [ ] Add type hints to new functions
- [ ] Include error handling (try/except)
- [ ] Add logging for important events
- [ ] Follow lifecycle pattern for apps/batches
- [ ] Update `.env.example` if adding config fields
- [ ] Update this CLAUDE.md if changing architecture

### Common Tasks

**Task: Add a new app**
1. Read `app/core/app.py` for pattern
2. Create new file in `app/core/`
3. Implement class with `run()` method
4. Read `app/main.py`
5. Add routing in `run_app()` function
6. Test: `uv run app <name> --env dev`

**Task: Add a new configuration field**
1. Read `app/utils/config.py`
2. Add field to appropriate Config class
3. Read `.env.example`
4. Add example value to `.env.example`
5. Use `config.<field>` in code

**Task: Add a new service integration**
1. Read `app/utils/supabase.py` or `telegram.py` for pattern
2. Create new file in `app/utils/`
3. Create Config class for service
4. Create Service class with graceful degradation
5. Create global singleton instance
6. Add to `AppConfig` in `config.py`
7. Add to `.env.example`

**Task: Debug an issue**
1. Check logs in `logs/` directory
2. Verify configuration in `.env` file
3. Check service initialization messages
4. Review error messages for exception traceback
5. Test with `LOG_LEVEL=DEBUG` for detailed output

### File-Specific Guidelines

**`app/main.py`**:
- Only modify for adding new apps/batches
- Don't add business logic here (belongs in `app/core/`)
- Keep routing simple (if/elif/else)

**`app/core/*.py`**:
- All classes should have a `run()` method
- Follow lifecycle pattern (start/try/except/finally)
- Log important events with emoji prefixes
- Include error handling

**`app/utils/*.py`**:
- Utility modules should be stateless or singleton services
- Include graceful degradation for optional services
- Log initialization status
- Handle errors without crashing

**`pyproject.toml`**:
- Maintain version pins for stability
- Update dependencies carefully (test after changes)
- Keep tool configurations organized

**`tests/*.py`**:
- Test files should mirror source structure
- Use descriptive test names
- Include docstrings for complex tests

### Error Handling Guidelines

**DO**:
```python
try:
    result = risky_operation()
    logger.info(f"Operation succeeded: {result}")
except SpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    telegram.send_sync(f"🚨 Error: {e}")
    supabase.insert_event("error", {"error": str(e)})
    raise  # Re-raise for proper error handling
```

**DON'T**:
```python
try:
    risky_operation()
except:
    pass  # Silently suppresses all errors

try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")  # Use logger, not print
```

### Logging Guidelines

**DO**:
```python
# Use appropriate log levels
logger.debug("Detailed debugging info")
logger.info("Important events")
logger.warning("Potential issues")
logger.error("Errors with context", exc_info=True)

# Use emoji prefixes for key events
logger.info("🚀 App Started")
logger.info("✅ Success")
logger.error("🚨 Error occurred")

# Include context
logger.info(f"Processing item {item_id}: {item_name}")
```

**DON'T**:
```python
# Don't use print()
print("Log message")  # Use logger.info() instead

# Don't log sensitive data
logger.info(f"API Key: {api_key}")  # Security issue

# Don't log at wrong level
logger.error("Processing item...")  # Should be info
logger.info("Fatal error occurred")  # Should be error
```

### Configuration Guidelines

**DO**:
```python
# Use config for all settings
timeout = config.api_configs.get("service.timeout", 30)

# Provide defaults
batch_size = config.api_configs.get("batch.size", 100)

# Validate configuration
if batch_size < 1:
    raise ValueError("batch_size must be positive")
```

**DON'T**:
```python
# Don't hardcode values
timeout = 30  # Should be configurable

# Don't access environment directly
import os
api_key = os.getenv("API_KEY")  # Use config instead
```

### Service Integration Guidelines

**DO**:
```python
# Check if service is available
if supabase.client:
    supabase.insert_event("start", {})

# Graceful degradation
def send_notification(msg):
    if not self.client:
        return  # No-op if not configured
    # ... send notification
```

**DON'T**:
```python
# Don't fail if service unavailable
supabase.insert_event("start", {})  # Will crash if not configured

# Don't assume services are configured
telegram.bot.send_message(...)  # Might be None
```

---

## 📚 Additional Resources

### Internal Documentation

- **Framework Guide**: `docs/framework_guide.md` - Comprehensive 500+ line guide (Korean)
- **README**: `README.md` - Quick start guide (Korean)
- **Scripts README**: `scripts/README.md` - Standalone scripts documentation

### External Resources

- **Typer**: https://typer.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Loguru**: https://loguru.readthedocs.io/
- **Supabase**: https://supabase.com/docs
- **python-telegram-bot**: https://docs.python-telegram-bot.org/
- **uv**: https://github.com/astral-sh/uv
- **Ruff**: https://docs.astral.sh/ruff/

---

## 🔄 Maintenance

### Keeping This File Updated

When making significant changes to the codebase, update relevant sections:

- **Architecture changes**: Update "Core Architecture" section
- **New patterns**: Add to "Common Patterns" section
- **New services**: Update "Service Integration Patterns" section
- **Configuration changes**: Update "Configuration System" section
- **New workflows**: Update "Development Workflows" section

### Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-26 | 1.0.0 | Initial comprehensive CLAUDE.md created |

---

## 📞 Getting Help

### For Human Developers

1. Read `docs/framework_guide.md` for detailed framework documentation
2. Check `README.md` for quick start instructions
3. Review existing code in `app/core/` for examples
4. Check logs in `logs/` directory for runtime issues

### For AI Assistants

1. **Always read this file first** when working with the codebase
2. **Read target files** before making changes
3. **Follow existing patterns** shown in examples
4. **Ask clarifying questions** if requirements are unclear
5. **Reference line numbers** from this guide (e.g., "See app/main.py:5-28")

---

**End of CLAUDE.md**

*This file is maintained as a living document and should be updated with architectural changes.*
