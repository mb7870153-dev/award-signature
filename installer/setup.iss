#define MyAppName "Award Signature"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Учебный проект"
#define MyAppExeName "AwardSignature.exe"

[Setup]
AppId={{7E86D34A-9A2B-4E32-8C54-1A6F4B2D9C71}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\AwardSignature
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=Output
OutputBaseFilename=AwardSignatureSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "Создать значок на рабочем столе"; GroupDescription: "Дополнительные значки:"

[Files]
Source: "..\dist\AwardSignature.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Award Signature"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Award Signature"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Запустить Award Signature"; Flags: nowait postinstall skipifsilent