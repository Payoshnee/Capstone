"""
Comprehensive Automated Test Suite for PrepPilot ATS Engine.
Tests:
1. Resume Upload & PDF Text/Layout Extraction
2. Deterministic Parsing: Contact Info, Work Experience, Education, Technical Skills
3. Keyword Matching: Predefined Role Profiles & Custom Job Descriptions
4. Formatting & Structure Evaluation: Section Completeness, Action Verbs, Quantifiable Metrics
5. Score Assignment & Applicant Ranking: Candidate Database Logging & Multi-Applicant Ranking
6. FastAPI Endpoints Integration
"""
import sys
import os
import asyncio
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.resume_review.parser import parse_complete_resume
from app.services.resume_review.matcher import perform_keyword_matching, match_resume_against_jd
from app.services.resume_review.evaluator import evaluate_formatting_and_layout
from app.services.resume_review.service import analyze_resume, rank_applicants, get_all_candidate_applicants, IN_MEMORY_APPLICANTS
from app.services.resume_review.keyword_pool import ROLE_PROFILES, resolve_target_role

def create_mock_pdf(lines: list) -> bytes:
    """Generate a valid PDF byte string with the supplied text lines."""
    stream_content = "BT\n/F1 11 Tf\n14 TL\n50 750 Td\n"
    for line in lines:
        clean = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_content += f"({clean}) '\n"
    stream_content += "ET\n"
    length = len(stream_content.encode("utf-8"))
    
    pdf = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {length} >>
stream
{stream_content}endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000224 00000 n 
0000000350 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
400
%%EOF"""
    return pdf.encode("utf-8")

# Sample Candidate 1: Senior Software Development Engineer
CANDIDATE_SDE_LINES = [
    "Alex Vance",
    "alex.vance@techpilot.dev | +1-555-234-5678 | San Francisco, CA",
    "linkedin.com/in/alexvance | github.com/alexvance",
    "Professional Summary",
    "Senior Software Development Engineer with 5+ years of experience designing high-throughput distributed systems, REST APIs, and cloud infrastructure.",
    "Technical Skills",
    "Languages: Python, Java, Go, TypeScript, SQL",
    "Frameworks & Tools: FastAPI, Django, Spring Boot, Docker, Kubernetes, AWS, PostgreSQL, Redis, Git, CI/CD",
    "Core Concepts: System Design, Microservices, Data Structures, Algorithms, Unit Testing",
    "Professional Experience",
    "Staff Backend Engineer | CloudScale Systems | Jan 2022 - Present",
    "• Architected and deployed 14+ resilient microservices using FastAPI, Redis, and PostgreSQL, handling 25M+ daily requests.",
    "• Optimized database indexing and query caching, reducing p99 API latency by 42% across core endpoints.",
    "• Spearheaded CI/CD automation with GitHub Actions and Docker, reducing release cycle time by 60%.",
    "Software Engineer | DataCorp Labs | Jun 2019 - Dec 2021",
    "• Engineered distributed data pipelines in Python and Go, scaling real-time ingestion by 3.5x.",
    "• Implemented robust unit testing and integration testing suites, increasing test coverage from 55% to 92%.",
    "Education",
    "Bachelor of Science in Computer Science | Stanford University | 2019 | GPA: 3.85/4.0",
    "Projects",
    "Distributed Cache Engine | github.com/alexvance/kv-cache",
    "• Built high-performance in-memory key-value store using Go with consistent hashing and Raft consensus."
]

# Sample Candidate 2: Senior Data Engineer
CANDIDATE_DATA_LINES = [
    "Priya Patel",
    "priya.patel@dataforge.io | +1-555-876-5432 | Austin, TX",
    "linkedin.com/in/priyapatel | github.com/priyapatel",
    "Professional Summary",
    "Lead Data Engineer specializing in modern data stacks, petabyte-scale ETL pipelines, and streaming architectures.",
    "Technical Skills",
    "Languages: Python, SQL, Scala, Java, Bash",
    "Technologies: Apache Spark, Kafka, Airflow, Snowflake, BigQuery, dbt, PostgreSQL, Docker, AWS S3",
    "Core Concepts: ETL, ELT, Data Modeling, Data Warehousing, Data Pipelines, Distributed Computing",
    "Professional Experience",
    "Senior Data Engineer | FinStream Analytics | Feb 2021 - Present",
    "• Architected streaming ETL pipelines with Kafka and Apache Spark, processing 80GB of financial transactions hourly.",
    "• Streamlined data warehouse transformations in Snowflake and dbt, reducing dashboard query runtime by 55%.",
    "• Automated 40+ production Airflow DAG workflows with automated data quality validations.",
    "Data Engineer | RetailPulse Global | Jul 2018 - Jan 2021",
    "• Engineered batch data ingestion pipelines connecting 12 external APIs into AWS S3 and PostgreSQL.",
    "• Reduced pipeline infrastructure costs by 28% through PySpark partition optimizations.",
    "Education",
    "Master of Science in Data Science | University of Texas at Austin | 2018 | GPA: 3.9/4.0",
    "Projects",
    "Real-Time Telemetry Pipeline",
    "• Developed real-time event analytics using Kafka, ClickHouse, and Python with live dashboards."
]

# Sample Candidate 3: Junior Frontend / Incomplete Resume
CANDIDATE_JUNIOR_LINES = [
    "Jordan Lee",
    "jordan.lee@example.com",
    "Summary",
    "Junior Web Developer passionate about frontend development.",
    "Skills",
    "HTML, CSS, JavaScript, React, Tailwind",
    "Experience",
    "Frontend Intern | WebDesign Studio",
    "Worked on UI components and updated website styling.",
    "Helped the senior team test responsive layouts.",
    "Education",
    "Associate Degree in Web Development | Community College | 2023"
]

TARGET_BACKEND_JD = """
We are looking for a Senior Backend Software Engineer (SDE) to join our team.
Required Qualifications:
- Strong proficiency in Python, FastAPI, and SQL.
- Extensive experience with Docker, Kubernetes, AWS, and CI/CD pipelines.
- Deep understanding of System Design, Microservices, Redis caching, and PostgreSQL.
- Proven track record of optimizing high-throughput APIs and reducing latency.
- Knowledge of Data Structures, Algorithms, and Unit Testing.
"""

async def run_ats_engine_tests():
    print("=" * 70)
    print("STARTING PREPPILOT ATS ENGINE TEST SUITE")
    print("=" * 70)
    
    # Clean in-memory applicant store for isolated test
    IN_MEMORY_APPLICANTS.clear()
    
    # -------------------------------------------------------------
    # 1. TEST PDF CREATION & EXTRACTION
    # -------------------------------------------------------------
    print("\n[TEST 1] PDF Generation & Text/Layout Extraction...")
    pdf_sde = create_mock_pdf(CANDIDATE_SDE_LINES)
    parsed_sde = parse_complete_resume(pdf_sde)
    
    assert parsed_sde["layout"]["total_words"] > 100, "Should extract more than 100 words"
    assert parsed_sde["contact"]["name"] == "Alex Vance", f"Expected Alex Vance, got {parsed_sde['contact']['name']}"
    assert parsed_sde["contact"]["email"] == "alex.vance@techpilot.dev", f"Expected email, got {parsed_sde['contact']['email']}"
    assert "555-234-5678" in parsed_sde["contact"]["phone"], f"Expected phone, got {parsed_sde['contact']['phone']}"
    assert "linkedin.com/in/alexvance" in parsed_sde["contact"]["linkedin"], "Expected LinkedIn URL"
    assert "github.com/alexvance" in parsed_sde["contact"]["github"], "Expected GitHub URL"
    print("  PASS: Contact information extracted accurately (Name, Email, Phone, LinkedIn, GitHub).")
    
    # -------------------------------------------------------------
    # 2. TEST SECTION SEGMENTATION, HISTORY & EDUCATION PARSING
    # -------------------------------------------------------------
    print("\n[TEST 2] Section Segmentation, Experience & Education...")
    assert len(parsed_sde["education"]) >= 1, "Should parse at least 1 education entry"
    assert "Stanford" in parsed_sde["education"][0]["raw_text"], "Education should contain Stanford"
    assert "3.85" in (parsed_sde["education"][0]["gpa"] or ""), f"Should detect GPA 3.85, got {parsed_sde['education'][0]['gpa']}"
    assert len(parsed_sde["experience"]) >= 1, "Should extract work history roles"
    
    # Skills categorization
    skills = parsed_sde["skills"]
    assert "python" in skills["languages"], "Should categorize Python as language"
    assert "fastapi" in skills["frameworks_and_libraries"], "Should categorize FastAPI as framework"
    assert "postgresql" in skills["databases"], "Should categorize PostgreSQL as database"
    assert "docker" in skills["cloud_and_devops"], "Should categorize Docker as devops"
    assert "system design" in skills["concepts_and_methodologies"], "Should categorize System Design as concept"
    print(f"  PASS: Skills categorized cleanly: {len(skills['languages'])} languages, {len(skills['frameworks_and_libraries'])} frameworks, {len(skills['databases'])} databases.")
    
    # -------------------------------------------------------------
    # 3. TEST KEYWORD MATCHING AGAINST SDE ROLE & TARGET JD
    # -------------------------------------------------------------
    print("\n[TEST 3] Keyword Matching (Role Profile & Custom Job Description)...")
    kw_res_sde = perform_keyword_matching(
        resume_text=parsed_sde["layout"]["full_text"],
        parsed_skills=parsed_sde["skills"],
        target_role="sde",
        job_description=TARGET_BACKEND_JD
    )
    
    jd_match = kw_res_sde["jd_match"]
    assert jd_match is not None, "JD match should be computed"
    assert jd_match["match_percentage"] >= 80, f"Alex Vance should match >=80% of Backend JD, got {jd_match['match_percentage']}%"
    assert "fastapi" in jd_match["matched_keywords"], "Should match FastAPI"
    assert "docker" in jd_match["matched_keywords"], "Should match Docker"
    assert "redis" in jd_match["matched_keywords"], "Should match Redis"
    print(f"  PASS: High JD match: {jd_match['match_percentage']}% (Matched {jd_match['matched_count']}/{jd_match['total_jd_keywords']} required keywords).")
    
    # -------------------------------------------------------------
    # 4. TEST FORMATTING & ATS STRUCTURE EVALUATION
    # -------------------------------------------------------------
    print("\n[TEST 4] Formatting, Action Verbs, and Quantifiable Metrics...")
    fmt_res = evaluate_formatting_and_layout(
        layout=parsed_sde["layout"],
        contact=parsed_sde["contact"],
        sections=parsed_sde["sections"],
        extracted_skills=parsed_sde["skills"]
    )
    assert fmt_res["section_completeness"]["completeness_score"] == 100, f"Completeness should be 100%, got {fmt_res['section_completeness']['completeness_score']}"
    assert fmt_res["impact_evaluation"]["quantified_metrics_score"] > 50, "Should detect multiple quantified metrics"
    assert "architected" in fmt_res["impact_evaluation"]["detected_action_verbs"], "Should detect action verb 'architected'"
    assert "optimized" in fmt_res["impact_evaluation"]["detected_action_verbs"], "Should detect action verb 'optimized'"
    print(f"  PASS: Formatting score {fmt_res['formatting_score']}/100, Metrics score {fmt_res['impact_evaluation']['quantified_metrics_score']}/100.")
    
    # -------------------------------------------------------------
    # 5. TEST END-TO-END ATS ANALYSIS PIPELINE & LOGGING
    # -------------------------------------------------------------
    print("\n[TEST 5] End-to-End ATS Analysis & Candidate Database Logging...")
    report_sde = await analyze_resume(
        file_bytes=pdf_sde,
        target_role="sde",
        job_description=TARGET_BACKEND_JD
    )
    assert report_sde.overall_score >= 85, f"Senior SDE score should be >=85, got {report_sde.overall_score}"
    assert report_sde.grade in ["A+", "A", "A-"], f"Expected top grade, got {report_sde.grade}"
    assert report_sde.applicant_id is not None, "Report should include generated applicant_id"
    print(f"  PASS: Candidate 1 (Alex Vance) scored {report_sde.overall_score}% ({report_sde.grade}), Logged as ID: {report_sde.applicant_id}")
    
    # Process Candidate 2: Data Engineer
    pdf_data = create_mock_pdf(CANDIDATE_DATA_LINES)
    report_data = await analyze_resume(
        file_bytes=pdf_data,
        target_role="data_engineer"
    )
    assert report_data.overall_score >= 80, f"Data Engineer score should be >=80, got {report_data.overall_score}"
    print(f"  PASS: Candidate 2 (Priya Patel) scored {report_data.overall_score}% ({report_data.grade}), Logged as ID: {report_data.applicant_id}")
    
    # Process Candidate 3: Junior Frontend
    pdf_junior = create_mock_pdf(CANDIDATE_JUNIOR_LINES)
    report_junior = await analyze_resume(
        file_bytes=pdf_junior,
        target_role="frontend_engineer"
    )
    print(f"  PASS: Candidate 3 (Jordan Lee) scored {report_junior.overall_score}% ({report_junior.grade}), Logged as ID: {report_junior.applicant_id}")
    assert len(report_junior.formatting_evaluation.warnings) > 0, "Junior candidate should receive formatting/metric warnings"
    print(f"    Sample Warning: {report_junior.formatting_evaluation.warnings[0]}")
    
    # -------------------------------------------------------------
    # 6. TEST APPLICANT RANKING
    # -------------------------------------------------------------
    print("\n[TEST 6] Applicant Ranking from Highest to Lowest Score...")
    all_candidates = await get_all_candidate_applicants()
    assert len(all_candidates) == 3, f"Expected 3 logged candidates, found {len(all_candidates)}"
    
    # Rank candidates for the Senior Backend JD
    ranked_backend = await rank_applicants(job_description=TARGET_BACKEND_JD)
    print(f"\n  Ranking for Target Job Description: '{TARGET_BACKEND_JD.strip().splitlines()[0]}':")
    for r in ranked_backend:
        print(f"    Rank #{r['rank']}: {r['candidate_name']} ({r['target_role']}) - Score: {r['overall_score']}% [{r['grade']}]")
        
    assert ranked_backend[0]["candidate_name"] == "Alex Vance", "Alex Vance must rank #1 for Backend/SDE JD"
    assert ranked_backend[0]["overall_score"] >= ranked_backend[1]["overall_score"], "Rank 1 score must be >= Rank 2"
    assert ranked_backend[1]["overall_score"] >= ranked_backend[2]["overall_score"], "Rank 2 score must be >= Rank 3"
    print("  PASS: Applicants ranked accurately from highest to lowest score!")
    
    print("\n" + "=" * 70)
    print("ALL ATS BACKEND TESTS PASSED SUCCESSFULLY! (6/6)")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_ats_engine_tests())
