# HiyoConvert — Project Info

## Repo
- **GitHub**: https://github.com/hiyo412012/Convert2ogg
- **Branch**: main

## Files
| File | Purpose |
|------|---------|
| `hiyo-convert.py` | Main converter script (song ngữ, 19+ định dạng, đa luồng) |
| `setup.bat` | Auto-install ffmpeg via winget |
| `README.md` | Bilingual documentation |
| `.gitignore` | Excludes audio files & cache |

## Commands
```bash
# Run converter
python hiyo-convert.py
python hiyo-convert.py "D:\Music"

# Setup new machine
setup.bat
```

## Token (local only — DO NOT commit)
Lưu token ở local, không commit lên GitHub.
Ví dụ tạo file `D:\Music\Convert2ogg\.gitpush.bat`:
```
@git push https://<TOKEN>@github.com/hiyo412012/Convert2ogg.git
```

## Workflow
- Chạy `hiyo-convert.py` → chọn ngôn ngữ → chọn kiểu convert → chọn thư mục → convert
- Đa luồng tự động: `CPU - 1` threads
- Hỗ trợ: MP3, OGG, FLAC, WAV, AAC, Opus
