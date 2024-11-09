import webbrowser

def open_youtube():
    """Open YouTube in the default web browser."""
    webbrowser.open("https://www.youtube.com")
    
def search_video(video_name):
    """Search for a video on YouTube."""
    query = '+'.join(video_name.split())  # Format the search query
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
