#!/usr/bin/env python3
"""
Enhanced API Client with Retry Logic and Error Handling
"""

import asyncio
import aiohttp
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import hashlib
import os

from config_manager import config_manager

logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    """API Response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    response_time: float = 0.0
    from_cache: bool = False

class APICache:
    """Simple file-based cache for API responses"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_file(self, cache_key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, cache_key: str, max_age: int = 3600) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired"""
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            # Check if cache is expired
            if time.time() - cache_file.stat().st_mtime > max_age:
                logger.debug(f"Cache expired for key: {cache_key}")
                cache_file.unlink()
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"Cache hit for key: {cache_key}")
                return data
                
        except Exception as e:
            logger.warning(f"Failed to read cache for key {cache_key}: {e}")
            return None
    
    def set(self, cache_key: str, data: Dict[str, Any]):
        """Store data in cache"""
        cache_file = self._get_cache_file(cache_key)
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Data cached for key: {cache_key}")
            
        except Exception as e:
            logger.warning(f"Failed to cache data for key {cache_key}: {e}")

class EnhancedAPIClient:
    """Enhanced API client with retry logic and error handling"""
    
    def __init__(self):
        self.cache = APICache()
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=60)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'Car-Widget-Client/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_with_retry(self, api_name: str, use_cache: bool = True) -> APIResponse:
        """Fetch data from API with retry logic"""
        start_time = time.time()
        
        # Get API configuration
        api_config = config_manager.get_api_config(api_name)
        if not api_config:
            return APIResponse(
                success=False,
                error=f"API configuration '{api_name}' not found"
            )
        
        # Validate configuration
        if not config_manager.validate_api_config(api_name):
            return APIResponse(
                success=False,
                error=f"API configuration '{api_name}' is invalid"
            )
        
        # Check cache first
        cache_key = config_manager.get_cache_key(api_name)
        if use_cache:
            cached_data = self.cache.get(cache_key, config_manager.performance_config.cache_duration)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    response_time=time.time() - start_time,
                    from_cache=True
                )
        
        # Handle local file
        if api_name == 'local':
            return await self._fetch_local_file(api_config, cache_key, start_time)
        
        # Handle remote API with retries
        return await self._fetch_remote_api(api_config, cache_key, start_time)
    
    async def _fetch_local_file(self, api_config, cache_key: str, start_time: float) -> APIResponse:
        """Fetch data from local file"""
        try:
            file_path = Path(api_config.url)
            if not file_path.exists():
                # Try in docs directory
                file_path = Path("docs") / api_config.url
            
            if not file_path.exists():
                return APIResponse(
                    success=False,
                    error=f"Local file not found: {api_config.url}",
                    response_time=time.time() - start_time
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different data formats
            if isinstance(data, list):
                data = {'products': data}
            
            # Cache the data
            self.cache.set(cache_key, data)
            
            logger.info(f"Successfully loaded local data from {file_path}")
            return APIResponse(
                success=True,
                data=data,
                response_time=time.time() - start_time
            )
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in local file {api_config.url}: {e}"
            logger.error(error_msg)
            return APIResponse(
                success=False,
                error=error_msg,
                response_time=time.time() - start_time
            )
        except Exception as e:
            error_msg = f"Error reading local file {api_config.url}: {e}"
            logger.error(error_msg)
            return APIResponse(
                success=False,
                error=error_msg,
                response_time=time.time() - start_time
            )
    
    async def _fetch_remote_api(self, api_config, cache_key: str, start_time: float) -> APIResponse:
        """Fetch data from remote API with retries"""
        last_error = None
        
        for attempt in range(api_config.max_retries):
            try:
                logger.info(f"Fetching from {api_config.name} API (attempt {attempt + 1}/{api_config.max_retries})")
                
                async with self.session.get(
                    api_config.url,
                    headers=api_config.headers,
                    timeout=aiohttp.ClientTimeout(total=api_config.timeout)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Cache successful response
                        self.cache.set(cache_key, data)
                        
                        logger.info(f"Successfully fetched from {api_config.name} API")
                        return APIResponse(
                            success=True,
                            data=data,
                            status_code=response.status,
                            response_time=time.time() - start_time
                        )
                    
                    elif response.status == 429:  # Rate limited
                        wait_time = api_config.retry_delay * (2 ** attempt)
                        logger.warning(f"Rate limited. Waiting {wait_time}s before retry")
                        await asyncio.sleep(wait_time)
                        continue
                    
                    elif response.status >= 500:  # Server error, retry
                        error_msg = f"Server error {response.status}"
                        logger.warning(f"{error_msg}, retrying...")
                        last_error = error_msg
                        
                        if attempt < api_config.max_retries - 1:
                            wait_time = api_config.retry_delay * (2 ** attempt)
                            await asyncio.sleep(wait_time)
                        continue
                    
                    else:  # Client error, don't retry
                        error_msg = f"API error {response.status}: {await response.text()}"
                        logger.error(error_msg)
                        return APIResponse(
                            success=False,
                            error=error_msg,
                            status_code=response.status,
                            response_time=time.time() - start_time
                        )
            
            except asyncio.TimeoutError:
                error_msg = f"Timeout fetching from {api_config.name} API"
                logger.warning(f"{error_msg}, retrying...")
                last_error = error_msg
                
                if attempt < api_config.max_retries - 1:
                    await asyncio.sleep(api_config.retry_delay * (2 ** attempt))
                
            except aiohttp.ClientError as e:
                error_msg = f"Client error fetching from {api_config.name} API: {e}"
                logger.warning(f"{error_msg}, retrying...")
                last_error = error_msg
                
                if attempt < api_config.max_retries - 1:
                    await asyncio.sleep(api_config.retry_delay * (2 ** attempt))
            
            except Exception as e:
                error_msg = f"Unexpected error fetching from {api_config.name} API: {e}"
                logger.error(error_msg)
                return APIResponse(
                    success=False,
                    error=error_msg,
                    response_time=time.time() - start_time
                )
        
        # All retries failed
        final_error = last_error or f"Failed to fetch from {api_config.name} API after {api_config.max_retries} attempts"
        logger.error(final_error)
        
        return APIResponse(
            success=False,
            error=final_error,
            response_time=time.time() - start_time
        )
    
    async def health_check(self, api_name: str) -> bool:
        """Check if API is accessible"""
        try:
            response = await self.fetch_with_retry(api_name, use_cache=False)
            return response.success
        except Exception as e:
            logger.error(f"Health check failed for {api_name}: {e}")
            return False
    
    def clear_cache(self, api_name: Optional[str] = None):
        """Clear cache for specific API or all APIs"""
        if api_name:
            cache_key = config_manager.get_cache_key(api_name)
            cache_file = self.cache._get_cache_file(cache_key)
            if cache_file.exists():
                cache_file.unlink()
                logger.info(f"Cache cleared for {api_name}")
        else:
            for cache_file in self.cache.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("All cache cleared")

# Convenience function for simple usage
async def fetch_api_data(api_name: str, use_cache: bool = True) -> APIResponse:
    """Convenience function to fetch API data"""
    async with EnhancedAPIClient() as client:
        return await client.fetch_with_retry(api_name, use_cache)

# Health check for all configured APIs
async def health_check_all() -> Dict[str, bool]:
    """Check health of all configured APIs"""
    results = {}
    async with EnhancedAPIClient() as client:
        for api_name in config_manager.api_configs.keys():
            results[api_name] = await client.health_check(api_name)
    return results