from app.database import SessionLocal
from app.models.structure import MailTemplate
from app.translations import TRANSLATIONS

def seed_mail_templates():
    db = SessionLocal()
    try:
        count = db.query(MailTemplate).count()
        if count > 0:
            print(f"// MAIL TEMPLATES — bereits {count} Eintraege vorhanden. Skip.")
            return

        entries = []
        for language, keys in TRANSLATIONS.items():
            for key, content in keys.items():
                entries.append(MailTemplate(
                    language=language,
                    key=key,
                    content=content
                ))

        db.bulk_save_objects(entries)
        db.commit()
        print(f"// MAIL TEMPLATES — {len(entries)} Eintraege geseedet. ⚡")
    finally:
        db.close()

if __name__ == "__main__":
    seed_mail_templates()
