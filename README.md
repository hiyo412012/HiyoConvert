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
| ✅ Preserves metadata (title, artist, album...) | ✅ Giữ nguyên metadata (tên, ca sĩ, album...) |
| ✅ Auto-skip already converted files | ✅ Tự động bỏ qua file đã convert |
| ✅ Bilingual: English & Tiếng Việt | ✅ Song ngữ: Tiếng Việt & English |
| ✅ Option to keep or delete originals | ✅ Tuỳ chọn giữ hoặc xóa file gốc |
| ✅ Auto-setup with setup.bat | ✅ Tự động cài đặt với setup.bat |

---

## Quick Start / Bắt đầu nhanh

### 1. Install / Cài đặt

```bash
# Option A: Auto setup (installs Python + ffmpeg)
setup.bat

# Option B: Manual / Thủ công
winget install Python.Python.3.14
winget install ffmpeg
```

### 2. Run / Chạy

```bash
python hiyo-convert.py
```

Or with a specific directory / Hoặc với thư mục cụ thể:

```bash
python hiyo-convert.py "D:\Music"
python hiyo-convert.py "D:\Downloads\Music"
python hiyo-convert.py "C:\Users\%USERNAME%\Music"
```

### 3. Just choose / Chỉ cần chọn

```
Select language:
[1] English
[2] Tiếng Việt

Conversion type:
[1]  MP3 → OGG (Vorbis)
[2]  MP3 → FLAC (Lossless)
[3]  MP3 → WAV
[4]  MP3 → AAC (M4A)
[5]  MP3 → Opus
[6]  OGG → MP3
[7]  OGG → FLAC
[8]  FLAC → MP3
[9]  FLAC → OGG
[10] FLAC → WAV
[11] WAV → MP3
[12] WAV → FLAC
[13] WAV → OGG
[14] AAC → MP3
[15] Opus → MP3
[16] ALL → MP3
[17] ALL → OGG
[18] ALL → FLAC
[19] ALL → WAV
[C]  Custom / Tùy chỉnh
```

---

## Requirements / Yêu cầu

- **Python 3.7+** — `winget install Python.Python.3.14` or [python.org](https://python.org/downloads)
- **ffmpeg** — `winget install ffmpeg` or [ffmpeg.org](https://ffmpeg.org/download.html)

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
User input              Scanner              Converter
   │                       │                    │
   ├─ Language             │                    │
   ├─ Conversion type      │                    │
   ├─ Select dirs ───────► │ rglob *.mp3        │
   └─ Keep originals       │                    │
                           │                    │
                           ▼                    ▼
                     ThreadPoolExecutor ──► ffmpeg -i a.mp3 ...
                     (CPU-1 threads)        ffmpeg -i b.mp3 ...
                                            ffmpeg -i c.mp3 ...
```

- Uses **ffmpeg** as the backend encoder — supports virtually all audio formats
- **Multithreaded** via `concurrent.futures.ThreadPoolExecutor`
- Each file runs in its own ffmpeg process — true parallelism
- Smart thread count: `CPU cores - 1` (leaves 1 core for system)
- Metadata preserved with `-map_metadata 0`

---

## Project Structure / Cấu trúc

```
HiyoConvert/
├── hiyo-convert.py    # Main converter script
├── setup.bat          # Auto-installer for Windows
├── README.md          # This file
├── Choáy   Hiyo41/    # Vietnamese music
│   ├── Song1.ogg
│   └── Song2.mp3
└── Eng lẹc   Hiyo41/  # English music
    ├── Song1.mp3
    └── Song2.ogg
```

---

## License / Giấy phép

MIT — Free to use, modify, and share.  
MIT — Tự do sử dụng, chỉnh sửa và chia sẻ.
