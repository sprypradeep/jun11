"""Taskiq scheduled tasks (cron-like)."""

from app.worker.taskiq_app import broker
from app.worker.tasks.cleanup_tasks import cleanup_usage_events_task
from app.worker.tasks.email_tasks import send_low_credits_alerts_task, send_trial_reminders_task


@broker.task(schedule=[{"cron": "0 9 * * *"}])
async def scheduled_trial_reminders() -> dict:
    """Scheduled task: send trial-ending reminder emails."""
    result = await send_trial_reminders_task.kiq()
    return {"scheduled": True, "task_id": str(result.task_id)}


@broker.task(schedule=[{"cron": "0 */4 * * *"}])
async def scheduled_low_credits_alerts() -> dict:
    """Scheduled task: send low-credits alert emails."""
    result = await send_low_credits_alerts_task.kiq()
    return {"scheduled": True, "task_id": str(result.task_id)}


@broker.task(schedule=[{"cron": "0 3 * * 0"}])
async def scheduled_cleanup_usage_events() -> dict:
    """Scheduled task: purge old usage events and refresh daily matview."""
    result = await cleanup_usage_events_task.kiq()
    return {"scheduled": True, "task_id": str(result.task_id)}
