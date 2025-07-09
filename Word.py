from license_checker import is_pro_user
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from fpdf import FPDF
import os
import argparse

def add_header(section, text="Document Header"):
    """
    Ajoute un en-tête centré dans la section du document Word.
    """
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.runs[0]
    run.font.size = Pt(12)
    run.font.name = 'Arial'

def add_footer_with_page_numbers(section):
    """
    Ajoute un pied de page avec numéros de page centrés.
    """
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
    """
    Convertit un fichier .txt en document Word .docx.
    En mode gratuit, limite le contenu à 1000 caractères.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {input_file}")
        return

    pro = is_pro_user()

    if not pro:
        content = content[:1000]
        print("⚠️ Mode Gratuit activé : conversion limitée aux 1000 premiers caractères.")

    doc = Document()

    # Mise en page avec en-tête et pied de page
    section = doc.sections[0]
    add_header(section, text="Conversion TXT → DOCX")
    add_footer_with_page_numbers(section)

    # Style global
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Ajout des paragraphes avec détection simple des titres
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if (stripped.isupper() or stripped.startswith('#') or
            stripped.lower().startswith("titre") or stripped.endswith(":")):
            para = doc.add_paragraph(stripped, style='Heading 1')
        else:
            para = doc.add_paragraph(stripped, style='Normal')

    doc.save(output_file)
    print(f"✅ Document sauvegardé sous : {output_file}")
    print("🔓 Mode Pro activé" if pro else "🔒 Mode Gratuit")

def txt_to_pdf(input_file, output_file):
    """
    Convertit un fichier .txt en PDF simple, ligne par ligne.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {input_file}")
        return

    # Regroupement des lignes en paragraphes pour une meilleure lisibilité
    paragraph = ""
    for line in lines:
        if line.strip():
            paragraph += line.strip() + " "
        else:
            if paragraph:
                pdf.multi_cell(0, 10, paragraph)
                paragraph = ""
    if paragraph:
        pdf.multi_cell(0, 10, paragraph)

    pdf.output(output_file)
    print(f"✅ Document sauvegardé sous : {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convertir un fichier TXT en DOCX et/ou PDF")
    parser.add_argument('--input', '-i', required=True, help='Chemin du fichier .txt à convertir')
    parser.add_argument('--output', '-o', required=True, help='Nom du fichier de sortie sans extension')
    parser.add_argument('--docx', action='store_true', help='Générer un fichier Word (.docx)')
    parser.add_argument('--pdf', action='store_true', help='Générer un fichier PDF (.pdf)')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Le fichier spécifié n'existe pas : {args.input}")
        return

    if args.docx:
        convert_txt_to_word(args.input, args.output + '.docx')

    if args.pdf:
        txt_to_pdf(args.input, args.output + '.pdf')

    if not args.docx and not args.pdf:
        print("⚠️ Veuillez spécifier au moins --docx ou --pdf")

if __name__ == '__main__':
    main()
