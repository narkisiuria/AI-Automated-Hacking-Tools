def filter_payloads(keywords, filepath="msfvenom_payloads_encoders.txt"):
    """
    Reads the saved msfvenom payloads/encoders file and returns
    only the payload lines matching ALL given keywords (e.g. ["windows", "reverse"]).
    """
    keywords = [k.strip().lower() for k in keywords]

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_payload_section = False
    matched_lines = []

    for line in lines:
        if "START AVALIABLE PAYLOADS" in line:
            in_payload_section = True
            continue
        if "END AVALIABLE PAYLOADS" in line:
            in_payload_section = False
            continue

        if in_payload_section:
            stripped = line.strip()
            if not stripped:
                continue
            lowered = stripped.lower()
            if all(keyword in lowered for keyword in keywords):
                matched_lines.append(stripped)

    return matched_lines


if __name__ == "__main__":
    results = filter_payloads(["windows", "reverse"])
    print(f"Found {len(results)} matching payloads:")
    for r in results:
        print(r)