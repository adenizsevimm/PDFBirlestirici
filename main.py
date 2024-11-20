import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, MULTIPLE
import fitz  # PyMuPDF kütüphanesi

class PDFMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title('PDF Birleştirici')

        self.label = tk.Label(master, text='Henüz bir PDF dosyası seçilmedi.')
        self.label.pack(pady=10)

        self.file_listbox = Listbox(master, selectmode=MULTIPLE, width=50, height=10)
        self.file_listbox.pack(pady=10)

        self.add_files_button = tk.Button(master, text='PDF Dosyalarını Ekle', command=self.add_files)
        self.add_files_button.pack(pady=5)

        self.merge_button = tk.Button(master, text='PDF Birleştir', command=self.mergePDFs)
        self.merge_button.pack(pady=5)

        self.export_button = tk.Button(master, text='Birleştirilen PDF\'i Kaydet', command=self.exportPDF)
        self.export_button.pack(pady=5)

    def add_files(self):
        # Seçilen dosyaları sırayla ekle
        files = filedialog.askopenfilenames(title='PDF Dosyalarını Seç', filetypes=[('PDF Files', '*.pdf')])

        if files:
            for file in files:
                self.file_listbox.insert(tk.END, file)

            self.label.config(text=f'{len(files)} PDF dosyası eklendi.')

    def mergePDFs(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning('Uyarı', 'Birleştirme için PDF dosyalarını seçin.')
            return

        # Dosyaları seçildiği sıraya göre birleştir
        self.merged_pdf = fitz.open()
        for index in selected_indices:
            file_path = self.file_listbox.get(index)
            pdf_document = fitz.open(file_path)
            self.merged_pdf.insert_pdf(pdf_document)

        self.label.config(text=f'{len(selected_indices)} PDF dosyası birleştirildi.')

    def exportPDF(self):
        try:
            self.merged_pdf
        except AttributeError:
            messagebox.showwarning('Uyarı', 'Önce PDF dosyalarını birleştirin.')
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if save_path:
            try:
                self.merged_pdf.save(save_path)
                self.merged_pdf.close()
                messagebox.showinfo('Başarılı', f'PDF dosyası başarıyla kaydedildi: {save_path}')
            except Exception as e:
                messagebox.showerror('Hata', f'Hata oluştu: {str(e)}')
        else:
            messagebox.showinfo('Bilgi', 'Kaydetme işlemi iptal edildi.')

def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
