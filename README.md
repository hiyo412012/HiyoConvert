# HiyoConvert 🎵

> Batch audio converter with multithreading — fast, smart, easy.  
> Công cụ chuyển đổi audio hàng loạt với đa luồng — nhanh, thông minh, dễ dùng.

---

## Features / Tính năng

| English | Tiếng Việt |
|---------|------------|
| ✅ Batch convert audio files (18+ formats) | ✅ Chuyển đổi audio hàng loạt (18+ định dạng) |
| ✅ Multithreading (auto CPU-1 threads) | ✅ Đa luồng thông minh (tự động CPU-1 luồng) |
| ✅ Interactive menu — just run and choose | ✅ Menu tương tác — chỉ cần chạy và chọn |
| ✅ Choose source format + target format (no flat presets) | ✅ Chọn định dạng nguồn + đích (không danh sách phẳng) |
| ✅ Quality slider 1-10, auto-mapped per codec | ✅ Thanh trượt chất lượng 1-10, tự động ánh xạ theo codec |
| ✅ Output directory option | ✅ Tuỳ chọn thư mục đầu ra |
| ✅ Sample rate selection (44.1k, 48k, 96k, 192k) | ✅ Chọn tần số lấy mẫu |
| ✅ Channel mode (Stereo, Mono, Original) | ✅ Chọn kênh (Stereo, Mono, Gốc) |
| ✅ Loudness normalization (EBU R128) | ✅ Chuẩn hoá âm lượng (EBU R128) |
| ✅ Strip metadata (privacy) | ✅ Xoá metadata (riêng tư) |
| ✅ Simplify filenames (strip artist, special chars) | ✅ Rút gọn tên file |
| ✅ Dry-run mode (preview before converting) | ✅ Chạy thử (xem trước trước khi chuyển) |
| ✅ File size comparison (before vs after) | ✅ So sánh dung lượng (trước vs sau) |
| ✅ Error logging to file | ✅ Ghi lỗi ra file |
| ✅ Auto-skip already converted files | ✅ Tự động bỏ qua file đã convert |
| ✅ Option to keep or delete originals | ✅ Tuỳ chọn giữ hoặc xóa file gốc |
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

--- Source format ---
[1]  All audio formats / Tất cả
[2]  MP3
[3]  FLAC
[4]  OGG (Vorbis)
...
[19] Speex
[Q]  Quit

--- Target format ---
[1]  MP3 (LAME)
[2]  OGG (Vorbis)
[3]  FLAC (Lossless)
[4]  WAV (PCM 16-bit)
[5]  AAC (M4A)
[6]  Opus
[7]  WMA (Windows Media)
[8]  AC3 (Dolby Digital)
[9]  ALAC (Apple Lossless)
[10] MP2 (MPEG Audio)

--- Settings ---
[1] Quality: 5/10 (192kbps)
[2] Output dir: (none)
[3] Sample rate: (original)
[4] Channels: (original)
[5] Normalize: OFF
[6] Strip metadata: OFF
[7] Simplify names: OFF
[8] Keep originals: NO
[9] Dry-run: OFF
[0] Start conversion!

Select directories:
[1] AlbumA
[2] AlbumB
[A] All
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

## Supported Codecs / Codec hỗ trợ

### Source formats (decode) / Định dạng nguồn (giải mã)

MP3, OGG, FLAC, WAV, AAC (M4A), Opus, WMA, AIFF, ALAC,
AC3, DTS, AMR, AU, MP2, WavPack, TTA, APE, Speex

### Target formats (encode) / Định dạng đích (mã hoá)

| Format | Codec | Quality options |
|--------|-------|-----------------|
| MP3 | libmp3lame | VBR q=0-9 (1=best, 10=worst) |
| OGG (Vorbis) | libvorbis | VBR q=0-10 (10=best) |
| FLAC | flac | Compression level 0-8 |
| WAV | pcm_s16le | Uncompressed |
| AAC (M4A) | aac | CBR 96k-320k |
| Opus | libopus | CBR 64k-320k |
| WMA | wmav2 | CBR 64k-320k |
| AC3 | ac3 | CBR 64k-640k |
| ALAC | alac | Lossless |
| MP2 | mp2 | CBR 64k-384k |

Quality 1-10 is automatically mapped to the appropriate range for each codec.

---

## How it works / Cách hoạt động

```
User input                           Scanner                  Converter
   │                                    │                        │
   ├─ Language                          │                        │
   ├─ Source format                     │                        │
   ├─ Target format                     │                        │
   ├─ Settings menu                     │                        │
   │  ├─ Quality (1-10)                 │                        │
   │  ├─ Output directory               │                        │
   │  ├─ Sample rate                    │                        │
   │  ├─ Channels                       │                        │
   │  ├─ Normalize / Strip / Simplify   │                        │
   │  ├─ Keep / Dry-run                 │                        │
   ├─ Select dirs             ────────► │ rglob *.ext            │
   │                                    │                        │
   │                                    ▼                        ▼
   │                             ThreadPoolExecutor ──► ffmpeg -i a.mp3 ...
   │                             (CPU-1 threads)        ffmpeg -i b.mp3 ...
   │                                                      ffmpeg -i c.mp3 ...
```

- Uses **ffmpeg** as the backend encoder — supports virtually all audio formats
- **Multithreaded** via `concurrent.futures.ThreadPoolExecutor`
- Each file runs in its own ffmpeg process — true parallelism
- Smart thread count: `CPU cores - 1` (leaves 1 core for system)
- Quality 1-10 mapped per codec: VBR, CBR, compression level, or lossless
- Loudness normalization via EBU R128 (`loudnorm` filter)
- File size comparison shown after batch completes
- Errors logged to `hiyo-convert_errors.log`

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
