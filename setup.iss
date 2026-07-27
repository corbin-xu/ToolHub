[Setup]
AppName=ToolHub
AppVersion=1.6
AppPublisher=xgb819
AppPublisherURL=https://github.com/xgb819/ToolHub
AppSupportURL=https://github.com/xgb819/ToolHub
AppUpdatesURL=https://github.com/xgb819/ToolHub
DefaultDirName={autopf}\ToolHub
DefaultGroupName=ToolHub
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename=ToolHub-1.6
Compression=zip
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\ToolHub.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "templates\*.pld"; DestDir: "{app}\templates"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ToolHub"; Filename: "{app}\ToolHub.exe"
Name: "{group}\{cm:UninstallProgram,ToolHub}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ToolHub"; Filename: "{app}\ToolHub.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ToolHub.exe"; Description: "{cm:LaunchProgram,ToolHub}"; Flags: nowait postinstall skipifsilent
