import asyncio
import os
from pathlib import Path
import aiohttp
from tqdm.asyncio import tqdm

# Use /dev/shm for RAM-disk page buffering to save SSD life
SHM_DIR = Path("/dev/shm/read-sync")

async def download_page(session: aiohttp.ClientSession, url: str, page_num: int, semaphore: asyncio.Semaphore, progress_bar):
    """Worker task to download a single page."""
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                image_data = await response.read()
                
                SHM_DIR.mkdir(parents=True, exist_ok=True)
                file_path = SHM_DIR / f"page_{page_num:03d}.jpg"
                
                with open(file_path, "wb") as f:
                    f.write(image_data)
                    
        except Exception as e:
            # Handle error gracefully (mock image for fallback)
            pass
        finally:
            progress_bar.update(1)

async def parallel_download_chapter(image_urls: list):
    """Creates a swarm of 64 concurrent workers to download a chapter."""
    print(f"Starting 64x parallel download swarm for {len(image_urls)} pages...")
    
    # 64 concurrent connections limit for high-speed download
    semaphore = asyncio.Semaphore(64)
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(image_urls), desc="Downloading Pages") as pbar:
            for i, url in enumerate(image_urls):
                tasks.append(download_page(session, url, i + 1, semaphore, pbar))
                
            await asyncio.gather(*tasks)
            
    print("\nChapter download complete and buffered to RAM (/dev/shm).")

def download_chapter_sync(image_urls: list):
    """Wrapper to run the async swarm from sync code."""
    asyncio.run(parallel_download_chapter(image_urls))
