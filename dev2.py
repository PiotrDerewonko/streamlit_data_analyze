import pandas as pd
from xhtml2pdf import pisa

# Przykładowy DataFrame
df = pd.DataFrame({
    "Kolumna1": ["Wartość 1", "Wartość 2"],
    "Kolumna2": ["Wartość 3", "Wartość 4"]
})

# Konwersja DataFrame do HTML
df_html = df.to_html(index=False)

# Zawartość HTML
html_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: DejaVu Sans, sans-serif;
            font-size: 14px;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h1>Raport</h1>
    <p>To jest przykładowy tekst zawierający polskie znaki: ą, ć, ę, ł, ń, ó, ś, ź, ż.</p>
    {df_html}
</body>
</html>
"""

# Funkcja do zapisu HTML jako PDF
def create_pdf(html_content, filename):
    with open(filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    return pisa_status.err

# Przykładowe użycie
create_pdf(html_content, "report.pdf")
