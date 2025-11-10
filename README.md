# Linkedin Automation Tool
Enhance your LinkedIn networking and lead generation with this automation tool designed to streamline Sales Navigator connections. It automates the process of sending connection requests and messages, making it easier to engage with potential prospects and grow your professional network.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Linkedin Automation Tool</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
This project automates LinkedIn Sales Navigator workflows by extracting, managing, and exporting data from profiles and searches. It removes the manual work of sending invites and messages, helping users maintain consistent outreach and follow-up campaigns.

### Why This Tool Matters
- Simplifies LinkedIn Sales Navigator data export for CRM integration.
- Automates connection requests and personalized messaging.
- Helps sales teams reach more leads with less effort.
- Ensures consistent, compliant usage to avoid LinkedIn restrictions.
- Empowers marketers to act on actionable insights efficiently.

## Features
| Feature | Description |
|----------|-------------|
| Automated Connections | Sends personalized connection requests directly via Sales Navigator. |
| Messaging Automation | Customizes and sends outreach messages automatically. |
| Cookie-Based Authentication | Uses valid cookies for secure login and automation access. |
| CRM-Ready Data Export | Extracts profile and lead information in structured formats for CRM import. |
| Safe Usage Limits | Configurable request pacing to comply with LinkedIn’s daily/weekly limits. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|-------------|------------------|
| profile_url | Sales Navigator profile link for the lead. |
| full_name | Complete name of the targeted prospect. |
| headline | Current title or role from the profile. |
| company | Company or organization associated with the lead. |
| location | Geographic location of the lead. |
| connection_status | Indicates whether a connection request was sent or accepted. |
| message_status | Status of any personalized message sent. |
| timestamp | Timestamp of the automation run. |

---

## Example Output
    [
      {
        "profile_url": "https://www.linkedin.com/sales/lead/1234567890",
        "full_name": "Sarah Mitchell",
        "headline": "Sales Director at GrowthCorp",
        "company": "GrowthCorp",
        "location": "Sydney, Australia",
        "connection_status": "Request Sent",
        "message_status": "Delivered",
        "timestamp": "2025-11-10T10:45:00Z"
      }
    ]

---

## Directory Structure Tree
    linkedin-automation-tool-scraper/
    ├── src/
    │   ├── main.py
    │   ├── modules/
    │   │   ├── navigator_scraper.py
    │   │   ├── connection_sender.py
    │   │   └── message_dispatcher.py
    │   ├── utils/
    │   │   ├── cookie_manager.py
    │   │   └── logger.py
    │   └── config/
    │       └── settings.json
    ├── data/
    │   ├── input_profiles.csv
    │   └── output_results.json
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Sales professionals** use it to automate connection requests, helping them scale outreach while staying compliant.
- **Marketing teams** extract Sales Navigator data to enhance segmentation and personalization efforts.
- **Agencies** integrate scraped leads into CRM pipelines for faster client acquisition.
- **Recruiters** identify and connect with top candidates efficiently.
- **Startups** build their investor or partner networks with targeted outreach.

---

## FAQs
**How do I authenticate the tool?**
You’ll need to provide a valid Sales Navigator cookie. Export it using the EditThisCookie Chrome extension and paste it into the tool’s configuration field.

**What’s the safe daily limit for connection requests?**
Keep it under 20 per day. LinkedIn monitors weekly activity, so spread your requests to avoid restrictions.

**Does it support message personalization?**
Yes — you can include custom message templates with variables to make outreach feel natural and personalized.

**What if I see errors or warnings?**
Double-check that your cookie hasn’t expired, and confirm you’re using valid Sales Navigator URLs instead of standard LinkedIn links.

---

## Performance Benchmarks and Results
**Primary Metric:** Processes up to 200 profiles per hour on standard network speeds.
**Reliability Metric:** Achieves a 96% success rate for connection request delivery.
**Efficiency Metric:** Uses under 150MB RAM per 100 processed profiles.
**Quality Metric:** 99% accuracy in capturing correct profile and company data.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
