from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user

from app.schemas.user_schema import UserRead
from app.schemas.opening_schema import (
    OpeningCreate,
    OpeningRead,
    OpeningUpdate,
    OpeningsList,
    AddMoveRequest,
)

from app.services.opening_service import (
    create_opening,
    get_openings_by_user,
    get_user_opening_by_id,
    delete_user_opening_by_id,
    update_user_opening,
    compute_opening_after_move,
)

router = APIRouter()


# opening router
@router.post("", response_model=OpeningRead)
async def add_opening(
    opening: OpeningCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    created_opening = create_opening(
        db=db, opening_create=opening, user_id=current_user.id
    )
    return created_opening


@router.get("", response_model=OpeningsList)
async def read_user_openings(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
    name: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    openings_data = get_openings_by_user(
        db, user_id=current_user.id, name=name, skip=skip, limit=limit
    )
    return OpeningsList(
        total=openings_data["total"], openings=openings_data["openings"]
    )


@router.get("/{id}", response_model=OpeningRead)
async def read_user_opening_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    opening: OpeningRead = get_user_opening_by_id(db, current_user.id, id)
    return opening


@router.patch("/{id}/add_move", response_model=OpeningRead)
async def add_move_to_opening(
    id: int,
    add_move_request: AddMoveRequest,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    opening = get_user_opening_by_id(db, current_user.id, id)
    computed_updated_opening = compute_opening_after_move(
        opening,
        add_move_request.move,
        add_move_request.move_name,
        add_move_request.path,
    )
    opening_update = OpeningUpdate(data=computed_updated_opening.data)
    updated_opening = update_user_opening(
        db, current_user.id, opening.id, opening_update
    )
    return updated_opening


@router.delete("/{id}", response_model=OpeningRead)
async def remove_user_opening_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    deleted_opening: OpeningRead = delete_user_opening_by_id(db, current_user.id, id)
    return deleted_opening
