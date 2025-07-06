import os
from collections import Counter
from datetime import datetime

def generate_stats_html(success_log, failed_log, output_file):
    total_downloads = 0
    total_failures = 0
    channels = []

    # Load successes
    if os.path.exists(success_log):
        with open(success_log, "r", encoding="utf-8") as f:
            success_lines = [line.strip() for line in f if line.strip()]
        total_downloads = len(success_lines)
        for line in success_lines:
            if "https://www.youtube.com/" in line and "/channel/" in line:
                channel_id = line.split("/channel/")[1].split("/")[0]
                channels.append(channel_id)
    else:
        pass

    # Load failures
    if os.path.exists(failed_log):
        with open(failed_log, "r", encoding="utf-8") as f:
            failed_lines = [line.strip() for line in f if line.strip()]
        total_failures = len(failed_lines)
    else:
        pass

    # Top channels
    top_channels = Counter(channels).most_common(5)

    # HTML Report
    html = f"""
    <html>
    <head>
        <title>YouTube Downloader Stats</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }}
            .card {{ background: #fff; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
        </style>
    </head>
    <body>
        <h1>📊 YouTube Download Stats</h1>
        <div class="card">
            <h2>Overview</h2>
            <p><strong>Total Downloads:</strong> {total_downloads}</p>
            <p><strong>Failed Downloads:</strong> {total_failures}</p>
            <p><strong>Last Updated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    """

    if top_channels:
        html += """
        <div class="card">
            <h2>Top Downloaded Channels</h2>
            <table>
                <tr><th>Channel ID</th><th>Downloads</th></tr>
        """
        for ch, count in top_channels:
            html += f"<tr><td>{ch}</td><td>{count}</td></tr>"
        html += "</table></div>"

    html += "</body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[STATS] Dashboard saved to: {output_file}")
