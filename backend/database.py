import os
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db = None

async def get_db():
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    res = await db[collection_name].insert_one({**data})
    doc = await db[collection_name].find_one({"_id": res.inserted_id})
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])  # expose as string id
        del doc["_id"]
    return doc or {}

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int | None = None) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {})
    if limit:
        cursor = cursor.limit(limit)
    results: List[Dict[str, Any]] = []
    async for d in cursor:
        d["id"] = str(d["_id"]) if d.get("_id") else None
        d.pop("_id", None)
        results.append(d)
    return results

async def get_document_by_id(collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    from bson import ObjectId
    db = await get_db()
    try:
        oid = ObjectId(doc_id)
    except Exception:
        return None
    d = await db[collection_name].find_one({"_id": oid})
    if not d:
        return None
    d["id"] = str(d["_id"]) if d.get("_id") else None
    d.pop("_id", None)
    return d
