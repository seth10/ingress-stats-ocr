# Ingress Stats OCR


## Overview: What is this project?

This project is targeted towards "agents" who plays the game [Ingress](https://ingress.com/), using the [Ingress Prime app](https://apps.apple.com/us/app/ingress/id576505181) developed by [Niantic, Inc](https://nianticlabs.com/en/products/).

Ingress Stats OCR allows agents to easily track their progress over time. This is achieved by taking screenshots of the stats on your profile page and running a [shortcut](https://support.apple.com/en-us/HT208309). This will display the difference in each of your stats since the last time you recorded them.


## Technologies

At the heart of this project is Tesseract, an optical character recognition engine. Ingress Stats OCR is entirely serverless and hosted in Amazon Web Services. Tesseract and the application logic runs in an AWS Lambda function. This is called from the iOS Shortcut via API Gateway. Data persistence is handled by a DynamoDB table accessed from the Lambda.


## Deploying

1. Create an AWS Lambda in the N. Virginia (us-east-1) region with the Python 2.7 runtime. Set the memory limit to 512 MB and timeout to 30 sec. Clone this git repo and zip everything _except_ for this README.md, iOS Shortcut.md, and the .git folder. Upload this zip as the function package.
2. In the AWS Lambda designer, click Add trigger and select API Gateway. Follow the prompts to get your API, in the end you should get a path like https://r3plac3m3.execute-api.us-east-1.amazonaws.com/default/ingress-stats-ocr.
3. Create a DynamoDB table in the same region named `ingress-stats-ocr`. Make the primary partition key a String `timestamp`.
   - Populate a record with the "latest" key. See [#9](https://github.com/seth10/ingress-stats-ocr/issues/9)
4. Open [iOS Shortcut.md](/iOS%20Shortcut.md) and open the link at the top on your iOS device. Tap "Get Shortcut", review the actions, and "Add Untrusted Shortcut". Scroll down to the Network action and replace the URL with your actual API Gateway URL. If you're not on an iPhone X/Xs/11 Pro, you might have to adjust the crop dimensions, see [#7](https://github.com/seth10/ingress-stats-ocr/issues/7).
   - Consider tapping the ellipsis next to the shortcut name and selecting "Add to Home Screen" for ease of access.

### Usage

1. Open the Ingress Prime app and tap your username or XM indicator to open your agent profile.
2. Tap the "ALL TIME" tab and scroll down until the words "ALL TIME" is overlapped by the current time. The "NOW" tab will also be obscured by the network and battery indicators. Your first screenshot could be at this point or lower, as long as "Unique Portals Visited" and the number should be completely visible below the sensor housing "notch" and status bar. Take a screenshot.
3. Scroll down _all the way_ so "Longest Hacking Streak" is completely visible with no gradient shadow obscuring it. Take a screenshot.
4. Scroll up until you can tap the "NOW" tab and tap it. If you scrolled up too far, scroll back down so all five stats are completely visible. If you tapped "NOW" when it was in the top half of your screen, you won't have to scroll at all. Take a screenshot.
5. Swipe up twice to go home and tap the Ingress Stats OCR shortcut link you added to your homescreen. Wait a moment and you'll see your results!


## DynamoDB Table Format

You might be surprised that the DynamoDB table uses human-readable timestamps, full statistic names, and leaves commas and units in values. The reason for this is to make the table readable on its own, without a separate UI. This project does not currently have its own UI, so besides the text response you get at the time of submitting new stats, the table can be used for further historical insights and interesting discoveries.


## History

Development began on Monday, May 18th, 2020 and concluded on Friday, May 22nd, 2020. This personal project became obsolete on Monday, May 25th, 2020 when I discovered that there is a text export button I overlooked, and the existence of https://www.agent-stats.com/. On Saturday, June 6th, 2020 I uploaded the last of my work missing from this repository and wrote issues for any ideas and thoughts I had.
