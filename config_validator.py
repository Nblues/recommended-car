#!/usr/bin/env python3
"""
Configuration Validation System
Validates all configurations and provides setup guidance
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import asdict

from config_manager import config_manager
from error_handler import log_error

class ConfigValidator:
    """Validates all system configurations"""
    
    def __init__(self):
        self.validation_results = []
        self.warnings = []
        self.errors = []
        
    def validate_all(self) -> Dict[str, Any]:
        """Validate all configurations"""
        print("🔍 Starting comprehensive configuration validation...")
        
        results = {
            'environment': self._validate_environment(),
            'api_configs': self._validate_api_configs(),
            'image_config': self._validate_image_config(),
            'performance_config': self._validate_performance_config(),
            'error_config': self._validate_error_config(),
            'files_and_directories': self._validate_files_and_directories(),
            'summary': self._generate_summary()
        }
        
        return results
    
    def _validate_environment(self) -> Dict[str, Any]:
        """Validate environment variables and system setup"""
        print("📋 Validating environment configuration...")
        
        env_results = {
            'status': 'valid',
            'issues': [],
            'recommendations': []
        }
        
        # Check critical environment variables
        required_env_vars = [
            ('SHOPIFY_API_KEY', 'Shopify API access'),
            ('SHOPIFY_STORE_URL', 'Shopify store URL'),
        ]
        
        optional_env_vars = [
            ('CUSTOM_API_URL', 'Custom API endpoint'),
            ('CUSTOM_API_KEY', 'Custom API authentication'),
            ('LOG_LEVEL', 'Logging verbosity'),
            ('DEBUG', 'Debug mode'),
        ]
        
        for var_name, description in required_env_vars:
            value = config_manager.env.get(var_name)
            if not value or value == f'your_{var_name.lower()}_here':
                env_results['issues'].append(f"❌ Missing {var_name} ({description})")
                env_results['status'] = 'invalid'
        
        for var_name, description in optional_env_vars:
            value = config_manager.env.get(var_name)
            if not value:
                env_results['recommendations'].append(f"💡 Consider setting {var_name} ({description})")
        
        # Validate URLs
        for url_var in ['SHOPIFY_STORE_URL', 'CUSTOM_API_URL']:
            url = config_manager.env.get(url_var)
            if url and not self._is_valid_url(url):
                env_results['issues'].append(f"❌ Invalid URL format for {url_var}: {url}")
                env_results['status'] = 'invalid'
        
        return env_results
    
    def _validate_api_configs(self) -> Dict[str, Any]:
        """Validate API configurations"""
        print("🔗 Validating API configurations...")
        
        api_results = {
            'status': 'valid',
            'configs': {},
            'issues': []
        }
        
        for api_name, api_config in config_manager.api_configs.items():
            config_status = {
                'enabled': api_config.enabled,
                'url_valid': self._is_valid_url(api_config.url) if api_config.url else False,
                'has_auth': bool(api_config.api_key),
                'timeout_reasonable': 5 <= api_config.timeout <= 60,
                'retry_settings_ok': 1 <= api_config.max_retries <= 5,
                'issues': []
            }
            
            # Validate URL
            if not config_status['url_valid'] and api_name != 'local':
                config_status['issues'].append(f"Invalid URL: {api_config.url}")
            
            # Check timeout
            if not config_status['timeout_reasonable']:
                config_status['issues'].append(f"Timeout {api_config.timeout}s is not recommended (5-60s)")
            
            # Check retry settings
            if not config_status['retry_settings_ok']:
                config_status['issues'].append(f"Retry count {api_config.max_retries} is not recommended (1-5)")
            
            # API-specific validation
            if api_name == 'shopify' and not config_status['has_auth']:
                config_status['issues'].append("No API key configured for Shopify")
            
            if api_name == 'custom' and api_config.enabled and not config_status['has_auth']:
                config_status['issues'].append("No API key configured for custom API")
            
            # Overall config status
            if config_status['issues']:
                config_status['status'] = 'invalid'
                api_results['status'] = 'warning'
            else:
                config_status['status'] = 'valid'
            
            api_results['configs'][api_name] = config_status
        
        return api_results
    
    def _validate_image_config(self) -> Dict[str, Any]:
        """Validate image configuration"""
        print("🖼️ Validating image configuration...")
        
        image_config = config_manager.image_config
        
        image_results = {
            'status': 'valid',
            'issues': [],
            'recommendations': []
        }
        
        # Validate placeholder URLs
        if not self._is_valid_url(image_config.placeholder_url):
            image_results['issues'].append("Invalid placeholder URL")
            image_results['status'] = 'invalid'
        
        if not self._is_valid_url(image_config.error_image_url):
            image_results['issues'].append("Invalid error image URL")
            image_results['status'] = 'invalid'
        
        # Validate file size limits
        if image_config.max_file_size > 10 * 1024 * 1024:  # 10MB
            image_results['recommendations'].append("Max file size is quite large (>10MB)")
        
        # Validate allowed formats
        if not image_config.allowed_formats:
            image_results['issues'].append("No allowed image formats specified")
            image_results['status'] = 'invalid'
        
        # Validate CDN domains
        if not image_config.cdn_domains:
            image_results['recommendations'].append("No CDN domains configured")
        
        return image_results
    
    def _validate_performance_config(self) -> Dict[str, Any]:
        """Validate performance configuration"""
        print("⚡ Validating performance configuration...")
        
        perf_config = config_manager.performance_config
        
        perf_results = {
            'status': 'valid',
            'issues': [],
            'recommendations': []
        }
        
        # Validate cache duration
        if perf_config.cache_duration < 300:  # 5 minutes
            perf_results['recommendations'].append("Cache duration is very short (<5 min)")
        elif perf_config.cache_duration > 24 * 3600:  # 24 hours
            perf_results['recommendations'].append("Cache duration is very long (>24h)")
        
        # Validate auto refresh interval
        if perf_config.auto_refresh_interval < 600:  # 10 minutes
            perf_results['recommendations'].append("Auto refresh is very frequent (<10 min)")
        
        return perf_results
    
    def _validate_error_config(self) -> Dict[str, Any]:
        """Validate error handling configuration"""
        print("🚨 Validating error configuration...")
        
        error_config = config_manager.error_config
        
        error_results = {
            'status': 'valid',
            'issues': [],
            'recommendations': []
        }
        
        # Check log file path
        log_path = Path(error_config.error_log_file)
        if not log_path.parent.exists():
            error_results['issues'].append(f"Log directory doesn't exist: {log_path.parent}")
            error_results['status'] = 'invalid'
        
        # Check log size limits
        if error_config.max_log_size > 100 * 1024 * 1024:  # 100MB
            error_results['recommendations'].append("Max log size is very large (>100MB)")
        
        return error_results
    
    def _validate_files_and_directories(self) -> Dict[str, Any]:
        """Validate required files and directories"""
        print("📁 Validating files and directories...")
        
        files_results = {
            'status': 'valid',
            'missing_files': [],
            'missing_directories': [],
            'recommendations': []
        }
        
        # Required directories
        required_dirs = [
            'docs',
            'config',
            'logs',
            'cache'
        ]
        
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                files_results['missing_directories'].append(dir_name)
                files_results['status'] = 'warning'
        
        # Important files
        important_files = [
            'cars.json',
            'style.css',
            'sw.js'
        ]
        
        for file_name in important_files:
            if not Path(file_name).exists():
                files_results['missing_files'].append(file_name)
                files_results['status'] = 'warning'
        
        # Check if templates directory exists
        if not Path('templates').exists():
            files_results['recommendations'].append("Consider creating templates/ directory for custom templates")
        
        return files_results
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary"""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'overall_status': 'valid' if not self.errors else 'invalid',
            'setup_complete': len(self.errors) == 0 and len(self.warnings) < 5
        }
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        if not url:
            return False
        
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    def create_setup_guide(self) -> str:
        """Create setup guide based on validation results"""
        validation_results = self.validate_all()
        
        guide = f"""
# 🚀 Car Widget Setup Guide

## Configuration Status
- Overall Status: {'✅ READY' if validation_results['summary']['setup_complete'] else '⚠️ NEEDS ATTENTION'}
- Errors: {validation_results['summary']['total_errors']}
- Warnings: {validation_results['summary']['total_warnings']}

## Quick Setup Steps

### 1. Environment Variables
Create a `.env` file with the following:

```bash
# Required for Shopify integration
SHOPIFY_API_KEY=your_shopify_api_key_here
SHOPIFY_STORE_URL=https://your-store.myshopify.com

# Optional custom API
CUSTOM_API_URL=https://your-api.com/cars
CUSTOM_API_KEY=your_api_key_here

# Performance settings
API_TIMEOUT=30
MAX_RETRIES=3
CACHE_DURATION=3600

# Debug mode
DEBUG=false
LOG_LEVEL=INFO
```

### 2. Required Files
"""
        
        # Add missing files information
        if validation_results['files_and_directories']['missing_files']:
            guide += "\nMissing files to create:\n"
            for file in validation_results['files_and_directories']['missing_files']:
                guide += f"- {file}\n"
        
        if validation_results['files_and_directories']['missing_directories']:
            guide += "\nMissing directories to create:\n"
            for dir in validation_results['files_and_directories']['missing_directories']:
                guide += f"- {dir}/\n"
        
        guide += """
### 3. API Configuration Issues
"""
        
        for api_name, api_status in validation_results['api_configs']['configs'].items():
            if api_status['issues']:
                guide += f"\n**{api_name.upper()} API:**\n"
                for issue in api_status['issues']:
                    guide += f"- {issue}\n"
        
        guide += """
### 4. Next Steps
1. Fix any configuration issues above
2. Run validation again: `python config_validator.py`
3. Test API connections: `python -c "from api_client import health_check_all; import asyncio; print(asyncio.run(health_check_all()))"`
4. Generate HTML: `python python_ssr_generator.py --api local`
5. Deploy using: `python simple_online_deploy.py`

### 5. Testing Your Setup
```bash
# Test image optimization
python optimize_images.py

# Test SSR generation
python python_ssr_generator.py --api local

# Test API rendering
python render_api_to_html.py --api local

# Create deployment package
python simple_online_deploy.py
```

---
Generated: {os.getcwd()}
"""
        
        return guide
    
    def print_validation_report(self):
        """Print comprehensive validation report"""
        results = self.validate_all()
        
        print("\n" + "="*50)
        print("🔍 CONFIGURATION VALIDATION REPORT")
        print("="*50)
        
        for section, data in results.items():
            if section == 'summary':
                continue
                
            print(f"\n📋 {section.upper().replace('_', ' ')}")
            print("-" * 30)
            
            if isinstance(data, dict):
                if 'status' in data:
                    status_icon = "✅" if data['status'] == 'valid' else "⚠️" if data['status'] == 'warning' else "❌"
                    print(f"Status: {status_icon} {data['status'].upper()}")
                
                for key, value in data.items():
                    if key == 'status':
                        continue
                    elif isinstance(value, list) and value:
                        print(f"{key}:")
                        for item in value:
                            print(f"  • {item}")
                    elif isinstance(value, dict):
                        print(f"{key}:")
                        for subkey, subvalue in value.items():
                            print(f"  • {subkey}: {subvalue}")
        
        # Summary
        summary = results['summary']
        print(f"\n📊 SUMMARY")
        print("-" * 30)
        print(f"Overall Status: {'✅ READY' if summary['setup_complete'] else '⚠️ NEEDS ATTENTION'}")
        print(f"Errors: {summary['total_errors']}")
        print(f"Warnings: {summary['total_warnings']}")
        
        if not summary['setup_complete']:
            print(f"\n💡 Run setup guide: python config_validator.py --setup-guide")

def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate car widget configuration')
    parser.add_argument('--setup-guide', action='store_true', help='Generate setup guide')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    validator = ConfigValidator()
    
    if args.setup_guide:
        guide = validator.create_setup_guide()
        setup_file = Path('SETUP-GUIDE.md')
        setup_file.write_text(guide, encoding='utf-8')
        print(f"📝 Setup guide created: {setup_file}")
        print(guide)
        
    elif args.json:
        results = validator.validate_all()
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
    else:
        validator.print_validation_report()

if __name__ == "__main__":
    main()