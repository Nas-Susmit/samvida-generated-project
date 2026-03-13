# Routes for high score API
from fastapi import APIRouter, HTTPException
from backend.models import HighScore
from backend.database import db
router = APIRouter()
@router.post('/api/scores')
def submit_score(player_name: str, score: int):
    if score < 0:
        raise HTTPException(status_code=400, detail='Score must be non-negative')
    high_score = HighScore(player_name=player_name, score=score)
    db.add(high_score)
    db.commit()
    return {'message': 'Score submitted successfully', 'score_id': high_score.id}
@router.get('/api/scores')
def get_high_scores(limit: int = 10):
    high_scores = db.query(HighScore).order_by(HighScore.score.desc()).limit(limit).all()
    return [{'player_name': score.player_name, 'score': score.score} for score in high_scores]
