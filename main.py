from pytubefix import YouTube
from pytubefix.cli import on_progress
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Downloader")
        self.root.geometry("600x350")  # Aumentei a altura para o rodapé
        self.root.resizable(False, False)
        
        # Configuração de estilo
        self.setup_styles()
        
        # Variáveis
        self.url_var = tk.StringVar()
        self.destino_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.progress_var = tk.DoubleVar(value=0)
        self.status_var = tk.StringVar(value="Pronto para baixar")
        
        # Interface
        self.create_widgets()
        
        # Configurações de download
        self.yt = None
        self.audio_stream = None
    
    def setup_styles(self):
        """Configura os estilos visuais da aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurações gerais
        style.configure('.', background='#f0f0f0', foreground='#333')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('TEntry', padding=5)
        
        # Barra de progresso
        style.configure("Horizontal.TProgressbar", 
                       thickness=20, 
                       troughcolor='#e0e0e0',
                       background='#4CAF50')
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        ttk.Label(title_frame, 
                 text="YouTube para MP3", 
                 font=('Helvetica', 16, 'bold'),
                 foreground='#333').pack()
        
        # URL do vídeo
        ttk.Label(main_frame, text="URL do vídeo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=45)
        url_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Pasta de destino
        ttk.Label(main_frame, text="Pasta de destino:").grid(row=2, column=0, sticky=tk.W, pady=5)
        destino_frame = ttk.Frame(main_frame)
        destino_frame.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        destino_entry = ttk.Entry(destino_frame, textvariable=self.destino_var, width=35)
        destino_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(destino_frame, text="Selecionar", command=self.selecionar_pasta)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Barra de progresso
        ttk.Label(main_frame, text="Progresso:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100,
                                          style="Horizontal.TProgressbar")
        self.progress_bar.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        # Status (centralizado)
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.status_label = ttk.Label(status_frame, 
                                    textvariable=self.status_var,
                                    font=('Helvetica', 10, 'italic'),
                                    foreground='#555')
        self.status_label.pack()
        
        # Botão de download (centralizado)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        download_btn = ttk.Button(btn_frame, 
                                 text="BAIXAR ÁUDIO (MP3)", 
                                 command=self.iniciar_download,
                                 style='Accent.TButton')
        download_btn.pack(ipadx=20, ipady=5)
        
        # Rodapé
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=6, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Label(footer_frame, 
                 text="Desenvolvido por Guilherme Lima", 
                 font=('Helvetica', 8),
                 foreground='#888').pack()
        
        # Linha decorativa
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
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