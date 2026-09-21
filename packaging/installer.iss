#ifndef MyAppVersion
  #define MyAppVersion "2.0.0"
#endif

#define MyAppName "Backroom Bratzz: Boss Shift"
#define MyAppPublisher "Danny Morgan / LAB-137"
#define MyAppExeName "BackroomBratzz.exe"
#define MyShortcutName "Backroom Bratzz - Boss Shift"

[Setup]
AppId={{7D3A870F-6EBD-4A80-9B6B-5D2DBD01137B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\LAB-137\Backroom Bratzz
DefaultGroupName=LAB-137\Backroom Bratzz
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=BackroomBratzz-Setup
SetupIconFile=..\assets\icons\backroom_bratzz.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\LICENSE
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "..\dist\BackroomBratzz\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyShortcutName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyShortcutName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
