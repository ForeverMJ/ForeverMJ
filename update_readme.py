def replace_section(content, marker_start, marker_end, replacement):
    start = content.find(marker_start)
    end = content.find(marker_end)

    if start == -1 or end == -1:
        raise ValueError(f"Markers not found: {marker_start} or {marker_end}")

    new_content = (
        content[:start + len(marker_start)]
        + "\n" + replacement.strip() + "\n"
        + content[end:]
    )
    return new_content


if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    with open("trend.md", "r", encoding="utf-8") as f:
        trend = f.read()

    with open("total.md", "r", encoding="utf-8") as f:
        total = f.read()

    updated = replace_section(readme, "<!--START_SECTION:waka-->", "<!--END_SECTION:waka-->", trend)
    updated = replace_section(updated, "<!--START_SECTION:total-->", "<!--END_SECTION:total-->", total)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

    print("✅ README.md updated successfully.")
