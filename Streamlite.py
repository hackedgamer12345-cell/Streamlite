from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Welcome to StreamLite 🎬</h1>
    <form action="/search" method="get">
        Search Videos: <input type="text" name="query" style="width:300px;">
        <input type="submit" value="Search">
    </form>
    '''

@app.route('/search')
def search():
    query = request.args.get("query")
    if not query:
        return "No search query provided"

    try:
        ydl_opts = {'quiet': True, 'extract_flat': 'in_playlist', 'force_generic_extractor': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch10:{query}", download=False)
        
        results = ""
        for entry in info['entries']:
            results += f'<li><a href="/watch?url=https://www.youtube.com/watch?v={entry["id"]}">{entry["title"]}</a></li>'
        
        return f'''
        <h2>Search results for: {query}</h2>
        <ul>{results}</ul>
        <br><a href="/">Back</a>
        '''
    except Exception as e:
        return f"Error: {e}"

@app.route('/watch')
def watch():
    url = request.args.get("url")
    quality = request.args.get("quality", "360p")

    if not url:
        return "No URL provided"

    try:
        quality_map = {
            "240p": "133+140",
            "360p": "18",
            "480p": "135+140",
            "720p": "22"
        }

        ydl_opts = {
            'quiet': True,
            'format': quality_map.get(quality, "18")
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']

        html = f'''
        <h2>{info.get("title", "StreamLite Video")}</h2>
        <form method="get" action="/watch">
            <input type="hidden" name="url" value="{url}">
            <label for="quality">Choose quality:</label>
            <select name="quality" onchange="this.form.submit()">
                <option value="240p" {"selected" if quality=="240p" else ""}>240p</option>
                <option value="360p" {"selected" if quality=="360p" else ""}>360p</option>
                <option value="480p" {"selected" if quality=="480p" else ""}>480p</option>
                <option value="720p" {"selected" if quality=="720p" else ""}>720p</option>
            </select>
        </form>
        <br>
        <video controls width="640" autoplay>
            <source src="{video_url}" type="video/mp4">
            Your browser does not support video.
        </video>
        <br><a href="/">Home</a>
        '''
        return render_template_string(html)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
