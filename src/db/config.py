from contextlib import asynccontextmanager
from tortoise import Tortoise
from config import settings


def patch_aiosqlite_for_tortoise():
  import aiosqlite

  if hasattr(aiosqlite.Connection, "start"):
    return

  def start(self):
    if not self._thread.is_alive():
      self._thread.start()

  aiosqlite.Connection.start = start


@asynccontextmanager
async def db_connection():
  patch_aiosqlite_for_tortoise()
  await Tortoise.init(
    db_url=settings.DATABASE_URL, modules={"models": settings.MODELS_MODULES}
  )
  await Tortoise.generate_schemas()

  try:
    yield
  finally:
    await Tortoise.close_connections()
