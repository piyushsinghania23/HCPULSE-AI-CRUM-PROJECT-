import json

from sqlalchemy.orm import Session

from app import models, schemas


def list_interactions(db: Session) -> list[models.Interaction]:
    return db.query(models.Interaction).order_by(models.Interaction.interaction_date.desc()).all()


def get_interaction(db: Session, interaction_id: int) -> models.Interaction | None:
    return db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()


def create_interaction(db: Session, payload: schemas.InteractionCreate) -> models.Interaction:
    item = models.Interaction(
        representative_name=payload.representative_name,
        hcp_name=payload.hcp_name,
        specialty=payload.specialty,
        interaction_type=payload.interaction_type,
        channel=payload.channel,
        interaction_date=payload.interaction_date,
        notes_raw=payload.notes_raw,
        notes_summary=payload.notes_summary or payload.notes_raw,
        key_entities=json.dumps(payload.key_entities),
        products_discussed=payload.products_discussed,
        follow_up_action=payload.follow_up_action,
        follow_up_date=payload.follow_up_date,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_interaction(
    db: Session, interaction_id: int, payload: schemas.InteractionUpdate
) -> models.Interaction | None:
    item = get_interaction(db, interaction_id)
    if not item:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "key_entities" and value is not None:
            value = json.dumps(value)
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

