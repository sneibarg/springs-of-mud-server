"""Ordered blocking I/O, isolated from the live runtime owner loop."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor


_worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ContentIO")


def submit(operation, *args):
    """Submit prepared data; callers must snapshot mutable models first."""
    future = _worker.submit(operation, *args)
    future.add_done_callback(_report_error)
    return future


def _report_error(future):
    if not future.cancelled() and (error := future.exception()) is not None:
        logging.getLogger(__name__).error("Background content I/O failed", exc_info=(type(error), error, error.__traceback__))


async def run(operation, *args):
    return await asyncio.wrap_future(submit(operation, *args))
