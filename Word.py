from license_checker import is_pro_user
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_header(section, text="Document Header"):
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.runs[0]
    run.font.size = Pt(12)
    run.font.name = 'Arial'

def add_footer_with_page_numbers(section):
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.text = "PAGE"

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def convert_txt_to_word(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {input_file}")
        return

    pro = is_pro_user()

    if not pro:
        content = content[:1000]  # Version gratuite : 1000 caractères max
        print("⚠️ Mode Gratuit activé : seuls les 1000 premiers caractères seront convertis.")

    doc = Document()

    # Mise en page
    section = doc.sections[0]
    add_header(section)
    add_footer_with_page_numbers(section)

    # Style global
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Ajout paragraphe par paragraphe avec détection de titres
    for line in content.splitlines():
        stripped = line.strip()

        # Ignore les lignes vides
        if not stripped:
            continue

        # Détection simple des titres
        if (stripped.isupper() or  # tout en MAJUSCULES
                stripped.startswith('#') or
                stripped.lower().startswith("titre") or
                stripped.endswith(":")):
            para = doc.add_paragraph(stripped, style='Heading 1')
        else:
            para = doc.add_paragraph(stripped, style='Normal')
    doc.save(output_file)

    print(f"✅ Document sauvegardé sous : {output_file}")
    print("🔓 Mode Pro activé" if pro else "🔒 Mode Gratuit")

# Exemple d'appel
convert_txt_to_word("file_root/input.txt", "file_root/output.docx")
