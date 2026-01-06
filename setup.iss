[Setup]
AppName=ToolHub
AppVersion=1.0
AppPublisher=corbin-xu
AppPublisherURL=https://github.com/corbin-xu/ToolHub
AppSupportURL=https://github.com/corbin-xu/ToolHub
AppUpdatesURL=https://github.com/corbin-xu/ToolHub
DefaultDirName={autopf}\ToolHub
DefaultGroupName=ToolHub
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename=ToolHub-1.0-setup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\ToolHub.exe
Compression=lz4
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimp"; MessagesFile: "compiler:ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\ToolHub\ToolHub.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ToolHub\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ToolHub"; Filename: "{app}\ToolHub.exe"
Name: "{group}\{cm:UninstallProgram,ToolHub}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ToolHub"; Filename: "{app}\ToolHub.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ToolHub.exe"; Description: "{cm:LaunchProgram,ToolHub}"; Flags: nowait postinstall skipifsilent
