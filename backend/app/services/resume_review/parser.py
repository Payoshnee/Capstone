"""
Text Extraction & ATS Resume Parsing Engine.
Extracts structured candidate contact information, work history, education,
skills, and layout metadata from raw PDF bytes using deterministic heuristics.
"""
import io
import re
from typing import Dict, List, Any, Optional
from pypdf import PdfReader
from app.services.resume_review.keyword_pool import (
    PROGRAMMING_LANGUAGES,
    FRAMEWORKS_AND_LIBRARIES,
    DATABASES_AND_STORAGE,
    CLOUD_AND_DEVOPS,
    CORE_CONCEPTS,
    ALL_ACTION_VERBS
)

SECTION_PATTERNS: Dict[str, List[str]] = {
    "summary": [
        r"^(?:professional\s+)?summary\b",
        r"^objective\b",
        r"^career\s+objective\b",
        r"^profile\b",
        r"^about\s+me\b"
    ],
    "experience": [
        r"^(?:work|professional|relevant)?\s*experience\b",
        r"^employment\s+history\b",
        r"^work\s+history\b",
        r"^career\s+history\b"
    ],
    "education": [
        r"^education\b",
        r"^academic\s+background\b",
        r"^academics\b",
        r"^qualifications\b"
    ],
    "skills": [
        r"^(?:technical|core)?\s*skills\b",
        r"^technical\s+competencies\b",
        r"^technologies\s+and\s+tools\b",
        r"^skills\s+(?:&|and)\s+(?:tools|technologies)\b",
        r"^tech\s+stack\b"
    ],
    "projects": [
        r"^(?:key\s+|featured\s+|academic\s+|personal\s+)?projects\b",
        r"^technical\s+projects\b",
        r"^project\s+experience\b"
    ],
    "certifications": [
        r"^certifications?\b",
        r"^certificates?\b",
        r"^licenses?(?:\s+(?:&|and)\s+certifications)?\b",
        r"^awards?(?:\s+(?:&|and)\s+honors)?\b",
        r"^achievements\b"
    ]
}

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+91[-.\s]?\d{10}|\b\d{10}\b)')
LINKEDIN_REGEX = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)', re.IGNORECASE)
GITHUB_REGEX = re.compile(r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)', re.IGNORECASE)
URL_REGEX = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)', re.IGNORECASE)

DEGREE_PATTERNS = [
    r"\b(?:bachelor|bachelors|b\.?s\.?|b\.?tech\.?|b\.?e\.?|bca|b\.?sc\.?)\b",
    r"\b(?:master|masters|m\.?s\.?|m\.?tech\.?|m\.?e\.?|mca|m\.?sc\.?|mba)\b",
    r"\b(?:ph\.?d\.?|doctorate)\b",
    r"\b(?:associate|diploma)\b"
]

YEAR_REGEX = re.compile(r'\b(19\d\d|20\d\d)\b')
DATE_RANGE_REGEX = re.compile(
    r'(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[.\s]+)?'
    r'(\d{4})\s*(?:-|–|—|to)\s*'
    r'(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[.\s]+)?'
    r'(\d{4}|present|current)',
    re.IGNORECASE
)

def extract_text_and_layout(file_bytes: bytes) -> Dict[str, Any]:
    """Extract raw text, page count, and layout metrics from PDF bytes."""
    reader = PdfReader(io.BytesIO(file_bytes))
    page_texts: List[str] = []
    
    for page in reader.pages:
        txt = page.extract_text() or ""
        page_texts.append(txt)
        
    full_text = "\n".join(page_texts)
    lines = [line.strip() for line in full_text.splitlines() if line.strip()]
    words = [w for w in re.split(r'\s+', full_text) if w]
    
    # Bullet points heuristic detection
    bullet_lines = [
        line for line in lines 
        if line.startswith(("•", "-", "*", "▪", "–", "—", "►", "✓")) 
        or re.match(r'^\d+[\.\)]\s+', line)
    ]
    
    return {
        "full_text": full_text,
        "page_texts": page_texts,
        "page_count": max(1, len(reader.pages)),
        "lines": lines,
        "total_words": len(words),
        "total_characters": len(full_text),
        "bullet_count": len(bullet_lines),
        "bullet_lines": bullet_lines
    }

def extract_contact_info(text: str, lines: List[str]) -> Dict[str, Any]:
    """Extract candidate name, email, phone, links, and location."""
    # 1. Email
    emails = EMAIL_REGEX.findall(text)
    primary_email = emails[0].strip() if emails else None
    
    # 2. Phone
    phones = PHONE_REGEX.findall(text)
    primary_phone = phones[0].strip() if phones else None
    
    # 3. LinkedIn & GitHub
    linkedin_match = LINKEDIN_REGEX.search(text)
    linkedin = linkedin_match.group(0) if linkedin_match else None
    
    github_match = GITHUB_REGEX.search(text)
    github = github_match.group(0) if github_match else None
    
    # 4. Other Portfolio URL
    all_urls = URL_REGEX.findall(text)
    portfolio = None
    for u in all_urls:
        if "linkedin" not in u.lower() and "github" not in u.lower():
            portfolio = u
            break
            
    # 5. Candidate Name Heuristic (usually top 1-5 non-empty lines)
    name = None
    skip_keywords = ["resume", "curriculum vitae", "cv", "portfolio", "profile", "contact", "email", "phone"]
    for line in lines[:8]:
        cleaned = line.strip()
        lower_line = cleaned.lower()
        if (
            len(cleaned) >= 2 
            and len(cleaned) <= 40 
            and not any(sk in lower_line for sk in skip_keywords)
            and not EMAIL_REGEX.search(cleaned)
            and not PHONE_REGEX.search(cleaned)
            and not URL_REGEX.search(cleaned)
            and not any(cleaned.startswith(b) for b in ["•", "-", "*", "▪"])
        ):
            # Check if line looks like a human name (2-4 words, alphabetic or spaces/periods)
            words = cleaned.split()
            if 1 <= len(words) <= 4 and all(re.match(r'^[A-Za-z\.\'-]+$', w) for w in words):
                name = cleaned.title()
                break
                
    if not name and lines:
        first_line = lines[0].strip()
        if len(first_line) < 35 and not EMAIL_REGEX.search(first_line):
            name = first_line.title()

    # 6. Basic Location Heuristic
    location = None
    location_match = re.search(r'\b([A-Z][a-zA-Z\s]+,\s*[A-Z]{2}(?:\s+\d{5})?|[A-Z][a-zA-Z\s]+,\s*(?:USA|India|Canada|UK|Germany|Singapore))\b', text)
    if location_match:
        location = location_match.group(0).strip()

    return {
        "name": name or "Candidate",
        "email": primary_email,
        "phone": primary_phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "location": location
    }

def segment_sections(lines: List[str]) -> Dict[str, str]:
    """Segment resume lines into standardized semantic sections."""
    sections: Dict[str, List[str]] = {
        "header": [],
        "summary": [],
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "other": []
    }
    
    current_section = "header"
    
    for line in lines:
        cleaned_lower = line.lower().strip()
        
        # Check if line is a section heading
        matched_sec = None
        for sec_name, patterns in SECTION_PATTERNS.items():
            if any(re.search(pat, cleaned_lower) for pat in patterns):
                matched_sec = sec_name
                break
                
        if matched_sec:
            current_section = matched_sec
            continue
            
        sections[current_section].append(line)
        
    return {k: "\n".join(v) for k, v in sections.items()}

def extract_education_entries(education_text: str) -> List[Dict[str, Any]]:
    """Extract degree, institution, graduation year, and GPA from education section."""
    entries: List[Dict[str, Any]] = []
    if not education_text.strip():
        return entries
        
    lines = [line.strip() for line in education_text.splitlines() if line.strip()]
    
    current_entry: Dict[str, Any] = {
        "degree": None,
        "institution": None,
        "year": None,
        "gpa": None,
        "raw_text": ""
    }
    
    gpa_regex = re.compile(r'\b(?:gpa|cgpa)?\s*:?\s*(\d(?:\.\d{1,2})?)\s*(?:/\s*(?:4\.0|10\.0|4|10))?\b', re.IGNORECASE)
    
    for line in lines:
        # Check degree
        degree_found = None
        for pat in DEGREE_PATTERNS:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                degree_found = line
                break
                
        # Check year
        year_found = None
        ym = YEAR_REGEX.findall(line)
        if ym:
            year_found = ym[-1] # Usually graduation year
            
        # Check GPA
        gpam = gpa_regex.search(line)
        gpa_val = gpam.group(1) if gpam else None
        
        # Check Institution keywords
        is_inst = any(k in line.lower() for k in ["university", "college", "institute", "school", "academy", "polytechnic"])
        
        if degree_found or is_inst:
            if current_entry["degree"] or current_entry["institution"]:
                entries.append(current_entry)
                current_entry = {"degree": None, "institution": None, "year": None, "gpa": None, "raw_text": ""}
                
        if degree_found and not current_entry["degree"]:
            current_entry["degree"] = line
        elif is_inst and not current_entry["institution"]:
            current_entry["institution"] = line
            
        if year_found and not current_entry["year"]:
            current_entry["year"] = year_found
        if gpa_val and not current_entry["gpa"]:
            current_entry["gpa"] = gpa_val
            
        current_entry["raw_text"] += line + " "

    if current_entry["degree"] or current_entry["institution"] or current_entry["raw_text"]:
        entries.append(current_entry)
        
    return entries

def extract_work_experience_entries(experience_text: str) -> List[Dict[str, Any]]:
    """Extract individual work history roles, titles, dates, and bullet points."""
    entries: List[Dict[str, Any]] = []
    if not experience_text.strip():
        return entries
        
    lines = [line.strip() for line in experience_text.splitlines() if line.strip()]
    
    current_entry: Dict[str, Any] = {
        "title": None,
        "company": None,
        "date_range": None,
        "bullets": [],
        "raw_text": ""
    }
    
    title_keywords = [
        "engineer", "developer", "architect", "lead", "manager", "intern",
        "consultant", "analyst", "specialist", "scientist", "administrator", "associate"
    ]
    
    for line in lines:
        is_bullet = line.startswith(("•", "-", "*", "▪", "–", "—")) or re.match(r'^\d+[\.\)]\s+', line)
        date_match = DATE_RANGE_REGEX.search(line)
        
        has_title_kw = any(tk in line.lower() for tk in title_keywords)
        
        if not is_bullet and (date_match or (has_title_kw and len(line) < 80)):
            if current_entry["title"] or current_entry["company"] or current_entry["bullets"]:
                entries.append(current_entry)
                current_entry = {"title": None, "company": None, "date_range": None, "bullets": [], "raw_text": ""}
                
            if date_match and not current_entry["date_range"]:
                current_entry["date_range"] = date_match.group(0)
                
            if has_title_kw and not current_entry["title"]:
                current_entry["title"] = line
            elif not current_entry["company"]:
                current_entry["company"] = line
        else:
            cleaned_bullet = re.sub(r'^[•\-*▪–—\d\.\)]\s*', '', line).strip()
            if cleaned_bullet:
                current_entry["bullets"].append(cleaned_bullet)
                
        current_entry["raw_text"] += line + " "

    if current_entry["title"] or current_entry["company"] or current_entry["bullets"]:
        entries.append(current_entry)
        
    return entries

def extract_categorized_skills(full_text: str, skills_section_text: str) -> Dict[str, List[str]]:
    """Extract skills found in the resume categorized into technical taxonomy groups."""
    target_corpus = (skills_section_text + " " + full_text).lower()
    
    # Normalized search helper
    def find_in_corpus(keyword_set):
        found = set()
        for kw in keyword_set:
            # Word boundary check for symbols and words
            escaped = re.escape(kw)
            pattern = rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))'
            if re.search(pattern, target_corpus):
                found.add(kw)
        return sorted(list(found))
        
    languages = find_in_corpus(PROGRAMMING_LANGUAGES)
    frameworks = find_in_corpus(FRAMEWORKS_AND_LIBRARIES)
    databases = find_in_corpus(DATABASES_AND_STORAGE)
    cloud_devops = find_in_corpus(CLOUD_AND_DEVOPS)
    concepts = find_in_corpus(CORE_CONCEPTS)
    
    return {
        "languages": languages,
        "frameworks_and_libraries": frameworks,
        "databases": databases,
        "cloud_and_devops": cloud_devops,
        "concepts_and_methodologies": concepts
    }

def parse_complete_resume(file_bytes: bytes) -> Dict[str, Any]:
    """Master orchestrator extracting text, layout, contact info, sections, experience, education, and skills."""
    layout = extract_text_and_layout(file_bytes)
    sections = segment_sections(layout["lines"])
    contact = extract_contact_info(layout["full_text"], layout["lines"])
    education = extract_education_entries(sections["education"])
    experience = extract_work_experience_entries(sections["experience"])
    skills = extract_categorized_skills(layout["full_text"], sections["skills"])
    
    return {
        "layout": layout,
        "contact": contact,
        "sections": sections,
        "education": education,
        "experience": experience,
        "skills": skills
    }
