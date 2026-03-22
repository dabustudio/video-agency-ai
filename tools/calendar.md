# Calendar Tool — Google Calendar MCP — Moon Studio

> תיאום לוח ימי צילום ופגישות דרך Google Calendar.
> **סטטוס: ✅ מחובר ופעיל — dvirgolanmusic@gmail.com | Asia/Jerusalem**

---

## מי משתמש בכלי זה

| סוכן | שימוש |
|------|-------|
| **Production Coord** | רישום ימי צילום ללקוחות, בדיקת זמינות |
| **Marketing** | תזמון ימי צילום פנימיים לתוכן הסטודיו |

---

## פעולות MCP

| פעולה | כלי MCP | תיאור |
|-------|---------|-------|
| רשימת אירועים | `mcp__claude_ai_Google_Calendar__gcal_list_events` | שליפת אירועים לפי טווח |
| יצירת אירוע | `mcp__claude_ai_Google_Calendar__gcal_create_event` | יצירת יום צילום / פגישה |
| עדכון אירוע | `mcp__claude_ai_Google_Calendar__gcal_update_event` | עדכון פרטים |
| מציאת זמן פנוי | `mcp__claude_ai_Google_Calendar__gcal_find_my_free_time` | בדיקת זמינות |

---

## שימוש Production Coord — יום צילום ללקוח

```
1. בדוק זמינות בתאריך המבוקש (gcal_find_my_free_time)
2. אם פנוי → צור אירוע:
   כותרת: "🎬 צילום — [שם לקוח] — [סוג]"
   תיאור: לוקיישן + call time + פרטי פרויקט
   משך: יום מלא / חצי יום
3. שמור shoot_id ב-output/production/schedule.json
```

### פורמט אירוע מומלץ
```
כותרת: 🎬 [שם לקוח] — [יום מלא / חצי יום]
תיאור:
  לוקיישן: [כתובת]
  Call time: [HH:MM]
  סוג: [פרסומת / תדמית / סושיאל]
  Supabase project ID: [ID]
```

---

## שימוש Marketing — יום צילום פנימי

```
1. דביר אישר רעיון + סקריפט → Marketing מתזמן יום צילום
2. בדוק זמינות (gcal_find_my_free_time)
3. צור אירוע:
   כותרת: "📹 צילום פנימי — [שם הסרטון]"
   תיאור: סקריפט: output/marketing/scripts/...
   משך: [לפי הסקריפט — בדרך כלל 2-4 שעות]
4. עדכן status ב-output/marketing/ideas/ ל-"מתוזמן"
```

---

## לוח זמנים קבוע

| מתי | פעולה |
|-----|-------|
| כל ראשון | Production Coord בודק לוח השבוע הקרוב |
| 3 ימים לפני צילום | בדיקת ציוד מיוחד |
| יום לפני צילום | תזכורת לדביר + call sheet ללקוח |
