import tkinter as tk
from tkinter import ttk, scrolledtext
import yt_dlp


def youtube_search(query, max_results=10, order='date'):
    try:
        ydl = yt_dlp.YoutubeDL()
        search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

        videos = []

        for i, result in enumerate(search_results['entries'], start=1):
            video_id = result['id']
            title = result['title']
            videos.append({'title': title, 'video_id': video_id})

        if order == 'date':
            return videos
        elif order == 'alphabetical':
            return quicksort(videos, key=lambda x: x['title'].lower())
        else:
            return sorted(videos, key=lambda x: x['title'].lower(), reverse=True)

    except yt_dlp.utils.DownloadError as e:
        print(f"Search failed: {e}")
        return []


def quicksort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if key(x) < key(pivot)]
    middle = [x for x in arr if key(x) == key(pivot)]
    right = [x for x in arr if key(x) > key(pivot)]
    return quicksort(left, key) + middle + quicksort(right, key)


def search_button_clicked():
    query = entry.get()
    selected_order = order_combobox.get()

    if selected_order == "Date":
        order_param = "date"
    elif selected_order == "Alphabetical":
        order_param = "alphabetical"
    else:
        order_param = "relevance"

    search_results = youtube_search(query, order=order_param)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    for i, result in enumerate(search_results, start=1):
        result_text.insert(tk.END, f"{i}. {result['title']} (Video ID: {result['video_id']})\n")

    result_text.config(state=tk.DISABLED)
