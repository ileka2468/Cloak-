# CloakAI

This is a GUI based desktop automation wrapper for an AI rewriting service,
enhances rewrite concurrency and other issues with original service. No
longer supported - was for educational purposes and software licensing
practice. reproduce at your own risk. Original service will not be named.



---

### What does this application do?

This desktop app was a wrapper for an AI rewriting web app, the service took AI generated content, and rewrote it in a manner that was indistinguishable from human writing. The issue with the application was that it forced all inputted content into paragraph form. So if you had a bulleted or numbered list, after running it through the rewriter it was turned into a paragraph. To fix this, one would have to run each bullet or numbered question separately and one at a time which was a horrible user experience. My app solved these issues, through the GUI, you would add your bulleted or separate content that was meant to be rewritten separately. Then the application would concurrently launch multiple automated web browsers to rewrite each bullet separately, and then recombine them into an output file, keeping the intended bulleted or numbered format.



### How was it used?

To use the app you would enter a registration key, your credentials to the rewriting service and then if all was valid you will be met with the main GUI screen.

<img title="" src="https://ik.imagekit.io/smec/git/ss.PNG?updatedAt=1692382465435" alt="" data-align="center">

<img title="" src="https://ik.imagekit.io/smec/git/Care.PNG?updatedAt=1692382465393" alt="" data-align="center">

### Why is it no longer supported?

It was never supported to begin with, the project started off as a joke with a friend who showed me the rewriting service and told me jokingly "to use my degree and make it better", so I graciously accepted and wrote CloakAI in like 2 days. The project from the beginning was meant to be an educational experience in terms of learning how to integrate APIs, Databases and software registration into 1 deployable package. A lot of websites don't like web scrapers, so I will be respecting that. This app is not intended to be used so all references to the rewriting service have been removed.
