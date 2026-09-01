import json
from openai import OpenAI
from config import AI_API_KEY, AI_BASE_URL, OPENAI_MODEL

_client = None

def _get_client():
    global _client
    if _client is None:
        if AI_BASE_URL:
            _client = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)
        else:
            _client = OpenAI(api_key=AI_API_KEY)
    return _client


async def optimize_resume(
    resume_text: str,
    job_description: str,
    job_title: str = "",
    company: str = "",
) -> str:
    """
    Optimize a resume for ATS and a specific job description.
    Returns the optimized resume text in markdown format.
    """
    system_prompt = """You are an expert resume writer and ATS (Applicant Tracking System) optimization specialist. 
Your job is to rewrite resumes to:

1. **ATS Optimization**: Include keywords from the job description naturally throughout the resume
2. **Quantify Achievements**: Convert vague statements into measurable, quantified accomplishments
3. **Strong Action Verbs**: Start each bullet point with powerful action verbs
4. **Clean Formatting**: Use clean, ATS-friendly formatting (no tables, columns, or graphics)
5. **Relevance**: Prioritize skills and experiences most relevant to the target job
6. **Professional Summary**: Write a compelling 3-4 line professional summary at the top
7. **Skills Section**: Organize technical and soft skills matching the job requirements

Return the optimized resume in clean markdown format with these sections:
- Professional Summary
- Skills (grouped by category)
- Professional Experience (with quantified achievements)
- Education
- Certifications (if applicable)

Make sure EVERY bullet point has a number or percentage. Don't use generic language — be specific and impactful."""

    user_prompt = f"""Please optimize the following resume for this specific job:

**Target Job Title**: {job_title}
**Company**: {company}

**Job Description**:
{job_description[:3000]}

**Original Resume**:
{resume_text[:5000]}

Rewrite this resume to maximize ATS matching and make it stand out. Focus on quantifiable achievements and keywords from the job description."""

    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=4000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error optimizing resume: {str(e)}"


async def generate_cover_letter(
    resume_text: str,
    job_description: str,
    job_title: str = "",
    company: str = "",
) -> str:
    """
    Generate a compelling cover letter tailored to the job.
    """
    system_prompt = """You are an expert cover letter writer. Write compelling, personalized cover letters that:

1. Open with a strong hook showing genuine interest in the company
2. Connect the candidate's experience directly to the job requirements
3. Use specific, quantified examples from the resume
4. Show knowledge of the company and its mission
5. End with a confident call to action
6. Keep it to 3-4 concise paragraphs
7. Professional but warm tone

Return in clean markdown format. Include the date, company address block, and proper salutation."""

    user_prompt = f"""Write a cover letter for this position:

**Job Title**: {job_title}
**Company**: {company}

**Job Description**:
{job_description[:3000]}

**Candidate's Resume**:
{resume_text[:4000]}

Write a cover letter that connects the candidate's experience to the specific job requirements."""

    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"


async def generate_linkedin_tips(
    resume_text: str,
    job_description: str,
    job_title: str = "",
) -> str:
    """
    Generate LinkedIn profile optimization tips.
    """
    system_prompt = """You are a LinkedIn optimization expert. 
Analyze the resume and job description, then provide specific LinkedIn profile optimization tips.
Return in markdown format with bullet points for each section: Headline, About, Featured, Skills, and Activity."""

    user_prompt = f"""Analyze this resume and provide LinkedIn optimization tips for:
**Target Job**: {job_title}

**Job Description**:
{job_description[:2000]}

**Resume**:
{resume_text[:3000]}

Provide specific, actionable tips in markdown format."""

    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating LinkedIn tips: {str(e)}"