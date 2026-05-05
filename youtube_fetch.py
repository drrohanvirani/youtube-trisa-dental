from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_id, proxy=None):
    """
    Fetch clean transcript from YouTube video
    
    Args:
        video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')
        proxy: Optional proxy dict like {'http': 'http://user:pass@host:port'}
    
    Returns:
        Clean transcript text or error message
    """
    try:
        # Try with default settings
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        # Some videos need cookie/auth - try alternative method
        try:
            from youtube_transcript_api._cli import get_transcript as alt_get
            transcript_list = alt_get([video_id], proxies=proxy)
        except:
            return f"Error: Could not fetch transcript. Video might have captions disabled. Details: {str(e)}"
    
    formatter = TextFormatter()
    text = formatter.format_transcript(transcript_list)
    return text

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    import re
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]+)',
        r'(?:youtu\.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # assume it's already an ID
