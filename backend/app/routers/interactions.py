import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/interactions", tags=["interactions"])


@router.get("", response_model=list[schemas.InteractionRead])
def list_items(db: Session = Depends(get_db)):
    rows = crud.list_interactions(db)
    output = []
    for row in rows:
        output.append(
            schemas.InteractionRead(
                id=row.id,
                representative_name=row.representative_name,
                hcp_name=row.hcp_name,
                specialty=row.specialty,
                interaction_type=row.interaction_type,
                channel=row.channel,
                interaction_date=row.interaction_date,
                notes_raw=row.notes_raw,
                notes_summary=row.notes_summary,
                key_entities=json.loads(row.key_entities or "{}"),
                products_discussed=row.products_discussed,
                follow_up_action=row.follow_up_action,
                follow_up_date=row.follow_up_date,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
        )
    return output


@router.post("", response_model=schemas.InteractionRead)
def create_item(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    row = crud.create_interaction(db, payload)
    return schemas.InteractionRead(
        id=row.id,
        representative_name=row.representative_name,
        hcp_name=row.hcp_name,
        specialty=row.specialty,
        interaction_type=row.interaction_type,
        channel=row.channel,
        interaction_date=row.interaction_date,
        notes_raw=row.notes_raw,
        notes_summary=row.notes_summary,
        key_entities=json.loads(row.key_entities or "{}"),
        products_discussed=row.products_discussed,
        follow_up_action=row.follow_up_action,
        follow_up_date=row.follow_up_date,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


@router.put("/{interaction_id}", response_model=schemas.InteractionRead)
def update_item(interaction_id: int, payload: schemas.InteractionUpdate, db: Session = Depends(get_db)):
    row = crud.update_interaction(db, interaction_id, payload)
    if not row:
        raise HTTPException(status_code=404, detail="Interaction not found")

    return schemas.InteractionRead(
        id=row.id,
        representative_name=row.representative_name,
        hcp_name=row.hcp_name,
        specialty=row.specialty,
        interaction_type=row.interaction_type,
        channel=row.channel,
        interaction_date=row.interaction_date,
        notes_raw=row.notes_raw,
        notes_summary=row.notes_summary,
        key_entities=json.loads(row.key_entities or "{}"),
        products_discussed=row.products_discussed,
        follow_up_action=row.follow_up_action,
        follow_up_date=row.follow_up_date,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )

