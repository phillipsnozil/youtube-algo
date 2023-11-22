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


window = tk.Tk()
window.title("FINAL YouTube Search")

window.configure(bg='#2E2E2E')

style = ttk.Style()

style.configure('TButton', foreground='#FFFFFF', background='#444444', font=('calibri', 10, 'bold'), borderwidth='4')
style.configure('TLabel', foreground='#FFFFFF', background='#2E2E2E', font=('calibri', 12, 'bold'))
style.configure('TEntry', foreground='#000000', background='#FFFFFF', font=('calibri', 12))
style.configure('TCombobox', foreground='#000000', background='#FFFFFF', font=('calibri', 12))


label = ttk.Label(window, text="YouTube Video Search", style='TLabel')
label.grid(row=0, column=0, columnspan=4, pady=10)

entry = ttk.Entry(window, width=50, font=('calibri', 12))
entry.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

order_combobox = ttk.Combobox(window, values=["Date", "Alphabetical"], state="readonly", font=('calibri', 12))
order_combobox.current(0)
order_combobox.grid(row=1, column=3, padx=10, pady=10)

search_button = ttk.Button(window, text="Search", command=search_button_clicked, style='TButton')
search_button.grid(row=1, column=4, padx=10, pady=10)

result_text = scrolledtext.ScrolledText(window, width=80, height=15, wrap=tk.WORD, font=('calibri', 11))
result_text.grid(row=2, column=0, columnspan=5, pady=10)

# Separator
separator = ttk.Separator(window, orient='horizontal')
separator.grid(row=3, column=0, columnspan=5, sticky='ew', pady=10)

# Footer
footer_label = ttk.Label(window, text="© final project by ivan and phillip", font=('calibri', 8), style='TLabel')
footer_label.grid(row=4, column=0, columnspan=5)


window.mainloop()
