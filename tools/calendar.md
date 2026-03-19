# Calendar Tool — Google Calendar MCP — Moon Studio

> תיאום לוח ימי צילום דרך Google Calendar.
> **סטטוס: 🔄 הבא לבנות — נדרש חיבור MCP ל-Claude**

---

## מה הכלי יעשה

- Production Coordinator Agent קורא ומעדכן את לוח הצילומים של דביר
- יצירת אירועים אוטומטית עם call time, לוקיישן, פרטי לקוח
- בדיקת זמינות לפני קביעת צילום חדש
- תזכורות אוטומטיות לדביר

---

## ⚙️ הגדרה — נדרש מדביר

### שלב 1: הפעלת MCP ב-Claude Desktop

הוסף ל-`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "[your-client-id]",
        "GOOGLE_CLIENT_SECRET": "[your-client-secret]",
        "GOOGLE_REFRESH_TOKEN": "[your-refresh-token]"
      }
    }
  }
}
```

### שלב 2: קבלת Google OAuth Credentials

1. [console.cloud.google.com](https://console.cloud.google.com) → New Project
2. Enable "Google Calendar API"
3. Create OAuth 2.0 Client ID (Desktop App)
4. הורד `client_secret.json`
5. הרץ את flow ה-OAuth לקבלת `refresh_token`

---

## פעולות שה-MCP מאפשר

| פעולה | תיאור |
|-------|-------|
| `list_events` | שליפת אירועים לפי טווח תאריכים |
| `create_event` | יצירת אירוע חדש (יום צילום) |
| `update_event` | עדכון אירוע קיים |
| `check_availability` | בדיקת זמינות לתאריך מסוים |

---

## שימוש Production Coordinator

```
בדיקת זמינות לפני קביעת צילום:
1. שלוף אירועים לשבוע המבוקש
2. אם התאריך פנוי → צור אירוע עם הפרטים
3. כלול: שם לקוח, לוקיישן, call time, סוג צילום

שם אירוע מומלץ: "[סוג] — [שם לקוח] — [HH:MM]"
```

---

## לוח זמנים קבוע

| יום | משימה |
|-----|-------|
| ראשון | בדיקת לוח השבוע הקרוב |
| כל יום | תזכורת לדביר אם יש צילום למחרת |
| 3 ימים לפני | בדיקת ציוד מיוחד |
