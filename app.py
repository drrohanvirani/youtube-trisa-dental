import os
from dotenv import load_dotenv
from youtube_fetch import get_transcript, extract_video_id
from analyzer import analyze_transcript, generate_script
import json
from datetime import datetime

load_dotenv()

def save_results(video_id, insights):
    """Save insights to a JSON file for later reference"""
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(insights, f, indent=2)
    print(f"\n💾 Saved to {filename}")

def run_single(video_input):
    """Analyze a single video"""
    video_id = extract_video_id(video_input)
    print(f"\n🎬 Analyzing: https://youtube.com/watch?v={video_id}")
    
    print("📝 Fetching transcript...")
    text = get_transcript(video_id)
    
    if text.startswith("Error"):
        print(f"❌ {text}")
        return None
    
    print("🧠 Running AI analysis...")
    insights = analyze_transcript(text)
    
    if "error" in insights:
        print(f"❌ Analysis failed: {insights['error']}")
        return None
    
    print("\n" + "="*60)
    print("📊 VIRAL INSIGHTS")
    print("="*60)
    
    print("\n🔥 TOP HOOKS:")
    for hook in insights.get('hooks', [])[:5]:
        print(f"  • {hook}")
    
    print("\n💡 VIDEO IDEAS:")
    for idea in insights.get('video_ideas', [])[:5]:
        print(f"  • {idea}")
    
    print("\n🎯 VIRAL PATTERNS:")
    for pattern in insights.get('viral_patterns', []):
        print(f"  • {pattern}")
    
    save_results(video_id, insights)
    return insights

def batch_analyze(video_ids):
    """Analyze multiple videos"""
    results = {}
    for vid in video_ids:
        results[vid] = run_single(vid)
    return results

def main():
    print("🚀 Viral Content Engine")
    print("-" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Analyze single video")
        print("2. Analyze batch (pre-defined list)")
        print("3. Generate script from hook")
        print("4. Exit")
        
        choice = input("\nChoose (1-4): ").strip()
        
        if choice == "1":
            url = input("Enter YouTube URL or Video ID: ")
            run_single(url)
            
        elif choice == "2":
            print("Edit video_ids list in app.py or enter comma-separated IDs:")
            ids = input("Video IDs (comma separated): ").split(',')
            batch_analyze([id.strip() for id in ids])
            
        elif choice == "3":
            hook = input("Enter hook: ")
            topic = input("Enter topic: ")
            script = generate_script(hook, topic)
            print("\n📝 GENERATED SCRIPT:\n")
            print(script)
            
        elif choice == "4":
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
