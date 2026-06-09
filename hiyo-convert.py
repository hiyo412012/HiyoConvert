import os, shutil, subprocess, sys, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

_lock = Lock()
L = None  # current language dict


LANG = {
    "en": {
        "title": "=== HiyoConvert ===",
        "lang": "Language / Ng\u00f4n ng\u1eef:",
        "type": "Conversion type / Lo\u1ea1i chuy\u1ec3n \u0111\u1ed5i:",
        "dirs": "Select directories / Ch\u1ecdn th\u01b0 m\u1ee5c:",
        "dir_pick": "Enter numbers (e.g. 1,2) or A for all / Nh\u1eadp s\u1ed1 (vd: 1,2) ho\u1eb7c A:",
        "keep": "Keep original files? / Gi\u1eef l\u1ea1i file g\u1ed1c? (y/N): ",
        "threads": "Threads / Lu\u1ed3ng",
        "quit": "Quit / Tho\u00e1t",
        "all": "All / T\u1ea5t c\u1ea3",
        "ok": "OK",
        "skip": "SKIP",
        "fail": "FAIL",
        "done": "Done / Xong",
        "time": "Time / Th\u1eddi gian",
        "no_ffmpeg": "Install ffmpeg first: winget install ffmpeg",
        "no_mp3": "No files found to convert / Kh\u00f4ng t\u00ecm th\u1ea5y file",
        "none_sel": "Nothing selected / Kh\u00f4ng c\u00f3 m\u1ee5c n\u00e0o \u0111\u01b0\u1ee3c ch\u1ecdn",
        "custom": "Custom / T\u00f9y ch\u1ec9nh",
        "src_ext": "Source extension (e.g. .mp3): ",
        "dst_ext": "Target extension (e.g. .ogg): ",
        "codec": "Codec (e.g. libvorbis, libmp3lame): ",
        "converting": "Converting / \u0110ang chuy\u1ec3n",
        "files": "files / t\u1ec7p",
        "scanning": "Scanning for files / \u0110ang qu\u00e9t...",
        "choose_lang": "Choose language / Ch\u1ecdn ng\u00f4n ng\u1eef:",
        "found": "Found / T\u00ecm th\u1ea5y",
    },
    "vi": {
        "title": "=== HiyoConvert ===",
        "lang": "Ng\u00f4n ng\u1eef / Language:",
        "type": "Lo\u1ea1i chuy\u1ec3n \u0111\u1ed5i / Conversion type:",
        "dirs": "Ch\u1ecdn th\u01b0 m\u1ee5c / Select directories:",
        "dir_pick": "Nh\u1eadp s\u1ed1 (vd: 1,2) ho\u1eb7c A / Enter numbers or A:",
        "keep": "Gi\u1eef l\u1ea1i file g\u1ed1c? / Keep original files? (y/N): ",
        "threads": "Lu\u1ed3ng / Threads",
        "quit": "Tho\u00e1t / Quit",
        "all": "T\u1ea5t c\u1ea3 / All",
        "ok": "OK",
        "skip": "SKIP",
        "fail": "FAIL",
        "done": "Xong / Done",
        "time": "Th\u1eddi gian / Time",
        "no_ffmpeg": "C\u00e0i ffmpeg tr\u01b0\u1edbc: winget install ffmpeg",
        "no_mp3": "Kh\u00f4ng t\u00ecm th\u1ea5y file n\u00e0o \u0111\u1ec3 convert / No files found",
        "none_sel": "Kh\u00f4ng c\u00f3 m\u1ee5c n\u00e0o \u0111\u01b0\u1ee3c ch\u1ecdn / Nothing selected",
        "custom": "T\u00f9y ch\u1ec9nh / Custom",
        "src_ext": "\u0110u\u00f4i ngu\u1ed3n (vd: .mp3): ",
        "dst_ext": "\u0110u\u00f4i \u0111\u00edch (vd: .ogg): ",
        "codec": "Codec (vd: libvorbis, libmp3lame): ",
        "converting": "\u0110ang chuy\u1ec3n / Converting",
        "files": "t\u1ec7p / files",
        "scanning": "\u0110ang qu\u00e9t / Scanning...",
        "choose_lang": "Ch\u1ecdn ng\u00f4n ng\u1eef / Choose language:",
        "found": "T\u00ecm th\u1ea5y / Found",
    },
}

CONVERSIONS = [
    ("MP3  \u2192 OGG (Vorbis)",     ".mp3",  ".ogg",  "libvorbis"),
    ("MP3  \u2192 FLAC (Lossless)",  ".mp3",  ".flac", "flac"),
    ("MP3  \u2192 WAV",              ".mp3",  ".wav",  "pcm_s16le"),
    ("MP3  \u2192 AAC (M4A)",        ".mp3",  ".m4a",  "aac"),
    ("MP3  \u2192 Opus",             ".mp3",  ".opus", "libopus"),
    ("OGG  \u2192 MP3",              ".ogg",  ".mp3",  "libmp3lame"),
    ("OGG  \u2192 FLAC",             ".ogg",  ".flac", "flac"),
    ("FLAC \u2192 MP3",              ".flac", ".mp3",  "libmp3lame"),
    ("FLAC \u2192 OGG",              ".flac", ".ogg",  "libvorbis"),
    ("FLAC \u2192 WAV",              ".flac", ".wav",  "pcm_s16le"),
    ("WAV  \u2192 MP3",              ".wav",  ".mp3",  "libmp3lame"),
    ("WAV  \u2192 FLAC",             ".wav",  ".flac", "flac"),
    ("WAV  \u2192 OGG",              ".wav",  ".ogg",  "libvorbis"),
    ("AAC  \u2192 MP3 (M4A)",        ".m4a",  ".mp3",  "libmp3lame"),
    ("Opus \u2192 MP3",              ".opus", ".mp3",  "libmp3lame"),
    ("ALL  \u2192 MP3",              None,    ".mp3",  "libmp3lame"),
    ("ALL  \u2192 OGG",              None,    ".ogg",  "libvorbis"),
    ("ALL  \u2192 FLAC",             None,    ".flac", "flac"),
    ("ALL  \u2192 WAV",              None,    ".wav",  "pcm_s16le"),
]


def tr(key):
    return L.get(key, key)


def pick_menu(items, prompt, cancel_key="q"):
    for i, (label, *_) in enumerate(items, 1):
        print(f"  [{i}] {label}")
    print(f"  [{cancel_key.upper()}] {tr('quit')}")
    while True:
        sel = input(f"> {prompt} ").strip().lower()
        if sel == cancel_key:
            return None
        try:
            n = int(sel)
            if 1 <= n <= len(items):
                return items[n - 1]
        except ValueError:
            pass


def scan_dirs(root: Path, src_ext):
    dirs = []
    if src_ext is None and any(f.suffix.lower() in (".mp3", ".ogg", ".flac", ".wav", ".m4a", ".opus") for f in root.iterdir()):
        dirs.append(root)
    elif src_ext and list(root.glob(f"*{src_ext}")):
        dirs.append(root)
    for d in sorted(root.iterdir()):
        if not d.is_dir():
            continue
        if src_ext is None:
            if any(f.suffix.lower() in (".mp3", ".ogg", ".flac", ".wav", ".m4a", ".opus") for f in d.rglob("*")):
                dirs.append(d)
        elif list(d.rglob(f"*{src_ext}")):
            dirs.append(d)
    return dirs


def pick_dirs(dirs):
    print(f"\n--- {tr('dirs')} ---")
    for i, d in enumerate(dirs, 1):
        print(f"  [{i}] {d.name}")
    print(f"  [A] {tr('all')}")
    print(f"  [Q] {tr('quit')}")
    while True:
        sel = input(f"> {tr('dir_pick')} ").strip().lower()
        if sel == "q":
            return None
        if sel == "a":
            return dirs
        try:
            indices = [int(x.strip()) for x in sel.split(",") if x.strip()]
            return [dirs[i - 1] for i in indices if 1 <= i <= len(dirs)]
        except ValueError:
            pass


def convert_file(mp3: Path, dst_ext: str, codec: str, keep: bool, quality: int):
    ogg = mp3.with_suffix(dst_ext)
    name = mp3.stem
    idx = name.find(" - ")
    short = name[:idx] if idx > 0 else name

    if ogg.exists():
        return "skip", short

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-i", str(mp3)]

    if codec == "flac":
        cmd += ["-c:a", "flac", "-compression_level", str(min(quality, 8))]
    elif codec == "libmp3lame":
        q = max(0, 9 - quality)  # 0=best → 9=worst
        cmd += ["-c:a", "libmp3lame", "-q:a", str(q)]
    elif codec == "libvorbis":
        cmd += ["-c:a", "libvorbis", "-q:a", str(min(quality, 10))]
    elif codec == "aac":
        bitrates = [96, 128, 160, 192, 224, 256, 320]
        br = bitrates[min(quality - 1, len(bitrates) - 1)]
        cmd += ["-c:a", "aac", "-b:a", f"{br}k"]
    elif codec == "libopus":
        bitrates = [64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
        br = bitrates[min(quality - 1, len(bitrates) - 1)]
        cmd += ["-c:a", "libopus", "-b:a", f"{br}k"]
    elif codec in ("pcm_s16le", "wmav2", "ac3"):
        cmd += ["-c:a", codec]
    else:
        cmd += ["-c:a", codec, "-q:a", str(min(quality, 10))]

    cmd += ["-map_metadata", "0", str(ogg)]

    try:
        subprocess.run(cmd, check=True)
        if not keep:
            mp3.unlink()
        return "ok", short
    except subprocess.CalledProcessError:
        return "fail", short


def run_batch(mp3s, dst_ext, codec, keep, quality):
    threads = max(1, os.cpu_count() - 1) if os.cpu_count() else 2
    print(f"\n--- {tr('converting')} {len(mp3s)} {tr('files')} ({tr('threads')}: {threads}) ---\n")

    start = time.time()
    ok = skip = fail = 0

    with ThreadPoolExecutor(max_workers=threads) as pool:
        fut = {pool.submit(convert_file, f, dst_ext, codec, keep, quality): f for f in mp3s}
        for f in as_completed(fut):
            status, name = f.result()
            if status == "ok":
                ok += 1
                print(f"  [{tr('ok')}] {name}")
            elif status == "skip":
                skip += 1
            else:
                fail += 1
                print(f"  [{tr('fail')}] {name}")

    elapsed = time.time() - start
    print(f"\n--- {tr('done')} ---")
    print(f"  {tr('ok')}: {ok}  |  {tr('skip')}: {skip}  |  {tr('fail')}: {fail}  |  {tr('time')}: {elapsed:.1f}s")


def main():
    global L
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found. Install with: winget install ffmpeg")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"'{root}' is not a directory")
        sys.exit(1)

    # --- Language ---
    print(f"\n  === HiyoConvert ===")
    print(f"\n  {LANG['en']['choose_lang']}")
    print(f"  [1] English")
    print(f"  [2] Tiếng Việt")
    print(f"  [Q] {LANG['en']['quit']}")
    while True:
        sel = input("> ").strip().lower()
        if sel == "1":
            L = LANG["en"]
            break
        elif sel == "2":
            L = LANG["vi"]
            break
        elif sel == "q":
            return

    # --- Conversion type ---
    print(f"\n--- {tr('type')} ---")
    conv = pick_menu(CONVERSIONS, f"[1-{len(CONVERSIONS)}]:")
    if conv is None:
        return

    label, src_ext, dst_ext, codec = conv
    if label.startswith("CUSTOM"):
        src_ext = input(tr("src_ext")).strip().lower()
        dst_ext = input(tr("dst_ext")).strip().lower()
        codec = input(tr("codec")).strip().lower()
        if not src_ext.startswith("."):
            src_ext = "." + src_ext
        if not dst_ext.startswith("."):
            dst_ext = "." + dst_ext

    # --- Scan directories ---
    print(f"\n{tr('scanning')}...")
    dirs = scan_dirs(root, src_ext)
    if not dirs:
        print(f"{tr('no_mp3')}")
        return

    selected = pick_dirs(dirs)
    if not selected:
        print(tr("none_sel"))
        return

    # --- Collect files ---
    mp3s = sorted(f for d in selected for f in d.rglob("*") if f.suffix.lower() == src_ext) if src_ext else sorted(
        f for d in selected for f in d.rglob("*") if f.suffix.lower() in (".mp3", ".ogg", ".flac", ".wav", ".m4a", ".opus"))
    if not mp3s:
        print(f"{tr('no_mp3')}")
        return

    keep = input(tr("keep")).strip().lower() == "y"
    quality = 5

    run_batch(mp3s, dst_ext, codec, keep, quality)
    input("\nPress Enter / Nhấn Enter...")


if __name__ == "__main__":
    main()
