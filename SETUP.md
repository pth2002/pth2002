# Publish this GitHub profile

GitHub shows a profile README when a public repository has the exact same name as the account. For this account, the repository must be named `pth2002`.

## 1. Create the repository

Create a new **public** repository at <https://github.com/new> with:

- Repository name: `pth2002`
- Visibility: Public
- Do not add a README, license, or `.gitignore` during creation

## 2. Push these files

Run the following commands from the `pth2002-profile` folder:

```powershell
git init
git add README.md assets/hero.svg
git commit -m "feat: launch profile README"
git branch -M main
git remote add origin https://github.com/pth2002/pth2002.git
git push -u origin main
```

The profile will appear automatically at <https://github.com/pth2002> after the push.

## Optional personal details

The draft deliberately avoids inventing private details. Add an email, personal site, LinkedIn, location, or real name only if you want them public. The safest places are the link buttons near the bottom of `README.md` and the short introduction below the banner.
