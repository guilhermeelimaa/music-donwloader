; Script para Inno Setup Compiler

[Setup]
AppName=YouTube MP3 Downloader
AppVersion=1.0
AppPublisher=Guilherme Lima
DefaultDirName={autopf}\YouTubeMP3Downloader
DefaultGroupName=YouTube MP3 Downloader
Compression=lzma
SolidCompression=yes
OutputDir=output
OutputBaseFilename=YouTubeMP3Downloader_Setup
SetupIconFile=seu_icone.ico
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
; Arquivo principal
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; Incluir o Python embutido (opcional para distribuição sem requisitos)
; Source: "python-embed\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\YouTube MP3 Downloader"; Filename: "{app}\main.exe"; IconFilename: "{app}\main.exe"
Name: "{commondesktop}\YouTube MP3 Downloader"; Filename: "{app}\main.exe"; IconFilename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Executar o programa agora"; Flags: postinstall nowait skipifsilent

[Code]
// Código opcional para verificar dependências
function InitializeSetup(): Boolean;
begin
  // Verificar se tem conexão com internet
  Result := True;
end;