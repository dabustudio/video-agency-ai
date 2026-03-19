# CRM Tool — Supabase — Moon Studio

> ניהול לידים, פרויקטים ומשימות דרך Supabase.
> **סטטוס: 🔄 הבא לבנות — נדרש Supabase API Key**

---

## מה הכלי יעשה

CRM מרכזי שמאפשר לסוכנים:
- לרשום ולעדכן לידים בזמן אמת
- לעקוב אחרי פרויקטים פעילים
- לצפות בסטטוס תשלומים
- להריץ queries פשוטים

---

## ⚙️ הגדרה — נדרש מדביר

```bash
# .env (לא לעלות ל-GitHub!)
SUPABASE_URL=https://[your-project].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]
```

---

## מבנה טבלאות (Supabase Schema)

### טבלה: `leads`

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה אוטומטי |
| `lead_id` | text | YYYY-MM-DD-שם |
| `name` | text | שם הליד |
| `phone` | text | טלפון |
| `email` | text | אימייל |
| `source` | text | מקור הפנייה |
| `segment` | text | פרטי/עסק קטן/היי-טק/... |
| `service_requested` | text | שירות מבוקש |
| `budget_indicated` | numeric | תקציב שצוין |
| `date_entered` | date | תאריך כניסה |
| `status` | text | ליד/בטיפול/הצעה נשלחה/... |
| `priority` | text | גבוהה/רגילה |
| `notes` | text | הערות |
| `created_at` | timestamp | אוטומטי |

### טבלה: `projects`

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה אוטומטי |
| `project_id` | text | YYYY-MM-DD-שם-לקוח |
| `lead_id` | text | FK → leads |
| `client_name` | text | שם לקוח |
| `service_type` | text | סוג שירות |
| `status` | text | בריף/צילום/עריכה/... |
| `amount_total` | numeric | סכום כולל |
| `amount_paid` | numeric | שולם עד כה |
| `shoot_date` | date | תאריך צילום |
| `delivery_target` | date | יעד מסירה |
| `created_at` | timestamp | אוטומטי |

### טבלה: `invoices`

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה אוטומטי |
| `invoice_id` | text | INV-YYYY-MM-DD-שם |
| `project_id` | text | FK → projects |
| `amount_total` | numeric | סכום כולל |
| `amount_paid` | numeric | שולם |
| `status` | text | נשלחה/שולמה/חוב |
| `due_date` | date | תאריך פירעון |
| `created_at` | timestamp | אוטומטי |

---

## API Calls (Python)

```python
from supabase import create_client
import os

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])

# הוספת ליד חדש
supabase.table("leads").insert({
    "lead_id": "2026-03-19-חברת-אבג",
    "name": "חברת אבג",
    "segment": "היי-טק",
    "priority": "גבוהה",
    "status": "ליד"
}).execute()

# שליפת כל הלידים הפתוחים
leads = supabase.table("leads").select("*").eq("status", "בטיפול").execute()

# עדכון סטטוס פרויקט
supabase.table("projects").update({"status": "עריכה"}).eq("project_id", "2026-03-19-לקוח").execute()
```

---

## צעדי הגדרה (לדביר)

1. צור חשבון ב-[supabase.com](https://supabase.com)
2. פתח Project חדש
3. צור את הטבלאות לפי הסכמה למעלה (ניתן להריץ SQL ישירות)
4. העתק את `SUPABASE_URL` ו-`SUPABASE_ANON_KEY` מ-Settings > API
5. שמור ב-`.env` (שאינו ב-git)
6. `pip install supabase`

---

## אינטגרציה עם הסוכנים

| סוכן | שימוש |
|------|-------|
| **Project Manager** | insert/update leads + projects |
| **Finance** | read projects, insert invoices, update amount_paid |
| **Marketing** | read leads by segment לסטטיסטיקות |
| **Orchestrator** | read summary לדוח שבועי |
