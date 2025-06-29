from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import structlog

from app import models, schemas, crud, dependencies
from app.models.chat import SenderType
from app.services.planner_service import PlannerService
from app.services.generator_service import GeneratorService
from app.services.emotion_service import EmotionService

router = APIRouter()
log = structlog.get_logger(__name__)


# Di app/api/v1/chat.py
def get_latest_journal(db: Session, user: models.User) -> str:
    journals = crud.journal.get_multi_by_owner(
        db=db,
        owner_id=user.id,
        limit=1,
        order_by="created_at desc",
    )
    return journals[0].content if journals else ""


@router.post("/", response_model=schemas.chat.ChatMessage)
async def handle_chat_message(
        *,
        db: Session = Depends(dependencies.get_db),
        chat_in: schemas.chat.ChatRequest,
        current_user: models.User = Depends(dependencies.get_current_user),
        planner: PlannerService = Depends(),
        generator: GeneratorService = Depends(),
        emotion_service: EmotionService = Depends(),
):
    log.info("handle_chat_message:start", user_id=current_user.id)

    # Ambil memori pengguna (profil psikologis jangka panjang)
    user_profile = crud.user_profile.get_by_user_id(db, user_id=current_user.id)

    # Ambil jurnal terbaru (konteks jangka pendek emosional)
    latest_journal = get_latest_journal(db, user=current_user)

    # Deteksi emosi dari pesan terbaru
    emotion_label = emotion_service.detect_emotion(chat_in.message)

    # Simpan pesan USER ke database
    user_message_obj = schemas.chat.ChatMessageCreate(
        content=chat_in.message,
        sender_type=SenderType.USER,
        emotion=emotion_label,
    )
    crud.chat_message.create_with_owner(
        db=db,
        obj_in=user_message_obj,
        owner_id=current_user.id
    )

    # Ambil 10 riwayat pesan terakhir (dalam urutan kronologis)
    history_db = crud.chat_message.get_multi_by_owner(
        db=db,
        owner_id=current_user.id,
        limit=10
    )
    history_db_reversed = history_db[::-1]  # kronologis dari paling awal ke akhir

    chat_history = [msg.content for msg in history_db_reversed]
    history_formatted = [
        {"role": msg.sender_type.value, "content": msg.content}
        for msg in history_db_reversed
    ]

    # Perencanaan strategi komunikasi
    conversation_plan = await planner.get_plan(
        user_message=chat_in.message,
        chat_history=chat_history,
        latest_journal=latest_journal,
        user_profile=user_profile,  # bisa None
        emotion_label=emotion_label,
    )

    # Hasilkan respons AI
    final_response = await generator.generate_response(
        plan=conversation_plan,
        history=history_formatted,
        emotion=emotion_label,
    )

    # Simpan pesan AI ke database
    ai_message_obj = schemas.chat.ChatMessageCreate(
        content=final_response,
        sender_type=SenderType.AI,
        ai_technique=conversation_plan.technique.value,
    )
    ai_message_db = crud.chat_message.create_with_owner(
        db=db,
        obj_in=ai_message_obj,
        owner_id=current_user.id
    )

    log.info(
        "handle_chat_message:success",
        user_id=current_user.id,
        ai_technique=conversation_plan.technique.value,
    )

    return ai_message_db


@router.patch("/{chat_id}/flag", response_model=schemas.chat.ChatMessage)
def flag_chat_message(
    *,
    chat_id: int,
    flag: schemas.chat.ChatFlagUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    msg = crud.chat_message.set_flag(
        db=db,
        id=chat_id,
        owner_id=current_user.id,
        flag=flag.flag,
    )
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.delete("/{chat_id}", response_model=schemas.chat.ChatMessage)
def delete_chat_message(
    *,
    chat_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    msg = crud.chat_message.remove(
        db=db,
        id=chat_id,
        owner_id=current_user.id,
    )
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
