from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_transcript(text, model="gpt-4o-mini"):
    """
    Analyze transcript and return structured insights
    """
    if len(text) < 100:
        return {"error": "Transcript too short or empty"}
    
    prompt = f"""
You are a viral content analyst. Analyze this transcript and return ONLY valid JSON with this exact structure:

{{
    "hooks": ["hook1", "hook2", "hook3", "hook4", "hook5"],
    "emotional_triggers": ["fear", "curiosity", "outrage", "hope", "surprise"],
    "viral_patterns": ["pattern1", "pattern2"],
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "video_ideas": ["idea1", "idea2", "idea3", "idea4", "idea5"],
    "high_retention_hooks": ["hook1", "hook2", "hook3", "hook4", "hook5"],
    "best_timestamp": "MM:SS",
    "content_structure": "hook -> problem -> solution -> cta"
}}

Transcript:
{text[:7000]}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        # Clean markdown JSON if present
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw": result}
    except Exception as e:
        return {"error": str(e)}

def generate_script(hook, topic, duration_sec=30):
    """Generate a short script from a hook + topic"""
    prompt = f"""
Create a {duration_sec}-second viral script:

Hook: "{hook}"
Topic: {topic}

Format as:
HOOK (first 3 seconds):
BODY (problem → solution):
CTA (call to action):

Keep it punchy, conversational, under 80 words total.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content
