from app.common.domain.database import SessionLocal
from app.common.data.models import File


def is_valid_reference(reference):
    db = SessionLocal()
    file = db.query(File).filter(File.reference == reference).first()
    db.close()

    if file:
        return True

    return False
