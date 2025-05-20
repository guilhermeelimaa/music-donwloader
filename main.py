from pytubefix import YouTube
from pytubefix.cli import on_progress
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Downloader")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        
        # Variáveis
        self.url_var = tk.StringVar()
        self.destino_var = tk.StringVar(value="")
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="Pronto para baixar")
        
        # Interface
        self.create_widgets()
        
        # Configurações de download
        self.yt = None
        self.audio_stream = None
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL do vídeo
        ttk.Label(main_frame, text="URL do vídeo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=45)
        url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Pasta de destino
        ttk.Label(main_frame, text="Pasta de destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        destino_frame = ttk.Frame(main_frame)
        destino_frame.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        destino_entry = ttk.Entry(destino_frame, textvariable=self.destino_var, width=35)
        destino_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(destino_frame, text="Selecionar", command=self.selecionar_pasta)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Barra de progresso
        ttk.Label(main_frame, text="Progresso:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Botão de download (centralizado)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        download_btn = ttk.Button(btn_frame, text="Baixar Áudio (MP3)", command=self.iniciar_download)
        download_btn.pack()
        
        # Configurar expansão
        main_frame.columnconfigure(1, weight=1)
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta para salvar o áudio")
        if pasta:
            self.destino_var.set(pasta)
    
    def progress_function(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        self.progress_var.set(progress)
        self.status_var.set(f"Baixando... {int(progress)}%")
        self.root.update_idletasks()
    
    def iniciar_download(self):
        url = self.url_var.get().strip()
        destino = self.destino_var.get()
        
        if not url:
            self.status_var.set("Erro: URL não informada")
            return
        
        if not destino:
            self.status_var.set("Erro: Pasta de destino não selecionada")
            return
        
        try:
            self.progress_var.set(0)
            self.status_var.set("Conectando...")
            self.root.update_idletasks()
            
            self.yt = YouTube(url, on_progress_callback=self.progress_function)
            self.status_var.set(f"Preparando: {self.yt.title[:30]}...")
            self.root.update_idletasks()
            
            # Obtém a melhor stream de áudio disponível
            self.audio_stream = self.yt.streams.filter(
                only_audio=True
            ).order_by('abr').desc().first()
            
            if not self.audio_stream:
                self.status_var.set("Erro: Nenhum stream de áudio encontrado")
                return
            
            # Baixa o arquivo
            self.status_var.set("Iniciando download...")
            arquivo = self.audio_stream.download(output_path=destino)
            
            # Renomeia para .mp3 (mesmo que internamente seja outro formato)
            base, ext = os.path.splitext(arquivo)
            novo_arquivo = base + ".mp3"
            os.rename(arquivo, novo_arquivo)
            
            self.status_var.set(f"Concluído: {os.path.basename(novo_arquivo)}")
            self.progress_var.set(100)
            
        except Exception as e:
            self.status_var.set(f"Erro: {str(e)}")
            self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeAudioDownloader(root)
    root.mainloop()