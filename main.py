import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import threading

class CrawlerApp:
    def __init__(self, root):
        self.visited = set()
        self.root_url = ""
        self.report = {}
        self.max_depth = 3
        self.max_requests = 50
        self.request_count = 0
        self.is_crawling = True

        # Main Frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input Frame
        url_frame = ttk.LabelFrame(main_frame, text="URL do Site", padding="10")
        url_frame.grid(row=0, column=0, sticky=tk.W + tk.E, pady=(0, 20))

        self.entry = ttk.Entry(url_frame, width=50)
        self.entry.grid(row=0, column=0, padx=(0, 10))

        self.button = ttk.Button(url_frame, text="Iniciar Crawler", command=self.start_crawler)
        self.button.grid(row=0, column=1)

        # Botão de parada
        self.stop_button = ttk.Button(url_frame, text="Parar Crawler", command=self.stop_crawler)
        self.stop_button.grid(row=0, column=2)
        self.stop_button["state"] = tk.DISABLED

        # Report Text Frame
        report_frame = ttk.LabelFrame(main_frame, text="Relatório", padding="10")
        report_frame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.text = tk.Text(report_frame, wrap=tk.WORD, width=75, height=25)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Bottom Buttons Frame
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=2, column=0, sticky=tk.E, pady=20)

        self.save_button = ttk.Button(button_frame, text="Salvar Relatório", command=self.save_report)
        self.save_button.pack(side=tk.RIGHT)

    def check_link_status(self, link):
        try:
            response = requests.head(link, allow_redirects=True)
            return response.status_code
        except requests.RequestException as e:
            logging.error(f"Error checking status of {link}: {str(e)}")
            return "Erro"

    def get_links(self, url, depth=1):
        if not self.is_crawling or self.request_count > self.max_requests or depth > self.max_depth:
            return

        # Verifica se o domínio é o mesmo
        if urlparse(self.root_url).netloc != urlparse(url).netloc:
            return

        try:
            response = requests.get(url)
            self.request_count += 1
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(url, link.get('href'))
                
                # Ignora links de mídia
                if absolute_link.endswith(('jpg', 'jpeg', 'png', 'mp4')):
                    continue

                if absolute_link not in self.visited:
                    self.visited.add(absolute_link)
                    self.get_links(absolute_link, depth+1)
        except Exception as e:
            logging.error(f"Error crawling {url}: {str(e)}")
            self.text.insert(tk.END, f"Erro ao acessar {url}: {str(e)}\n")

    def stop_crawler(self):
        self.is_crawling = False
        self.stop_button["state"] = tk.DISABLED
        self.button["state"] = tk.NORMAL

    def start_crawler(self):
        self.root_url = self.entry.get()
        if not self.root_url:
            messagebox.showerror("Erro", "Por favor, insira uma URL.")
            return

        self.text.insert(tk.END, f"Iniciando crawler para: {self.root_url}\n")
        self.visited.clear()
        self.report.clear()
        self.request_count = 0
        self.is_crawling = True
        self.stop_button["state"] = tk.NORMAL
        self.button["state"] = tk.DISABLED

        # Iniciar o crawler em uma thread separada para não bloquear a GUI
        threading.Thread(target=self.run_crawler, daemon=True).start()

    def run_crawler(self):
        self.get_links(self.root_url)

        for link in self.visited:
            status = self.check_link_status(link)
            self.report[link] = status
            self.text.insert(tk.END, f"{link} - {status}\n")

        self.stop_button["state"] = tk.DISABLED
        self.button["state"] = tk.NORMAL
        if not self.is_crawling:
            self.text.insert(tk.END, "Crawling interrompido pelo usuário.\n")
        else:
            self.text.insert(tk.END, "Crawling concluído.\n")

    def save_report(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_name:
            with open(file_name, 'w') as file:
                for link, status in self.report.items():
                    file.write(f"{link} - {status}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crawler Splog")
    root.geometry("800x600")
    app = CrawlerApp(root)
    root.mainloop()