import os, re, shutil, subprocess, sys, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import OrderedDict
from threading import Lock

L = None

LANG = {
    "en": {
        "title": "=== HiyoConvert ===",
        "lang": "Language / Ng\u00f4n ng\u1eef:",
        "source": "Source format / \u0110\u1ecbnh d\u1ea1ng ngu\u1ed3n:",
        "target": "Target format / \u0110\u1ecbnh d\u1ea1ng \u0111\u00edch:",
        "dirs": "Select directories / Ch\u1ecdn th\u01b0 m\u1ee5c:",
        "dir_pick": "Enter numbers (e.g. 1,2) or A for all / Nh\u1eadp s\u1ed1 (vd: 1,2) ho\u1eb7c A:",
        "threads": "Threads / Lu\u1ed3ng",
        "quit": "Quit / Tho\u00e1t",
        "all": "All / T\u1ea5t c\u1ea3",
        "ok": "OK",
        "skip": "SKIP",
        "fail": "FAIL",
        "done": "Done / Xong",
        "time": "Time",
        "no_ffmpeg": "Install ffmpeg first: winget install ffmpeg",
        "no_files": "No files found to convert / Kh\u00f4ng t\u00ecm th\u1ea5y file",
        "none_sel": "Nothing selected / Kh\u00f4ng c\u00f3 m\u1ee5c n\u00e0o \u0111\u01b0\u1ee3c ch\u1ecdn",
        "converting": "Converting / \u0110ang chuy\u1ec3n",
        "files": "files / t\u1ec7p",
        "scanning": "Scanning / \u0110ang qu\u00e9t...",
        "choose_lang": "Choose language / Ch\u1ecdn ng\u00f4n ng\u1eef:",
        "found": "Found / T\u00ecm th\u1ea5y",
        "quality": "Quality / Ch\u1ea5t l\u01b0\u1ee3ng",
        "settings": "Settings / C\u00e0i \u0111\u1eb7t",
        "start": "Start / B\u1eaft \u0111\u1ea7u",
        "enter_quality": "Enter quality 1-10 (10=best) / Nh\u1eadp ch\u1ea5t l\u01b0\u1ee3ng 1-10 (10=t\u1ed1t nh\u1ea5t):",
        "output_dir": "Output directory / Th\u01b0 m\u1ee5c \u0111\u1ea7u ra",
        "enter_outdir": "Enter output directory path (Enter to keep alongside original) / Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn th\u01b0 m\u1ee5c \u0111\u1ea7u ra (Enter \u0111\u1ec3 gi\u1eef c\u1ea1nh file g\u1ed1c):",
        "sample_rate": "Sample rate / T\u1ea7n s\u1ed1 l\u1ea5y m\u1eabu",
        "channels": "Channels / K\u00eanh",
        "normalize": "Normalize / Chu\u1ea9n h\u00f3a",
        "strip_meta": "Strip metadata / Xo\u00e1 metadata",
        "simplify": "Simplify names / R\u00fat g\u1ecdn t\u00ean",
        "keep": "Keep originals / Gi\u1eef g\u1ed1c",
        "dry_run": "Dry-run / Ch\u1ea1y th\u1eed",
        "original": "Original / G\u1ed1c",
        "none": "None / Kh\u00f4ng",
        "off": "OFF",
        "on": "ON",
        "yes": "YES",
        "no": "NO",
        "toggle": "Toggle / Chuy\u1ec3n",
        "press_enter": "Press Enter / Nh\u1ea5n Enter...",
        "dry_run_title": "=== DRY-RUN / CH\u1ea0Y TH\u1eec ===",
        "dry_run_info": "Would convert / S\u1ebd chuy\u1ec3n",
        "to": "to / th\u00e0nh",
        "size": "Size / Dung l\u01b0\u1ee3ng",
        "error_log": "Error log saved to / L\u1ed7i \u0111\u00e3 l\u01b0u v\u00e0o",
        "config_header": "--- Settings / C\u00e0i \u0111\u1eb7t ---",
        "config_quality": "Quality / Ch\u1ea5t l\u01b0\u1ee3ng",
        "config_outdir": "Output dir / Th\u01b0 m\u1ee5c \u0111\u1ea7u ra",
        "config_samplerate": "Sample rate / T\u1ea7n s\u1ed1 m\u1eabu",
        "config_channels": "Channels / K\u00eanh",
        "config_normalize": "Normalize / Chu\u1ea9n h\u00f3a",
        "config_strip": "Strip metadata / Xo\u00e1 metadata",
        "config_simplify": "Simplify names / R\u00fat g\u1ecdn t\u00ean",
        "config_keep": "Keep originals / Gi\u1eef g\u1ed1c",
        "config_dryrun": "Dry-run / Ch\u1ea1y th\u1eed",
        "config_start": "Start conversion / B\u1eaft \u0111\u1ea7u",
        "choose_dir_title": "Select directory / Ch\u1ecdn th\u01b0 m\u1ee5c",
        "choose_dir_curr": "Use current directory / D\u00f9ng th\u01b0 m\u1ee5c hi\u1ec7n t\u1ea1i",
        "choose_dir_enter": "Enter path manually / Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn th\u1ee7 c\u00f4ng",
        "choose_dir_browse": "Browse (Windows folder picker) / Duy\u1ec7t (ch\u1ecdn th\u01b0 m\u1ee5c)",
        "choose_dir_path": "Enter full directory path / Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn \u0111\u1ea7y \u0111\u1ee7",
        "choose_dir_invalid": "Invalid path / \u0110\u01b0\u1eddng d\u1eabn kh\u00f4ng h\u1ee3p l\u1ec7",
        "choose_dir_pick": "Pick an option / Ch\u1ecdn m\u1ed9t m\u1ee5c",
        "source_type": "Source type / Lo\u1ea1i ngu\u1ed3n",
        "local_files": "Local files / File c\u1ee5c b\u1ed9",
        "youtube": "YouTube URL / URL YouTube",
        "enter_urls": "Enter YouTube URLs (one per line, empty line to finish) / Nh\u1eadp URL YouTube (m\u1ed7i d\u00f2ng m\u1ed9t URL, d\u00f2ng tr\u1ed1ng \u0111\u1ec3 k\u1ebft th\u00fac)",
        "no_urls": "No URLs entered / Ch\u01b0a nh\u1eadp URL",
        "downloading": "Downloading / \u0110ang t\u1ea3i",
        "downloaded": "Downloaded / \u0110\u00e3 t\u1ea3i",
        "from": "from / t\u1eeb",
        "playlist": "Playlist / Danh s\u00e1ch",
        "invalid_url": "Invalid URL / URL kh\u00f4ng h\u1ee3p l\u1ec7",
        "download_error": "Download failed / T\u1ea3i th\u1ea5t b\u1ea1i",
    },
    "vi": {
        "title": "=== HiyoConvert ===",
        "lang": "Ng\u00f4n ng\u1eef / Language:",
        "source": "\u0110\u1ecbnh d\u1ea1ng ngu\u1ed3n / Source format:",
        "target": "\u0110\u1ecbnh d\u1ea1ng \u0111\u00edch / Target format:",
        "dirs": "Ch\u1ecdn th\u01b0 m\u1ee5c / Select directories:",
        "dir_pick": "Nh\u1eadp s\u1ed1 (vd: 1,2) ho\u1eb7c A / Enter numbers or A:",
        "threads": "Lu\u1ed3ng / Threads",
        "quit": "Tho\u00e1t / Quit",
        "all": "T\u1ea5t c\u1ea3 / All",
        "ok": "OK",
        "skip": "SKIP",
        "fail": "FAIL",
        "done": "Xong / Done",
        "time": "Th\u1eddi gian",
        "no_ffmpeg": "C\u00e0i ffmpeg tr\u01b0\u1edbc: winget install ffmpeg",
        "no_files": "Kh\u00f4ng t\u00ecm th\u1ea5y file \u0111\u1ec3 convert / No files found",
        "none_sel": "Kh\u00f4ng c\u00f3 m\u1ee5c n\u00e0o \u0111\u01b0\u1ee3c ch\u1ecdn / Nothing selected",
        "converting": "\u0110ang chuy\u1ec3n / Converting",
        "files": "t\u1ec7p / files",
        "scanning": "\u0110ang qu\u00e9t / Scanning...",
        "choose_lang": "Ch\u1ecdn ng\u00f4n ng\u1eef / Choose language:",
        "found": "T\u00ecm th\u1ea5y / Found",
        "quality": "Ch\u1ea5t l\u01b0\u1ee3ng / Quality",
        "settings": "C\u00e0i \u0111\u1eb7t / Settings",
        "start": "B\u1eaft \u0111\u1ea7u / Start",
        "enter_quality": "Nh\u1eadp ch\u1ea5t l\u01b0\u1ee3ng 1-10 (10=t\u1ed1t nh\u1ea5t) / Enter quality 1-10 (10=best):",
        "output_dir": "Th\u01b0 m\u1ee5c \u0111\u1ea7u ra / Output directory",
        "enter_outdir": "Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn th\u01b0 m\u1ee5c \u0111\u1ea7u ra (Enter \u0111\u1ec3 gi\u1eef c\u1ea1nh file g\u1ed1c) / Enter output dir path (Enter to keep alongside original):",
        "sample_rate": "T\u1ea7n s\u1ed1 l\u1ea5y m\u1eabu / Sample rate",
        "channels": "K\u00eanh / Channels",
        "normalize": "Chu\u1ea9n h\u00f3a / Normalize",
        "strip_meta": "Xo\u00e1 metadata / Strip metadata",
        "simplify": "R\u00fat g\u1ecdn t\u00ean / Simplify names",
        "keep": "Gi\u1eef g\u1ed1c / Keep originals",
        "dry_run": "Ch\u1ea1y th\u1eed / Dry-run",
        "original": "G\u1ed1c / Original",
        "none": "Kh\u00f4ng / None",
        "off": "T\u1eaeT",
        "on": "B\u1eacT",
        "yes": "C\u00d3",
        "no": "KH\u00d4NG",
        "toggle": "Chuy\u1ec3n / Toggle",
        "press_enter": "Nh\u1ea5n Enter / Press Enter...",
        "dry_run_title": "=== CH\u1ea0Y TH\u1eec / DRY-RUN ===",
        "dry_run_info": "S\u1ebd chuy\u1ec3n / Would convert",
        "to": "th\u00e0nh / to",
        "size": "Dung l\u01b0\u1ee3ng / Size",
        "error_log": "L\u1ed7i \u0111\u00e3 l\u01b0u v\u00e0o / Error log saved to",
        "config_header": "--- C\u00e0i \u0111\u1eb7t / Settings ---",
        "config_quality": "Ch\u1ea5t l\u01b0\u1ee3ng / Quality",
        "config_outdir": "Th\u01b0 m\u1ee5c \u0111\u1ea7u ra / Output dir",
        "config_samplerate": "T\u1ea7n s\u1ed1 m\u1eabu / Sample rate",
        "config_channels": "K\u00eanh / Channels",
        "config_normalize": "Chu\u1ea9n h\u00f3a / Normalize",
        "config_strip": "Xo\u00e1 metadata / Strip metadata",
        "config_simplify": "R\u00fat g\u1ecdn t\u00ean / Simplify names",
        "config_keep": "Gi\u1eef g\u1ed1c / Keep originals",
        "config_dryrun": "Ch\u1ea1y th\u1eed / Dry-run",
        "config_start": "B\u1eaft \u0111\u1ea7u / Start",
        "choose_dir_title": "Ch\u1ecdn th\u01b0 m\u1ee5c / Select directory",
        "choose_dir_curr": "D\u00f9ng th\u01b0 m\u1ee5c hi\u1ec7n t\u1ea1i / Use current directory",
        "choose_dir_enter": "Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn th\u1ee7 c\u00f4ng / Enter path manually",
        "choose_dir_browse": "Duy\u1ec7t (ch\u1ecdn th\u01b0 m\u1ee5c) / Browse (Windows folder picker)",
        "choose_dir_path": "Nh\u1eadp \u0111\u01b0\u1eddng d\u1eabn \u0111\u1ea7y \u0111\u1ee7 / Enter full directory path",
        "choose_dir_invalid": "\u0110\u01b0\u1eddng d\u1eabn kh\u00f4ng h\u1ee3p l\u1ec7 / Invalid path",
        "choose_dir_pick": "Ch\u1ecdn m\u1ed9t m\u1ee5c / Pick an option",
        "source_type": "Lo\u1ea1i ngu\u1ed3n / Source type",
        "local_files": "File c\u1ee5c b\u1ed9 / Local files",
        "youtube": "URL YouTube / YouTube URL",
        "enter_urls": "Nh\u1eadp URL YouTube (m\u1ed7i d\u00f2ng m\u1ed9t URL, d\u00f2ng tr\u1ed1ng \u0111\u1ec3 k\u1ebft th\u00fac) / Enter YouTube URLs (one per line, empty line to finish)",
        "no_urls": "Ch\u01b0a nh\u1eadp URL / No URLs entered",
        "downloading": "\u0110ang t\u1ea3i / Downloading",
        "downloaded": "\u0110\u00e3 t\u1ea3i / Downloaded",
        "from": "t\u1eeb / from",
        "playlist": "Danh s\u00e1ch / Playlist",
        "invalid_url": "URL kh\u00f4ng h\u1ee3p l\u1ec7 / Invalid URL",
        "download_error": "T\u1ea3i th\u1ea5t b\u1ea1i / Download failed",
    },
}

CODECS = OrderedDict([
    (".mp3",  {"name": "MP3 (LAME)",            "codec": "libmp3lame", "quality": ("inv_vbr", 0, 9)}),
    (".ogg",  {"name": "OGG (Vorbis)",          "codec": "libvorbis",  "quality": ("vbr", 0, 10)}),
    (".flac", {"name": "FLAC (Lossless)",       "codec": "flac",       "quality": ("level", 0, 8)}),
    (".wav",  {"name": "WAV (PCM 16-bit)",      "codec": "pcm_s16le",  "quality": None}),
    (".m4a",  {"name": "AAC (M4A)",             "codec": "aac",        "quality": ("cbr", 96, 320)}),
    (".opus", {"name": "Opus",                  "codec": "libopus",    "quality": ("cbr", 64, 320)}),
    (".wma",  {"name": "WMA (Windows Media)",   "codec": "wmav2",      "quality": ("cbr", 64, 320)}),
    (".ac3",  {"name": "AC3 (Dolby Digital)",   "codec": "ac3",        "quality": ("cbr", 64, 640)}),
    (".alac", {"name": "ALAC (Apple Lossless)", "codec": "alac",       "quality": None}),
    (".mp2",  {"name": "MP2 (MPEG Audio)",      "codec": "mp2",        "quality": ("cbr", 64, 384)}),
])

ALL_AUDIO_EXTS = {".mp3", ".ogg", ".flac", ".wav", ".m4a", ".opus",
                  ".wma", ".aiff", ".alac", ".ac3", ".dts", ".amr",
                  ".au", ".mp2", ".wv", ".tta", ".ape", ".spx"}

SRC_FORMATS = [
    ("All audio formats / T\u1ea5t c\u1ea3", None),
    ("MP3", ".mp3"),
    ("FLAC", ".flac"),
    ("OGG (Vorbis)", ".ogg"),
    ("WAV (PCM)", ".wav"),
    ("AAC (M4A)", ".m4a"),
    ("Opus", ".opus"),
    ("WMA", ".wma"),
    ("AIFF", ".aiff"),
    ("ALAC (Apple Lossless)", ".alac"),
    ("AC3 (Dolby Digital)", ".ac3"),
    ("DTS", ".dts"),
    ("AMR", ".amr"),
    ("AU", ".au"),
    ("MP2", ".mp2"),
    ("WavPack", ".wv"),
    ("True Audio (TTA)", ".tta"),
    ("Monkey's Audio (APE)", ".ape"),
    ("Speex", ".spx"),
]

TGT_FORMATS = [(v["name"], k, k, v["codec"]) for k, v in CODECS.items()]


class Settings:
    def __init__(self):
        self.quality = 5
        self.output_dir = None
        self.sample_rate = 0
        self.channels = 0
        self.normalize = False
        self.strip_meta = False
        self.simplify = False
        self.keep = False
        self.dry_run = False


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
    has_audio = lambda f: f.suffix.lower() in ALL_AUDIO_EXTS
    if src_ext is None:
        if any(has_audio(f) for f in root.iterdir()):
            dirs.append(root)
    elif list(root.glob(f"*{src_ext}")):
        dirs.append(root)
    for d in sorted(root.iterdir()):
        if not d.is_dir():
            continue
        if src_ext is None:
            if any(has_audio(f) for f in d.rglob("*")):
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


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.1f}MB"
    else:
        return f"{size_bytes / 1024 ** 3:.2f}GB"


def quality_to_params(codec_info, quality_lvl):
    qtype = codec_info["quality"]
    if qtype is None:
        return []
    qmode, qmin, qmax = qtype
    if qmode == "inv_vbr":
        val = qmin + (qmax - qmin) * (10 - quality_lvl) / 9
        val = int(round(val))
        return ["-q:a", str(val)]
    elif qmode == "vbr":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        val = int(round(val))
        return ["-q:a", str(val)]
    elif qmode == "cbr":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        val = int(round(val))
        val = max(qmin, min(qmax, val))
        return ["-b:a", f"{val}k"]
    elif qmode == "level":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        val = int(round(val))
        return ["-compression_level", str(val)]
    return []


def describe_quality(codec_info, quality_lvl):
    qtype = codec_info["quality"]
    if qtype is None:
        return tr("none")
    qmode, qmin, qmax = qtype
    if qmode == "inv_vbr":
        val = qmin + (qmax - qmin) * (10 - quality_lvl) / 9
        return f"VBR q={int(round(val))}"
    elif qmode == "vbr":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        return f"VBR q={int(round(val))}"
    elif qmode == "cbr":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        val = max(qmin, min(qmax, val))
        return f"{val}kbps"
    elif qmode == "level":
        val = qmin + (qmax - qmin) * (quality_lvl - 1) / 9
        return f"level {int(round(val))}"
    return ""


def configure_settings(tgt_ext, codec_info):
    settings = Settings()
    sr_items = [(f"{tr('original')} / {tr('original')}", 0),
                ("44100 Hz", 44100), ("48000 Hz", 48000),
                ("96000 Hz", 96000), ("192000 Hz", 192000)]
    ch_items = [(f"{tr('original')} / {tr('original')}", 0),
                ("Stereo", 2), ("Mono", 1)]

    while True:
        print(f"\n{tr('config_header')}")
        qual_desc = describe_quality(codec_info, settings.quality)
        outdir_str = str(settings.output_dir) if settings.output_dir else tr("none")
        sr_str = f"{settings.sample_rate}Hz" if settings.sample_rate > 0 else tr("original")
        ch_str = {0: tr("original"), 1: "Mono", 2: "Stereo"}.get(settings.channels, str(settings.channels))
        print(f"  [1] {tr('config_quality')}: {settings.quality}/10 ({qual_desc})")
        print(f"  [2] {tr('config_outdir')}: {outdir_str}")
        print(f"  [3] {tr('config_samplerate')}: {sr_str}")
        print(f"  [4] {tr('config_channels')}: {ch_str}")
        print(f"  [5] {tr('config_normalize')}: {tr('on') if settings.normalize else tr('off')}")
        print(f"  [6] {tr('config_strip')}: {tr('on') if settings.strip_meta else tr('off')}")
        print(f"  [7] {tr('config_simplify')}: {tr('on') if settings.simplify else tr('off')}")
        print(f"  [8] {tr('config_keep')}: {tr('yes') if settings.keep else tr('no')}")
        print(f"  [9] {tr('config_dryrun')}: {tr('on') if settings.dry_run else tr('off')}")
        print(f"  [0] {tr('config_start')}!")
        sel = input("> ").strip().lower()
        if sel in ("0", "s", "start"):
            return settings
        elif sel == "1":
            try:
                q = int(input(f"> {tr('enter_quality')} "))
                settings.quality = max(1, min(10, q))
            except ValueError:
                pass
        elif sel == "2":
            p = input(f"> {tr('enter_outdir')} ").strip()
            if p:
                pobj = Path(p).resolve()
                pobj.mkdir(parents=True, exist_ok=True)
                settings.output_dir = pobj
            else:
                settings.output_dir = None
        elif sel == "3":
            item = pick_menu(sr_items, "")
            if item:
                settings.sample_rate = item[1]
        elif sel == "4":
            item = pick_menu(ch_items, "")
            if item:
                settings.channels = item[1]
        elif sel in ("5", "6", "7", "8", "9"):
            toggles = {"5": "normalize", "6": "strip_meta", "7": "simplify", "8": "keep", "9": "dry_run"}
            setattr(settings, toggles[sel], not getattr(settings, toggles[sel]))


def simplify_name(name):
    idx = name.find(" - ")
    if idx > 0:
        name = name[:idx]
    name = re.sub(r'[\[\](){}#&,;:!?@$%^*+=<>"\'/\\|~`]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > 60:
        name = name[:60].rstrip()
    return name


def get_output_path(src: Path, dst_ext, settings, root=None):
    name = src.stem
    if settings.simplify:
        name = simplify_name(name)
    if settings.output_dir:
        if root:
            try:
                rel = src.relative_to(root)
                dst = settings.output_dir / rel.with_name(name + dst_ext)
            except ValueError:
                dst = settings.output_dir / src.with_name(name + dst_ext).name
        else:
            dst = settings.output_dir / src.with_name(name + dst_ext).name
        dst.parent.mkdir(parents=True, exist_ok=True)
    else:
        dst = src.with_name(name + dst_ext)
    counter = 1
    while dst.exists():
        stem = f"{name}_{counter}"
        if settings.output_dir:
            dst = settings.output_dir / f"{stem}{dst_ext}"
        else:
            dst = src.with_name(f"{stem}{dst_ext}")
        counter += 1
    return dst


def get_short_name(name):
    idx = name.find(" - ")
    return name[:idx] if idx > 0 else name


def convert_file(src: Path, dst_ext, codec, settings, codec_info, root=None):
    dst = get_output_path(src, dst_ext, settings, root)
    short = get_short_name(src.stem)
    if dst == src:
        return "skip", short
    if dst.exists():
        return "skip", short

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src)]
    if settings.strip_meta:
        cmd += ["-map_metadata", "-1", "-vn"]
    else:
        cmd += ["-map_metadata", "0"]
    cmd += ["-c:a", codec]
    cmd += quality_to_params(codec_info, settings.quality)
    if settings.sample_rate > 0:
        cmd += ["-ar", str(settings.sample_rate)]
    if settings.channels > 0:
        cmd += ["-ac", str(settings.channels)]
    if settings.normalize:
        cmd += ["-af", "loudnorm=I=-16:LRA=11:TP=-1.5"]
    cmd += [str(dst)]
    try:
        subprocess.run(cmd, check=True)
        if not settings.keep:
            src.unlink()
        orig_size = src.stat().st_size if settings.keep else 0
        dst_size = dst.stat().st_size
        return "ok", short, orig_size, dst_size
    except subprocess.CalledProcessError:
        return "fail", short, 0, 0


def run_batch(files, dst_ext, codec, settings, codec_info, root=None):
    threads = max(1, os.cpu_count() - 1) if os.cpu_count() else 2
    total = len(files)
    print(f"\n--- {tr('converting')} {total} {tr('files')} ({tr('threads')}: {threads}) ---\n")
    start = time.time()
    ok = skip = fail = 0
    errors = []
    total_orig = 0
    total_dst = 0
    with ThreadPoolExecutor(max_workers=threads) as pool:
        fut = {pool.submit(convert_file, f, dst_ext, codec, settings, codec_info, root): f for f in files}
        for f in as_completed(fut):
            result = f.result()
            if len(result) == 4:
                status, name, orig_size, dst_size = result
            else:
                status, name = result
                orig_size = dst_size = 0
            if status == "ok":
                ok += 1
                total_orig += orig_size
                total_dst += dst_size
                print(f"  [{tr('ok')}] {name}")
            elif status == "skip":
                skip += 1
            else:
                fail += 1
                errors.append(fut[f])
                print(f"  [{tr('fail')}] {name}")

    elapsed = time.time() - start
    print(f"\n--- {tr('done')} ---")
    print(f"  {tr('ok')}: {ok}  |  {tr('skip')}: {skip}  |  {tr('fail')}: {fail}")
    print(f"  {tr('time')}: {elapsed:.1f}s")
    if total_orig > 0 and total_dst > 0:
        saved = total_orig - total_dst
        direction = "smaller" if saved >= 0 else "larger"
        print(f"  {tr('size')}: {format_size(total_orig)} \u2192 {format_size(total_dst)} ({format_size(abs(saved))} {direction})")
    if errors:
        log_path = Path("hiyo-convert_errors.log")
        with open(log_path, "w", encoding="utf-8") as f:
            for e in errors:
                f.write(f"{e}\n")
        print(f"  {tr('error_log')}: {log_path.resolve()}")


def choose_directory():
    items = [
        (tr("choose_dir_curr"), 1),
        (tr("choose_dir_enter"), 2),
    ]
    if sys.platform == "win32":
        items.append((tr("choose_dir_browse"), 3))
    print(f"\n--- {tr('choose_dir_title')} ---")
    for i, (label, _) in enumerate(items, 1):
        print(f"  [{i}] {label}")
    print(f"  [Q] {tr('quit')}")
    while True:
        sel = input(f"> {tr('choose_dir_pick')} ").strip().lower()
        if sel == "q":
            return None
        try:
            n = int(sel)
            if n < 1 or n > len(items):
                continue
            _, action = items[n - 1]
            if action == 1:
                return Path.cwd()
            elif action == 2:
                p = input(f"> {tr('choose_dir_path')}: ").strip()
                if not p:
                    continue
                pobj = Path(p).resolve()
                if pobj.is_dir():
                    return pobj
                print(f"  [!] {tr('choose_dir_invalid')}: {pobj}")
            elif action == 3:
                import subprocess as _sp
                ps_cmd = (
                    'Add-Type -AssemblyName System.Windows.Forms; '
                    ' $f=New-Object System.Windows.Forms.FolderBrowserDialog; '
                    ' $f.Description="Select a music folder"; '
                    ' $f.ShowDialog() | Out-Null; '
                    ' Write-Output $f.SelectedPath'
                )
                try:
                    result = _sp.run(
                        ["powershell", "-NoProfile", "-Command", ps_cmd],
                        capture_output=True, text=True, timeout=15
                    )
                    p = result.stdout.strip()
                    if p and Path(p).is_dir():
                        return Path(p).resolve()
                    print(f"  [!] {tr('choose_dir_invalid')}")
                except Exception:
                    print(f"  [!] {tr('choose_dir_invalid')}")
        except ValueError:
            pass
    return None


def choose_language():
    print(f"\n  === HiyoConvert ===")
    print(f"\n  {LANG['en']['choose_lang']}")
    print(f"  [1] English")
    print(f"  [2] Ti\u1ebfng Vi\u1ec7t")
    print(f"  [Q] {LANG['en']['quit']}")
    while True:
        sel = input("> ").strip().lower()
        if sel == "1":
            return LANG["en"]
        elif sel == "2":
            return LANG["vi"]
        elif sel == "q":
            return None


def choose_source_type():
    items = [
        (tr("local_files"), "local"),
        (tr("youtube"), "youtube"),
    ]
    print(f"\n--- {tr('source_type')} ---")
    for i, (label, _) in enumerate(items, 1):
        print(f"  [{i}] {label}")
    print(f"  [Q] {tr('quit')}")
    while True:
        sel = input("> ").strip().lower()
        if sel == "q":
            return None
        try:
            n = int(sel)
            if 1 <= n <= len(items):
                return items[n - 1][1]
        except ValueError:
            pass


def input_youtube_urls():
    print(f"\n--- {tr('enter_urls')} ---")
    urls = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        if re.match(r'^https?://(www\.)?(youtube\.com|youtu\.be)/', line):
            urls.append(line)
        else:
            print(f"  [!] {tr('invalid_url')}: {line}")
    if not urls:
        print(f"  [!] {tr('no_urls')}")
        return None
    return urls


def download_youtube_audio(url, temp_dir):
    try:
        import yt_dlp
    except ImportError:
        print(f"  [!] yt-dlp not installed. Run: pip install yt-dlp")
        return None
    outtmpl = str(temp_dir / "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "unknown")
            ext = info.get("ext", "webm")
            downloaded = temp_dir / f"{info.get('title', 'unknown')}.{ext}"
            if not downloaded.exists():
                for f in temp_dir.iterdir():
                    if f.is_file() and f.name.startswith(info.get("title", "")):
                        downloaded = f
                        break
            return downloaded, title
    except Exception as e:
        print(f"  [!] {tr('download_error')}: {e}")
        return None


def convert_youtube_files(downloaded, dst_ext, codec, settings, codec_info):
    threads = max(1, os.cpu_count() - 1) if os.cpu_count() else 2
    total = len(downloaded)
    print(f"\n--- {tr('converting')} {total} {tr('files')} ({tr('threads')}: {threads}) ---\n")
    start = time.time()
    ok = skip = fail = 0
    errors = []
    total_orig = 0
    total_dst = 0

    with ThreadPoolExecutor(max_workers=threads) as pool:
        fut = {}
        for src_path, title in downloaded:
            if src_path is None:
                continue
            output = get_youtube_output_path(title, dst_ext, settings)
            fut[pool.submit(convert_youtube_one, src_path, output, dst_ext, codec, settings, codec_info)] = title

        for f in as_completed(fut):
            result = f.result()
            if result is None:
                continue
            status, name, orig_sz, dst_sz = result
            if status == "ok":
                ok += 1
                total_orig += orig_sz
                total_dst += dst_sz
                print(f"  [{tr('ok')}] {name}")
            else:
                fail += 1
                print(f"  [{tr('fail')}] {name}")

    elapsed = time.time() - start
    print(f"\n--- {tr('done')} ---")
    print(f"  {tr('ok')}: {ok}  |  {tr('fail')}: {fail}")
    print(f"  {tr('time')}: {elapsed:.1f}s")
    if total_orig > 0 and total_dst > 0:
        saved = total_orig - total_dst
        direction = "smaller" if saved >= 0 else "larger"
        print(f"  {tr('size')}: {format_size(total_orig)} \u2192 {format_size(total_dst)} ({format_size(abs(saved))} {direction})")


def get_youtube_output_path(title, dst_ext, settings):
    name = title
    if settings.simplify:
        name = simplify_name(name)
    if settings.output_dir:
        dst = settings.output_dir / f"{name}{dst_ext}"
    else:
        dst = Path.cwd() / f"{name}{dst_ext}"
    counter = 1
    while dst.exists():
        stem = f"{name}_{counter}"
        if settings.output_dir:
            dst = settings.output_dir / f"{stem}{dst_ext}"
        else:
            dst = Path.cwd() / f"{stem}{dst_ext}"
        counter += 1
    return dst


def convert_youtube_one(src_path, dst, dst_ext, codec, settings, codec_info):
    short = get_short_name(src_path.stem)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src_path)]
    if settings.strip_meta:
        cmd += ["-map_metadata", "-1", "-vn"]
    else:
        cmd += ["-map_metadata", "0"]
    cmd += ["-c:a", codec]
    cmd += quality_to_params(codec_info, settings.quality)
    if settings.sample_rate > 0:
        cmd += ["-ar", str(settings.sample_rate)]
    if settings.channels > 0:
        cmd += ["-ac", str(settings.channels)]
    if settings.normalize:
        cmd += ["-af", "loudnorm=I=-16:LRA=11:TP=-1.5"]
    cmd += [str(dst)]
    try:
        subprocess.run(cmd, check=True)
        orig_size = src_path.stat().st_size
        dst_size = dst.stat().st_size
        src_path.unlink(missing_ok=True)
        return "ok", short, orig_size, dst_size
    except subprocess.CalledProcessError:
        return "fail", short, 0, 0


def run_youtube(yourls, tgt_ext, tgt_codec, codec_info):
    settings = configure_settings(tgt_ext, codec_info)
    if settings.dry_run:
        print(f"\n=== {tr('dry_run_title')} ===")
        print(f"{tr('dry_run_info')} {len(yourls)} video(s) {tr('from')} YouTube {tr('to')} {tgt_ext}:\n")
        for url in yourls:
            print(f"  {url}")
        print(f"\n--- {tr('done')} ---")
        input(f"\n{tr('press_enter')}")
        return

    import tempfile as _tf
    temp_dir = Path(_tf.mkdtemp(prefix="hiyoconvert_yt_"))
    print(f"\n--- {tr('downloading')} {len(yourls)} video(s) ---\n")
    downloaded = []
    for url in yourls:
        print(f"  {tr('downloading')}: {url}")
        result = download_youtube_audio(url, temp_dir)
        if result:
            src_path, title = result
            downloaded.append((src_path, title))
            print(f"  [{tr('ok')}] {title}")
        else:
            print(f"  [{tr('fail')}] {url}")

    if not downloaded:
        print(f"  [!] {tr('no_files')}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        input(f"\n{tr('press_enter')}")
        return

    convert_youtube_files(downloaded, tgt_ext, tgt_codec, settings, codec_info)
    shutil.rmtree(temp_dir, ignore_errors=True)
    input(f"\n{tr('press_enter')}")


def main():
    global L
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found. Install with: winget install ffmpeg")
        sys.exit(1)

    L = choose_language()
    if L is None:
        return

    src_type = choose_source_type()
    if src_type is None:
        return

    if src_type == "local":
        if len(sys.argv) > 1:
            root = Path(sys.argv[1]).resolve()
            if not root.is_dir():
                print(f"'{root}' is not a directory")
                sys.exit(1)
        else:
            root = choose_directory()
            if root is None:
                return

        print(f"\n--- {tr('source')} ---")
        src_item = pick_menu(SRC_FORMATS, "")
        if src_item is None:
            return
        src_ext = src_item[1]

        print(f"\n--- {tr('target')} ---")
        tgt_item = pick_menu(TGT_FORMATS, "")
        if tgt_item is None:
            return
        _, tgt_ext, _, tgt_codec = tgt_item

        codec_info = CODECS.get(tgt_ext)
        if codec_info is None:
            print(f"Unknown target format: {tgt_ext}")
            return

        print(f"\n{tr('scanning')}...")
        dirs = scan_dirs(root, src_ext)
        if not dirs:
            print(f"{tr('no_files')}")
            return

        selected = pick_dirs(dirs)
        if not selected:
            print(tr("none_sel"))
            return

        all_files = sorted(f for d in selected for f in d.rglob("*")
                           if src_ext is None and f.suffix.lower() in ALL_AUDIO_EXTS
                           or src_ext is not None and f.suffix.lower() == src_ext)
        if not all_files:
            print(f"{tr('no_files')}")
            return

        print(f"\n{tr('found')} {len(all_files)} {tr('files')}")
        settings = configure_settings(tgt_ext, codec_info)

        if settings.dry_run:
            print(f"\n=== {tr('dry_run_title')} ===")
            print(f"{tr('dry_run_info')} {len(all_files)} {tr('files')} {tr('to')} {tgt_ext}:\n")
            for f in all_files:
                dst = get_output_path(f, tgt_ext, settings, root)
                short = get_short_name(f.stem)
                sz = format_size(f.stat().st_size) if f.exists() else "?"
                print(f"  [{sz}] {short} -> {dst.name}")
            print(f"\n--- {tr('done')} ---")
            input(f"\n{tr('press_enter')}")
            return

        run_batch(all_files, tgt_ext, tgt_codec, settings, codec_info, root)
        input(f"\n{tr('press_enter')}")

    else:
        print(f"\n--- {tr('target')} ---")
        tgt_item = pick_menu(TGT_FORMATS, "")
        if tgt_item is None:
            return
        _, tgt_ext, _, tgt_codec = tgt_item

        codec_info = CODECS.get(tgt_ext)
        if codec_info is None:
            print(f"Unknown target format: {tgt_ext}")
            return

        yourls = input_youtube_urls()
        if yourls is None:
            return

        run_youtube(yourls, tgt_ext, tgt_codec, codec_info)


if __name__ == "__main__":
    main()
