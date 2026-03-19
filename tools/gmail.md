# Gmail Tool — MCP — Moon Studio

> שליחת הצעות מחיר, follow-ups ותכתובת מקצועית דרך Gmail.
> **סטטוס: 🔄 הבא לבנות — נדרש חיבור MCP ל-Claude**
> ⚠️ **חשוב:** סוכנים מכינים טיוטות בלבד. דביר שולח.

---

## מה הכלי יעשה

- Finance Agent → מכין טיוטת מייל עם הצעת מחיר מצורפת
- Marketing Agent → מכין טיוטת Cold Outreach
- Project Manager → מכין טיוטת follow-up ללקוח
- **דביר בוחן ושולח — שום סוכן לא שולח לבד**

---

## ⚙️ הגדרה — נדרש מדביר

### שלב 1: הפעלת MCP ב-Claude Desktop

הוסף ל-`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "[your-client-id]",
        "GOOGLE_CLIENT_SECRET": "[your-client-secret]",
        "GOOGLE_REFRESH_TOKEN": "[your-refresh-token]"
      }
    }
  }
}
```

> ניתן לשתף את אותם credentials עם Calendar MCP אם מוגדרים על אותו Google Account.

---

## פעולות שה-MCP מאפשר

| פעולה | מי משתמש | תיאור |
|-------|----------|-------|
| `create_draft` | Finance, Marketing, PM | יצירת טיוטה — דביר שולח |
| `list_drafts` | Orchestrator | הצגת טיוטות ממתינות לשליחה |
| `search_emails` | PM, Finance | חיפוש תכתובת עם לקוח |

---

## כלל ברזל

```
✅ מותר: create_draft
❌ אסור: send_email — דביר שולח תמיד
```

---

## שימוש Finance Agent — הצעת מחיר

```
1. קבל אישור דביר להצעה
2. צור טיוטת מייל:
   נושא: "הצעת מחיר — Moon Studio — [שם הפרויקט]"
   גוף: [תבנית מ-core/prompt_templates.md]
   מצורף: output/quotes/[quote_id]/quote.pdf
3. שמור כ-draft
4. עדכן דביר: "טיוטה מוכנה לשליחה"
```

## שימוש Marketing Agent — Cold Outreach

```
1. כתוב טקסט לפי תבנית Cold Outreach (core/prompt_templates.md)
2. צור טיוטה:
   נושא: "שיתוף פעולה — Moon Studio"
3. שמור ב-outreach_log
4. דביר בוחן ושולח
```

---

## תבנית מייל — הצעת מחיר

```
נושא: הצעת מחיר — Moon Studio — [שם הפרויקט]

היי [שם],

בהמשך לשיחתנו, מצורפת הצעת המחיר ל[שם הפרויקט].

ההצעה בתוקף ל-14 יום.
שמח לענות על כל שאלה.

דביר
Moon Studio
```
