# Supabase CRM Tool — Moon Studio

> CRM מחובר של הסטודיו — לידים, פרויקטים, משימות.
> **סטטוס: 🔄 דורש הגדרה — ראה "שלבי חיבור" למטה**

---

## מה הכלי עושה

- Project Manager → קורא ומעדכן לידים ופרויקטים
- Client Relations → קורא סטטוס פולואפ, מעדכן משימות
- Finance → קורא פרטי פרויקט לצורך הצעת מחיר
- **כל קריאה ועדכון ל-CRM עוברים דרך Bash + curl לסביבת Supabase**

---

## שלבי חיבור (פעם אחת)

### שלב 1 — מצא את ה-API URL והמפתח שלך
1. כנס ל-[supabase.com](https://supabase.com) → הפרויקט שלך
2. **Settings → API**
3. העתק:
   - `Project URL` (נראה כך: `https://[project-id].supabase.co`)
   - `anon public` key

### שלב 2 — הוסף ל-.env
```bash
SUPABASE_URL=https://[your-project-id].supabase.co
SUPABASE_ANON_KEY=eyJ...
```

> ⚠️ `.env` ב-`.gitignore` — לא לעשות commit עם credentials

### שלב 3 — טעינה בתחילת session
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
```

---

## מבנה הטבלאות הצפוי

> ⚠️ שמות הטבלאות והעמודות הבאים הם הנחת עבודה — יש לאמת מול הסכמה האמיתית בפרויקט Supabase שלך.

### טבלת לידים (leads / contacts)

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה ייחודי |
| `name` | text | שם הליד / הלקוח |
| `email` | text | כתובת מייל |
| `phone` | text | טלפון |
| `segment` | text | פרטי / עסק קטן / היי-טק / מותג / מסעדה |
| `status` | text | ליד / בטיפול / הצעה נשלחה / סגור-כן / סגור-לא |
| `source` | text | פה לאוזן / הפניה / שיווק / אחר |
| `notes` | text | הערות חופשיות |
| `created_at` | timestamp | תאריך כניסה |

### טבלת פרויקטים (projects / deals)

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה ייחודי |
| `client_id` | uuid | FK → leads |
| `title` | text | שם הפרויקט |
| `status` | text | בריף / צילום / עריכה / אישור / סגור |
| `value` | numeric | ערך הפרויקט ב-₪ |
| `start_date` | date | תאריך פתיחה |
| `deadline` | date | דדליין |
| `notes` | text | הערות |

### טבלת משימות (tasks / follow-ups)

| עמודה | סוג | תיאור |
|-------|-----|-------|
| `id` | uuid | מזהה ייחודי |
| `project_id` | uuid | FK → projects |
| `title` | text | תיאור המשימה |
| `due_date` | date | תאריך יעד |
| `status` | text | פתוח / בטיפול / סגור |
| `assigned_to` | text | שם הסוכן / דביר |

---

## שאילתות נפוצות

### שליפת כל הלידים הפעילים
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
curl -s "$SUPABASE_URL/rest/v1/leads?status=neq.סגור-לא&status=neq.סגור-כן&select=*" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY"
```

### שליפת פרויקטים פעילים
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
curl -s "$SUPABASE_URL/rest/v1/projects?status=neq.סגור&select=*" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY"
```

### עדכון סטטוס פרויקט
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
curl -s -X PATCH "$SUPABASE_URL/rest/v1/projects?id=eq.[PROJECT_ID]" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "עריכה"}'
```

### הוספת ליד חדש
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
curl -s -X POST "$SUPABASE_URL/rest/v1/leads" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"[שם]","email":"[מייל]","segment":"[סגמנט]","status":"ליד","source":"פה לאוזן"}'
```

### שליפת משימות פתוחות שעברו דדליין
```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
TODAY=$(date +%Y-%m-%d)
curl -s "$SUPABASE_URL/rest/v1/tasks?status=eq.פתוח&due_date=lt.$TODAY&select=*" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY"
```

---

## אמת את הסכמה לפני שימוש ראשון

```bash
source "/Users/dvirgolan/Desktop/Moon studio/claude/video-agency-ai/.env"
# ראה אילו טבלאות קיימות
curl -s "$SUPABASE_URL/rest/v1/" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "apikey: $SUPABASE_ANON_KEY"
```

---

## כלל חשוב

> תמיד לקרוא מ-Supabase **לפני** כל עדכון.
> לא לסמוך על מה שנאמר בשיחה — תמיד לאמת מול ה-DB.
