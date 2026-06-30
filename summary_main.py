# ═══════════════════════════════════════════════════════════════════════════════
# FINAL: Show the main.py code summary for user reference
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("📄 JOKERATC v2.0 - main.py CODE SUMMARY")
print("=" * 70)

with open('/mnt/agents/output/jokeratc/main.py', 'r') as f:
    lines = f.readlines()

# Show key sections
sections = []
current_section = []
current_title = "START"

for line in lines:
    if line.strip().startswith('# ───') and line.strip().endswith('─'):
        if current_section:
            sections.append((current_title, len(current_section)))
        current_title = line.strip().strip('# ─')
        current_section = []
    else:
        current_section.append(line)

if current_section:
    sections.append((current_title, len(current_section)))

print("\n📋 Code Structure:")
print("-" * 50)
for title, count in sections:
    print(f"  📌 {title:<40} ({count:>4} lines)")

print(f"\n📊 Total Lines: {len(lines)}")
print(f"📊 Total Characters: {sum(len(l) for l in lines):,}")

# Show the first 50 lines as preview
print("\n" + "=" * 70)
print("👁️  CODE PREVIEW (First 50 lines):")
print("=" * 70)
for i, line in enumerate(lines[:50], 1):
    print(f"{i:>3} | {line.rstrip()}")
print("...")
print(f"\n📄 Full code saved to: jokeratc/main.py")
