import asyncio
import os
from pathlib import Path

# Use /dev/shm for RAM-disk page buffering to save SSD life
SHM_DIR = Path("/dev/shm/read-sync")

async def download_page(url: str, page_num: int, semaphore: asyncio.Semaphore):
    """Worker task to download a single page."""
    async with semaphore:
        # Mock download delay
        await asyncio.sleep(0.5)
        
        SHM_DIR.mkdir(parents=True, exist_ok=True)
        file_path = SHM_DIR / f"page_{page_num:03d}.jpg"
        
        # Write dummy byte data
        with open(file_path, "wb") as f:
            f.write(b"MOCK_IMAGE_DATA")
            
        print(f"Downloaded page {page_num} to {file_path}")

async def parallel_download_chapter(chapter_url: str, total_pages: int):
    """Creates a swarm of 64 concurrent workers to download a chapter."""
    print(f"Starting 64x parallel download swarm for {chapter_url}...")
    
    # 64 concurrent connections limit
    semaphore = asyncio.Semaphore(64)
    
    tasks = []
    for i in range(1, total_pages + 1):
        tasks.append(download_page(f"{chapter_url}/{i}.jpg", i, semaphore))
        
    await asyncio.gather(*tasks)
    print("Chapter download complete and buffered to RAM.")

def download_chapter_sync(chapter_url: str, total_pages: int):
    """Wrapper to run the async swarm from sync code."""
    asyncio.run(parallel_download_chapter(chapter_url, total_pages))
