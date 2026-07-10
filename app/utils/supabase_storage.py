import os
import uuid

from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

BUCKET = "notes"


def upload_file(file):

    extension = os.path.splitext(file.filename)[1].lower()

    filename = f"{uuid.uuid4()}{extension}"

    path = filename

    file.seek(0)

    supabase.storage.from_(BUCKET).upload(
        path,
        file.read(),
        {
            "content-type": file.content_type
        }
    )

    public_url = supabase.storage.from_(BUCKET).get_public_url(path)

    return {
        "path": path,
        "url": public_url,
        "filename": filename
    }


def delete_file(path):

    supabase.storage.from_(BUCKET).remove([path])