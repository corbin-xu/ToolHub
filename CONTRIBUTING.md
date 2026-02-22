# Contributing

## Git commit messages

**Please use English for commit messages** to avoid encoding issues when pushing to GitHub (especially on Windows with non-UTF-8 terminal). This keeps the commit history readable everywhere.

Examples:

- `Add carton mark template for Shantou B warehouse`
- `Fix date parsing in export`
- `Update dependencies`

## Optional: use a commit message template

To remind yourself to write in English, you can set a template:

```bash
git config commit.template .gitmessage
```

Then each time you run `git commit`, the editor will open with the template as a reminder.

## Optional: force UTF-8 for Git (Windows)

If you still see encoding issues, set Git to use UTF-8 in this repo:

```bash
git config i18n.commitEncoding utf-8
git config i18n.logOutputEncoding utf-8
```

In PowerShell you can also set `$env:LC_ALL = "en_US.UTF-8"` before running Git commands.
