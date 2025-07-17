from typing import List, Annotated
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.db_setup import SessionDep
from db.models.course import Section, SectionPublic, ContentBlock, ContentBlockPublic, SectionCreate,SectionUpdate,ContentBlockCreate,ContentBlockUpdate
router = APIRouter(tags=['sections'])

@router.post("/sections/", response_model=SectionPublic)
async def create_section(section: SectionCreate, session: SessionDep):
    db_section = Section.model_validate(section)
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section

@router.get("/sections/{id}", response_model=SectionPublic)
async def read_section(id: int, session: SessionDep):
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.patch("/sections/{id}", response_model=SectionPublic)
async def update_section(id: int, section: SectionUpdate, session: SessionDep):
    db_section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    section_data = section.model_dump(exclude_unset=True)
    db_section.sqlmodel_update(section_data)
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section

@router.delete("/sections/{id}")
async def delete_section(id: int, session: SessionDep):
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    session.delete(section)
    session.commit()
    return {"ok": True}

@router.get("/sections/{id}/content-blocks", response_model=List[ContentBlockPublic])
async def read_section_content_blocks(id: int, session: SessionDep):
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    content_blocks = session.exec(select(ContentBlock).where(ContentBlock.section_id == id)).all()
    return content_blocks

@router.post("/content-blocks/", response_model=ContentBlockPublic)
async def create_content_block(content_block: ContentBlockCreate, session: SessionDep):
    db_content_block = ContentBlock.model_validate(content_block)
    session.add(db_content_block)
    session.commit()
    session.refresh(db_content_block)
    return db_content_block

@router.get("/content-blocks/{id}", response_model=ContentBlockPublic)
async def read_content_block(id: int, session: SessionDep):
    content_block = session.get(ContentBlock, id)
    if not content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    return content_block

@router.patch("/content-blocks/{id}", response_model=ContentBlockPublic)
async def update_content_block(id: int, content_block: ContentBlockUpdate, session: SessionDep):
    db_content_block = session.get(ContentBlock, id)
    if not db_content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    content_block_data = content_block.model_dump(exclude_unset=True)
    db_content_block.sqlmodel_update(content_block_data)
    session.add(db_content_block)
    session.commit()
    session.refresh(db_content_block)
    return db_content_block

@router.delete("/content-blocks/{id}")
async def delete_content_block(id: int, session: SessionDep):
    content_block = session.get(ContentBlock, id)
    if not content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    session.delete(content_block)
    session.commit()
    return {"ok": True}