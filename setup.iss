[Setup]
AppName=京东供应商标签生成器
AppVersion=1.1.0
AppPublisher=xgb819
AppPublisherURL=https://github.com/xgb819/jd-supplier-label-generator
AppSupportURL=https://github.com/xgb819/jd-supplier-label-generator
AppUpdatesURL=https://github.com/xgb819/jd-supplier-label-generator/releases
DefaultDirName={autopf}\JD Supplier Label Generator
DefaultGroupName=JD Supplier Label Generator
AllowNoIcons=yes
LicenseFile=LICENSE
SetupIconFile=assets\favicon.ico
OutputDir=dist
OutputBaseFilename=jd-supplier-label-generator-v1.1.0-20260819
Compression=zip
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\JD Supplier Label Generator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "templates\*.pld"; DestDir: "{app}\templates"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\京东供应商标签生成器"; Filename: "{app}\JD Supplier Label Generator.exe"
Name: "{group}\{cm:UninstallProgram,京东供应商标签生成器}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\京东供应商标签生成器"; Filename: "{app}\JD Supplier Label Generator.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\JD Supplier Label Generator.exe"; Description: "{cm:LaunchProgram,京东供应商标签生成器}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\JD Supplier Label Generator.exe"; Flags: nowait skipifnotsilent