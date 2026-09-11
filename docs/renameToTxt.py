import os
import shutil
from pathlib import Path

def flatten_and_copy_filtered(source_dir: str, dest_dir: str):
    # Convert string paths to Path objects
    src_path = Path(source_dir).resolve()
    dst_path = Path(dest_dir).resolve()
    
    # Define allowable file extensions (case-insensitive matching)
    ALLOWED_EXTENSIONS = {".css", ".ts", ".tsx"}
    
    # Ensure destination folder exists
    dst_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Scanning files in: {src_path}")
    print(f"Filtering extensions: {', '.join(ALLOWED_EXTENSIONS)}")
    print(f"Copying flattened results to: {dst_path}\n")
    
    copied_count = 0
    
    # Recursively iterate over all items under the source directory
    for file_path in src_path.rglob("*"):
        # Process only files that match our specific extension whitelist
        if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
            # Get the path relative to the source directory's parent folder
            relative_path = file_path.relative_to(src_path.parent)
            
            # Join the path parts with underscores (e.g., 'frontend_components_Style.css')
            flattened_name = "_".join(relative_path.parts)
            
            # Append the trailing .txt extension
            final_filename = f"{flattened_name}.txt"
            
            # Build final destination target path
            target_file_path = dst_path / final_filename
            
            # Copy the file
            shutil.copy2(file_path, target_file_path)
            print(f"Copied: {file_path.name} -> {final_filename}")
            copied_count += 1
            
    print(f"\nSuccess! Total matching files copied and flattened: {copied_count}")

if __name__ == "__main__":
    # --- CONFIGURE YOUR PATHS HERE ---
    input_folder = "./frontend"       # Path to your source folder
    output_folder = "./flattened_out" # Path to your single destination folder
    # ---------------------------------
    
    flatten_and_copy_filtered(input_folder, output_folder)
