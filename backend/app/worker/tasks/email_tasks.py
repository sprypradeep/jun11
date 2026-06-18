"""Lifecycle email tasks — trial reminders and low-credits alerts."""

import logging

from app.db.session import get_worker_db_context
from app.services.billing import BillingService
from app.worker.taskiq_app import broker

logger = logging.getLogger(__name__)


async def _send_trial_reminders() -> int:
    async with get_worker_db_context() as db:
        return await BillingService(db).send_trial_ending_reminders()


async def _send_low_credits_alerts() -> int:
    async with get_worker_db_context() as db:
        return await BillingService(db).send_low_credits_alerts()


@broker.task
async def send_trial_reminders_task() -> dict[str, int]:
    """Cron: send trial-ending reminder emails."""
    count = await _send_trial_reminders()
    logger.info("trial_reminders_sent", extra={"count": count})
    return {"sent": count}


@broker.task
async def send_low_credits_alerts_task() -> dict[str, int]:
    """Cron: send low-credits alert emails to orgs below threshold."""
    count = await _send_low_credits_alerts()
    logger.info("low_credits_alerts_sent", extra={"count": count})
    return {"sent": count}
