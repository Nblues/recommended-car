#!/usr/bin/env python3
"""
Configuration Management System
Handles API credentials, environment variables, and validation
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class APIConfig:
    """API Configuration with validation"""
    name: str
    url: str
    headers: Dict[str, str]
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    api_key: Optional[str] = None
    enabled: bool = True

@dataclass 
class ImageConfig:
    """Image processing configuration"""
    enable_webp: bool = True
    enable_cors_fallback: bool = True
    placeholder_url: str = "https://via.placeholder.com/300x200?text=Loading..."
    error_image_url: str = "https://via.placeholder.com/300x200?text=Error+Loading+Image"
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_formats: list = None
    cdn_domains: list = None

    def __post_init__(self):
        if self.allowed_formats is None:
            self.allowed_formats = ['jpg', 'jpeg', 'png', 'webp', 'avif']
        if self.cdn_domains is None:
            self.cdn_domains = ['cdn.shopify.com', 'images.unsplash.com']

@dataclass
class PerformanceConfig:
    """Performance and caching configuration"""
    enable_service_worker: bool = True
    cache_duration: int = 3600  # 1 hour
    enable_lazy_loading: bool = True
    enable_compression: bool = True
    auto_refresh_interval: int = 1800  # 30 minutes

@dataclass
class ErrorConfig:
    """Error handling configuration"""
    enable_error_logging: bool = True
    enable_error_tracking: bool = True
    error_log_file: str = "logs/errors.log"
    max_log_size: int = 10 * 1024 * 1024  # 10MB
    enable_graceful_degradation: bool = True

class ConfigManager:
    """Central configuration manager"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Create logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        self._load_environment_variables()
        self._setup_logging()
        
        # Load configurations
        self.api_configs = self._load_api_configs()
        self.image_config = self._load_image_config()
        self.performance_config = self._load_performance_config()
        self.error_config = self._load_error_config()

    def _setup_logging(self):
        """Setup comprehensive logging"""
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.logs_dir / 'app.log', encoding='utf-8')
            ]
        )

    def _load_environment_variables(self):
        """Load environment variables with defaults"""
        self.env = {
            'SHOPIFY_API_KEY': os.getenv('SHOPIFY_API_KEY', ''),
            'SHOPIFY_API_SECRET': os.getenv('SHOPIFY_API_SECRET', ''),
            'SHOPIFY_STORE_URL': os.getenv('SHOPIFY_STORE_URL', 'https://quickstart-f2f5a8c8.myshopify.com'),
            'CUSTOM_API_URL': os.getenv('CUSTOM_API_URL', ''),
            'CUSTOM_API_KEY': os.getenv('CUSTOM_API_KEY', ''),
            'API_TIMEOUT': int(os.getenv('API_TIMEOUT', '30')),
            'MAX_RETRIES': int(os.getenv('MAX_RETRIES', '3')),
            'CACHE_DURATION': int(os.getenv('CACHE_DURATION', '3600')),
            'DEBUG': os.getenv('DEBUG', 'false').lower() == 'true',
        }

    def _load_api_configs(self) -> Dict[str, APIConfig]:
        """Load API configurations"""
        configs = {}
        
        # Local API
        configs['local'] = APIConfig(
            name='local',
            url='cars.json',
            headers={},
            timeout=5,
            max_retries=1
        )
        
        # Shopify API with environment variables
        shopify_url = f"{self.env['SHOPIFY_STORE_URL']}/admin/api/2023-10/products.json"
        shopify_headers = {'Content-Type': 'application/json'}
        
        if self.env['SHOPIFY_API_KEY']:
            shopify_headers['X-Shopify-Access-Token'] = self.env['SHOPIFY_API_KEY']
        
        configs['shopify'] = APIConfig(
            name='shopify',
            url=shopify_url,
            headers=shopify_headers,
            timeout=self.env['API_TIMEOUT'],
            max_retries=self.env['MAX_RETRIES'],
            api_key=self.env['SHOPIFY_API_KEY']
        )
        
        # Custom API
        configs['custom'] = APIConfig(
            name='custom',
            url=self.env['CUSTOM_API_URL'] or 'https://api.example.com/cars',
            headers={
                'Authorization': f"Bearer {self.env['CUSTOM_API_KEY']}" if self.env['CUSTOM_API_KEY'] else 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            },
            timeout=self.env['API_TIMEOUT'],
            max_retries=self.env['MAX_RETRIES'],
            api_key=self.env['CUSTOM_API_KEY'],
            enabled=bool(self.env['CUSTOM_API_URL'])
        )
        
        return configs

    def _load_image_config(self) -> ImageConfig:
        """Load image configuration"""
        config_file = self.config_dir / 'image_config.json'
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return ImageConfig(**data)
            except Exception as e:
                logger.warning(f"Failed to load image config: {e}")
        
        # Return default config
        config = ImageConfig()
        self._save_config(config_file, asdict(config))
        return config

    def _load_performance_config(self) -> PerformanceConfig:
        """Load performance configuration"""
        config_file = self.config_dir / 'performance_config.json'
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return PerformanceConfig(**data)
            except Exception as e:
                logger.warning(f"Failed to load performance config: {e}")
        
        # Return default config
        config = PerformanceConfig()
        self._save_config(config_file, asdict(config))
        return config

    def _load_error_config(self) -> ErrorConfig:
        """Load error handling configuration"""
        config_file = self.config_dir / 'error_config.json'
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return ErrorConfig(**data)
            except Exception as e:
                logger.warning(f"Failed to load error config: {e}")
        
        # Return default config
        config = ErrorConfig()
        self._save_config(config_file, asdict(config))
        return config

    def _save_config(self, file_path: Path, config_data: dict):
        """Save configuration to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save config to {file_path}: {e}")

    def get_api_config(self, api_name: str) -> Optional[APIConfig]:
        """Get API configuration by name"""
        return self.api_configs.get(api_name)

    def validate_api_config(self, api_name: str) -> bool:
        """Validate API configuration"""
        config = self.get_api_config(api_name)
        if not config:
            logger.error(f"API config '{api_name}' not found")
            return False
        
        if not config.enabled:
            logger.warning(f"API '{api_name}' is disabled")
            return False
        
        if not config.url:
            logger.error(f"API '{api_name}' has no URL configured")
            return False
        
        # Check API key for APIs that require it
        if api_name in ['shopify', 'custom'] and not config.api_key:
            logger.warning(f"API '{api_name}' has no API key configured")
            # Don't return False here as some APIs might work without keys
        
        return True

    def get_cache_key(self, api_name: str, params: Dict = None) -> str:
        """Generate cache key for API requests"""
        key_data = f"{api_name}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def create_env_file_template(self):
        """Create .env template file"""
        env_template = """# Car Widget Configuration
# Copy this file to .env and fill in your values

# Shopify API Configuration
SHOPIFY_API_KEY=your_shopify_api_key_here
SHOPIFY_API_SECRET=your_shopify_secret_here
SHOPIFY_STORE_URL=https://your-store.myshopify.com

# Custom API Configuration
CUSTOM_API_URL=https://your-api.com/cars
CUSTOM_API_KEY=your_custom_api_key_here

# Performance Settings
API_TIMEOUT=30
MAX_RETRIES=3
CACHE_DURATION=3600

# Debug Mode
DEBUG=false

# Logging Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
"""
        env_file = Path('.env.template')
        env_file.write_text(env_template)
        logger.info(f"Created environment template: {env_file}")

# Global configuration instance
config_manager = ConfigManager()