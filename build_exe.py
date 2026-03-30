import os
import sys
import subprocess

def main():
    print("--- ETSY FAST IMAGE PRO (NATIVE) - Windows EXE Derleyici ---")
    print("PyInstaller derlemesi basliyor, bu islem 1-3 dakika arasi surebilir...\n")

    # Paths
    project_dir = os.path.abspath(os.path.dirname(__file__))
    src_dir = os.path.join(project_dir, "src")
    assets_dir = os.path.join(project_dir, "assets")
    entry_script = os.path.join(src_dir, "gui_app.py")
    
    # Separator for PyInstaller --add-data depends on OS. On Windows it's ';'
    sep = ';' if os.name == 'nt' else ':'

    # Pyinstaller command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconfirm",         # Overwrite dist/
        "--onedir",            # Directory mode for clean extraction
        "--windowed",          # No console window (Native UI only)
        "--name=ETSY_FAST_IMAGE_Pro", 
        "--distpath=dist_final",
        f"--add-data={src_dir}{sep}src",
        f"--add-data={assets_dir}{sep}assets",
        entry_script
    ]
    
    # Explicitly define hidden imports that Pyinstaller might miss for CustomTkinter and ImageProcessing
    hidden_imports = [
        "customtkinter",
        "pandas",
        "numpy",
        "PIL.Image",
        "imagehash",
        "openpyxl"
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
        
    print("\nDerleme Komutu Çalisiyor...")
    print(" ".join(cmd))
    print("-" * 50)
    
    try:
        # Run pyinstaller programmatically through subprocess to ensure it picks up the virtualenv correctly
        subprocess.check_call(cmd, cwd=project_dir)
        print("\n" + "=" * 50)
        print("✅ DERLEME BAŞARIYLA TAMAMLANDI!")
        print(f"📁 Uygulamanizi su klasörde bulabilirsiniz: {os.path.join(project_dir, 'dist', 'ETSY_FAST_IMAGE_Pro')}")
        print("=" * 50)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Derleme sirasinda bir hata olustu: {e}")
        print("\nLutfen hatayi kontrol edin.")

if __name__ == "__main__":
    main()
