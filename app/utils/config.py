from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

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
    
    # Generic API configs (for backward compatibility or dynamic services)
    api_configs: Dict[str, Any] = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

# Global config instance
config = AppConfig()
