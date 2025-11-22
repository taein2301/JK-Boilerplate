from app.utils.config import config

def test_config_defaults():
    """Test that default configuration values are set correctly."""
    assert config.env == "dev"
    assert config.name == "jk-boilerplate"
    assert config.log_level == "INFO"

def test_app_import():
    """Test that the app module can be imported."""
    from app.main import run_app
    assert callable(run_app)
