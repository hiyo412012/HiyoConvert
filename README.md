# HiyoConvert 🎵

> Batch audio converter with multithreading — fast, smart, easy.  
> Công cụ chuyển đổi audio hàng loạt với đa luồng — nhanh, thông minh, dễ dùng.

---

## Features / Tính năng

| English | Tiếng Việt |
|---------|------------|
| ✅ Batch convert audio files (MP3, OGG, FLAC, WAV, AAC, Opus) | ✅ Chuyển đổi audio hàng loạt (MP3, OGG, FLAC, WAV, AAC, Opus) |
| ✅ Multithreading (auto CPU-1 threads) | ✅ Đa luồng thông minh (tự động CPU-1 luồng) |
| ✅ 19 preset conversion types + custom | ✅ 19 loại chuyển đổi có sẵn + tùy chỉnh |
| ✅ Interactive menu — just run and choose | ✅ Menu tương tác — chỉ cần chạy và chọn |
| ✅ Auto-skip already converted files | ✅ Tự động bỏ qua file đã convert |
| ✅ Option to keep or delete originals | ✅ Tuỳ chọn giữ hoặc xóa file gốc |
| ✅ Strip metadata option (privacy) | ✅ Tuỳ chọn xoá metadata (riêng tư) |
| ✅ Simplify filenames (strip artist, special chars) | ✅ Tuỳ chọn rút gọn tên file |
| ✅ Auto-setup with setup.bat / setup.sh | ✅ Tự động cài đặt với setup.bat / setup.sh |

---

## Quick Start / Bắt đầu nhanh

### Windows

```bash
# Auto setup (installs Python + ffmpeg)
setup.bat

# Or manual
winget install -e --id Python.Python.3.14
winget install -e --id Gyan.FFmpeg

# Run
python hiyo-convert.py
python hiyo-convert.py "D:\Music"
```

### Linux / macOS

```bash
# Auto setup
chmod +x setup.sh && ./setup.sh

# Or manual (Linux)
sudo apt install -y python3 ffmpeg

# Or manual (macOS)
brew install python ffmpeg

# Run
python3 hiyo-convert.py
python3 hiyo-convert.py /home/user/Music
```

### 3. Just choose / Chỉ cần chọn

```
Select language:
[1] English
[2] Tiếng Việt

Conversion type:
[1]  MP3 → OGG (Vorbis)
[2]  MP3 → FLAC (Lossless)
...
[19] ALL → WAV
[C]  Custom / Tùy chỉnh

Select directories:
[1] AlbumA
[2] AlbumB
[A] All

Keep original files? (y/N):
Strip metadata? (y/N):
Simplify file names? (y/N):
```

---

## Requirements / Yêu cầu

- **Python 3.7+**
  - Windows: `winget install -e --id Python.Python.3.14`
  - Linux: `sudo apt install -y python3 python3-pip python3-venv`
  - macOS: `brew install python@3.14`
- **ffmpeg**
  - Windows: `winget install -e --id Gyan.FFmpeg` (run as Admin)
  - Linux: `sudo apt install -y ffmpeg`
  - macOS: `brew install ffmpeg`

---

## Supported Conversions / Các loại chuyển đổi

| From → To | Codec | Quality |
|-----------|-------|---------|
| MP3 → OGG | libvorbis | `-q:a 0-10` |
| MP3 → FLAC | flac | `-compression_level 0-8` |
| MP3 → WAV | pcm_s16le | Uncompressed |
| MP3 → AAC | aac | `-b:a 96k-320k` |
| MP3 → Opus | libopus | `-b:a 64k-320k` |
| OGG → MP3 | libmp3lame | `-q:a 0-9` |
| OGG → FLAC | flac | Lossless |
| FLAC → MP3 | libmp3lame | `-q:a 0-9` |
| FLAC → OGG | libvorbis | `-q:a 0-10` |
| FLAC → WAV | pcm_s16le | Uncompressed |
| WAV → MP3 | libmp3lame | `-q:a 0-9` |
| WAV → FLAC | flac | Lossless |
| WAV → OGG | libvorbis | `-q:a 0-10` |
| AAC → MP3 | libmp3lame | `-q:a 0-9` |
| Opus → MP3 | libmp3lame | `-q:a 0-9` |
| ALL → MP3 | libmp3lame | Auto-detect |
| ALL → OGG | libvorbis | Auto-detect |
| ALL → FLAC | flac | Auto-detect |
| ALL → WAV | pcm_s16le | Auto-detect |
| Custom | You choose | You choose |

---

## How it works / Cách hoạt động

```
User input                  Scanner              Converter
   │                           │                    │
   ├─ Language                 │                    │
   ├─ Conversion type          │                    │
   ├─ Select dirs     ───────► │ rglob *.mp3        │
   ├─ Keep originals           │                    │
   ├─ Strip metadata?          │                    │
   ├─ Simplify filenames?      │                    │
   │                           │                    │
                               ▼                    ▼
                         ThreadPoolExecutor ──► ffmpeg -i a.mp3 ...
                         (CPU-1 threads)        ffmpeg -i b.mp3 ...
                                                ffmpeg -i c.mp3 ...
```

- Uses **ffmpeg** as the backend encoder — supports virtually all audio formats
- **Multithreaded** via `concurrent.futures.ThreadPoolExecutor`
- Each file runs in its own ffmpeg process — true parallelism
- Smart thread count: `CPU cores - 1` (leaves 1 core for system)
- Option to preserve (`-map_metadata 0`) or strip (`-map_metadata -1`) metadata
- Option to simplify filenames (strip ` - Artist`, remove special chars, 60-char limit)

---

## Project Structure / Cấu trúc

```
HiyoConvert/
├── hiyo-convert.py    # Main converter script
├── requirements.txt   # Python dependencies (stdlib only)
├── setup.bat          # Auto-installer for Windows
├── setup.sh           # Auto-installer for Linux / macOS
├── README.md          # This file
├── AGENTS.md          # Private local config
└── .gitignore
```

---

## License / Giấy phép

MIT — Free to use, modify, and share.  
MIT — Tự do sử dụng, chỉnh sửa và chia sẻ.
