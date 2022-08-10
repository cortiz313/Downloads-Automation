import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import shutil


source_dir = "/Users/corti/Downloads"
dest_dir_images = '/Users/corti/OneDrive/Documents/Downloaded Images'
dest_dir_videos = '/Users/corti/OneDrive/Documents/Downloaded Videos'
dest_dir_sounds = '/Users/corti/OneDrive/Documents/Downloaded Sounds'
dest_dir_pdfs = '/Users/corti/OneDrive/Documents/Downloaded PDFs'

with os.scandir(source_dir) as entries:
    for entry in entries:
        print(entry.name)

def makeUnique(name):
    name = name + "1"
    return name

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)

class MoverHandler(LoggingEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png') or name.endswith('.svg'):
                    dest = dest_dir_images
                    move(dest, entry, name)
                elif name.endswith('.wav') or name.endswith('.mp3'):
                    dest = dest_dir_sounds
                    move(dest, entry, name)
                elif name.endswith('.mov') or name.endswith('.mp4'):
                    dest = dest_dir_videos
                    move(dest, entry, name)
                elif name.endswith('.pdf'):
                    dest = dest_dir_pdfs
                    move(dest, entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()