"""
FastAPI HTTP Integration Tests for Resume Review & ATS Endpoints:
- GET /api/resume/health
- GET /api/resume/keywords
- POST /api/resume/analyze
- GET /api/resume/candidates
- POST /api/resume/rank
- POST /api/resume/match-jd
"""
import sys
import io
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.main import app
from tests.test_ats_engine import create_mock_pdf, CANDIDATE_SDE_LINES, CANDIDATE_DATA_LINES, TARGET_BACKEND_JD

client = TestClient(app)

def test_api_health():
    res = client.get("/api/resume/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    print("  [API] /health passed")

def test_api_keywords():
    res = client.get("/api/resume/keywords")
    assert res.status_code == 200
    data = res.json()["data"]
    assert "roles" in data
    assert len(data["roles"]) >= 9
    assert "programming_languages" in data
    assert "python" in data["programming_languages"]
    print(f"  [API] /keywords passed ({len(data['roles'])} roles, {len(data['programming_languages'])} languages)")

def test_api_analyze_and_rank():
    # 1. Upload Alex Vance
    pdf_bytes = create_mock_pdf(CANDIDATE_SDE_LINES)
    files = {"file": ("alex_vance_resume.pdf", pdf_bytes, "application/pdf")}
    data = {
        "target_role": "sde",
        "job_description": TARGET_BACKEND_JD,
        "candidate_name": "Alex Vance",
        "candidate_email": "alex.vance@techpilot.dev"
    }
    res = client.post("/api/resume/analyze", files=files, data=data)
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["error"] is None
    report = json_data["data"]
    assert report["overall_score"] >= 85
    assert report["applicant_id"] is not None
    assert report["parsed_data"]["contact"]["name"] == "Alex Vance"
    print(f"  [API] /analyze passed (Score: {report['overall_score']}, ID: {report['applicant_id']})")
    
    # 2. Upload Priya Patel
    pdf_data = create_mock_pdf(CANDIDATE_DATA_LINES)
    files2 = {"file": ("priya_patel_resume.pdf", pdf_data, "application/pdf")}
    res2 = client.post("/api/resume/analyze", files=files2, data={"target_role": "data_engineer"})
    assert res2.status_code == 200
    assert res2.json()["data"]["overall_score"] >= 80
    print("  [API] /analyze second candidate passed")

    # 3. List candidates
    res_list = client.get("/api/resume/candidates")
    assert res_list.status_code == 200
    candidates = res_list.json()["data"]
    assert len(candidates) >= 2
    print(f"  [API] /candidates passed ({len(candidates)} candidates in database)")

    # 4. Rank applicants
    res_rank = client.post("/api/resume/rank", json={"job_description": TARGET_BACKEND_JD})
    assert res_rank.status_code == 200
    ranking = res_rank.json()["data"]
    assert ranking["total_applicants"] >= 2
    ranked_list = ranking["ranked_applicants"]
    assert ranked_list[0]["rank"] == 1
    assert ranked_list[0]["candidate_name"] == "Alex Vance"
    print(f"  [API] /rank passed: Rank #1 is {ranked_list[0]['candidate_name']} ({ranked_list[0]['overall_score']}%)")

    # 5. Match JD
    res_jd = client.post("/api/resume/match-jd", json={
        "applicant_id": report["applicant_id"],
        "job_description": TARGET_BACKEND_JD
    })
    assert res_jd.status_code == 200
    jd_res = res_jd.json()["data"]
    assert jd_res["match_percentage"] >= 80
    print(f"  [API] /match-jd passed ({jd_res['match_percentage']}% match)")

if __name__ == "__main__":
    test_api_health()
    test_api_keywords()
    test_api_analyze_and_rank()
    print("\nALL FASTAPI INTEGRATION TESTS PASSED!")
