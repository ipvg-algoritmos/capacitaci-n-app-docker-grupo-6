import os

def remove_source_mapping_lines(base_dir):
    removed = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(".js"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = [line for line in lines if not line.strip().startswith("//# sourceMappingURL=")]

                if len(new_lines) != len(lines):
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    removed += 1
                    print(f"🧼 Limpiado: {filepath}")

    print(f"\n✅ Limpieza completada. Archivos modificados: {removed}")

# Cambia el path si lo estás ejecutando desde otro lugar
remove_source_mapping_lines("static")
