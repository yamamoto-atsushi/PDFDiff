import os
from tkinter import Tk, filedialog, Button, Label, messagebox
from difflib import HtmlDiff
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup

def extract_text_with_pdfminer(file_path):
    """Extract text from a PDF file."""
    try:
        return extract_text(file_path)
    except Exception as e:
        return f"Error extracting text: {e}"

def generate_diff_report(file1, file2):
    """Generate a diff report in HTML format."""
    # Extract text
    text1 = extract_text_with_pdfminer(file1)
    text2 = extract_text_with_pdfminer(file2)
    
    # Split into lines for comparison
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    # Generate diff
    html_diff = HtmlDiff().make_file(lines1, lines2, context=True, numlines=3)
    
    # Add explanation and header
    soup = BeautifulSoup(html_diff, "html.parser")
    header = soup.new_tag("h1")
    header.string = "改訂履歴レポート - 解説付き"
    soup.body.insert(0, header)
    explanation = soup.new_tag("p")
    explanation.string = (
        "このレポートでは、2つのPDF文書間の変更履歴を比較し、削除された部分と追加された部分が色分けされて表示されています。"
        "削除された内容は赤、追加された内容は緑でハイライトされています。また、変更のあった周辺3行の文脈も表示されています。"
    )
    soup.body.insert(1, explanation)
    
    # Save the HTML report
    output_path = os.path.join(os.getcwd(), "diff_report_with_explanation.html")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    return output_path

def select_file(label):
    """Open a file dialog to select a file and update the label."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        label.config(text=file_path)

def compare_files():
    """Compare the selected files and generate a diff report."""
    file1 = file1_label.cget("text")
    file2 = file2_label.cget("text")
    if not os.path.isfile(file1) or not os.path.isfile(file2):
        messagebox.showerror("エラー", "有効なPDFファイルを選択してください。")
        return
    try:
        output_path = generate_diff_report(file1, file2)
        messagebox.showinfo("成功", f"レポートが生成されました: {output_path}")
    except Exception as e:
        messagebox.showerror("エラー", f"比較中にエラーが発生しました: {e}")

# Initialize the GUI
root = Tk()
root.title("PDF比較ツール")

# Labels and buttons for file selection
Label(root, text="PDFファイル1を選択:").grid(row=0, column=0, padx=10, pady=10)
file1_label = Label(root, text="未選択", width=50, anchor="w")
file1_label.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="ファイルを選択", command=lambda: select_file(file1_label)).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="PDFファイル2を選択:").grid(row=1, column=0, padx=10, pady=10)
file2_label = Label(root, text="未選択", width=50, anchor="w")
file2_label.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="ファイルを選択", command=lambda: select_file(file2_label)).grid(row=1, column=2, padx=10, pady=10)

# Compare button
Button(root, text="比較を実行", command=compare_files).grid(row=2, column=0, columnspan=3, pady=20)

# Start the GUI loop
root.mainloop()
