from src.worker.celery_app import celery_app
import asyncio
import logging

logger = logging.getLogger(__name__)

def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

@celery_app.task(bind=True, name="run_import_job")
def run_import_job(self, job_id: int):
    """
    Synchronous wrapper for the async import logic.
    Celery runs sync, so we spin up an event loop for the async IO.
    """
    from src.worker.import_logic import process_import_job
    logger.info(f"Starting import job {job_id}")
    try:
        run_async(process_import_job(job_id))
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        # Mark as failed in DB handled inside logic or here
        raise e

@celery_app.task(bind=True, name="run_broadcast")
def run_broadcast(self, broadcast_id: int):
    from src.worker.broadcast_logic import process_broadcast
    logger.info(f"Starting broadcast {broadcast_id}")
    try:
        run_async(process_broadcast(broadcast_id))
    except Exception as e:
        logger.error(f"Broadcast {broadcast_id} failed: {e}")
        raise e
