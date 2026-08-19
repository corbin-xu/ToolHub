[Setup]
AppName=JD Supplier Label Generator
AppVersion=1.0.7
AppPublisher=xgb819
AppPublisherURL=https://github.com/xgb819/jd-supplier-label-generator
AppSupportURL=https://github.com/xgb819/jd-supplier-label-generator
AppUpdatesURL=https://github.com/xgb819/jd-supplier-label-generator/releases
DefaultDirName={autopf}\JD Supplier Label Generator
DefaultGroupName=JD Supplier Label Generator
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename=jd-supplier-label-generator-1.0.7
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
Source: "dist\jd-supplier-label-generator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "templates\*.pld"; DestDir: "{app}\templates"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\JD Supplier Label Generator"; Filename: "{app}\jd-supplier-label-generator.exe"
Name: "{group}\{cm:UninstallProgram,JD Supplier Label Generator}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\JD Supplier Label Generator"; Filename: "{app}\jd-supplier-label-generator.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\jd-supplier-label-generator.exe"; Description: "{cm:LaunchProgram,JD Supplier Label Generator}"; Flags: nowait postinstall skipifsilent
