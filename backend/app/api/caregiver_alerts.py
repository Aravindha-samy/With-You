from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from database import get_db

router = APIRouter(prefix="/caregiver-alerts", tags=["caregiver-alerts"])


@router.post("/", response_model=schemas.CaregiverAlert)
def create_caregiver_alert(alert: schemas.CaregiverAlertCreate, db: Session = Depends(get_db)):
    """Create an alert for caregiver (Agent systems will call this when patient needs attention)"""
    return crud.create_caregiver_alert(db=db, alert=alert)


@router.get("/caregiver/{caregiver_id}", response_model=list[schemas.CaregiverAlert])
def get_caregiver_alerts(caregiver_id: int, acknowledged: bool = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get alerts for a caregiver.
    
    Query params:
    - acknowledged: true/false/null (null returns all)
    """
    return crud.get_caregiver_alerts(db=db, caregiver_id=caregiver_id, acknowledged=acknowledged, skip=skip, limit=limit)


@router.get("/patient/{user_id}", response_model=list[schemas.CaregiverAlert])
def get_patient_alerts(user_id: int, acknowledged: bool = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all alerts for a specific patient"""
    return crud.get_user_alerts(db=db, user_id=user_id, acknowledged=acknowledged, skip=skip, limit=limit)


@router.get("/{alert_id}", response_model=schemas.CaregiverAlert)
def get_caregiver_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific alert"""
    db_alert = crud.get_caregiver_alert(db, alert_id=alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@router.put("/{alert_id}", response_model=schemas.CaregiverAlert)
def update_caregiver_alert(alert_id: int, alert: schemas.CaregiverAlertUpdate, db: Session = Depends(get_db)):
    """Update an alert (acknowledge it)"""
    db_alert = crud.update_caregiver_alert(db=db, alert_id=alert_id, alert=alert)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@router.delete("/{alert_id}")
def delete_caregiver_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert"""
    db_alert = crud.delete_caregiver_alert(db=db, alert_id=alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted successfully"}
