## VerificationBot
This bot allows user to verify in DISCORD through Email Verification with specific domain. Additionally, the bot will utilize googlesheets as database for verification. This bot was coded with python (discordpy).

Join my discord channel to try the bot!
> Discord Invite Link: https://discord.gg/jWkjxWyEbQ

<p align="center">
  <img src="docs/verification bot.jpg" />
</p>


## Requirements
- [ ] Discord Bot API Token
- [ ] GOOGLE API Token [(tutorial here)](https://youtu.be/4ssigWmExak?t=226)
- [ ] SENDGRID API Token [(How to set up Sendgrid)](https://youtu.be/Xqb8W17i1PI)

## Set Up
After getting the requirements from above
- Download `keys.json` and place it in the same folder as `bot.py` [tutorial here](https://youtu.be/4ssigWmExak?t=439)
- Make a copy of [THIS SPREADSHEET](https://docs.google.com/spreadsheets/d/1K7L-1lI9d1L4FMcvW3Kr4H_nt0dJCTrLWM0C2tusYDk/edit#gid=240624144)
- Acquire and fill in all the required tokens and IDs on `Sheet2` (image 1)
- Take note of `SAMPLE_SPREADSHEET_ID` and replace the value on `bot.py` at line 16
<p align="center">
  <img src="docs/id and tokens.jpg" />
</p>
<p align="center">
  Image 1: ID and Tokens
</p>

## Verification Process
- React on message
- Reply your `EMAIL` and `CODE` on the DM
- Role and Access Granted to User


<p>Image 2: React on message</p>
<p><img src="docs/1 - react here.jpg" /></p>
<p>Image 3: Email and Code on DMs</p>
<p><img src="docs/2 - email.jpg" /></p>
<p>Image 4: Verified Access</p>
<p><img src="docs/3 - verified access.jpg" /></p>

## Additional Information
- Embedded messages can be edited from the function at `bot.py` at `lines 90 to 154`, read more from [discordpy Embed](https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#discord.Embed)
- Email message can be changed by editing `html_content` at `line 161`, [Example Email](https://media.discordapp.net/attachments/1032348940592496645/1047096620459773992/image.png)

## Lisence
VerificationBot is licensed under [GNU GPL v3](LICENSE).

- This project uses Open Source components. You can find the source code of his open source projects along with license information below. I acknowledge and is grateful to the developer for their contributions to open source.
- This project is a derivative work and took inspiration from the work of [EmailBot](https://github.com/gg2001/EmailBot) by [gg2001](https://github.com/gg2001) which is under the GNU General Public Liscence, version 3.
