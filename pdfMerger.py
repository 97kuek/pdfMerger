import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF結合ツール")
        self.root.geometry("500x400")

        self.pdf_files = []

        # 説明文
        tk.Label(root, text="PDFファイルをこのウィンドウにドラッグ＆ドロップしてください").pack(pady=5)

        # ファイル一覧リストボックス
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60)
        self.listbox.pack(pady=10, expand=True)

        # ボタン
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="↑ 上へ", command=self.move_up).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="↓ 下へ", command=self.move_down).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="PDF結合", command=self.merge_pdfs).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="リセット", command=self.reset_list).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="使い方", command=self.show_help).grid(row=0, column=4, padx=5)

        # ドラッグ＆ドロップ設定
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.add_files)

    def add_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith(".pdf") and file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def move_up(self):
        i = self.listbox.curselection()
        if not i or i[0] == 0:
            return
        i = i[0]
        self.pdf_files[i-1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i-1]
        self.update_listbox(i-1)

    def move_down(self):
        i = self.listbox.curselection()
        if not i or i[0] == len(self.pdf_files) - 1:
            return
        i = i[0]
        self.pdf_files[i+1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i+1]
        self.update_listbox(i+1)

    def update_listbox(self, new_index):
        self.listbox.delete(0, tk.END)
        for f in self.pdf_files:
            self.listbox.insert(tk.END, os.path.basename(f))
        self.listbox.select_set(new_index)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("警告", "PDFファイルが追加されていません。")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return
        merger = PdfMerger()
        try:
            for file in self.pdf_files:
                merger.append(file)
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("成功", f"PDFを保存しました:\n{save_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"PDF結合中にエラーが発生しました:\n{e}")

    def reset_list(self):
        self.pdf_files = []
        self.listbox.delete(0, tk.END)

    def show_help(self):
        msg = (
            "【使い方】\n\n"
            "1. PDFファイルをこのウィンドウにドラッグ＆ドロップしてください。\n"
            "2. ファイルが一覧に追加されます。\n"
            "3. 順番を↑↓ボタンで調整します。\n"
            "4. 「PDF結合」ボタンで保存先を選び、結合PDFを作成します。\n"
            "5. 「リセット」でリストを空にできます。"
        )
        messagebox.showinfo("使い方", msg)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
