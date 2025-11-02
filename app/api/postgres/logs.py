from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from datetime import datetime

from app.core.database import get_postgres_session

router = APIRouter(tags=["PostgreSQL - Logs"])


@router.get("/validation",
    summary="Get validation logs",
    description="Retrieve validation failure logs (BMI validation failures)"
)
def get_validation_logs(
    patient_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_postgres_session)
):
    """
    Get validation logs from the ValidationLog table.
    
    - **patient_id**: Optional filter by patient ID
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        if patient_id:
            query = text("""
                SELECT 
                    "ValidationID",
                    "TableName",
                    "PatientID",
                    "ColumnName",
                    "Value",
                    "ValidationRule",
                    "ErrorMessage",
                    "ValidatedAt",
                    "ValidatedBy"
                FROM "ValidationLog"
                WHERE "PatientID" = :patient_id
                ORDER BY "ValidatedAt" DESC
                OFFSET :skip
                LIMIT :limit
            """)
            results = db.execute(query, {"patient_id": patient_id, "skip": skip, "limit": limit}).fetchall()
            
            total_query = text('SELECT COUNT(*) FROM "ValidationLog" WHERE "PatientID" = :patient_id')
            total = db.execute(total_query, {"patient_id": patient_id}).scalar()
        else:
            query = text("""
                SELECT 
                    "ValidationID",
                    "TableName",
                    "PatientID",
                    "ColumnName",
                    "Value",
                    "ValidationRule",
                    "ErrorMessage",
                    "ValidatedAt",
                    "ValidatedBy"
                FROM "ValidationLog"
                ORDER BY "ValidatedAt" DESC
                OFFSET :skip
                LIMIT :limit
            """)
            results = db.execute(query, {"skip": skip, "limit": limit}).fetchall()
            
            total_query = text('SELECT COUNT(*) FROM "ValidationLog"')
            total = db.execute(total_query).scalar()
        
        logs = []
        for result in results:
            log = {
                "ValidationID": result[0],
                "TableName": result[1],
                "PatientID": result[2],
                "ColumnName": result[3],
                "Value": result[4],
                "ValidationRule": result[5],
                "ErrorMessage": result[6],
                "ValidatedAt": result[7].isoformat() if result[7] else None,
                "ValidatedBy": result[8]
            }
            logs.append(log)
        
        return {
            "total": total or 0,
            "skip": skip,
            "limit": limit,
            "returned": len(logs),
            "logs": logs
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving validation logs: {str(e)}"
        )


@router.get("/validation/recent",
    summary="Get recent validation logs",
    description="Retrieve the most recent validation failure logs"
)
def get_recent_validation_logs(
    limit: int = 50,
    db: Session = Depends(get_postgres_session)
):
    """
    Get the most recent validation logs.
    
    - **limit**: Maximum number of recent logs to return (default: 50)
    """
    try:
        query = text("""
            SELECT 
                "ValidationID",
                "TableName",
                "PatientID",
                "ColumnName",
                "Value",
                "ValidationRule",
                "ErrorMessage",
                "ValidatedAt",
                "ValidatedBy"
            FROM "ValidationLog"
            ORDER BY "ValidatedAt" DESC
            LIMIT :limit
        """)
        results = db.execute(query, {"limit": limit}).fetchall()
        
        logs = []
        for result in results:
            log = {
                "ValidationID": result[0],
                "TableName": result[1],
                "PatientID": result[2],
                "ColumnName": result[3],
                "Value": result[4],
                "ValidationRule": result[5],
                "ErrorMessage": result[6],
                "ValidatedAt": result[7].isoformat() if result[7] else None,
                "ValidatedBy": result[8]
            }
            logs.append(log)
        
        return {
            "limit": limit,
            "returned": len(logs),
            "logs": logs
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving recent validation logs: {str(e)}"
        )


@router.get("/validation/stats",
    summary="Get validation log statistics",
    description="Get statistics about validation failures"
)
def get_validation_stats(db: Session = Depends(get_postgres_session)):
    """
    Get statistics about validation failures.
    
    Returns:
    - Total validation failures
    - Failures by table
    - Failures by column
    - Recent failure trend
    """
    try:
        # Total failures
        total_query = text('SELECT COUNT(*) FROM "ValidationLog"')
        total_failures = db.execute(total_query).scalar()
        
        # Failures by table
        by_table_query = text("""
            SELECT "TableName", COUNT(*) as count
            FROM "ValidationLog"
            GROUP BY "TableName"
            ORDER BY count DESC
        """)
        by_table_results = db.execute(by_table_query).fetchall()
        by_table = [{"table": row[0], "count": row[1]} for row in by_table_results]
        
        # Failures by column
        by_column_query = text("""
            SELECT "ColumnName", COUNT(*) as count
            FROM "ValidationLog"
            GROUP BY "ColumnName"
            ORDER BY count DESC
        """)
        by_column_results = db.execute(by_column_query).fetchall()
        by_column = [{"column": row[0], "count": row[1]} for row in by_column_results]
        
        # Recent failures (last 24 hours)
        recent_query = text("""
            SELECT COUNT(*) 
            FROM "ValidationLog"
            WHERE "ValidatedAt" >= NOW() - INTERVAL '24 hours'
        """)
        recent_failures = db.execute(recent_query).scalar()
        
        # Most common validation rules broken
        rules_query = text("""
            SELECT "ValidationRule", COUNT(*) as count
            FROM "ValidationLog"
            GROUP BY "ValidationRule"
            ORDER BY count DESC
            LIMIT 5
        """)
        rules_results = db.execute(rules_query).fetchall()
        common_rules = [{"rule": row[0], "count": row[1]} for row in rules_results]
        
        return {
            "total_failures": total_failures or 0,
            "recent_24h": recent_failures or 0,
            "by_table": by_table,
            "by_column": by_column,
            "common_validation_rules": common_rules
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving validation statistics: {str(e)}"
        )


@router.delete("/validation/{validation_id}",
    summary="Delete a validation log entry",
    description="Delete a specific validation log by ID"
)
def delete_validation_log(
    validation_id: int,
    db: Session = Depends(get_postgres_session)
):
    """
    Delete a validation log entry by ID.
    
    - **validation_id**: The ID of the validation log to delete
    """
    try:
        # Check if log exists
        check_query = text('SELECT COUNT(*) FROM "ValidationLog" WHERE "ValidationID" = :id')
        exists = db.execute(check_query, {"id": validation_id}).scalar()
        
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Validation log with ID {validation_id} not found"
            )
        
        # Delete the log
        delete_query = text('DELETE FROM "ValidationLog" WHERE "ValidationID" = :id')
        db.execute(delete_query, {"id": validation_id})
        db.commit()
        
        return {
            "message": f"Validation log {validation_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting validation log: {str(e)}"
        )


@router.delete("/validation/clear",
    summary="Clear old validation logs",
    description="Clear validation logs older than specified days"
)
def clear_old_logs(
    days: int = 30,
    db: Session = Depends(get_postgres_session)
):
    """
    Clear validation logs older than the specified number of days.
    
    - **days**: Number of days to keep (default: 30)
    """
    try:
        if days < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days must be at least 1"
            )
        
        # Count logs to be deleted
        count_query = text("""
            SELECT COUNT(*) FROM "ValidationLog"
            WHERE "ValidatedAt" < NOW() - INTERVAL ':days days'
        """)
        count = db.execute(count_query, {"days": days}).scalar()
        
        # Delete old logs
        delete_query = text("""
            DELETE FROM "ValidationLog"
            WHERE "ValidatedAt" < NOW() - INTERVAL ':days days'
        """)
        db.execute(delete_query, {"days": days})
        db.commit()
        
        return {
            "message": f"Cleared {count or 0} validation logs older than {days} days"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing old logs: {str(e)}"
        )

