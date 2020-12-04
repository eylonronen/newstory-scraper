from datetime import datetime
import json
import os
import logging

from azure.storage.blob import BlobServiceClient

from . import producers
from .scraper import get_profile
from .util import read_blob, get_bool_from_env

logger = logging.getLogger(__name__)


if get_bool_from_env("WORKER", 0):
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )


def echo(event):
    event_data = event.value
    print(event_data)


def scrape_profile(user) -> dict:
    profile = get_profile(user, "/tmp/scraper")
    path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    producers["newstory.tasks.upload"].send("newstory.tasks.upload", user, path).get(
        timeout=60
    )
    return profile


def insert_to_db(blob, container_name=None) -> dict:
    data = read_blob(
        blob_service_client, container_name or os.environ["CONTAINER_NAME"], blob
    )
    path = f"/tmp/profiles/{user}/profile.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        json.dump({"created_at": datetime.utcnow().isoformat(), "data": profile}, fp)
    upload.apply_async(args=[path])
    return profile


def upload(path) -> str:
    container_name = os.environ["CONTAINER_NAME"]
    with open(path, "r") as fp:
        profile = json.load(fp)
    date = datetime.fromisoformat(profile["created_at"]).isoformat().split("T")[0]
    user = profile["data"]["GraphProfileInfo"]["username"]
    blob = f"profiles/{date}/{user}/profile.json"
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob
    )
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    producers["newstory.tasks.newEntry"].send(
        "newstory.tasks.newEntry", user, blob
    ).get(timeout=60)
    return blob


tasks = {"profile": scrape_profile, "Echo": echo}