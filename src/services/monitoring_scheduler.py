"""
Background Monitoring Task Scheduler
Handles periodic monitoring of vendors and alert generation
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set
import json
from pathlib import Path

from .ai_monitoring import monitor_vendor_ai

# Configure logging
logger = logging.getLogger(__name__)

class BackgroundMonitoringScheduler:
    """
    Manages background monitoring tasks for all enabled vendors
    """
    
    def __init__(self):
        self.monitored_vendors: Dict[str, Dict] = {}
        self.running = False
        self.task = None
        self.check_interval = 300  # 5 minutes default
        
        # In-memory storage for demo (in production, use database)
        self.storage_file = Path("storage/monitoring_data.json")
        self.storage_file.parent.mkdir(exist_ok=True)
        
        # Load existing monitoring config
        self._load_monitoring_config()
    
    def add_vendor_monitoring(self, vendor_domain: str, vendor_name: str = None, assessment_id: str = None) -> bool:
        """Add a vendor to continuous monitoring"""
        try:
            config = {
                "vendor_domain": vendor_domain,
                "vendor_name": vendor_name or vendor_domain,
                "assessment_id": assessment_id,
                "enabled": True,
                "added_at": datetime.now().isoformat(),
                "last_checked": None,
                "next_check": (datetime.now() + timedelta(minutes=self.check_interval)).isoformat(),
                "check_count": 0,
                "alert_count": 0,
                "status": "active"
            }
            
            self.monitored_vendors[vendor_domain] = config
            self._save_monitoring_config()
            
            logger.info(f"➕ Added {vendor_domain} to continuous monitoring")
            return True
            
        except Exception as e:
            logger.error(f"Error adding vendor monitoring for {vendor_domain}: {str(e)}")
            return False
    
    def remove_vendor_monitoring(self, vendor_domain: str) -> bool:
        """Remove a vendor from continuous monitoring"""
        try:
            if vendor_domain in self.monitored_vendors:
                del self.monitored_vendors[vendor_domain]
                self._save_monitoring_config()
                logger.info(f"➖ Removed {vendor_domain} from continuous monitoring")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing vendor monitoring for {vendor_domain}: {str(e)}")
            return False
    
    def get_monitored_vendors(self) -> List[Dict]:
        """Get list of all monitored vendors"""
        return list(self.monitored_vendors.values())
    
    def get_vendor_status(self, vendor_domain: str) -> Dict:
        """Get monitoring status for a specific vendor"""
        return self.monitored_vendors.get(vendor_domain, {})
    
    async def start_monitoring(self):
        """Start the background monitoring process"""
        if self.running:
            logger.warning("Monitoring is already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._monitoring_loop())
        logger.info("🚀 Started background monitoring scheduler")
    
    async def stop_monitoring(self):
        """Stop the background monitoring process"""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Stopped background monitoring scheduler")
    
    async def _monitoring_loop(self):
        """Main monitoring loop that runs in the background"""
        logger.info("🔄 Starting monitoring loop")
        
        while self.running:
            try:
                # Check which vendors need monitoring
                vendors_to_check = self._get_vendors_due_for_check()
                
                if vendors_to_check:
                    logger.info(f"📊 Checking {len(vendors_to_check)} vendors for updates")
                    
                    # Check vendors in parallel (but limit concurrency)
                    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent checks
                    tasks = [
                        self._check_vendor_with_semaphore(semaphore, vendor_domain, config)
                        for vendor_domain, config in vendors_to_check
                    ]
                    
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                # Wait before next cycle
                await asyncio.sleep(60)  # Check every minute for due vendors
                
            except asyncio.CancelledError:
                logger.info("Monitoring loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def _get_vendors_due_for_check(self) -> List[tuple]:
        """Get vendors that are due for their next check"""
        now = datetime.now()
        due_vendors = []
        
        for vendor_domain, config in self.monitored_vendors.items():
            if not config.get("enabled", True):
                continue
            
            next_check_str = config.get("next_check")
            if not next_check_str:
                # Schedule immediate check if no next_check time
                due_vendors.append((vendor_domain, config))
                continue
            
            try:
                next_check = datetime.fromisoformat(next_check_str.replace('Z', '+00:00'))
                if now >= next_check:
                    due_vendors.append((vendor_domain, config))
            except Exception as e:
                logger.warning(f"Invalid next_check time for {vendor_domain}: {e}")
                due_vendors.append((vendor_domain, config))
        
        return due_vendors
    
    async def _check_vendor_with_semaphore(self, semaphore: asyncio.Semaphore, vendor_domain: str, config: Dict):
        """Check a single vendor with concurrency control"""
        async with semaphore:
            await self._check_single_vendor(vendor_domain, config)
    
    async def _check_single_vendor(self, vendor_domain: str, config: Dict):
        """Perform monitoring check for a single vendor"""
        start_time = datetime.now()
        
        try:
            logger.info(f"🔍 Starting monitoring check for {vendor_domain}")
            
            vendor_name = config.get("vendor_name", vendor_domain)
            
            # Perform AI monitoring
            alerts = await monitor_vendor_ai(vendor_domain, vendor_name)
            
            # Update vendor config
            config["last_checked"] = start_time.isoformat()
            config["next_check"] = (start_time + timedelta(minutes=self.check_interval)).isoformat()
            config["check_count"] = config.get("check_count", 0) + 1
            config["alert_count"] = config.get("alert_count", 0) + len(alerts)
            
            if alerts:
                logger.warning(f"⚠️  Found {len(alerts)} alerts for {vendor_domain}")
                # Store alerts (in production, save to database)
                self._store_alerts(vendor_domain, alerts)
            else:
                logger.info(f"✅ No alerts found for {vendor_domain}")
            
            # Save updated config
            self._save_monitoring_config()
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Completed monitoring check for {vendor_domain} in {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Error checking vendor {vendor_domain}: {str(e)}")
            # Update config with error info
            config["last_error"] = str(e)
            config["last_error_at"] = datetime.now().isoformat()
            self._save_monitoring_config()
    
    def _store_alerts(self, vendor_domain: str, alerts: List[Dict]):
        """Store alerts for a vendor (in-memory for demo)"""
        try:
            alerts_file = Path(f"storage/alerts_{vendor_domain.replace('.', '_')}.json")
            
            # Load existing alerts
            existing_alerts = []
            if alerts_file.exists():
                with open(alerts_file, 'r') as f:
                    existing_alerts = json.load(f)
            
            # Add new alerts
            existing_alerts.extend(alerts)
            
            # Keep only last 100 alerts per vendor
            existing_alerts = existing_alerts[-100:]
            
            # Save alerts
            with open(alerts_file, 'w') as f:
                json.dump(existing_alerts, f, indent=2, default=str)
                
            logger.info(f"💾 Stored {len(alerts)} new alerts for {vendor_domain}")
            
        except Exception as e:
            logger.error(f"Error storing alerts for {vendor_domain}: {str(e)}")
    
    def get_vendor_alerts(self, vendor_domain: str, limit: int = 50) -> List[Dict]:
        """Get recent alerts for a vendor"""
        try:
            alerts_file = Path(f"storage/alerts_{vendor_domain.replace('.', '_')}.json")
            
            if not alerts_file.exists():
                return []
            
            with open(alerts_file, 'r') as f:
                alerts = json.load(f)
            
            # Return most recent alerts
            return alerts[-limit:]
            
        except Exception as e:
            logger.error(f"Error loading alerts for {vendor_domain}: {str(e)}")
            return []
    
    def get_all_recent_alerts(self, limit: int = 50) -> List[Dict]:
        """Get all recent alerts across all vendors"""
        all_alerts = []
        
        try:
            storage_dir = Path("storage")
            for alerts_file in storage_dir.glob("alerts_*.json"):
                try:
                    with open(alerts_file, 'r') as f:
                        vendor_alerts = json.load(f)
                    all_alerts.extend(vendor_alerts)
                except Exception as e:
                    logger.warning(f"Error reading alerts file {alerts_file}: {e}")
            
            # Sort by timestamp (most recent first)
            all_alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return all_alerts[:limit]
            
        except Exception as e:
            logger.error(f"Error loading all alerts: {str(e)}")
            return []
    
    def _load_monitoring_config(self):
        """Load monitoring configuration from storage"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r') as f:
                    self.monitored_vendors = json.load(f)
                logger.info(f"📂 Loaded monitoring config for {len(self.monitored_vendors)} vendors")
        except Exception as e:
            logger.warning(f"Could not load monitoring config: {e}")
            self.monitored_vendors = {}
    
    def _save_monitoring_config(self):
        """Save monitoring configuration to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.monitored_vendors, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Could not save monitoring config: {e}")

# Global monitoring scheduler instance
monitoring_scheduler = BackgroundMonitoringScheduler()

# Convenience functions for API use
async def add_vendor_to_monitoring(vendor_domain: str, vendor_name: str = None, assessment_id: str = None) -> bool:
    """Add a vendor to continuous monitoring"""
    success = monitoring_scheduler.add_vendor_monitoring(vendor_domain, vendor_name, assessment_id)
    
    # Start monitoring if not already running
    if success and not monitoring_scheduler.running:
        await monitoring_scheduler.start_monitoring()
    
    return success

async def remove_vendor_from_monitoring(vendor_domain: str) -> bool:
    """Remove a vendor from continuous monitoring"""
    return monitoring_scheduler.remove_vendor_monitoring(vendor_domain)

async def get_monitoring_status() -> Dict:
    """Get overall monitoring system status"""
    return {
        "running": monitoring_scheduler.running,
        "monitored_vendors": len(monitoring_scheduler.monitored_vendors),
        "vendor_list": list(monitoring_scheduler.monitored_vendors.keys()),
        "check_interval_minutes": monitoring_scheduler.check_interval
    }

async def get_vendor_monitoring_alerts(vendor_domain: str, limit: int = 50) -> List[Dict]:
    """Get alerts for a specific vendor"""
    return monitoring_scheduler.get_vendor_alerts(vendor_domain, limit)

async def get_all_monitoring_alerts(limit: int = 50) -> List[Dict]:
    """Get all recent monitoring alerts"""
    return monitoring_scheduler.get_all_recent_alerts(limit)